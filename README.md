# Bounty Harvest

Bounty Harvest is a Forge 1.20.1 farm-management modpack built around a staged agricultural economy. Instead of treating progression as a vanilla checklist, the pack asks you to grow an increasingly interconnected farm, turn production into repeatable Bountiful income, fund level promotions, and eventually automate industrial-scale orders.

## Progression model

The main game is organized into 15 economic levels. Every level expands the farm with new crops, animals, processors, technology, cuisine, or exploration systems and ends in a one-time Market Order.

The quest book is intentionally **branched** rather than a straight promotion -> production -> order line. Each level exposes the relevant crop, livestock, processing, technology, exploration, and support paths separately, then converges the important branches on the Market Order. Optional guidance can remain visible without becoming a mandatory progression tax.

Quest descriptions are formatted for the compact FTB Quests window: distinct ideas are separated into paragraphs and long prose is reflowed instead of appearing as a wall of text. Natural-language ampersands are avoided because FTB Quests interprets `&` as a formatting prefix.

| Level | Economy focus |
| --- | --- |
| 1 | Homestead, wheat, tools, storage, Bounty Board and first sale |
| 2 | Poultry, hearth, fuel, clay and shelter |
| 3 | Cattle, leather, fertilizer, ranching and brickwork |
| 4 | Carrots, pigs, wheat dough, flint tools and glass |
| 5 | Fishing, Aquaculture and Ocean's Delight |
| 6 | Sheep, textiles, potatoes, sugar and pantry production |
| 7 | Copper Workshop, copper tools and workshop supplies |
| 8 | Cabbage Market Garden, Cutting Board and pre-iron prepared food |
| 9 | Corn, tomato, cornbread, tortillas and tacos |
| 10 | Ironworking, onion, Iron Kitchen, Create and redstone |
| 11 | Pineapple, rice, Slice and Dice and tropical automation |
| 12 | Create Crafts and Additions power, storage and logistics |
| 13 | Wildlife cuisine and mature farm exports |
| 14 | Alex's Caves deep expeditions and industrial provisioning |
| 15 | Twilight/End frontier, Twilight's Flavors and Delight, and End's Delight |

Copper deliberately remains the active technology tier through Levels 7-9. Ironworking unlocks only at Level 10, when Create arrives and the economy begins shifting from hand production toward automation.

## Automation curve

Level 9 is the last intentionally hand-manageable tier. After Create unlocks, renewable Bountiful demand grows geometrically:

- Level 10: 4x
- Level 11: 8x
- Level 12: 16x
- Level 13: 32x
- Level 14: 64x
- Level 15: 128x

Late promotions and Market Orders also grow sharply. By the final levels, a player is expected to operate automated farms, kitchens, storage, processing, and logistics rather than hand-crafting hundreds of products.

Permanent infrastructure is normally retained. Motors, accumulators, Cave Tablets, and navigation maps prove capability or enable the economy; orders consume the renewable production they make possible instead of requiring the player to throw expensive machines away.

## Repeatable market

Bountiful is the repeatable market layer. Each level awards a decree for that tier, and later bounty pools intentionally mix newly unlocked goods with older staples and increasingly processed products.

The goal is for old production to gain value as the farm grows. Wheat, livestock products, fish, corn, prepared foods, and other early chains continue to appear in later recipes, promotions, Market Orders, and repeatable bounties.

Required renewable inputs that can otherwise depend on world-generation luck have expensive deterministic recovery routes. Natural exploration remains cheaper, but a bad seed or biome location should not permanently block progression.

## Validation

The repository contains automated progression checks for:

- quest IDs, dependencies, cycles and reachability;
- the complete 15-level Market Order spine;
- branched level structure rather than three-node linear chapters;
- readable paragraph spacing and safe FTB quest-text formatting;
- non-empty quest descriptions;
- delayed Level 10 Ironworking;
- crop pacing and recovery paths;
- processor use;
- promotion and automation-demand scaling;
- retained infrastructure;
- late-game integration demand;
- client/server archive construction and dedicated-server smoke boot.

For the design rules behind these checks, see `PROGRESSION_DESIGN.md`.

## Building the pack

The repository includes PowerShell tooling for constructing the client and dedicated-server archives and for publishing CurseForge builds. CI validates both archive variants and performs a dedicated Forge server boot before release changes are considered safe.

Version: **0.12.0**
