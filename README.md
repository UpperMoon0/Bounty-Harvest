# Bounty Harvest

CurseForge page: https://legacy.curseforge.com/minecraft/modpacks/bounty-harvest

Minecraft 1.20.1 · Forge 47.4.23 · Java 17 · Beta

![Bounty Harvest](https://i.imgur.com/qIHoZxx.png?1)

Bounty Harvest is a progression-based farming and production modpack built around a 15-level farm economy. Grow crops, raise animals, process food, automate production, explore for specialist resources, and sell the results through Bountiful orders.

The level system follows a farm-management progression rather than a vanilla checklist:

- every level introduces a coherent production expansion;
- older crops and goods remain useful in later recipes and bounty pools;
- each level ends with a one-time Market Order that proves the new supply chain works;
- the Bounty Board is the repeatable order board that turns production into copper, iron, and gold coins;
- coins remain globally usable and can be exchanged at 9:1 between denominations.

The detailed design contract lives in [`PROGRESSION_DESIGN.md`](PROGRESSION_DESIGN.md). In particular, major production lines should gain a new processing layer within roughly two levels and meaningful demand within roughly three; technology eras must have room to breathe instead of acting as instant prerequisites.

## Progression

| Level | Economy expansion |
| --- | --- |
| 1 | Homestead, wheat, bread, Bounty Board |
| 2 | Poultry, eggs, charcoal hearth |
| 3 | Cattle, beef, leather |
| 4 | Carrots, pork, Farmer's Delight dough |
| 5 | Fishing, Aquaculture 2, Ocean's Delight |
| 6 | Sheep, wool processing, potatoes, sugar, mushrooms |
| 7 | Better Copper workshop, copper tools, workshop supplies; copper era begins |
| 8 | Cabbage Market Garden, flint-knife processing, chicken/fish/apple prepared foods |
| 9 | Corn Delight + tomato; tacos reconnect pork and cabbage to the new crops |
| 10 | Ironworking, onion, iron kitchen, Create foundations and redstone |
| 11 | Pineapple Delight + rice + Slice & Dice; rice reconnects fisheries through fish rolls |
| 12 | Create Crafts & Additions power and logistics |
| 13 | Alex's Mobs fieldwork + Alex's Delight cuisine |
| 14 | Alex's Caves expeditions and deep resources |
| 15 | Twilight Forest + Twilight's Flavors & Delight + End's Delight frontier economy |

Copper is intentionally the active metal across Levels 7-9. Completing the copper tool milestone does **not** unlock iron; the Level 10 promotion is the only main-progression reward that grants Ironworking.

Create begins the automation era at Level 10. Repeatable renewable order demand then scales geometrically from 4x at Level 10 to 128x at Level 15, while rare maps, tablets, and enabling machines stay out of bulk repeatable objectives. The late game is deliberately balanced around automated farms, kitchens, storage, and logistics rather than manual crafting hundreds of items.

ItemStages is used where item or namespace containment is reliable. The pack does **not** claim to stage entity spawning, dimensions, or arbitrary world systems that ItemStages cannot actually enforce.

![Quests](https://i.imgur.com/Gscc4gd.png)
![Bounties](https://i.imgur.com/ggEx4YP.png)
![Farm](https://i.imgur.com/jcWJjKg.png)
![Wilderness](https://i.imgur.com/hYRrwNi.png)

## Reproducible releases

`pack/pack.json` is the source of truth for the pack version, Minecraft/Forge versions, Java requirement, release channel, and client/server exclusions. `minecraftinstance.json` stores sanitized CurseForge project/file metadata from the tested launcher profile.

The local CurseForge Dev profile can use `tools/link_curseforge_instance.ps1` from an elevated PowerShell window to link its metadata to this repository. After changing mods in CurseForge, run `./tools/sanitize_minecraftinstance.ps1` before validating or committing so launcher paths and local state are not published.

Build both release archives from PowerShell:

```powershell
./tools/build_modpack.ps1
python tools/verify_archives.py
```

Outputs:

- `dist/Bounty-Harvest-<version>.zip` — CurseForge client manifest with runtime overrides
- `dist/Bounty-Harvest-<version>-server.zip` — dedicated server, Forge installer, and launchers

Pull requests validate the 15-level quest graph, declared roots, market-order spine, delayed Ironworking gate, generated Bountiful data, deterministic crop recovery, processor use, automation-economy scaling, retained infrastructure, late-game integration branches, pack invariants, archive client/server split, and dedicated-server boot. A version change merged into `main` creates the GitHub release after a successful build; CurseForge publishing runs independently.

CurseForge publication is split into client and server-child jobs. After the client upload succeeds, its file ID and archive hash are persisted as a short-lived Actions artifact so **Re-run failed jobs** can retry a failed server-child upload without uploading the client again. `CURSEFORGE_API_TOKEN` is required for author uploads. `CURSEFORGE_CORE_API_KEY` remains optional but recommended for duplicate-file recovery across separate workflow runs or ambiguous upload responses.
