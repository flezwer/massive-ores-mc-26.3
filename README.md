# Massive Ores — Minecraft Java 26.3

An open-source, data-only ore generation mod for **Minecraft Java 26.3**.
Original tools and modifications are available under the MIT license.

## Download and install

- **Mod:** [massive-ores-1.0.0-mc26.3.jar](massive-ores-1.0.0-mc26.3.jar). Open the file on GitHub, select
  **Download raw file**, and place the JAR in your instance's `mods/` directory.
- **Datapack:** [massive-ores-1.0.0-mc26.3.zip](massive-ores-1.0.0-mc26.3.zip). Place the ZIP in
  `saves/<world>/datapacks/` and restart the world. Do not extract it.
- Install only one of these options. **Code → Download ZIP** downloads this
  repository's source code, not the installable datapack.
- Fabric requires Fabric API. Quilt requires a resource API compatible with
  your Quilt version. Forge and NeoForge do not require Fabric API.
- Use a loader available for Minecraft 26.3. On servers, install on the
  server. Explore newly generated terrain to find the modified veins.

## Ores and generation

Includes coal, iron, gold, lapis lazuli, diamond, emerald, redstone, copper,
Nether quartz, Nether gold, and ancient debris for netherite, including
deepslate variants. Ancient debris generates in clusters instead of scattered
individual blocks.

Each generation attempt selects a **generation size from 20 to 30**, with equal
probability. **This does not guarantee 20–30 physical blocks per vein:** terrain,
caves, geometry and intersecting veins affect the resulting block count.
Vanilla's noise-based giant iron/copper veins remain unchanged.
Height ranges, biomes, frequency, replacement rules and air-exposure settings
are preserved. Existing terrain and ores added by other mods are not modified.

## Compatibility and testing

Includes metadata for Fabric, Quilt through Fabric compatibility, Forge and
NeoForge. Compatibility is based on their data-mod formats; **not tested in
Minecraft** or across every loader combination. Other mods or datapacks may
override the same ore definitions.

Static validation checks JSON, references, ore coverage, uniform probabilities,
metadata, archive integrity and SHA-256 checksums.

## Build from source

Requires Python 3.11 or newer. No external packages, Java or network required:

```sh
python build.py
python verify.py
```

`core.py` implements generation and defines `MIN_SIZE` and `MAX_SIZE`.
`vanilla.json` stores the reference data for Minecraft 26.3 and its source
URL. `build.py` creates reproducible JAR and datapack files.
`SHA256SUMS.txt` contains checksums for the downloads. Tests currently verify
the 20–30 range; update `verify.py` if you change that range.

## Contributing

Report issues with your Minecraft version, loader and reproduction steps.
For changes, create a branch, run the build and validation, and submit a pull
request. Original code is MIT-licensed; vanilla data retains its own terms.

## Attribution

Vanilla data is extracted by [misode/mcmeta](https://github.com/misode/mcmeta),
tag `26.3-data`. Minecraft belongs to Mojang/Microsoft.
This project is not affiliated with Mojang or Microsoft.
