import hashlib
import json
from pathlib import Path
from core import resources, encode, write_zip, mod_toml, MOD

ROOT = Path(__file__).resolve().parent

def build():
    snapshot = json.loads((ROOT / 'vanilla.json').read_text(encoding='utf-8'))
    version = snapshot['version']['id']
    data, count = resources(snapshot)
    data['README.md'] = (ROOT / 'README.md').read_bytes()
    data['LICENSE'] = (ROOT / 'LICENSE').read_bytes()
    stem = f'massive-ores-1.0.0-mc{version}'
    datapack = ROOT / (stem + '.zip')
    write_zip(datapack, data)
    mod = dict(data)
    mod['fabric.mod.json'] = encode({
        'schemaVersion': 1, 'id': MOD, 'version': '1.0.0',
        'name': 'Massive Ores', 'environment': '*', 'license': 'MIT',
        'description': 'Ore veins with a random generation size from 20 to 30.',
        'depends': {'fabricloader': '>=0.14.0', 'minecraft': '=' + version},
        'recommends': {'fabric-api': '*'},
    })
    mod['META-INF/mods.toml'] = mod_toml(version)
    mod['META-INF/neoforge.mods.toml'] = mod_toml(version, neo=True)
    mod['META-INF/MANIFEST.MF'] = b'Manifest-Version: 1.0\r\nFMLModType: MOD\r\n\r\n'
    jar = ROOT / (stem + '.jar')
    write_zip(jar, mod)
    checksums = ''.join(hashlib.sha256(p.read_bytes()).hexdigest() + '  ' + p.name + '\n' for p in (jar, datapack))
    (ROOT / 'SHA256SUMS.txt').write_text(checksums, encoding='utf-8')
    print(f'Built Minecraft {version}: {count} ore definitions')

if __name__ == '__main__':
    build()
