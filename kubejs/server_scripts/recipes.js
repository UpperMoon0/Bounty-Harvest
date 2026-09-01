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
    // Keep the vanilla fishing-rod recipe. The previous iron-nugget replacement
    // made the fisheries tier impossible before Level 7 Ironworking.

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

    // Level 7 · Copper Workshop / Ironworking
    e.remove({id: 'minecraft:iron_ingot_from_smelting_iron_ore'})
    e.remove({id: 'minecraft:iron_ingot_from_smelting_deepslate_iron_ore'})
    e.remove({id: 'minecraft:iron_ingot_from_smelting_raw_iron'})
    e.remove({id: 'create:smelting/iron_ingot_from_crushed'})
    e.smelting('3x minecraft:iron_nugget', 'minecraft:raw_iron').xp(0.7)

    e.remove({id: 'minecraft:copper_ingot_from_smelting_copper_ore'})
    e.remove({id: 'minecraft:copper_ingot_from_smelting_deepslate_copper_ore'})
    e.remove({id: 'minecraft:copper_ingot_from_smelting_raw_copper'})
    e.smelting('3x bettercopper:copper_nugget', 'minecraft:raw_copper').xp(0.7)

    e.remove({id: 'farmersdelight:stuffed_potato'})
    e.shaped('farmersdelight:stuffed_potato', [
        'AB',
        'C '
    ], {
        A: 'minecraft:baked_potato',
        B: 'minecraft:cooked_beef',
        C: 'minecraft:milk_bucket'
    })

    e.remove({id: 'farmersdelight:pie_crust'})
    e.shaped('farmersdelight:pie_crust', [
        'WMW',
        ' W '
    ], {
        W: 'minecraft:wheat',
        M: 'minecraft:milk_bucket'
    })

    e.remove({id: 'minecraft:glass_bottle'})
    e.shaped('3x minecraft:glass_bottle', [
        ' C ',
        'G G',
        ' G '
    ], {
        C: 'bettercopper:copper_nugget',
        G: '#forge:glass'
    })

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

    e.remove({id: 'minecraft:composter'})
    e.shaped('minecraft:composter', [
        'A A',
        'A A',
        'ABA'
    ], {
        A: '#minecraft:wooden_slabs',
        B: 'minecraft:copper_ingot'
    })

    // Level 8 · Iron Kitchen
    e.remove({id: 'bettercopper:copper_helmet'})
    e.remove({id: 'bettercopper:copper_chestplate'})
    e.remove({id: 'bettercopper:copper_leggings'})
    e.remove({id: 'bettercopper:copper_boots'})

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

    e.shaped('farmersdelight:stuffed_potato', [
        'AB',
        'C '
    ], {
        A: 'minecraft:baked_potato',
        B: 'farmersdelight:beef_patty',
        C: 'farmersdelight:milk_bottle'
    })

    e.remove({id: 'farmersdelight:cutting/cooked_chicken'})
    e.remove({id: 'farmersdelight:cabbage_from_leaves'})

    e.remove({id: 'farmersdelight:chicken_sandwich'})
    e.shaped('farmersdelight:chicken_sandwich', [
        'AB',
        'CD'
    ], {
        A: 'minecraft:bread',
        B: 'farmersdelight:cooked_chicken_cuts',
        C: 'farmersdelight:cabbage_leaf',
        D: 'minecraft:carrot'
    })
    e.shaped('farmersdelight:chicken_sandwich', [
        'AB',
        'CD'
    ], {
        A: 'minecraft:bread',
        B: 'farmersdelight:cooked_chicken_cuts',
        C: 'delightful:chopped_clover',
        D: 'minecraft:carrot'
    })

    // Currency exchange remains lossless. Bounties introduce copper at Levels
    // 1-6, iron at Levels 7-11, and gold at Levels 12-15.
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
