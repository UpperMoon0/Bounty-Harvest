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

## 7. Every main level ends in a Market Order

Each level's main progression must culminate in a one-time Market Order.

The Market Order should:

- consume multiple outputs from that level's economy;
- normally pull at least one older production line back into demand;
- prove that the new chain is sustainable, not just that one item was found;
- unlock the next promotion path.

## 8. Promotions consume value from the previous economy

Promotion quests should require goods and currency earned from the preceding tier. This makes level advancement an economic decision rather than a free stage toggle.

Do not require a currency denomination before that denomination is a normal reward tier.

## 9. Bountiful is the repeatable market layer

The Bounty Board and level decrees are repeatable orders. Their job is to keep the whole farm economically relevant between one-time Market Orders.

Later bounty pools should deliberately mix:

- newly unlocked goods;
- staples from older levels;
- increasingly processed versions of old ingredients.

A later pool should not consist entirely of that level's newest items.

## 10. Side shops support progression; they do not replace it

Animal, crop, decoration, and decree shops are support systems. They should unlock when their goods become economically relevant and use currency appropriate for that point in progression.

Buying a replacement decree never advances the main level spine.

## 11. Stage only what can be staged reliably

ItemStages can reliably gate items and namespaces. It cannot reliably gate every entity, world-generation system, dimension mechanic, or exploration event.

Do not describe or design a stage as if it blocks systems that technically remain accessible. Gate progression-facing items where reliable and let quests/economy provide the intended path for the rest.

## 12. Validate the progression contract

Automated validation should protect structural rules that are easy to regress, including:

- every quest has a useful description;
- all 15 main levels remain connected;
- every level has a Market Order;
- the promotion spine has no cycles or dangling dependencies;
- currency tiers are coherent;
- Copper remains pre-Ironworking progression;
- Ironworking is not granted before Level 10;
- major introduced production lines continue to receive later demand.

When a validator cannot prove a qualitative rule, review the progression manually against this document before merging.
