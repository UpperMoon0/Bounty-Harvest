from __future__ import annotations

import re
import sys
from pathlib import Path

from validate_quests import ID_RE, LEVEL_COUNT, extract_quest_blocks, title_for

ROOT = Path(__file__).resolve().parents[1]
QUESTS = ROOT / "config" / "ftbquests" / "quests" / "chapters"
BOUNTIFUL = ROOT / "kubejs" / "server_scripts" / "bountiful_data.js"
RECIPES = ROOT / "kubejs" / "server_scripts" / "recipes.js"
STAGES = ROOT / "scripts" / "gen_item_stages.zs"
CROP_SHOP = QUESTS / "crop.snbt"
BOARD_LEVELS = ROOT / "kubejs" / "server_scripts" / "bounty_board_levels.js"


def has_consumed_item(block: str, item: str, count: int | None = None) -> bool:
    item_pos = block.find(f'item: "{item}"')
    if item_pos < 0:
        return False
    prefix = block[max(0, item_pos - 220):item_pos]
    if "consume_items: true" not in prefix:
        return False
    if count is None:
        return True
    return re.search(rf'count:\s*{count}L?\b', prefix) is not None


def has_item(block: str, item: str, count: int | None = None) -> bool:
    item_pos = block.find(f'item: "{item}"')
    if item_pos < 0:
        return False
    if count is None:
        return True
    prefix = block[max(0, item_pos - 180):item_pos]
    return re.search(rf'count:\s*{count}L?\b', prefix) is not None


def quest_blocks(level: int) -> list[str]:
    path = QUESTS / f"level_{level}.snbt"
    return extract_quest_blocks(path.read_text(encoding="utf-8"))


def promotion_block(level: int, blocks: list[str]) -> str:
    if level == 1:
        return next(block for block in blocks if 'id: "74402ECAFFAFAEC4"' in block)
    matches = [block for block in blocks if re.search(rf'\bstage:\s*"level_{level}"', block)]
    return matches[0] if len(matches) == 1 else ""


def market_block(level: int, blocks: list[str]) -> str:
    matches = [block for block in blocks if title_for(block) == f"Level {level} Market Order"]
    return matches[0] if len(matches) == 1 else ""


