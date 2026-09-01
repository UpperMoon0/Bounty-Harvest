ItemEvents.tooltip((e) => {
    // Coins
    e.add('kubejs:copper_coin', ['Value: 1'])
    e.add('kubejs:iron_coin', ['Value: 9'])
    e.add('kubejs:gold_coin', ['Value: 81'])

    e.add('minecraft:torch', ['Crafting becomes practical at Level 2 with charcoal.'])

    const ironworking = [
        'minecraft:raw_iron', 'minecraft:iron_nugget', 'minecraft:iron_ingot',
        'minecraft:iron_block', 'minecraft:iron_axe', 'minecraft:iron_hoe',
        'minecraft:iron_pickaxe', 'minecraft:iron_shovel', 'minecraft:iron_sword',
        'minecraft:iron_helmet', 'minecraft:iron_chestplate',
        'minecraft:iron_leggings', 'minecraft:iron_boots', 'minecraft:shield'
    ]
    ironworking.forEach(item => e.add(item, ['Requires Level 7 — Ironworking']))
});
