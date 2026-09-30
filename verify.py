import hashlib
import json
from pathlib import Path
import tomllib
import zipfile
from core import ORES, state_name

ROOT = Path(__file__).resolve().parent
snapshot = json.loads((ROOT / 'vanilla.json').read_text(encoding='utf-8'))
version = snapshot['version']['id']
stem = f'massive-ores-1.0.0-mc{version}'
with zipfile.ZipFile(ROOT / (stem + '.jar')) as jar, zipfile.ZipFile(ROOT / (stem + '.zip')) as dp:
    assert jar.testzip() is None and dp.testzip() is None
    for path in dp.namelist():
        assert jar.read(path) == dp.read(path)
    data = {p: json.loads(jar.read(p)) for p in jar.namelist() if p.endswith('.json')}
    assert data['fabric.mod.json']['depends']['minecraft'] == '=' + version
    assert json.loads(jar.read('pack.mcmeta'))['pack']['pack_format'] == snapshot['version']['data_pack_version']
    for p in ('META-INF/mods.toml', 'META-INF/neoforge.mods.toml'):
        metadata = tomllib.loads(jar.read(p).decode())
        assert metadata['dependencies']['massive_ores'][0]['versionRange'] == '[' + version + ']'
    covered = set()
    for path, selector in data.items():
        if not path.startswith('data/minecraft/'):
            continue
        source = snapshot['files'][path]
        source_config = source.get('config', source)
        assert selector['type'] == 'minecraft:random_selector'
        config = selector.get('config', selector)
        assert len(config['features']) == 10
        remaining = 1.0
        choices = config['features'] + [{'feature': config['default']}]
        folder = 'configured_feature' if '/configured_feature/' in path else 'feature'
        for index, option in enumerate(choices):
            chance = option.get('chance', 1.0)
            assert abs(remaining * chance - 1/11) < 1e-12
            remaining *= 1 - chance
            placed = option['feature']
            assert placed['placement'] == []
            namespace, name = placed['feature'].split(':')
            ore = data[f'data/{namespace}/worldgen/{folder}/{name}.json']
            assert ore['type'] == 'minecraft:ore'
            ore_config = ore.get('config', ore)
            assert ore_config['size'] == index + 20
            assert ore_config['targets'] == source_config['targets']
            assert ore_config['discard_chance_on_air_exposure'] == source_config['discard_chance_on_air_exposure']
            covered.update(state_name(t).removeprefix('minecraft:') for t in ore_config['targets'])
    assert covered == ORES
for line in (ROOT / 'SHA256SUMS.txt').read_text().splitlines():
    sha, name = line.split('  ')
    assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == sha
print('PASS: Minecraft ' + version + ' — archives, ores, probabilities, references and metadata; not runtime-tested.')
