// Runtime compatibility repairs for bundled mods with broken data.
ServerEvents.highPriorityData(event => {
    // Alex's Delight 1.20.1 ships this recipe with the nonexistent
    // amfd:singular_cooked_moose_rib ingredient. Override it with the actual
    // cooked moose-rib item registered by Alex's Delight.
    event.addJson('alexsdelight:recipes/barbecue_on_a_stick', {
        group: 'barbecue_stick',
        type: 'minecraft:crafting_shapeless',
        ingredients: [
            { item: 'farmersdelight:tomato' },
            { item: 'farmersdelight:onion' },
            { item: 'alexsdelight:cooked_loose_moose_rib' },
            { item: 'minecraft:cooked_chicken' },
            { item: 'minecraft:stick' },
            { item: 'minecraft:stick' }
        ],
        result: {
            item: 'farmersdelight:barbecue_stick',
            count: 2
        }
    })
})
