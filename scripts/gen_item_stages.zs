import mods.itemstages.ItemStages;

// Bounty Harvest progression is item/namespace gating only. It does not claim
// to gate entity spawning, dimensions, or arbitrary world systems.

// Level 1 · Homestead & Orders (granted automatically on join)
ItemStages.restrict(<tag:items:minecraft:planks>, "level_1");
ItemStages.restrict(<item:minecraft:crafting_table>, "level_1");
ItemStages.restrict(<item:minecraft:stick>, "level_1");
ItemStages.restrict(<item:minecraft:wheat_seeds>, "level_1");
ItemStages.restrict(<item:minecraft:wheat>, "level_1");
ItemStages.restrict(<item:minecraft:bread>, "level_1");
ItemStages.restrict(<item:minecraft:wooden_axe>, "level_1");
ItemStages.restrict(<item:minecraft:wooden_hoe>, "level_1");
ItemStages.restrict(<item:minecraft:wooden_pickaxe>, "level_1");
ItemStages.restrict(<item:minecraft:wooden_shovel>, "level_1");
ItemStages.restrict(<item:minecraft:wooden_sword>, "level_1");

// Level 2 · Poultry & Hearth
ItemStages.restrict(<item:minecraft:egg>, "level_2");
ItemStages.restrict(<item:minecraft:feather>, "level_2");
ItemStages.restrict(<item:minecraft:chicken>, "level_2");
ItemStages.restrict(<item:minecraft:cooked_chicken>, "level_2");
ItemStages.restrict(<item:minecraft:furnace>, "level_2");
ItemStages.restrict(<item:minecraft:charcoal>, "level_2");
ItemStages.restrict(<item:farmersdelight:fried_egg>, "level_2");

// Level 3 · Cattle & Leather
ItemStages.restrict(<item:minecraft:beef>, "level_3");
ItemStages.restrict(<item:minecraft:cooked_beef>, "level_3");
ItemStages.restrict(<item:minecraft:leather>, "level_3");
ItemStages.restrict(<item:minecraft:leather_boots>, "level_3");
ItemStages.restrict(<item:minecraft:leather_chestplate>, "level_3");
ItemStages.restrict(<item:minecraft:leather_helmet>, "level_3");
ItemStages.restrict(<item:minecraft:leather_leggings>, "level_3");
ItemStages.restrict(<item:minecraft:string>, "level_3");
ItemStages.restrict(<item:minecraft:bow>, "level_3");

// Level 4 · Roots & Pork
ItemStages.restrict(<item:minecraft:carrot>, "level_4");
ItemStages.restrict(<item:minecraft:porkchop>, "level_4");
ItemStages.restrict(<item:minecraft:cooked_porkchop>, "level_4");
ItemStages.restrict(<item:farmersdelight:wheat_dough>, "level_4");
ItemStages.restrict(<item:minecraft:flint>, "level_4");
ItemStages.restrict(<item:minecraft:stone_axe>, "level_4");
ItemStages.restrict(<item:minecraft:stone_hoe>, "level_4");
ItemStages.restrict(<item:minecraft:stone_pickaxe>, "level_4");
ItemStages.restrict(<item:minecraft:stone_shovel>, "level_4");
ItemStages.restrict(<item:minecraft:stone_sword>, "level_4");

// Level 5 · Fisheries & Coast
ItemStages.restrict(<item:minecraft:fishing_rod>, "level_5");
ItemStages.restrict(<item:minecraft:cod>, "level_5");
ItemStages.restrict(<item:minecraft:salmon>, "level_5");
ItemStages.restrict(<item:minecraft:cooked_cod>, "level_5");
ItemStages.restrict(<item:minecraft:cooked_salmon>, "level_5");
ItemStages.restrict(<item:minecraft:bowl>, "level_5");
ItemStages.restrict(<item:minecraft:seagrass>, "level_5");
ItemStages.createModRestriction("aquaculture", "level_5");
ItemStages.createModRestriction("oceansdelight", "level_5");

