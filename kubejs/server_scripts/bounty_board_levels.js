// A pristine Bountiful 6.0.4 board creates a blank decree and resolves it to a
// random loaded decree on its first ticks. Bounty Harvest has one decree per
// progression level, so random resolution can bypass progression or leave a board
// showing the wrong market. Seed newly crafted boards from the placer's highest
// GameStage before Bountiful performs its initial population.
//
// Boards broken and placed again carry their BoardBlockEntity NBT on the item.
// Preserve those boards exactly as-is; only genuinely plain/new board items are
// initialized here.

function bountyHarvestHighestLevel(player, server) {
    for (let level = 23; level >= 1; level--) {
        if (server.runCommandSilent(`gamestage check ${player.username} level_${level}`) > 0) {
            return level
        }
    }

    // Level 1 is granted on join, but defaulting here also makes a newly placed
    // board deterministic during first-login timing and in test worlds.
    return 1
}

BlockEvents.placed('bountiful:bountyboard', event => {
    const itemNbt = event.item && event.item.nbt

    // Bountiful serializes decree_inv/bounty_inv directly onto the dropped board
    // item. Do not replace an existing board's decrees, bounties, or reputation.
    if (itemNbt && (itemNbt.contains('decree_inv') || itemNbt.contains('bounty_inv'))) {
        return
    }

    const server = event.player.server
    const level = bountyHarvestHighestLevel(event.player, server)
    const pos = event.block

    // BoardBlockEntity.readNbt/writeNbt uses vanilla Inventories for decree_inv.
    // A decree is therefore an ordinary inventory item in one of three slots.
    // Use a single deterministic slot; Bountiful may still accept two more decrees
    // if the player deliberately adds them later.
    const boardNbt = `{decree_inv:{Items:[{Slot:0b,id:"bountiful:decree",Count:1b,tag:{"bountiful:decree_data":'{"ids":["level_${level}"]}',display:{Name:'{"text":"Level ${level} Decree"}'}}}]}}`
    const merged = server.runCommandSilent(`data merge block ${pos.x} ${pos.y} ${pos.z} ${boardNbt}`)

    if (merged <= 0) {
        console.error(`[Bounty Harvest] Failed to seed bounty board at ${pos.x},${pos.y},${pos.z} with level_${level}`)
    }
})
