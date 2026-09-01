# Bounty Harvest

CurseForge page: https://legacy.curseforge.com/minecraft/modpacks/bounty-harvest

Minecraft 1.20.1 · Forge 47.4.23 · Java 17 · Beta

![Bounty Harvest](https://i.imgur.com/qIHoZxx.png?1)

Embark on an exciting journey with Bounty Harvest - a progression-based farming modpack! As you cultivate your farm, delve into the mines, forage for resources, and explore the vast landscapes, you’ll find yourself leveling up and unlocking new possibilities.

Featuring over 155 quests that systematically guide you through various stages of the game.

The Bountiful mods allow you to monetize your efforts by selling your products for coins. These coins serve as a currency to level up and unlock a plethora of new elements including crops, animals, products, and items.

The game is set against the backdrop of a breathtaking and diverse wilderness landscape. Most of the content will eventually be integrated into the modpack progression, providing a cohesive gaming experience.

There are currently 8 playable levels, with more planned for the future.

Please note that as the modpack is in its early alpha stage, you may encounter several bugs and unintentionally ungated items. I appreciate your understanding and patience as we work towards refining Bounty Harvest. Your feedback during this phase is invaluable to us. Enjoy your journey!

![Quests](https://i.imgur.com/Gscc4gd.png)
![Bounties](https://i.imgur.com/ggEx4YP.png)
![Farm](https://i.imgur.com/jcWJjKg.png)
![Wilderness](https://i.imgur.com/hYRrwNi.png)

## Reproducible releases

`pack/pack.json` is the source of truth for the pack version, Minecraft/Forge versions, Java requirement, release channel, and client/server exclusions. `minecraftinstance.json` stores sanitized CurseForge project/file metadata from the tested launcher profile.

The local CurseForge Dev profile can use `tools/link_curseforge_instance.ps1` from an elevated PowerShell window to link its metadata to this repository. After changing mods in CurseForge, run `./tools/sanitize_minecraftinstance.ps1` before validating or committing so launcher paths and local state are not published.

Build both release archives from PowerShell:

```powershell
./tools/build_modpack.ps1
python tools/verify_archives.py
```

Outputs:

- `dist/Bounty-Harvest-<version>.zip` — CurseForge client manifest with runtime overrides
- `dist/Bounty-Harvest-<version>-server.zip` — dedicated server, Forge installer, and launchers

Pull requests validate the quest graph, critical progression gates, pack invariants, archive client/server split, and dedicated-server boot. A version change merged into `main` creates the GitHub release after a successful build; CurseForge preflight/publishing runs independently and requires the `CURSEFORGE_API_TOKEN` repository secret. `CURSEFORGE_CORE_API_KEY` is optional and is used only for idempotent duplicate-file lookup through the separate CurseForge Core API.
