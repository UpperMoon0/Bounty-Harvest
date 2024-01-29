// priority: 0

// Visit the wiki for more info - https://kubejs.com/

console.info('Hello, World! (Loaded startup scripts)')

StartupEvents.registry('item', e => {
    e.create('kubejs:copper_coin').displayName('Copper Coin')
    e.create('kubejs:iron_coin').displayName('Iron Coin')
    e.create('kubejs:gold_coin').displayName('Gold Coin')
    e.create('kubejs:wool_yarn').displayName('Wool Yarn')
    e.create('kubejs:wool_sweater').displayName('Wool Sweater')
})