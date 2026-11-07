ServerEvents.recipes((e) => {
    // Level 1 · Homestead & Orders
    e.remove({id: 'bountiful:crafting/bountyboard'})
    e.shaped('bountiful:bountyboard', [
        'WWW',
        'WCW',
        'WWW'
    ], {
        W: '#minecraft:planks',
        C: 'minecraft:wheat_seeds'
    })

    // Level 2 · Poultry & Hearth
    e.remove({output: 'minecraft:torch'})
    e.shaped('2x minecraft:torch', [
        'C',
        'S'
    ], {
        C: 'minecraft:charcoal',
        S: 'minecraft:stick'
    })

    // Level 4 · Roots & Pork
    e.remove({id: 'create:smelting/bread'})
    e.remove({output: 'farmersdelight:wheat_dough'})
    e.shaped('2x farmersdelight:wheat_dough', [
        'WW',
        'WE'
    ], {
        W: 'minecraft:wheat',
        E: 'minecraft:egg'
    })

    const flintTools = {
        stone_pickaxe: ['AAA', ' B ', ' B '],
        stone_axe: ['AA', 'AB', ' B'],
        stone_shovel: ['A', 'B', 'B'],
        stone_hoe: ['AA', ' B', ' B'],
        stone_sword: ['A', 'A', 'B']
    }
    Object.entries(flintTools).forEach(([tool, pattern]) => {
        e.remove({id: `minecraft:${tool}`})
        e.shaped(`minecraft:${tool}`, pattern, {
            A: 'minecraft:flint',
            B: 'minecraft:stick'
        })
    })

    // Level 5 · Fisheries & Coast
    // Keep the vanilla fishing-rod recipe. Fisheries must remain available before Ironworking.

    // Level 6 · Wool, Sugar & Pantry
    e.remove({id: 'minecraft:white_wool_from_string'})
    e.shaped('2x kubejs:wool_yarn', [
        'WS',
        'SW'
    ], {
        W: '#minecraft:wool',
        S: 'minecraft:string'
    })
    e.shaped('kubejs:wool_sweater', [
        'W W',
        'WDW',
        'WWW'
    ], {
        W: 'kubejs:wool_yarn',
        D: 'minecraft:orange_dye'
    })

    // Level 7 · Copper Workshop
    // Iron recipes exist globally, but ItemStages keeps every iron input/output behind
    // the Ironworking stage granted by the Level 10 promotion.
    e.remove({id: 'minecraft:iron_ingot_from_smelting_iron_ore'})
    e.remove({id: 'minecraft:iron_ingot_from_smelting_deepslate_iron_ore'})
    e.remove({id: 'minecraft:iron_ingot_from_smelting_raw_iron'})
    e.remove({id: 'create:smelting/iron_ingot_from_crushed'})
    e.smelting('3x minecraft:iron_nugget', 'minecraft:raw_iron').xp(0.7)

    e.remove({id: 'minecraft:copper_ingot_from_smelting_copper_ore'})
    e.remove({id: 'minecraft:copper_ingot_from_smelting_deepslate_copper_ore'})
    e.remove({id: 'minecraft:copper_ingot_from_smelting_raw_copper'})
    e.smelting('3x bettercopper:copper_nugget', 'minecraft:raw_copper').xp(0.7)

    // Copper has utility recipes across the whole L7-L9 era instead of existing only
    // as a five-minute tool prerequisite.
    e.remove({id: 'minecraft:glass_bottle'})
    e.shaped('3x minecraft:glass_bottle', [
        ' C ',
        'G G',
        ' G '
    ], {
        C: 'bettercopper:copper_nugget',
        G: '#forge:glass'
    })

    e.remove({id: 'minecraft:composter'})
    e.shaped('minecraft:composter', [
        'A A',
        'A A',
        'ABA'
    ], {
        A: '#minecraft:wooden_slabs',
        B: 'minecraft:copper_ingot'
    })

    // Level 8 · Market Garden & Hearth
    // Prepared foods now require the cutting-board outputs unlocked at this level.
    // The flint knife/cutting board therefore form a real processing tier rather than
    // cosmetic unlocks that can be bypassed by whole-meat crafting recipes.
    e.remove({output: 'farmersdelight:chicken_sandwich'})
    e.shaped('farmersdelight:chicken_sandwich', [
        'BC',
        'DR'
    ], {
        B: 'minecraft:bread',
        C: 'farmersdelight:cooked_chicken_cuts',
        D: 'farmersdelight:cabbage',
        R: 'minecraft:carrot'
    })

    e.remove({output: 'farmersdelight:fish_stew'})
    e.shapeless('farmersdelight:fish_stew', [
        'minecraft:bowl',
        'farmersdelight:cooked_cod_slice',
        'farmersdelight:cooked_salmon_slice',
        'minecraft:baked_potato',
        'minecraft:carrot'
    ])

    e.remove({output: 'farmersdelight:stuffed_potato'})
    e.shaped('farmersdelight:stuffed_potato', [
        'AB',
        'C '
    ], {
        A: 'minecraft:baked_potato',
        B: 'farmersdelight:beef_patty',
        C: 'farmersdelight:cabbage'
    })

    // Apple finally becomes a processed product without waiting for an iron bucket.
    e.remove({output: 'farmersdelight:pie_crust'})
    e.shaped('farmersdelight:pie_crust', [
        'DDD',
        ' E '
    ], {
        D: 'farmersdelight:wheat_dough',
        E: 'minecraft:egg'
    })

    e.remove({output: 'farmersdelight:apple_pie'})
    e.shaped('farmersdelight:apple_pie', [
        'AAA',
        ' S ',
        ' C '
    ], {
        A: 'minecraft:apple',
        S: 'minecraft:sugar',
        C: 'farmersdelight:pie_crust'
    })

    // Level 9 · Corn & Tomato Market
    // The taco is the main cross-level product: L9 corn/tomato + L8 cabbage + L4 pork.
    e.remove({output: 'corn_delight:taco'})
    e.shapeless('2x corn_delight:taco', [
        'corn_delight:tortilla',
        'minecraft:cooked_porkchop',
        'farmersdelight:tomato',
        'farmersdelight:cabbage'
    ])

    // Level 10 · Iron & Industry
    e.remove({id: 'minecraft:chain'})
    e.shaped('3x minecraft:chain', [
        ' N ',
        ' I ',
        ' N '
    ], {
        N: 'minecraft:iron_nugget',
        I: 'minecraft:iron_ingot'
    })
    e.shaped('minecraft:chainmail_helmet', ['III', 'I I'], { I: 'minecraft:chain' })
    e.shaped('minecraft:chainmail_chestplate', ['I I', 'III', 'III'], { I: 'minecraft:chain' })
    e.shaped('minecraft:chainmail_leggings', ['III', 'I I', 'I I'], { I: 'minecraft:chain' })
    e.shaped('minecraft:chainmail_boots', ['I I', 'I I'], { I: 'minecraft:chain' })

    e.remove({id: 'minecraft:cake'})
    e.remove({id: 'farmersdelight:cake_from_milk_bottle'})
    e.remove({id: 'create:crafting/curiosities/cake'})
    e.shaped('minecraft:cake', [
        'AAA',
        'BDB',
        'CCC'
    ], {
        A: 'minecraft:milk_bucket',
        B: 'minecraft:sugar',
        D: 'minecraft:egg',
        C: 'farmersdelight:wheat_dough'
    })

    // Currency exchange remains lossless. Currency denomination is an economic tier,
    // not proof that the matching metal material is already unlocked.
    e.shaped('kubejs:iron_coin', [
        'CCC',
        'CCC',
        'CCC'
    ], { C: 'kubejs:copper_coin' })
    e.shapeless('9x kubejs:copper_coin', ['kubejs:iron_coin'])
    e.shaped('kubejs:gold_coin', [
        'III',
        'III',
        'III'
    ], { I: 'kubejs:iron_coin' })
    e.shapeless('9x kubejs:iron_coin', ['kubejs:gold_coin'])
})
