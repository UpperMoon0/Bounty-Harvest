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
DESIGN_DOC = ROOT / "PROGRESSION_DESIGN.md"
LEVEL_COUNT = 23


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
            yield text[start:index + 1]


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
    if not DESIGN_DOC.is_file():
        errors.append("missing PROGRESSION_DESIGN.md design contract")

    required_runtime = [
        ROOT / "scripts" / "gen_item_stages.zs",
        DEFAULT_STAGES,
        ROOT / "resourcepacks" / "gen_bh_bounties.zip",
        BOUNTIFUL_DATA,
        ROOT / "kubejs" / "server_scripts" / "bounty_board_levels.js",
        QUESTS / "research.snbt",
        QUESTS / "decree.snbt",
        QUESTS / "crop.snbt",
    ]
    required_runtime.extend(QUESTS / f"level_{level}.snbt" for level in range(1, LEVEL_COUNT + 1))
    for path in required_runtime:
        if not path.is_file():
            errors.append(f"missing runtime file {path.relative_to(ROOT)}")

    archives = [path for path in QUESTS.iterdir() if path.is_file() and path.suffix != ".snbt"]
    if archives:
        errors.append("non-SNBT files in quest chapters: " + ", ".join(path.name for path in archives))

    with zipfile.ZipFile(ROOT / "resourcepacks" / "gen_bh_bounties.zip") as archive:
        names = archive.namelist()
        if not any(name.startswith("data/bountiful/bounty_decrees/") for name in names):
            errors.append("legacy Bountiful fallback has no bounty decrees")
        if not any(name.startswith("data/bountiful/bounty_pools/") for name in names):
            errors.append("legacy Bountiful fallback has no bounty pools")

    bounty_data = BOUNTIFUL_DATA.read_text(encoding="utf-8") if BOUNTIFUL_DATA.is_file() else ""
    if "ServerEvents.highPriorityData" not in bounty_data:
        errors.append("Bountiful level data is not registered as high-priority server data")
    if "bountiful:bounty_decrees/bountiful/level_${level}" not in bounty_data:
        errors.append("Bountiful generator does not register level decree resources")
    if "bountiful:bounty_pools/bountiful/${pool}" not in bounty_data:
        errors.append("Bountiful generator does not register level objective pools")
    defined_levels = {int(value) for value in re.findall(r"^\s*(\d+): \{ reward:", bounty_data, re.MULTILINE)}
    if defined_levels != set(range(1, LEVEL_COUNT + 1)):
        errors.append(f"Bountiful generator defines levels {sorted(defined_levels)}; expected 1-{LEVEL_COUNT}")
    for reward_pool in ("bh_copper_rews", "bh_iron_rews", "bh_gold_rews"):
        if reward_pool not in bounty_data:
            errors.append(f"missing Bountiful reward pool {reward_pool}")

    for legacy_good in ("minecraft:wheat", "minecraft:egg", "minecraft:leather", "minecraft:carrot", "minecraft:charcoal"):
        if bounty_data.count(legacy_good) < 2:
            errors.append(f"reuse invariant: {legacy_good} does not recur across bounty tiers")
    for layered_good in (
        "farmersdelight:chicken_sandwich",
        "corn_delight:taco",
        "farmersdelight:salmon_roll",
        "pineapple_delight:pineapple_pie",
        "ends_delight:chorus_fruit_pie",
    ):
        if layered_good not in bounty_data:
            errors.append(f"processed reuse invariant missing {layered_good} from repeatable markets")

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

    for level in range(1, LEVEL_COUNT + 1):
        path = QUESTS / f"level_{level}.snbt"
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if level >= 2:
            expected = rf'autoclaim:\s*1b[\s\S]{{0,120}}stage:\s*"level_{level}"[\s\S]{{0,80}}type:\s*"stage"'
            if not re.search(expected, text):
                errors.append(f"Level {level} lacks an auto-claimed stage reward")
        if f"Level {level} Market Order" not in text:
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
    for level in range(1, LEVEL_COUNT + 1):
        if f"Level {level} Decree" not in decree or f"level_{level}" not in decree:
            errors.append(f"decree market does not expose Level {level}")

    recipes = (ROOT / "kubejs" / "server_scripts" / "recipes.js").read_text(encoding="utf-8")
    if recipes.count("remove({output: 'farmersdelight:wheat_dough'})") != 1:
        errors.append("wheat dough must have exactly one global recipe removal")
    dough_window = re.search(r"wheat_dough[\s\S]{0,500}", recipes)
    if dough_window and "minecraft:water_bucket" in dough_window.group(0):
        errors.append("wheat dough still appears to require a water bucket")
    if "remove({id: 'minecraft:fishing_rod'})" in recipes:
        errors.append("fishing rod is still artificially locked behind a replacement recipe")
    if "remove({id: 'bettercopper:copper_helmet'})" in recipes:
        errors.append("copper armor is globally removed; the copper era needs viable equipment")
    for required_recipe_output in (
        "farmersdelight:chicken_sandwich",
        "farmersdelight:fish_stew",
        "farmersdelight:apple_pie",
        "corn_delight:taco",
    ):
        if required_recipe_output not in recipes:
            errors.append(f"missing layered recipe for {required_recipe_output}")

    tags = (ROOT / "kubejs" / "server_scripts" / "tags.js").read_text(encoding="utf-8")
    if "minecraft:tulip" in tags:
        errors.append("invalid minecraft:tulip ID remains")

    stages = (ROOT / "scripts" / "gen_item_stages.zs").read_text(encoding="utf-8")
    for coin in ("copper_coin", "iron_coin", "gold_coin"):
        if f"<item:kubejs:{coin}>" in stages:
            errors.append(f"currency kubejs:{coin} must remain outside ItemStages")
    if 'createModRestriction("alexsmobs"' in stages:
        errors.append("Alex's Mobs must not be namespace-gated; ItemStages cannot gate its entities")

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
        f"({len(addons)} CurseForge projects, {LEVEL_COUNT} economic levels)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
