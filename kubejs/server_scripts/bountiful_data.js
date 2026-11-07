// Bountiful order pools for the 23-level farm economy.
// High-priority data replaces the built-in/legacy level pools with one decree per
// progression level. Levels before Create stay deliberately hand-manageable; once
// mechanical farming is unlocked, renewable demand grows geometrically.
ServerEvents.highPriorityData(event => {
    const rewardPools = {
        bh_copper_rews: { content: { copper_coin: { type: 'item', content: 'kubejs:copper_coin', amount: { min: 1, max: 64 }, unitWorth: 100 } } },
        bh_iron_rews: { content: { iron_coin: { type: 'item', content: 'kubejs:iron_coin', amount: { min: 1, max: 192 }, unitWorth: 900 } } },
        bh_gold_rews: { content: { gold_coin: { type: 'item', content: 'kubejs:gold_coin', amount: { min: 1, max: 512 }, unitWorth: 8100 } } }
    }

    Object.keys(rewardPools).forEach(id => {
        event.addJson(`bountiful:bounty_pools/bountiful/${id}`, rewardPools[id])
    })

    // L15 is the first Create automation tier. From there every level doubles the
    // renewable throughput multiplier. Rare ores, navigation items, machines and
    // expedition keys use fixed quantities or are excluded entirely; the pressure
    // belongs on repeatable production rather than rebuilding infrastructure.
    const bulkScale = {
        1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1,
        9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1,
        15: 4,
        16: 8,
        17: 16,
        18: 32,
        19: 64,
        20: 128,
        21: 256,
        22: 512,
        23: 1024
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
            wool: { type: 'item', content: 'minecraft:white_wool', amount: { min: 4, max: 20 }, unitWorth: 125 },
            yarn: { type: 'item', content: 'kubejs:wool_yarn', amount: { min: 2, max: 12 }, unitWorth: 185 },
            sweater: { type: 'item', content: 'kubejs:wool_sweater', amount: { min: 1, max: 3 }, unitWorth: 700 },
            leather: { type: 'item', content: 'minecraft:leather', amount: { min: 2, max: 12 }, unitWorth: 145 }
        } },
        7: { reward: 'bh_copper_rews', content: {
            potato: { type: 'item', content: 'minecraft:potato', amount: { min: 8, max: 32 }, unitWorth: 70 },
            baked_potato: { type: 'item', content: 'minecraft:baked_potato', amount: { min: 4, max: 20 }, unitWorth: 100 },
            pork: { type: 'item', content: 'minecraft:cooked_porkchop', amount: { min: 2, max: 12 }, unitWorth: 165 },
            wool: { type: 'item', content: 'minecraft:white_wool', amount: { min: 4, max: 20 }, unitWorth: 125 }
        } },
        8: { reward: 'bh_copper_rews', content: {
            sugar: { type: 'item', content: 'minecraft:sugar', amount: { min: 8, max: 32 }, unitWorth: 70 },
            apple_pie: { type: 'item', content: 'farmersdelight:apple_pie', amount: { min: 1, max: 6 }, unitWorth: 350 },
            dough: { type: 'item', content: 'farmersdelight:wheat_dough', amount: { min: 4, max: 20 }, unitWorth: 120 },
            eggs: { type: 'item', content: 'minecraft:egg', amount: { min: 4, max: 20 }, unitWorth: 80 }
        } },
        9: { reward: 'bh_iron_rews', content: {
            copper: { type: 'item', content: 'minecraft:copper_ingot', amount: { min: 4, max: 24 }, unitWorth: 220 },
            charcoal: { type: 'item', content: 'minecraft:charcoal', amount: { min: 8, max: 32 }, unitWorth: 55 },
            bookshelf: { type: 'item', content: 'minecraft:bookshelf', amount: { min: 1, max: 6 }, unitWorth: 650 },
            sweater: { type: 'item', content: 'kubejs:wool_sweater', amount: { min: 1, max: 3 }, unitWorth: 700 }
        } },
        10: { reward: 'bh_iron_rews', content: {
            cabbage: { type: 'item', content: 'farmersdelight:cabbage', amount: { min: 8, max: 32 }, unitWorth: 115 },
            sandwich: { type: 'item', content: 'farmersdelight:chicken_sandwich', amount: { min: 2, max: 10 }, unitWorth: 420 },
            fish_stew: { type: 'item', content: 'farmersdelight:fish_stew', amount: { min: 2, max: 8 }, unitWorth: 430 },
            beef_patty: { type: 'item', content: 'farmersdelight:beef_patty', amount: { min: 4, max: 16 }, unitWorth: 220 },
            baked_potato: { type: 'item', content: 'minecraft:baked_potato', amount: { min: 6, max: 24 }, unitWorth: 100 }
        } },
        11: { reward: 'bh_iron_rews', content: {
            corn: { type: 'item', content: 'corn_delight:corn', amount: { min: 8, max: 32 }, unitWorth: 105 },
            cornbread: { type: 'item', content: 'corn_delight:cornbread', amount: { min: 3, max: 12 }, unitWorth: 280 },
            tortilla: { type: 'item', content: 'corn_delight:tortilla', amount: { min: 4, max: 16 }, unitWorth: 180 },
            pork: { type: 'item', content: 'minecraft:cooked_porkchop', amount: { min: 4, max: 16 }, unitWorth: 165 }
        } },
        12: { reward: 'bh_iron_rews', content: {
            tomato: { type: 'item', content: 'farmersdelight:tomato', amount: { min: 8, max: 32 }, unitWorth: 115 },
            taco: { type: 'item', content: 'corn_delight:taco', amount: { min: 2, max: 10 }, unitWorth: 460 },
            tortilla: { type: 'item', content: 'corn_delight:tortilla', amount: { min: 4, max: 20 }, unitWorth: 180 },
            cabbage: { type: 'item', content: 'farmersdelight:cabbage', amount: { min: 8, max: 32 }, unitWorth: 115 }
        } },
        13: { reward: 'bh_iron_rews', content: {
            iron: { type: 'item', content: 'minecraft:iron_ingot', amount: { min: 4, max: 24 }, unitWorth: 420 },
            taco: { type: 'item', content: 'corn_delight:taco', amount: { min: 4, max: 16 }, unitWorth: 460 },
            copper: { type: 'item', content: 'minecraft:copper_ingot', amount: { min: 8, max: 32 }, unitWorth: 220 },
            wheat: { type: 'item', content: 'minecraft:wheat', amount: { min: 16, max: 64 }, unitWorth: 40 }
        } },
        14: { reward: 'bh_iron_rews', content: {
            onion: { type: 'item', content: 'farmersdelight:onion', amount: { min: 8, max: 32 }, unitWorth: 125 },
            breakfast: { type: 'item', content: 'farmersdelight:bacon_and_eggs', amount: { min: 2, max: 10 }, unitWorth: 390 },
            sandwich: { type: 'item', content: 'farmersdelight:chicken_sandwich', amount: { min: 4, max: 16 }, unitWorth: 420 },
            taco: { type: 'item', content: 'corn_delight:taco', amount: { min: 4, max: 16 }, unitWorth: 460 }
        } },
        15: { reward: 'bh_iron_rews', content: {
            wheat: { type: 'item', content: 'minecraft:wheat', amount: bulk(15, 16, 64), unitWorth: 40 },
            corn: { type: 'item', content: 'corn_delight:corn', amount: bulk(15, 8, 32), unitWorth: 105 },
            cabbage: { type: 'item', content: 'farmersdelight:cabbage', amount: bulk(15, 8, 32), unitWorth: 115 },
            taco: { type: 'item', content: 'corn_delight:taco', amount: bulk(15, 2, 8), unitWorth: 460 },
            sandwich: { type: 'item', content: 'farmersdelight:chicken_sandwich', amount: bulk(15, 2, 8), unitWorth: 420 }
        } },
        16: { reward: 'bh_iron_rews', content: {
            pineapple: { type: 'item', content: 'pineapple_delight:pineapple', amount: bulk(16, 4, 16), unitWorth: 160 },
            pineapple_pie: { type: 'item', content: 'pineapple_delight:pineapple_pie', amount: bulk(16, 1, 4), unitWorth: 480 },
            apple_pie: { type: 'item', content: 'farmersdelight:apple_pie', amount: bulk(16, 2, 8), unitWorth: 350 },
            wheat: { type: 'item', content: 'minecraft:wheat', amount: bulk(16, 8, 32), unitWorth: 40 }
        } },
        17: { reward: 'bh_iron_rews', content: {
            rice: { type: 'item', content: 'farmersdelight:rice', amount: bulk(17, 4, 16), unitWorth: 130 },
            salmon_roll: { type: 'item', content: 'farmersdelight:salmon_roll', amount: bulk(17, 1, 4), unitWorth: 360 },
            fried_rice: { type: 'item', content: 'pineapple_delight:pineapple_fried_rice', amount: bulk(17, 1, 4), unitWorth: 520 },
            pineapple_pie: { type: 'item', content: 'pineapple_delight:pineapple_pie', amount: bulk(17, 1, 4), unitWorth: 480 },
            taco: { type: 'item', content: 'corn_delight:taco', amount: bulk(17, 2, 8), unitWorth: 460 }
        } },
        18: { reward: 'bh_gold_rews', content: {
            wheat: { type: 'item', content: 'minecraft:wheat', amount: bulk(18, 16, 64), unitWorth: 40 },
            taco: { type: 'item', content: 'corn_delight:taco', amount: bulk(18, 1, 4), unitWorth: 460 },
            fried_rice: { type: 'item', content: 'pineapple_delight:pineapple_fried_rice', amount: bulk(18, 1, 4), unitWorth: 520 },
            salmon_roll: { type: 'item', content: 'farmersdelight:salmon_roll', amount: bulk(18, 1, 4), unitWorth: 360 },
            gold: { type: 'item', content: 'minecraft:gold_ingot', amount: { min: 4, max: 20 }, unitWorth: 650 }
        } },
        19: { reward: 'bh_gold_rews', content: {
            wheat: { type: 'item', content: 'minecraft:wheat', amount: bulk(19, 16, 64), unitWorth: 40 },
            taco: { type: 'item', content: 'corn_delight:taco', amount: bulk(19, 1, 4), unitWorth: 460 },
            fried_rice: { type: 'item', content: 'pineapple_delight:pineapple_fried_rice', amount: bulk(19, 1, 4), unitWorth: 520 },
            leather: { type: 'item', content: 'minecraft:leather', amount: bulk(19, 2, 8), unitWorth: 145 },
            cornbread: { type: 'item', content: 'corn_delight:cornbread', amount: bulk(19, 1, 4), unitWorth: 280 }
        } },
        20: { reward: 'bh_gold_rews', content: {
            bison_burger: { type: 'item', content: 'alexsdelight:bison_burger', amount: bulk(20, 1, 4), unitWorth: 650 },
            blossom_soup: { type: 'item', content: 'alexsdelight:acacia_blossom_soup', amount: bulk(20, 1, 3), unitWorth: 580 },
            leather: { type: 'item', content: 'minecraft:leather', amount: bulk(20, 4, 16), unitWorth: 145 },
            cornbread: { type: 'item', content: 'corn_delight:cornbread', amount: bulk(20, 2, 8), unitWorth: 280 },
            pineapple_pie: { type: 'item', content: 'pineapple_delight:pineapple_pie', amount: bulk(20, 1, 4), unitWorth: 480 }
        } },
        21: { reward: 'bh_gold_rews', content: {
            diamond: { type: 'item', content: 'minecraft:diamond', amount: { min: 4, max: 16 }, unitWorth: 1100 },
            amethyst: { type: 'item', content: 'minecraft:amethyst_shard', amount: { min: 8, max: 32 }, unitWorth: 320 },
            sandwich: { type: 'item', content: 'farmersdelight:chicken_sandwich', amount: bulk(21, 1, 4), unitWorth: 420 },
            pineapple_pie: { type: 'item', content: 'pineapple_delight:pineapple_pie', amount: bulk(21, 1, 4), unitWorth: 480 },
            taco: { type: 'item', content: 'corn_delight:taco', amount: bulk(21, 1, 4), unitWorth: 460 },
            cornbread: { type: 'item', content: 'corn_delight:cornbread', amount: bulk(21, 2, 8), unitWorth: 280 }
        } },
        22: { reward: 'bh_gold_rews', content: {
            glowstew: { type: 'item', content: 'twilightdelight:glowstew', amount: { min: 8, max: 32 }, unitWorth: 720 },
            taco: { type: 'item', content: 'corn_delight:taco', amount: bulk(22, 1, 4), unitWorth: 460 },
            pineapple_pie: { type: 'item', content: 'pineapple_delight:pineapple_pie', amount: bulk(22, 1, 4), unitWorth: 480 },
            sandwich: { type: 'item', content: 'farmersdelight:chicken_sandwich', amount: bulk(22, 1, 4), unitWorth: 420 },
            cornbread: { type: 'item', content: 'corn_delight:cornbread', amount: bulk(22, 2, 8), unitWorth: 280 }
        } },
        23: { reward: 'bh_gold_rews', content: {
            chorus_pie: { type: 'item', content: 'ends_delight:chorus_fruit_pie', amount: bulk(23, 1, 4), unitWorth: 780 },
            taco: { type: 'item', content: 'corn_delight:taco', amount: bulk(23, 1, 4), unitWorth: 460 },
            pineapple_pie: { type: 'item', content: 'pineapple_delight:pineapple_pie', amount: bulk(23, 1, 4), unitWorth: 480 },
            sandwich: { type: 'item', content: 'farmersdelight:chicken_sandwich', amount: bulk(23, 1, 4), unitWorth: 420 },
            cornbread: { type: 'item', content: 'corn_delight:cornbread', amount: bulk(23, 2, 8), unitWorth: 280 },
            wheat: { type: 'item', content: 'minecraft:wheat', amount: bulk(23, 8, 32), unitWorth: 40 }
        } }
    }

    Object.keys(levels).forEach(level => {
        const data = levels[level]
        const pool = `level_${level}_objs`
        event.addJson(`bountiful:bounty_pools/bountiful/${pool}`, { content: data.content })
        event.addJson(`bountiful:bounty_decrees/bountiful/level_${level}`, {
            linkedProfessions: ['farmer'],
            objectives: [pool],
            rewards: [data.reward]
        })
    })
})
