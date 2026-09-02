// Generated Bountiful order pools for the 15-level farm economy.
// High-priority data intentionally overrides the legacy level_1..8 pack and
// extends the same decree IDs through level_15 without shipping another binary zip.
ServerEvents.highPriorityData(event => {
    // Reward caps are deliberately high enough for industrial objectives. unitWorth
    // still lets Bountiful match payout to order value; the larger cap avoids late
    // orders being artificially limited to a handful of coins.
    const rewardPools = {
        bh_copper_rews: { content: { copper_coin: { type: 'item', content: 'kubejs:copper_coin', amount: { min: 1, max: 64 }, unitWorth: 100 } } },
        bh_iron_rews: { content: { iron_coin: { type: 'item', content: 'kubejs:iron_coin', amount: { min: 1, max: 128 }, unitWorth: 900 } } },
        bh_gold_rews: { content: { gold_coin: { type: 'item', content: 'kubejs:gold_coin', amount: { min: 1, max: 256 }, unitWorth: 8100 } } }
    }

    Object.entries(rewardPools).forEach(([id, data]) => {
        event.addJson(`bountiful:bounty_pools/bountiful/${id}`, data)
    })

    // Demand stays human-scale before Create. Once industrial progression begins,
    // repeatable farm/food objectives grow geometrically: L10=4x, L11=8x,
    // L12=16x, L13=32x, L14=64x, L15=128x. Navigation tools, expedition keys,
    // and enabling machines are excluded from repeatable orders entirely: automation
    // pressure belongs on renewable output, not repeatedly rebuilding infrastructure.
    const bulkScale = {
        1: 1,
        2: 1,
        3: 1,
        4: 1,
        5: 1,
        6: 1,
        7: 1,
        8: 2,
        9: 3,
        10: 4,
        11: 8,
        12: 16,
        13: 32,
        14: 64,
        15: 128
    }
    const bulk = (level, min, max) => ({ min: min * bulkScale[level], max: max * bulkScale[level] })

    const levels = {
        1: { reward: 'bh_copper_rews', content: {
            wheat: { type: 'item', content: 'minecraft:wheat', amount: { min: 4, max: 24 }, unitWorth: 40 },
            bread: { type: 'item', content: 'minecraft:bread', amount: { min: 2, max: 12 }, unitWorth: 90 },
            apple: { type: 'item', content: 'minecraft:apple', amount: { min: 2, max: 10 }, unitWorth: 70 }
        } },
        2: { reward: 'bh_copper_rews', content: {
            eggs: { type: 'item', content: 'minecraft:egg', amount: { min: 2, max: 12 }, unitWorth: 80 },
            chicken: { type: 'item', content: 'minecraft:cooked_chicken', amount: { min: 2, max: 10 }, unitWorth: 130 },
            charcoal: { type: 'item', content: 'minecraft:charcoal', amount: { min: 4, max: 20 }, unitWorth: 55 },
            bread: { type: 'item', content: 'minecraft:bread', amount: { min: 2, max: 10 }, unitWorth: 90 }
        } },
        3: { reward: 'bh_copper_rews', content: {
            steak: { type: 'item', content: 'minecraft:cooked_beef', amount: { min: 2, max: 10 }, unitWorth: 170 },
            leather: { type: 'item', content: 'minecraft:leather', amount: { min: 2, max: 12 }, unitWorth: 145 },
            eggs: { type: 'item', content: 'minecraft:egg', amount: { min: 2, max: 12 }, unitWorth: 80 },
            bread: { type: 'item', content: 'minecraft:bread', amount: { min: 2, max: 10 }, unitWorth: 90 }
        } },
        4: { reward: 'bh_copper_rews', content: {
            carrots: { type: 'item', content: 'minecraft:carrot', amount: { min: 4, max: 24 }, unitWorth: 65 },
            pork: { type: 'item', content: 'minecraft:cooked_porkchop', amount: { min: 2, max: 12 }, unitWorth: 165 },
            dough: { type: 'item', content: 'farmersdelight:wheat_dough', amount: { min: 2, max: 12 }, unitWorth: 120 },
            bread: { type: 'item', content: 'minecraft:bread', amount: { min: 2, max: 12 }, unitWorth: 90 }
        } },
        5: { reward: 'bh_copper_rews', content: {
            cod: { type: 'item', content: 'minecraft:cod', amount: { min: 2, max: 12 }, unitWorth: 110 },
            salmon: { type: 'item', content: 'minecraft:salmon', amount: { min: 2, max: 10 }, unitWorth: 125 },
            fillet: { type: 'item', content: 'aquaculture:fish_fillet_raw', amount: { min: 2, max: 12 }, unitWorth: 140 },
            seagrass_salad: { type: 'item', content: 'oceansdelight:seagrass_salad', amount: { min: 1, max: 8 }, unitWorth: 180 },
            carrot: { type: 'item', content: 'minecraft:carrot', amount: { min: 4, max: 20 }, unitWorth: 65 }
        } },
        6: { reward: 'bh_copper_rews', content: {
            wool: { type: 'item', content: 'minecraft:white_wool', amount: { min: 2, max: 12 }, unitWorth: 125 },
            potato: { type: 'item', content: 'minecraft:baked_potato', amount: { min: 3, max: 16 }, unitWorth: 100 },
            yarn: { type: 'item', content: 'kubejs:wool_yarn', amount: { min: 2, max: 10 }, unitWorth: 185 },
            sugar: { type: 'item', content: 'minecraft:sugar', amount: { min: 4, max: 20 }, unitWorth: 70 },
            salmon: { type: 'item', content: 'minecraft:cooked_salmon', amount: { min: 2, max: 10 }, unitWorth: 150 }
        } },
        7: { reward: 'bh_iron_rews', content: {
            copper: { type: 'item', content: 'minecraft:copper_ingot', amount: { min: 2, max: 12 }, unitWorth: 220 },
            charcoal: { type: 'item', content: 'minecraft:charcoal', amount: { min: 4, max: 20 }, unitWorth: 55 },
            leather: { type: 'item', content: 'minecraft:leather', amount: { min: 2, max: 10 }, unitWorth: 145 },
            book: { type: 'item', content: 'minecraft:book', amount: { min: 1, max: 8 }, unitWorth: 220 },
            bookshelf: { type: 'item', content: 'minecraft:bookshelf', amount: { min: 1, max: 4 }, unitWorth: 650 },
            sweater: { type: 'item', content: 'kubejs:wool_sweater', amount: { min: 1, max: 2 }, unitWorth: 700 }
        } },
        8: { reward: 'bh_iron_rews', content: {
            sandwich: { type: 'item', content: 'farmersdelight:chicken_sandwich', amount: bulk(8, 1, 6), unitWorth: 420 },
            fish_stew: { type: 'item', content: 'farmersdelight:fish_stew', amount: bulk(8, 1, 5), unitWorth: 430 },
            cabbage: { type: 'item', content: 'farmersdelight:cabbage', amount: bulk(8, 3, 16), unitWorth: 115 },
            apple_pie: { type: 'item', content: 'farmersdelight:apple_pie', amount: bulk(8, 1, 4), unitWorth: 350 },
            beef_patty: { type: 'item', content: 'farmersdelight:beef_patty', amount: bulk(8, 2, 10), unitWorth: 220 },
            egg: { type: 'item', content: 'minecraft:egg', amount: bulk(8, 2, 12), unitWorth: 80 }
        } },
        9: { reward: 'bh_iron_rews', content: {
            corn: { type: 'item', content: 'corn_delight:corn', amount: bulk(9, 4, 24), unitWorth: 105 },
            tomato: { type: 'item', content: 'farmersdelight:tomato', amount: bulk(9, 3, 18), unitWorth: 115 },
            cornbread: { type: 'item', content: 'corn_delight:cornbread', amount: bulk(9, 2, 10), unitWorth: 280 },
            tortilla: { type: 'item', content: 'corn_delight:tortilla', amount: bulk(9, 2, 12), unitWorth: 180 },
            taco: { type: 'item', content: 'corn_delight:taco', amount: bulk(9, 1, 6), unitWorth: 460 },
            pork: { type: 'item', content: 'minecraft:cooked_porkchop', amount: bulk(9, 2, 10), unitWorth: 165 }
        } },
        10: { reward: 'bh_iron_rews', content: {
            iron: { type: 'item', content: 'minecraft:iron_ingot', amount: { min: 4, max: 24 }, unitWorth: 420 },
            alloy: { type: 'item', content: 'create:andesite_alloy', amount: { min: 4, max: 24 }, unitWorth: 380 },
            onion: { type: 'item', content: 'farmersdelight:onion', amount: bulk(10, 3, 16), unitWorth: 125 },
            charcoal: { type: 'item', content: 'minecraft:charcoal', amount: bulk(10, 4, 20), unitWorth: 55 },
            wheat: { type: 'item', content: 'minecraft:wheat', amount: bulk(10, 6, 28), unitWorth: 40 },
            breakfast: { type: 'item', content: 'farmersdelight:bacon_and_eggs', amount: bulk(10, 1, 5), unitWorth: 390 }
        } },
        11: { reward: 'bh_iron_rews', content: {
            pineapple: { type: 'item', content: 'pineapple_delight:pineapple', amount: bulk(11, 3, 18), unitWorth: 160 },
            rice: { type: 'item', content: 'farmersdelight:rice', amount: bulk(11, 3, 18), unitWorth: 130 },
            fried_rice: { type: 'item', content: 'pineapple_delight:pineapple_fried_rice', amount: bulk(11, 1, 6), unitWorth: 520 },
            pie: { type: 'item', content: 'pineapple_delight:pineapple_pie', amount: bulk(11, 1, 6), unitWorth: 480 },
            salmon_roll: { type: 'item', content: 'farmersdelight:salmon_roll', amount: bulk(11, 1, 6), unitWorth: 360 },
            taco: { type: 'item', content: 'corn_delight:taco', amount: bulk(11, 1, 5), unitWorth: 460 }
        } },
        12: { reward: 'bh_gold_rews', content: {
            wheat: { type: 'item', content: 'minecraft:wheat', amount: bulk(12, 8, 32), unitWorth: 40 },
            taco: { type: 'item', content: 'corn_delight:taco', amount: bulk(12, 1, 5), unitWorth: 460 },
            fried_rice: { type: 'item', content: 'pineapple_delight:pineapple_fried_rice', amount: bulk(12, 1, 5), unitWorth: 520 },
            salmon_roll: { type: 'item', content: 'farmersdelight:salmon_roll', amount: bulk(12, 1, 5), unitWorth: 360 }
        } },
        13: { reward: 'bh_gold_rews', content: {
            bison_burger: { type: 'item', content: 'alexsdelight:bison_burger', amount: bulk(13, 1, 4), unitWorth: 650 },
            blossom_soup: { type: 'item', content: 'alexsdelight:acacia_blossom_soup', amount: bulk(13, 1, 4), unitWorth: 580 },
            leather: { type: 'item', content: 'minecraft:leather', amount: bulk(13, 4, 16), unitWorth: 145 },
            cornbread: { type: 'item', content: 'corn_delight:cornbread', amount: bulk(13, 2, 8), unitWorth: 280 },
            pineapple_pie: { type: 'item', content: 'pineapple_delight:pineapple_pie', amount: bulk(13, 1, 5), unitWorth: 480 }
        } },
        14: { reward: 'bh_gold_rews', content: {
            diamond: { type: 'item', content: 'minecraft:diamond', amount: { min: 4, max: 24 }, unitWorth: 1100 },
            amethyst: { type: 'item', content: 'minecraft:amethyst_shard', amount: { min: 8, max: 48 }, unitWorth: 320 },
            sandwich: { type: 'item', content: 'farmersdelight:chicken_sandwich', amount: bulk(14, 1, 5), unitWorth: 420 },
            pineapple_pie: { type: 'item', content: 'pineapple_delight:pineapple_pie', amount: bulk(14, 1, 5), unitWorth: 480 },
            taco: { type: 'item', content: 'corn_delight:taco', amount: bulk(14, 1, 5), unitWorth: 460 }
        } },
        15: { reward: 'bh_gold_rews', content: {
            glowstew: { type: 'item', content: 'twilightdelight:glowstew', amount: { min: 16, max: 64 }, unitWorth: 720 },
            chorus_pie: { type: 'item', content: 'ends_delight:chorus_fruit_pie', amount: bulk(15, 1, 4), unitWorth: 780 },
            taco: { type: 'item', content: 'corn_delight:taco', amount: bulk(15, 1, 5), unitWorth: 460 },
            pineapple_pie: { type: 'item', content: 'pineapple_delight:pineapple_pie', amount: bulk(15, 1, 5), unitWorth: 480 },
            sandwich: { type: 'item', content: 'farmersdelight:chicken_sandwich', amount: bulk(15, 1, 5), unitWorth: 420 },
            cornbread: { type: 'item', content: 'corn_delight:cornbread', amount: bulk(15, 2, 8), unitWorth: 280 }
        } }
    }

    Object.entries(levels).forEach(([level, data]) => {
        const pool = `level_${level}_objs`
        event.addJson(`bountiful:bounty_pools/bountiful/${pool}`, { content: data.content })
        event.addJson(`bountiful:bounty_decrees/bountiful/level_${level}`, {
            linkedProfessions: ['farmer'],
            objectives: [pool],
            rewards: [data.reward]
        })
    })
})
