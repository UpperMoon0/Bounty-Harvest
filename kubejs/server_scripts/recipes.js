ServerEvents.recipes((e) => {
    // Level 1  
    e.remove({id: 'bountiful:crafting/bountyboard'})
    e.shaped('bountiful:bountyboard', [
        'WWW',
        'WCW',
        'WWW'
    ], {
        W: '#minecraft:planks',
        C: 'minecraft:wheat_seeds'
    })

    // Level 2
    e.remove({output: 'minecraft:torch'})
    e.shaped('2x minecraft:torch', [
        'C',
        'S'
    ], {
        C: 'minecraft:charcoal',
        S: 'minecraft:stick'
    })

    // Level 3
    e.remove({output: '#minecraft:boats'})

    let boat_recipe = (wood_type) => {
        if (Item.exists(wood_type.concat('_boat'))) {
            e.shaped(wood_type.concat('_boat'), [
                ' S ',
                'WSW',
                'WWW'
            ], {
                S: 'minecraft:wooden_shovel',
                W: wood_type.concat('_planks')
            });
        }
    
        if (Item.exists(wood_type.concat('_chest_boat'))) {
            e.shaped(wood_type.concat('_chest_boat'), [
                'CB'
            ], {
                C: '#forge:chests/wooden',
                B: wood_type.concat('_boat')
            });
        }
    }    

    Ingredient.of('#minecraft:planks').stacks.forEach(item => {
        boat_recipe(item.id.replace('_planks', ''))
    })

    e.remove({id: 'minecraft:bone_meal'})
    e.shapeless('2x minecraft:bone_meal', ['minecraft:bone'])

    // Level 4
    e.remove({id: 'create:smelting/bread'})
    e.remove({output: 'farmersdelight:wheat_dough'})
    e.shaped('2x farmersdelight:wheat_dough', [
        'WW',
        'WE'
    ], {
        W: 'minecraft:wheat',
        E: 'minecraft:egg'
    })

    e.remove({id: 'minecraft:stone_pickaxe'})
    e.shaped('minecraft:stone_pickaxe', [
        'AAA',
        ' B ',
        ' B '
    ], {
        A: 'minecraft:flint',
        B: 'minecraft:stick'
    })

    e.remove({id: 'minecraft:stone_axe'})
    e.shaped('minecraft:stone_axe', [
        'AA',
        'AB',
        ' B'
    ], {
        A: 'minecraft:flint',
        B: 'minecraft:stick'
    })

    e.remove({id: 'minecraft:stone_shovel'})
    e.shaped('minecraft:stone_shovel', [
        'A',
        'B',
        'B'
    ], {
        A: 'minecraft:flint',
        B: 'minecraft:stick'
    })

    e.remove({id: 'minecraft:stone_hoe'})
    e.shaped('minecraft:stone_hoe', [
        'AA',
        ' B',
        ' B'
    ], {
        A: 'minecraft:flint',
        B: 'minecraft:stick'
    })

    e.remove({id: 'minecraft:stone_sword'})
    e.shaped('minecraft:stone_sword', [
        'A',
        'A',
        'B'
    ], {
        A: 'minecraft:flint',
        B: 'minecraft:stick'
    })

    // Level 5
    e.remove({id: 'minecraft:white_wool_from_string'})

    // Level 6
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

    // Level 7
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

    e.remove({id: 'create:smelting/bread'})
    e.remove({output: 'farmersdelight:wheat_dough'})
    e.shaped('3x farmersdelight:wheat_dough', [
        'WWA',
        'WE '
    ], {
        W: 'minecraft:wheat',
        E: 'minecraft:egg',
        A: 'minecraft:water_bucket'
    })

    e.remove({id: 'minecraft:fishing_rod'})
    e.shaped('minecraft:fishing_rod', [
        '  A',
        ' AB',
        'ACB'
    ], {
        A: 'minecraft:stick',
        B: 'minecraft:string',
        C: 'minecraft:iron_nugget'
    })

    // Level 8
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
    e.shaped('minecraft:chainmail_helmet', [
        'III',
        'I I'
    ], {
        I: 'minecraft:chain'
    })
    e.shaped('minecraft:chainmail_chestplate', [
        'I I',
        'III',
        'III'
    ], {
        I: 'minecraft:chain'
    })
    e.shaped('minecraft:chainmail_leggings', [
        'III',
        'I I',
        'I I'
    ], {
        I: 'minecraft:chain'
    })
    e.shaped('minecraft:chainmail_boots', [
        'I I',
        'I I'
    ], {
        I: 'minecraft:chain'
    })

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
})
