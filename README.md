# Bounty Harvest

Bounty Harvest is a Forge 1.20.1 farm-management modpack built around a staged agricultural economy. Progression is about expanding an interconnected farm, turning production into repeatable Bountiful income, funding new tiers, and eventually automating industrial-scale orders.

## Progression model

The main game has **23 economic levels**. Every level adds one meaningful production layer, technology step, cuisine branch, or expedition system and ends in a one-time Market Order.

The quest book is intentionally branched. Core branches feed the level's Market Order; optional guidance branches reconnect through a post-market Mastery node instead of ending as disconnected spokes. Quest descriptions are normalized for compact FTB Quests windows with real paragraph spacing and safe display text.

| Level | Economy focus |
| --- | --- |
| 1 | Homestead, wheat, tools, storage, Bounty Board and first sale |
| 2 | Poultry, hearth, fuel, clay and shelter |
| 3 | Cattle, leather, fertilizer, ranching and brickwork |
| 4 | Carrots, pigs, wheat dough, flint tools and glass |
| 5 | Fishing, Aquaculture and Ocean's Delight |
| 6 | Sheep and textiles |
| 7 | Potatoes and pantry production |
| 8 | Sugar and baking |
| 9 | Copper workshop and copper-era utilities |
| 10 | Cabbage, Cutting Board and butchery |
| 11 | Corn, cornbread and tortillas |
| 12 | Tomato and taco economy |
| 13 | Ironworking |
| 14 | Onion and iron-kitchen expansion |
| 15 | Create mechanical farming and redstone control |
| 16 | Pineapple plantation and bakery |
| 17 | Rice, Slice and Dice, rolls and fried rice |
| 18 | Create Crafts and Additions power generation |
| 19 | Electric drive, storage and powered logistics |
| 20 | Wildlife cuisine and mature-farm exports |
| 21 | Alex's Caves deep expeditions |
| 22 | Twilight navigation and cuisine |
| 23 | End farming, End's Delight and final industrial provisioning |

Copper is deliberately a real era from Level 9 through Level 12. Ironworking arrives at Level 13. Create arrives at Level 15 only after the pre-automation farm economy has matured.

## Automation curve

Level 14 is the last intentionally hand-manageable tier. Once Create arrives at Level 15, renewable Bountiful demand doubles every level:

- L15: 4x
- L16: 8x
- L17: 16x
- L18: 32x
- L19: 64x
- L20: 128x
- L21: 256x
- L22: 512x
- L23: 1024x

The multiplier is for mature renewable production, not every newly introduced item. New frontier goods can begin at fixed volumes before later systems scale them, and rare ores, navigation items, expedition keys, motors, alternators, accumulators, maps, and tablets are not inflated just to make numbers larger.

Promotion costs follow the same industrial direction. Iron-coin costs grow through L15-L18, then the gold denomination continues the curve at 384 / 768 / 1536 / 3072 / 6144 gold coins for L19-L23 rather than resetting progression to a cheaper tier.

## Repeatable market and decrees

Bountiful is the repeatable market layer. Every level has a matching decree and objective pool. Older staples and processed goods continue returning so existing farms gain value instead of becoming obsolete.

Freshly crafted Bounty Boards are seeded with the placing player's highest unlocked `level_N` decree. This overrides Bountiful's default pristine-board behavior, which otherwise resolves a blank decree to a random loaded decree. Broken and re-placed boards retain their saved decree and bounty data.

World-generation-dependent progression crops such as corn and pineapple retain expensive deterministic recovery routes so biome luck cannot hard-lock progression.

## Validation and CI

CI protects:

- the complete 23-level promotion and Market Order spine;
- unique IDs, reachability, cycles, core-to-market connectivity, optional-to-Mastery connectivity, and controlled branch fan-out;
- readable paragraph spacing and safe FTB quest formatting;
- non-empty descriptions;
- crop and technology pacing;
- processor use and retained infrastructure;
- continuous promotion costs and 4x-1024x automation pressure;
- deterministic level-decree board seeding;
- CurseForge publisher modes;
- client/server archive construction and a hardened dedicated-server smoke boot.

CI is optimized for iteration: feature branches do not run duplicate `push` plus `pull_request` validation, superseded runs cancel automatically, and the expensive Windows archive/server job is gated behind a cheap Ubuntu preflight.

For the design rules behind these checks, see `PROGRESSION_DESIGN.md`.

Version: **0.12.0**
