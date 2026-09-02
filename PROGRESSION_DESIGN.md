# Bounty Harvest Progression Design Philosophy

This document is the design contract for Bounty Harvest. Quests, recipes, stages, shops, Bountiful pools, and future integrations should preserve these rules unless the progression model is deliberately changed.

## 1. The farm is an expanding economy, not a checklist

Every level should change the player's economy. A crop, animal, processor, machine, cuisine, expedition, or production method is useful only when it creates new production chains, new demand, or new ways to scale existing production.

A level whose core loop is only "obtain N of the new item" is incomplete.

## 2. Old production must keep gaining value

Important inputs should not become dead inventory after their introduction.

As a target:

- within about two levels, an important input should gain a new processing step, composite recipe, or upgraded use;
- within about three levels, it should receive meaningful demand again through a Market Order, Bountiful pool, promotion cost, or later product chain;
- later demand should preferably increase complexity: raw good -> processed ingredient -> prepared product -> industrial or premium use.

Simply asking for the same raw item again after a long gap is weak reuse.

## 3. New systems multiply old systems

A new crop or machine should make several existing production lines more useful. Prefer composite chains such as new crop + old meat + old vegetable, or a new processor that turns established farm output into a higher-value good.

Avoid isolated farms or machines that matter for one quest and are never relevant again.

## 4. Introduce new inputs at a controlled pace

One major new crop or production family per normal agricultural level is usually enough. Several outputs are fine when they form one coherent chain, such as corn -> tortilla -> taco.

Do not dump several independent ingredients, processors, and product families into one promotion merely because they are related to food.

The current 23-level spine deliberately separates systems that were previously compressed together:

- L6 wool/textiles
- L7 potatoes/pantry
- L8 sugar/baking
- L9 copper
- L10 cabbage/butchery
- L11 corn
- L12 tomato/tacos
- L13 iron
- L14 onion/kitchen
- L15 Create
- L16 pineapple
- L17 rice/Slice and Dice
- L18 power generation
- L19 electric drive/storage
- L20 wildlife cuisine
- L21 deep expeditions
- L22 Twilight
- L23 End

## 5. Technology tiers need room to breathe

A technology tier is an era, not a five-minute prerequisite.

Unlock the material first, let it support useful tools and infrastructure, and require the economy to mature before the next tier appears. Copper therefore begins at Level 9 and remains the active metal through Level 12. Ironworking arrives only at Level 13. Create arrives only at Level 15.

Electrical progression is also sequential: Level 18 establishes generation with the alternator; Level 19 adds electric drive and storage with the motor and accumulator.

## 6. Processing complexity rises gradually

A useful progression shape is:

1. raw crop or animal output
2. basic processed ingredient
3. simple prepared product
4. composite meal or manufactured good
5. automated or industrial production
6. premium or expedition product

Processors must matter. If a level introduces a Cutting Board, Slicer, machine, or logistics system, required products should use the outputs or capability of that processor rather than bypassing it through simpler recipes.

## 7. Automation is earned by throughput pressure

Automation should solve a real economic problem. Do not teach automation by asking the player to craft a machine and immediately sell it.

Create begins at Level 15. From there, repeatable renewable Bountiful demand follows an explicit geometric curve:

- L15: 4x
- L16: 8x
- L17: 16x
- L18: 32x
- L19: 64x
- L20: 128x
- L21: 256x
- L22: 512x
- L23: 1024x

This multiplier belongs on mature renewable production: crops, processed ingredients, prepared foods, livestock goods, and other automatable output. It does **not** automatically apply to a newly introduced frontier ingredient on the same level. A new item should first establish its production identity before later demand scales it.

Rare ores, maps, tablets, expedition keys, and enabling machines must not be multiplied into absurd quantities simply to make a tier look harder.

## 8. Promotion costs must not reset at denomination changes

Promotions consume value from the preceding economy. When currency changes denomination, effective cost must continue rising instead of becoming cheaper.

