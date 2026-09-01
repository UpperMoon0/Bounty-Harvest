from __future__ import annotations

import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTS = ROOT / "config" / "ftbquests" / "quests" / "chapters"
DEFAULT_STAGES = ROOT / "scripts" / "default_stages.zs"
BOUNTIFUL_DATA = ROOT / "kubejs" / "server_scripts" / "bountiful_data.js"


def compounds(text: str):
    stack: list[int] = []
    quoted = False
    escaped = False
    for index, char in enumerate(text):
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            continue
        if char == '"':
            quoted = True
        elif char == "{":
            stack.append(index)
        elif char == "}" and stack:
            start = stack.pop()
            yield text[start : index + 1]


def main() -> int:
    errors: list[str] = []
    pack = json.loads((ROOT / "pack" / "pack.json").read_text(encoding="utf-8"))
    instance_text = (ROOT / "minecraftinstance.json").read_text(encoding="utf-8")
    instance = json.loads(instance_text)
    expected_instance_keys = {"name", "gameVersion", "baseModLoader", "installedAddons"}
    if set(instance) != expected_instance_keys:
        errors.append("minecraftinstance.json contains launcher-local fields; run sanitize_minecraftinstance.ps1")
    if "C:\\\\Users\\\\" in instance_text:
        errors.append("minecraftinstance.json contains a personal Windows path")

    if not re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?", pack["version"]):
        errors.append("pack.version is not semantic versioning")
    if pack["minecraftVersion"] != instance["gameVersion"]:
        errors.append("Minecraft version differs between pack and instance metadata")
    if pack["forgeVersion"] != instance["baseModLoader"]["forgeVersion"]:
        errors.append("Forge version differs between pack and instance metadata")
    if not (ROOT / "changelog" / f"{pack['version']}.md").is_file():
        errors.append(f"missing changelog/{pack['version']}.md")

    required_runtime = [
        ROOT / "scripts" / "gen_item_stages.zs",
        DEFAULT_STAGES,
        ROOT / "resourcepacks" / "gen_bh_bounties.zip",
        BOUNTIFUL_DATA,
        QUESTS / "research.snbt",
        QUESTS / "decree.snbt",
    ]
    for level in range(1, 16):
        required_runtime.append(QUESTS / f"level_{level}.snbt")
    for path in required_runtime:
        if not path.is_file():
            errors.append(f"missing runtime file {path.relative_to(ROOT)}")

    archives = [path for path in QUESTS.iterdir() if path.is_file() and path.suffix != ".snbt"]
    if archives:
        errors.append("non-SNBT files in quest chapters: " + ", ".join(path.name for path in archives))

    # The old binary pack remains as a compatibility fallback, but KubeJS high-priority
    # data is now the readable source of truth for all 15 decree/order pools.
    with zipfile.ZipFile(ROOT / "resourcepacks" / "gen_bh_bounties.zip") as archive:
        names = archive.namelist()
        if not any(name.startswith("data/bountiful/bounty_decrees/") for name in names):
            errors.append("legacy Bountiful data pack has no bounty decrees")
        if not any(name.startswith("data/bountiful/bounty_pools/") for name in names):
            errors.append("legacy Bountiful data pack has no bounty pools")

    bounty_data = BOUNTIFUL_DATA.read_text(encoding="utf-8") if BOUNTIFUL_DATA.is_file() else ""
    if "ServerEvents.highPriorityData" not in bounty_data:
        errors.append("Bountiful level data is not registered as high-priority server data")
    if "bountiful:bounty_decrees/bountiful/level_${level}" not in bounty_data:
        errors.append("Bountiful generator does not register level decree resources")
    if "bountiful:bounty_pools/bountiful/${pool}" not in bounty_data:
        errors.append("Bountiful generator does not register level objective pools")
    defined_levels = {int(value) for value in re.findall(r"^\s*(\d+): \{ reward:", bounty_data, re.MULTILINE)}
    if defined_levels != set(range(1, 16)):
        errors.append(f"Bountiful generator defines levels {sorted(defined_levels)}; expected 1-15")
    for reward_pool in ("bh_copper_rews", "bh_iron_rews", "bh_gold_rews"):
        if reward_pool not in bounty_data:
            errors.append(f"missing Bountiful reward pool {reward_pool}")
    for legacy_good in ("minecraft:wheat", "minecraft:egg", "minecraft:leather", "minecraft:carrot"):
        if bounty_data.count(legacy_good) < 2:
            errors.append(f"Hay Day reuse invariant: {legacy_good} does not recur across bounty tiers")

    all_quests = "\n".join(path.read_text(encoding="utf-8") for path in QUESTS.glob("*.snbt"))
    if "gamestage add" in all_quests:
        errors.append("manual gamestage command reward remains")

    level_1 = (QUESTS / "level_1.snbt").read_text(encoding="utf-8")
    if re.search(r'stage:\s*"level_1"[\s\S]{0,60}type:\s*"stage"', level_1):
        errors.append("Level 1 must not expose a stage reward; it is the default player stage")

    default_stages = DEFAULT_STAGES.read_text(encoding="utf-8") if DEFAULT_STAGES.is_file() else ""
    if "import mods.gamestages.StageHelper;" not in default_stages:
        errors.append("default_stages.zs does not import GameStages StageHelper")
    if 'StageHelper.grantStageOnJoin("level_1");' not in default_stages:
        errors.append("Level 1 is not granted automatically on player join")

    for level in range(1, 16):
        text = (QUESTS / f"level_{level}.snbt").read_text(encoding="utf-8")
        if level >= 2:
            expected = rf'autoclaim:\s*1b[\s\S]{{0,100}}stage:\s*"level_{level}"[\s\S]{{0,60}}type:\s*"stage"'
            if not re.search(expected, text):
                errors.append(f"Level {level} lacks an auto-claimed stage reward")
        if "Market Order" not in text:
            errors.append(f"Level {level} has no market-order milestone")
        for block in compounds(text):
            if block.count('type: "item"') != 1:
                continue
            outer = re.search(r"\bcount:\s*(\d+)L?", block)
            embedded = re.search(r"\bCount:\s*(\d+)", block)
            if outer and embedded and outer.group(1) != embedded.group(1):
                errors.append(
                    f"Level {level} has mismatched task counts {outer.group(1)} and {embedded.group(1)}"
                )
                break

    decree = (QUESTS / "decree.snbt").read_text(encoding="utf-8")
    for level in range(1, 16):
        if f'Level {level} Decree' not in decree or f'level_{level}' not in decree:
            errors.append(f"decree market does not expose Level {level}")

    level_7 = (QUESTS / "level_7.snbt").read_text(encoding="utf-8")
    if 'stage: "iron_age"' not in level_7 or 'dependencies: ["34B5DF088E2F447E"]' not in level_7:
        errors.append("copper tools do not unlock the Ironworking quest path")

    recipes = (ROOT / "kubejs" / "server_scripts" / "recipes.js").read_text(encoding="utf-8")
    if recipes.count("remove({output: 'farmersdelight:wheat_dough'})") != 1:
        errors.append("wheat dough must have exactly one global recipe removal")
    if "minecraft:water_bucket" in re.search(
        r"wheat_dough[\s\S]{0,500}", recipes
    ).group(0):
        errors.append("wheat dough still appears to require a water bucket")
    if "remove({id: 'minecraft:fishing_rod'})" in recipes:
        errors.append("fishing rod is still artificially locked behind a replacement recipe")
    tags = (ROOT / "kubejs" / "server_scripts" / "tags.js").read_text(encoding="utf-8")
    if "minecraft:tulip" in tags:
        errors.append("invalid minecraft:tulip ID remains")

    stages = (ROOT / "scripts" / "gen_item_stages.zs").read_text(encoding="utf-8")
    for stage in [*(f"level_{n}" for n in range(1, 16)), "iron_age"]:
        if f'"{stage}"' not in stages:
            errors.append(f"item staging never references {stage}")
    for coin in ("copper_coin", "iron_coin", "gold_coin"):
        if f"<item:kubejs:{coin}>" in stages:
            errors.append(f"currency kubejs:{coin} must remain outside ItemStages")
    if '<item:minecraft:string>, "level_3"' not in stages or '<item:minecraft:string>, "level_4"' in stages:
        errors.append("string is not staged consistently with the Level 3 bow")

    expected_mod_policy = {
        "aquaculture": "level_5",
        "oceansdelight": "level_5",
        "bettercopper": "level_7",
        "cookingforblockheads": "level_8",
        "delightful": "level_8",
        "corn_delight": "level_9",
        "create": "level_10",
        "pineapple_delight": "level_11",
        "sliceanddice": "level_11",
        "createaddition": "level_12",
        "alexsdelight": "level_13",
        "alexscaves": "level_14",
        "twilightforest": "level_15",
        "twilightdelight": "level_15",
        "ends_delight": "level_15",
    }
    for mod_id, stage in expected_mod_policy.items():
        expected = f'createModRestriction("{mod_id}", "{stage}")'
        if expected not in stages:
            errors.append(f"missing integration policy {mod_id} -> {stage}")
    if 'createModRestriction("alexsmobs"' in stages:
        errors.append("Alex's Mobs must not be namespace-gated; ItemStages cannot gate its entities")
    if '<item:alexsmobs:animal_dictionary>, "level_13"' not in stages:
        errors.append("Alex's Mobs utility progression is not represented at Level 13")

    for item in ("iron_pickaxe", "iron_sword", "iron_helmet", "iron_chestplate", "iron_leggings", "iron_boots"):
        if f'<item:minecraft:{item}>, "iron_age"' not in stages:
            errors.append(f"minecraft:{item} leaks before Ironworking")
    for selector, stage in (
        ("item:minecraft:redstone", "level_10"),
        ("item:minecraft:gold_ingot", "level_12"),
        ("item:minecraft:diamond", "level_14"),
        ("item:minecraft:lapis_lazuli", "level_14"),
    ):
        if f'ItemStages.restrict(<{selector}>, "{stage}");' not in stages:
            errors.append(f"{selector} is not assigned to intended stage {stage}")

    addons = instance["installedAddons"]
    addon_ids = [int(addon["addonID"]) for addon in addons]
    if len(addon_ids) != len(set(addon_ids)):
        errors.append("duplicate CurseForge project IDs in minecraftinstance.json")
    for project_id in (388800, 250398, 790626, 429235):
        if project_id not in addon_ids:
            errors.append(f"missing requested QoL project {project_id}")
    tracked_mod_jars = subprocess.run(
        ["git", "ls-files", "--", "mods/*.jar"], cwd=ROOT, text=True,
        stdout=subprocess.PIPE, check=True
    ).stdout.splitlines()
    if tracked_mod_jars:
        errors.append("mod JARs must not be tracked; minecraftinstance.json is the source of truth")
    client_only = {int(value) for value in pack["clientOnlyProjectIds"]}
    if 250398 not in client_only:
        errors.append("Controlling is not excluded from the server pack")
    if 1119684 in addon_ids:
        errors.append("Biotech must be removed from the modpack")
    if 1149915 in addon_ids:
        errors.append("NsTut Lib must be removed with Biotech")

    tracked = subprocess.run(
        ["git", "ls-files", "--", "config/jei/world"], cwd=ROOT, text=True,
        stdout=subprocess.PIPE, check=True
    ).stdout.strip()
    if tracked:
        errors.append("personal JEI world state is still tracked")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(
        f"Pack invariants OK for Bounty Harvest {pack['version']} "
        f"({len(addons)} CurseForge projects, 15 economic levels)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