def main() -> int:
    errors: list[str] = []

    for level in range(1, LEVEL_COUNT + 1):
        if not (QUESTS / f"level_{level}.snbt").exists():
            errors.append(f"missing Level {level} chapter")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    blocks = {level: quest_blocks(level) for level in range(1, LEVEL_COUNT + 1)}
    promotions = {level: promotion_block(level, blocks[level]) for level in range(1, LEVEL_COUNT + 1)}
    markets = {level: market_block(level, blocks[level]) for level in range(1, LEVEL_COUNT + 1)}

    # Level 1 must teach the repeatable economy, including a deterministic level_1 decree.
    level1 = "\n".join(blocks[1])
    for needle, label in (
        ("bountiful:bountyboard", "Bounty Board"),
        ('\\"ids\\":[\\"level_1\\"]', "Level 1 decree"),
        ("kubejs:copper_coin", "first Bountiful sale"),
    ):
        if needle not in level1:
            errors.append(f"Level 1 onboarding no longer proves {label}")

    # Required worldgen crops always retain deterministic recovery routes.
    crop_shop = CROP_SHOP.read_text(encoding="utf-8")
    for recovery_item in ("corn_delight:corn_seeds", "pineapple_delight:pineapple_crop"):
        if recovery_item not in crop_shop:
            errors.append(f"missing deterministic crop recovery trade for {recovery_item}")

    # The butchery tier must use Cutting Board outputs rather than whole-meat shortcuts.
    recipes = RECIPES.read_text(encoding="utf-8")
    for processed_input in (
        "farmersdelight:cooked_chicken_cuts",
        "farmersdelight:cooked_cod_slice",
        "farmersdelight:cooked_salmon_slice",
        "farmersdelight:beef_patty",
    ):
        if processed_input not in recipes:
            errors.append(f"Level 10 processing can bypass required input {processed_input}")
    if not any(
        "farmersdelight:cutting_board" in block and "farmersdelight:flint_knife" in block
        for block in blocks[10]
    ):
        errors.append("Level 10 no longer establishes Cutting Board and flint-knife infrastructure")

    # Promotions remain expensive after the denomination change instead of resetting.
    promotion_costs = {
        15: ("kubejs:iron_coin", 192),
        16: ("kubejs:iron_coin", 384),
        17: ("kubejs:iron_coin", 768),
        18: ("kubejs:iron_coin", 1536),
        19: ("kubejs:gold_coin", 384),
        20: ("kubejs:gold_coin", 768),
        21: ("kubejs:gold_coin", 1536),
        22: ("kubejs:gold_coin", 3072),
        23: ("kubejs:gold_coin", 6144),
    }
    for level, (item, count) in promotion_costs.items():
        promotion = promotions[level]
        if not promotion:
            errors.append(f"Level {level} promotion block missing")
        elif not has_consumed_item(promotion, item, count):
            errors.append(f"Level {level} promotion must consume {count}x {item}")

    # Every promotion carries the matching decree. The board fix depends on the same IDs.
    for level in range(2, LEVEL_COUNT + 1):
        if f'\\"ids\\":[\\"level_{level}\\"]' not in promotions[level]:
            errors.append(f"Level {level} promotion does not reward level_{level} decree")

    stages = STAGES.read_text(encoding="utf-8")
    stage_expectations = {
        6: ["kubejs:wool_yarn", "kubejs:wool_sweater"],
        7: ["minecraft:potato"],
        8: ["minecraft:sugar_cane", "farmersdelight:apple_pie"],
        9: ['createModRestriction("bettercopper", "level_9")'],
        10: ["farmersdelight:cabbage", "farmersdelight:cutting_board"],
        11: ['createModRestriction("corn_delight", "level_11")'],
        12: ["farmersdelight:tomato"],
        14: ["farmersdelight:onion", 'createModRestriction("cookingforblockheads", "level_14")'],
        15: ['createModRestriction("create", "level_15")'],
        16: ['createModRestriction("pineapple_delight", "level_16")'],
        17: ['createModRestriction("sliceanddice", "level_17")', "farmersdelight:rice"],
        18: ["createaddition:alternator", "minecraft:gold_ingot"],
        19: ["createaddition:electric_motor", "createaddition:accumulator"],
        20: ['createModRestriction("alexsdelight", "level_20")'],
        21: ['createModRestriction("alexscaves", "level_21")', "minecraft:diamond"],
        22: ['createModRestriction("twilightforest", "level_22")', 'createModRestriction("twilightdelight", "level_22")'],
        23: ['createModRestriction("ends_delight", "level_23")'],
    }
    for level, needles in stage_expectations.items():
        for needle in needles:
            if needle not in stages:
                errors.append(f"Level {level} staging lost {needle}")
    if 'stage: "iron_age"' not in promotions[13]:
        errors.append("Level 13 promotion must grant iron_age")
    if 'createModRestriction("createaddition"' in stages:
        errors.append("Create Crafts and Additions must not be namespace-gated as one unlock dump")

    # Slice and Dice and the two-step electrical chain must be used as infrastructure.
    if not any("sliceanddice:slicer" in block for block in blocks[17]):
        errors.append("Level 17 no longer requires Slice and Dice infrastructure")
    for item in ("createaddition:alternator", "createaddition:electric_motor", "createaddition:accumulator"):
        if any(has_consumed_item(markets[level], item) for level in (18, 19)):
            errors.append(f"electrical Market Order consumes infrastructure {item}")
    if has_consumed_item(markets[21], "alexscaves:cave_tablet"):
        errors.append("Level 21 Market Order consumes the Cave Tablet")
    if has_consumed_item(markets[22], "twilightforest:magic_map"):
        errors.append("Level 22 Market Order consumes the Magic Map")
    if not any(has_item(block, "ends_delight:chorus_fruit_pie") for block in blocks[23]):
        errors.append("Level 23 no longer establishes chorus-fruit-pie production")
    if not has_consumed_item(markets[23], "ends_delight:chorus_fruit_pie"):
        errors.append("Level 23 Market Order no longer consumes chorus-fruit-pie output")

    # Automation starts at Create, then renewable Bountiful demand doubles each level.
    bounty = BOUNTIFUL.read_text(encoding="utf-8")
    expected_bulk_scale = {15: 4, 16: 8, 17: 16, 18: 32, 19: 64, 20: 128, 21: 256, 22: 512, 23: 1024}
    for level, scale in expected_bulk_scale.items():
        if not re.search(rf'\b{level}:\s*{scale}\b', bounty):
            errors.append(f"Bountiful bulk scale for Level {level} must remain {scale}x")
    if "const bulk =" not in bounty:
        errors.append("Bountiful renewable-demand scaling helper is missing")
    for level in range(1, LEVEL_COUNT + 1):
        if not re.search(rf'\b{level}:\s*\{{\s*reward:', bounty):
            errors.append(f"Bountiful objective pool missing Level {level}")
        if f"level_${{level}}" in bounty:
            break
    if "Object.keys(levels).forEach" not in bounty or "bounty_decrees/bountiful/level_${level}" not in bounty:
        errors.append("Bountiful decree generation no longer covers the complete level table")
    if not re.search(r"^\s*chorus_pie:.*content:\s*'ends_delight:chorus_fruit_pie'.*amount:\s*bulk\(23,", bounty, re.MULTILINE):
        errors.append("Level 23 repeatable orders no longer put chorus pies under 1024x renewable pressure")
    if re.search(r"^\s*glowstew:.*amount:\s*bulk\(22,", bounty, re.MULTILINE):
        errors.append("new Twilight frontier input Glowstew should stay fixed-volume instead of inheriting the 512x legacy multiplier")

    # Newly crafted boards are seeded deterministically from the placer's highest stage.
    if not BOARD_LEVELS.exists():
        errors.append("missing bounty-board level seeding script")
    else:
        board = BOARD_LEVELS.read_text(encoding="utf-8")
        required_board_tokens = (
            "BlockEvents.placed('bountiful:bountyboard'",
            "for (let level = 23; level >= 1; level--)",
            "gamestage check",
            "decree_inv",
            "bounty_inv",
            'bountiful:decree_data',
            'data merge block',
        )
        for token in required_board_tokens:
            if token not in board:
                errors.append(f"bounty-board seeding lost required behavior: {token}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(
        "Economy curve OK: 23 paced unlocks, deterministic board decrees, retained infrastructure, "
        "continuous promotion costs, and 4x-1024x renewable automation pressure are protected."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