The industrial curve currently reaches 192 / 384 / 768 / 1536 iron coins at L15-L18, then continues at 384 / 768 / 1536 / 3072 / 6144 gold coins at L19-L23, alongside previous-economy goods.

Late advancement should feel like funding a major expansion of the farm.

## 9. Every main level ends in a Market Order

The one-time Market Order is the proof that a level's economy is sustainable. It should consume multiple meaningful outputs, reconnect older production, and increasingly test throughput after automation arrives.

Core quest branches must lead into the Market Order. Intermediate convergence is encouraged when it makes the graph read naturally; the Market Order itself does not need artificial parallel prerequisites if several branches already converged in a meaningful production quest.

## 10. Optional branches must reconnect

Optional guidance should not become a mandatory progression tax, but it also should not appear as a disconnected line in the quest book.

An optional branch should reconnect through a post-market **Mastery** node. That keeps the main promotion path focused while making the chapter visually coherent.

A normal level should not explode into many unrelated quests directly from its promotion node. Related production steps should be sequenced downstream.

## 11. Infrastructure stays with the player

Motors, alternators, accumulators, Cutting Boards, Slicers, Cave Tablets, Magic Maps, and similar enabling objects prove capability and should normally be retained.

Markets consume the output those systems enable rather than repeatedly forcing the player to rebuild infrastructure.

## 12. Bountiful is the repeatable market layer

Each level has a matching decree and repeatable objective pool. Later pools should mix newly relevant goods, older staples, processed products, and high-volume renewable objectives.

Reward caps must be high enough that industrial orders remain economically worthwhile.

A fresh Bounty Board must reflect progression. Bountiful 6.0.4 normally gives a pristine board a blank decree and later resolves it to a random loaded decree, which is incompatible with a level-based economy. Bounty Harvest therefore seeds a newly crafted board with the placing player's highest unlocked `level_N` decree. A board carrying saved block-entity data must keep its existing decrees and bounties when re-placed.

## 13. Shops are recovery/support systems

Animal, crop, decoration, and decree shops support progression but do not replace it. Buying a decree never advances the main level spine.

A progression-required renewable input must have an expensive deterministic recovery route when world generation or exploration luck could otherwise hard-lock the player. Natural discovery should remain preferable.

## 14. Stage only what can be staged reliably

ItemStages reliably gates items and namespaces. It cannot honestly guarantee every entity spawn, dimension mechanic, world-generation feature, or exploration event.

Do not claim stronger gating than the implementation provides. Do not namespace-gate an integration just because it is installed; staged integrations need a real progression branch and recurring economic role.

Twilight and End are deliberately separate tiers. Level 22 establishes Twilight navigation before Twilight cuisine. Level 23 establishes renewable chorus fruit before End's Delight processing.

## 15. Quest text must be readable

FTB Quests is part of the gameplay interface, not a database dump.

- separate distinct ideas with blank paragraph entries;
- split oversized prose at sentence boundaries;
- keep short descriptions concise;
- avoid natural-language `&` in displayed text because FTB Quests treats it as a legacy formatting prefix;
- run `python tools/format_quest_text.py --write` after editing quest prose.

## 16. Validate the philosophy, not only syntax

CI protects rules that are easy to regress:

- all 23 main levels exist and form one promotion spine;
- IDs are unique and dependencies are reachable and acyclic;
- every core quest reaches its Market Order;
- optional branches reconnect through Mastery;
- promotion fan-out stays controlled instead of becoming an unlock dump;
- every quest has a useful description and normalized display text;
- crop, processor, metal, and integration pacing stays intentional;
- Ironworking remains at L13 and Create at L15;
- required crops keep deterministic recovery paths;
- processors cannot be bypassed by required progression recipes;
- promotion costs remain continuous across currency changes;
- renewable automation pressure remains 4x through 1024x from L15-L23;
- infrastructure is retained where the intended test is throughput;
- fresh Bounty Boards receive the correct level decree;
- staged late integrations have both a progression objective and repeatable economic demand.

When a qualitative rule cannot be proved mechanically, review the progression manually against this document before merging.
