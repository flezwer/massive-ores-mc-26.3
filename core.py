"""Build reproducible, data-only, multi-loader mods using cached vanilla data."""
import copy
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent
MOD = 'massive_ores'
MIN_SIZE, MAX_SIZE = 20, 30
ORES = {'coal_ore', 'iron_ore', 'gold_ore', 'lapis_ore', 'diamond_ore',
        'emerald_ore', 'redstone_ore', 'copper_ore', 'nether_quartz_ore',
        'nether_gold_ore', 'ancient_debris'}
ORES |= {'deepslate_' + x for x in list(ORES) if not x.startswith('nether_') and x != 'ancient_debris'}


def encode(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def state_name(target):
    state = target['state']
    return state if isinstance(state, str) else state.get('Name', state.get('id'))


def mod_toml(version, neo=False):
    modern = tuple(map(int, version.split('.'))) >= (1, 21, 5)
    text = '' if neo and modern else 'modLoader="lowcodefml"\nloaderVersion="[1,)"\n'
    text += 'license="MIT"\n\n[[mods]]\nmodId="massive_ores"\n'
    text += 'version="1.0.0"\ndisplayName="Massive Ores"\n'
    text += 'description="Ore veins with a random generation size from 20 to 30."\n'
    text += 'displayTest="IGNORE_ALL_VERSION"\n\n[[dependencies.massive_ores]]\n'
    text += 'modId="minecraft"\n'
    text += 'type="required"\n' if neo else 'mandatory=true\n'
    text += f'versionRange="[{version}]"\nordering="NONE"\nside="BOTH"\n'
    return text.encode('utf-8')


def resources(snapshot):
    version = snapshot['version']['id']
    files = snapshot['files']
    pack = copy.deepcopy(files['pack.mcmeta'])
    pack['pack']['description'] = f'Massive Ores | Java {version}'
    result = {'pack.mcmeta': encode(pack)}
    count = 0
    covered = set()
    for path, original in files.items():
        if original.get('type') not in ('minecraft:ore', 'minecraft:scattered_ore'):
            continue
        config = original.get('config', original)
        names = {state_name(t).removeprefix('minecraft:') for t in config['targets']}
        if not names & ORES:
            continue
        assert names <= ORES, (version, path, names)
        covered |= names
        count += 1
        folder = 'configured_feature' if '/configured_feature/' in path else 'feature'
        feature_name = Path(path).stem
        choices = []
        for size in range(MIN_SIZE, MAX_SIZE + 1):
            variant = copy.deepcopy(original)
            # Ancient debris must form a vein instead of scattered single blocks.
            variant['type'] = 'minecraft:ore'
            variant.get('config', variant)['size'] = size
            key = f'{MOD}:{feature_name}_{size}'
            result[f'data/{MOD}/worldgen/{folder}/{feature_name}_{size}.json'] = encode(variant)
            choices.append({'feature': key, 'placement': []})
        # Conditional probabilities yield an equal 1/11 chance for every size.
        selector = {
            'features': [{'chance': 1 / (MAX_SIZE - size + 1), 'feature': choice}
                         for size, choice in zip(range(MIN_SIZE, MAX_SIZE), choices[:-1])],
            'default': choices[-1],
        }
        result[path] = encode({'type': 'minecraft:random_selector', 'config': selector}
                              if 'config' in original else {'type': 'minecraft:random_selector', **selector})
    assert ORES <= covered, (version, ORES - covered)
    return result, count


def write_zip(path, files):
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 9, 28, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, data)

