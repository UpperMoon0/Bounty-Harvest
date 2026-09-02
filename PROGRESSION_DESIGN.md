# Bounty Harvest Progression Design Philosophy

This document is the design contract for Bounty Harvest's main progression. When adding or revising quests, recipes, stages, bounty pools, shops, or level themes, preserve these rules unless there is a deliberate reason to change the progression model.

## 1. The farm is an expanding economy, not a checklist

Each level should add a meaningful economic expansion: a crop, animal, processor, machine, cuisine, expedition, or production method that creates new goods and changes what existing goods are worth.

A level is weak if its core loop is only "obtain N of this new item." New content should feed into production chains, prepared goods, market demand, or later technology.

## 2. Old production must keep gaining value

A core ingredient should not become dead inventory after the level that introduces it.

As a target:

- Within about 2 levels, an important ingredient should gain a new processing step, composite recipe, or upgraded use.
- Within about 3 levels, it should receive meaningful demand again through a Market Order, Bountiful pool, promotion cost, or a later product chain.
- Re-requesting the exact same raw item after a long gap is not enough by itself. Prefer increasing complexity: raw ingredient -> processed ingredient -> prepared product -> industrial or premium use.

Strong examples are wheat, corn, and pineapple: later systems reuse earlier inputs and convert them into higher-value goods.

## 3. New levels multiply old systems instead of replacing them

Progression should resemble a farm-management game. A new crop or machine should make several existing production lines more useful.

Prefer recipes such as:

- new crop + old meat + old vegetable -> new prepared food
- old fuel + current metal -> new processing tier
- old textile + new machine -> higher-value product

Avoid isolated branches where a player builds an entire farm or processor for one level and never needs it again.

## 4. Introduce new inputs at a controlled pace

Do not overload one level with several independent crops, animals, or machines unless they are tightly linked.

For normal agricultural levels, one major new crop or production family is usually enough. Additional crops should be staggered into later levels so each one has room to establish its own recipes, demand, and identity.

A level may add several outputs when they belong to one coherent chain, such as corn -> tortilla -> taco.

## 5. Technology tiers must have room to breathe

A material tier should be an era, not a five-minute prerequisite for the next material.

For metals and machinery:

- Unlock the raw material first.
- Let it support useful tools, processors, recipes, and infrastructure across multiple levels.
- Require mastery of that era, plus older economic inputs, before the next technology tier appears.

Copper therefore must remain the active technology tier across Levels 7-9. Ironworking belongs at Level 10, after the player has had time to build a mature copper-era economy.

## 6. Processing complexity should rise gradually

Early levels should favor raw goods and simple cooking. Later levels should increasingly ask for processed and multi-input products.

A useful progression shape is:

1. raw crop or animal output
2. basic processed ingredient
3. simple prepared product
4. composite meal or manufactured good
5. automated / industrial production
6. premium or expedition product

Do not make sophisticated food depend entirely on Ironworking. The pre-iron economy still needs meaningful cooking and processing; iron should unlock new methods and scale, not cooking itself.

When a level introduces a processor, the progression should actually use its outputs. A cutting board, slicer, machine, or logistics system should not be a decorative unlock that the player's required recipes can bypass.

## 7. Automation is earned by throughput pressure

Automation should solve a real economic problem. Do not teach automation by asking the player to craft one machine and immediately sell or discard it.

Once Create arrives at Level 10, renewable order volume should grow geometrically. The current repeatable Bountiful target curve is intentionally explicit:

- Level 10: 4x renewable-demand scale
- Level 11: 8x
- Level 12: 16x
- Level 13: 32x
- Level 14: 64x
- Level 15: 128x

One-time Market Orders and promotion costs should follow the same direction: later tiers must require dramatically more economic output than earlier tiers. By the late game, hand production should remain technically possible but obviously inferior to building automated farms, kitchens, storage, and logistics.

Apply this pressure to renewable production: crops, processed ingredients, prepared foods, livestock products, and automatable industrial materials. Do **not** scale rare maps, tablets, unique exploration objects, or specialist machines to hundreds of copies merely to make a number larger.

Core infrastructure normally stays with the player. Motors, accumulators, navigation maps, expedition tablets, and similar enabling objects should prove capability and then be used; the market should consume the output they enable.

## 8. Every main level ends in a Market Order

Each level's main progression must culminate in a one-time Market Order.

The Market Order should:

- consume multiple outputs from that level's economy;
- normally pull at least one older production line back into demand;
- prove that the new chain is sustainable, not just that one item was found;
- become increasingly throughput-oriented after automation unlocks;
- unlock the next promotion path.

## 9. Promotions consume value from the previous economy

Promotion quests should require goods and currency earned from the preceding tier. This makes level advancement an economic decision rather than a free stage toggle.

Do not require a currency denomination before that denomination is a normal reward tier.

Promotion costs should rise sharply with the economy. After industrialization, each new level should feel like funding an expansion of the farm rather than paying a token quest fee.

## 10. Bountiful is the repeatable market layer

The Bounty Board and level decrees are repeatable orders. Their job is to keep the whole farm economically relevant between one-time Market Orders.

Later bounty pools should deliberately mix:

- newly unlocked goods;
- staples from older levels;
- increasingly processed versions of old ingredients;
- high-volume renewable objectives that reward investment in automation.

A later pool should not consist entirely of that level's newest items. Reward amount caps must also be high enough that industrial orders can remain economically worthwhile instead of demanding hundreds of items for a payout capped at a few coins.

## 11. Side shops support progression; they do not replace it

Animal, crop, decoration, and decree shops are support systems. They should unlock when their goods become economically relevant and use currency appropriate for that point in progression.

Buying a replacement decree never advances the main level spine.

A progression-required renewable input must have a deterministic recovery route if world generation or exploration luck can otherwise hard-lock the player. Recovery trades should be deliberately expensive so natural discovery remains preferable without making bad biome luck a progression blocker.

## 12. Stage only what can be staged reliably

ItemStages can reliably gate items and namespaces. It cannot reliably gate every entity, world-generation system, dimension mechanic, or exploration event.

Do not describe or design a stage as if it blocks systems that technically remain accessible. Gate progression-facing items where reliable and let quests/economy provide the intended path for the rest.

Do not stage an entire integration merely because it is installed. If a mod has no progression branch, meaningful order demand, or intentional support role yet, leave it out of the level contract until it does.

A staged integration is justified when the level actually establishes and retains its economy. Level 15 End's Delight is the reference example: the stage unlocks a chorus-fruit production branch, that branch consumes older farm inputs such as wheat, sugar, and pie crust, the one-time Market Order consumes the resulting pies at industrial scale, and repeatable Bountiful orders keep the product relevant afterward.

## 13. Validate the progression contract

Automated validation should protect structural rules that are easy to regress, including:

- every quest has a useful description;
- all 15 main levels remain connected;
- every level has a Market Order;
- the promotion spine has no cycles or dangling dependencies;
- currency tiers are coherent;
- Copper remains pre-Ironworking progression;
- Ironworking is not granted before Level 10;
- major introduced production lines continue to receive later demand;
- required crops have deterministic recovery paths when world generation can fail the player;
- processors used by the design cannot be bypassed by required recipes;
- automation-era promotion costs and Bountiful demand preserve the intended growth curve;
- infrastructure objects are retained where the economic test is supposed to be throughput;
- staged late-game integrations must have both a real progression objective and recurring economic demand.

When a validator cannot prove a qualitative rule, review the progression manually against this document before merging.