// Level 6 · Wool, Sugar & Pantry
ItemStages.restrict(<tag:items:minecraft:wool>, "level_6");
ItemStages.restrict(<item:minecraft:mutton>, "level_6");
ItemStages.restrict(<item:minecraft:cooked_mutton>, "level_6");
ItemStages.restrict(<item:minecraft:sugar_cane>, "level_6");
ItemStages.restrict(<item:minecraft:sugar>, "level_6");
ItemStages.restrict(<item:minecraft:potato>, "level_6");
ItemStages.restrict(<item:minecraft:baked_potato>, "level_6");
ItemStages.restrict(<item:minecraft:red_mushroom>, "level_6");
ItemStages.restrict(<item:minecraft:brown_mushroom>, "level_6");
ItemStages.restrict(<item:minecraft:mushroom_stew>, "level_6");
ItemStages.restrict(<item:kubejs:wool_yarn>, "level_6");
ItemStages.restrict(<item:kubejs:wool_sweater>, "level_6");

// Level 7 · Copper Workshop
ItemStages.createModRestriction("bettercopper", "level_7");
ItemStages.restrict(<tag:items:minecraft:copper_ores>, "level_7");
ItemStages.restrict(<item:minecraft:raw_copper>, "level_7");
ItemStages.restrict(<item:minecraft:raw_copper_block>, "level_7");
ItemStages.restrict(<item:minecraft:copper_ingot>, "level_7");

// Ironworking is not a Level 7 sub-stage. The Level 10 promotion is the only
// progression reward that grants iron_age.
ItemStages.restrict(<tag:items:minecraft:iron_ores>, "iron_age");
ItemStages.restrict(<item:minecraft:iron_nugget>, "iron_age");
ItemStages.restrict(<item:minecraft:raw_iron>, "iron_age");
ItemStages.restrict(<item:minecraft:raw_iron_block>, "iron_age");
ItemStages.restrict(<item:minecraft:iron_ingot>, "iron_age");
ItemStages.restrict(<item:minecraft:iron_block>, "iron_age");
ItemStages.restrict(<item:minecraft:iron_axe>, "iron_age");
ItemStages.restrict(<item:minecraft:iron_hoe>, "iron_age");
ItemStages.restrict(<item:minecraft:iron_pickaxe>, "iron_age");
ItemStages.restrict(<item:minecraft:iron_shovel>, "iron_age");
ItemStages.restrict(<item:minecraft:iron_sword>, "iron_age");
ItemStages.restrict(<item:minecraft:iron_helmet>, "iron_age");
ItemStages.restrict(<item:minecraft:iron_chestplate>, "iron_age");
ItemStages.restrict(<item:minecraft:iron_leggings>, "iron_age");
ItemStages.restrict(<item:minecraft:iron_boots>, "iron_age");
ItemStages.restrict(<item:minecraft:shield>, "iron_age");
ItemStages.restrict(<item:minecraft:bucket>, "iron_age");
ItemStages.restrict(<item:minecraft:water_bucket>, "iron_age");
ItemStages.restrict(<item:minecraft:milk_bucket>, "iron_age");

// Level 8 · Market Garden & Hearth — one new crop: cabbage.
ItemStages.restrict(<item:farmersdelight:cabbage>, "level_8");
ItemStages.restrict(<item:farmersdelight:cabbage_seeds>, "level_8");
ItemStages.restrict(<item:farmersdelight:cutting_board>, "level_8");
ItemStages.restrict(<item:farmersdelight:flint_knife>, "level_8");
ItemStages.restrict(<item:farmersdelight:bacon>, "level_8");
ItemStages.restrict(<item:farmersdelight:cooked_bacon>, "level_8");
ItemStages.restrict(<item:farmersdelight:beef_patty>, "level_8");
ItemStages.restrict(<item:farmersdelight:chicken_cuts>, "level_8");
ItemStages.restrict(<item:farmersdelight:cooked_chicken_cuts>, "level_8");
ItemStages.restrict(<item:farmersdelight:cod_slice>, "level_8");
ItemStages.restrict(<item:farmersdelight:cooked_cod_slice>, "level_8");
ItemStages.restrict(<item:farmersdelight:salmon_slice>, "level_8");
ItemStages.restrict(<item:farmersdelight:cooked_salmon_slice>, "level_8");
ItemStages.restrict(<item:farmersdelight:chicken_sandwich>, "level_8");
ItemStages.restrict(<item:farmersdelight:fish_stew>, "level_8");
ItemStages.restrict(<item:farmersdelight:stuffed_potato>, "level_8");
ItemStages.restrict(<item:farmersdelight:pie_crust>, "level_8");
ItemStages.restrict(<item:farmersdelight:apple_pie>, "level_8");

