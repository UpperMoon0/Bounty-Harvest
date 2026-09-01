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
        QUESTS / "research.snbt",
    ]
    for path in required_runtime:
        if not path.is_file():
            errors.append(f"missing runtime file {path.relative_to(ROOT)}")
    archives = [path for path in QUESTS.iterdir() if path.is_file() and path.suffix != ".snbt"]
    if archives:
        errors.append("non-SNBT files in quest chapters: " + ", ".join(path.name for path in archives))

    with zipfile.ZipFile(ROOT / "resourcepacks" / "gen_bh_bounties.zip") as archive:
        names = archive.namelist()
        if not any(name.startswith("data/bountiful/bounty_decrees/") for name in names):
            errors.append("Bountiful data pack has no bounty decrees")
        if not any(name.startswith("data/bountiful/bounty_pools/") for name in names):
            errors.append("Bountiful data pack has no bounty pools")

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

    for level in range(1, 9):
        text = (QUESTS / f"level_{level}.snbt").read_text(encoding="utf-8")
        if level >= 2:
            expected = rf'autoclaim:\s*1b[\s\S]{{0,100}}stage:\s*"level_{level}"[\s\S]{{0,60}}type:\s*"stage"'
            if not re.search(expected, text):
                errors.append(f"Level {level} lacks an auto-claimed stage reward")
        for block in compounds(text):
            if block.count('type: "item"') != 1:
                continue
            outer = re.search(r"\bcount:\s*(\d+)L?", block)
            embedded = re.search(r"\bCount:\s*(\d+)", block)
            if outer and embedded and outer.group(1) != embedded.group(1):
                errors.append(f"Level {level} has mismatched task counts {outer.group(1)} and {embedded.group(1)}")
                break

    level_6 = (QUESTS / "level_6.snbt").read_text(encoding="utf-8")
    level_7 = (QUESTS / "level_7.snbt").read_text(encoding="utf-8")
    if 'dependencies: ["015743E28B4488CE"]' not in level_6 or 'title: "Optional: poisonous potato"' not in level_6:
        errors.append("poisonous potato is not isolated as an optional quest")
    if "97C83D41E6A25BF0" in re.search(r"dependencies:\s*\[([^\]]*)\]", level_7, re.DOTALL).group(1):
        errors.append("Level 7 still depends on the poisonous-potato challenge")
    if 'stage: "iron_age"' not in level_7 or 'dependencies: ["34B5DF088E2F447E"]' not in level_7:
        errors.append("copper tools do not unlock the Ironworking quest path")

    recipes = (ROOT / "kubejs" / "server_scripts" / "recipes.js").read_text(encoding="utf-8")
    if recipes.count("remove({output: 'farmersdelight:wheat_dough'})") != 1:
        errors.append("wheat dough must have exactly one global recipe removal")
    if "minecraft:water_bucket'\n    })" in recipes and "wheat_dough" in recipes:
        errors.append("wheat dough still appears to require a water bucket")
    tags = (ROOT / "kubejs" / "server_scripts" / "tags.js").read_text(encoding="utf-8")
    if "minecraft:tulip" in tags:
        errors.append("invalid minecraft:tulip ID remains")

    stages = (ROOT / "scripts" / "gen_item_stages.zs").read_text(encoding="utf-8")
    for stage in [*(f"level_{n}" for n in range(1, 9)), "iron_age"]:
        if f'"{stage}"' not in stages:
            errors.append(f"item staging never references {stage}")
    for coin in ("copper_coin", "iron_coin", "gold_coin"):
        if f"<item:kubejs:{coin}>" in stages:
            errors.append(f"currency kubejs:{coin} must remain outside ItemStages")
    if '<item:minecraft:string>, "level_3"' not in stages or '<item:minecraft:string>, "level_4"' in stages:
        errors.append("string is not staged consistently with the Level 3 bow")
    for mod_id in ("create", "createaddition", "sliceanddice", "alexscaves", "twilightforest", "alexsmobs", "cookingforblockheads"):
        if f'createModRestriction("{mod_id}"' not in stages:
            errors.append(f"missing explicit integration policy for {mod_id}")
    for item in ("iron_pickaxe", "iron_sword", "iron_helmet", "iron_chestplate", "iron_leggings", "iron_boots"):
        if f"<item:minecraft:{item}>, \"iron_age\"" not in stages:
            errors.append(f"minecraft:{item} leaks before Ironworking")

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
    print(f"Pack invariants OK for Bounty Harvest {pack['version']} ({len(addons)} CurseForge projects).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