// Level 9 · Corn & Tomato Market — one new supporting crop: tomato.
ItemStages.restrict(<item:farmersdelight:tomato>, "level_9");
ItemStages.restrict(<item:farmersdelight:tomato_seeds>, "level_9");
ItemStages.createModRestriction("corn_delight", "level_9");

// Level 10 · Iron & Industry — one new crop: onion, plus the iron kitchen/Create.
ItemStages.restrict(<item:farmersdelight:onion>, "level_10");
ItemStages.restrict(<item:farmersdelight:milk_bottle>, "level_10");
ItemStages.restrict(<item:farmersdelight:iron_knife>, "level_10");
ItemStages.restrict(<item:farmersdelight:cooking_pot>, "level_10");
ItemStages.restrict(<item:farmersdelight:skillet>, "level_10");
ItemStages.restrict(<item:farmersdelight:stove>, "level_10");
ItemStages.restrict(<item:farmersdelight:bacon_and_eggs>, "level_10");
ItemStages.createModRestriction("cookingforblockheads", "level_10");
ItemStages.createModRestriction("delightful", "level_10");
ItemStages.createModRestriction("create", "level_10");
ItemStages.restrict(<tag:items:minecraft:redstone_ores>, "level_10");
ItemStages.restrict(<item:minecraft:redstone>, "level_10");
ItemStages.restrict(<item:minecraft:redstone_block>, "level_10");

// Level 11 · Tropical Automation — rice and pineapple feed Slice & Dice scale.
ItemStages.restrict(<item:farmersdelight:rice>, "level_11");
ItemStages.restrict(<item:farmersdelight:rice_panicle>, "level_11");
ItemStages.restrict(<item:farmersdelight:cooked_rice>, "level_11");
ItemStages.restrict(<item:farmersdelight:salmon_roll>, "level_11");
ItemStages.restrict(<item:farmersdelight:cod_roll>, "level_11");
ItemStages.createModRestriction("pineapple_delight", "level_11");
ItemStages.createModRestriction("sliceanddice", "level_11");

// Level 12 · Power & Logistics
ItemStages.createModRestriction("createaddition", "level_12");
ItemStages.restrict(<tag:items:minecraft:gold_ores>, "level_12");
ItemStages.restrict(<item:minecraft:raw_gold>, "level_12");
ItemStages.restrict(<item:minecraft:raw_gold_block>, "level_12");
ItemStages.restrict(<item:minecraft:gold_ingot>, "level_12");
ItemStages.restrict(<item:minecraft:gold_block>, "level_12");

// Level 13 · Wildlife Cuisine
// Alex's Mobs itself is not namespace-gated: ItemStages cannot gate its entities.
ItemStages.restrict(<item:alexsmobs:animal_dictionary>, "level_13");
ItemStages.createModRestriction("alexsdelight", "level_13");

// Level 14 · Deep Expeditions
ItemStages.createModRestriction("alexscaves", "level_14");
ItemStages.restrict(<tag:items:minecraft:diamond_ores>, "level_14");
ItemStages.restrict(<item:minecraft:diamond>, "level_14");
ItemStages.restrict(<item:minecraft:diamond_block>, "level_14");
ItemStages.restrict(<tag:items:minecraft:lapis_ores>, "level_14");
ItemStages.restrict(<item:minecraft:lapis_lazuli>, "level_14");
ItemStages.restrict(<item:minecraft:lapis_block>, "level_14");
ItemStages.restrict(<item:minecraft:amethyst_shard>, "level_14");

// Level 15 · Twilight Frontier
ItemStages.createModRestriction("twilightforest", "level_15");
ItemStages.createModRestriction("twilightdelight", "level_15");
