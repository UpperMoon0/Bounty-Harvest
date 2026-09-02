from __future__ import annotations

import re
import sys
from pathlib import Path

from validate_quests import FINAL_MARKET_IDS, ID_RE, LEVEL_STAGE_IDS, extract_quest_blocks

ROOT = Path(__file__).resolve().parents[1]
QUESTS = ROOT / "config" / "ftbquests" / "quests" / "chapters"
BOUNTIFUL = ROOT / "kubejs" / "server_scripts" / "bountiful_data.js"
RECIPES = ROOT / "kubejs" / "server_scripts" / "recipes.js"
STAGES = ROOT / "scripts" / "gen_item_stages.zs"
CROP_SHOP = QUESTS / "crop.snbt"


def has_consumed_item(block: str, item: str, count: int | None = None) -> bool:
    escaped = re.escape(item)
    if count is None:
        pattern = rf'consume_items:\s*true[\s\S]{{0,160}}item:\s*"{escaped}"'
    else:
        pattern = (
            rf'consume_items:\s*true[\s\S]{{0,80}}count:\s*{count}L?'
            rf'[\s\S]{{0,160}}item:\s*"{escaped}"'
        )
    return re.search(pattern, block) is not None


def has_item(block: str, item: str, count: int | None = None) -> bool:
    escaped = re.escape(item)
    if count is None:
        return re.search(rf'item:\s*"{escaped}"', block) is not None
    return re.search(
        rf'count:\s*{count}L?[\s\S]{{0,160}}item:\s*"{escaped}"', block
    ) is not None


def quest_map(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for block in extract_quest_blocks(text):
        match = ID_RE.search(block)
        if match:
            result[match.group(1).lower()] = block
    return result


def main() -> int:
    errors: list[str] = []

    levels = {
        level: (QUESTS / f"level_{level}.snbt").read_text(encoding="utf-8")
        for level in range(1, 16)
    }
    blocks = {level: extract_quest_blocks(text) for level, text in levels.items()}
    quests = {level: quest_map(text) for level, text in levels.items()}

    # Level 1 must teach the core economy before charging promotion currency. The
    # book is intentionally branched, so this invariant searches the chapter rather
    # than assuming specific array positions.
    if not any("bountiful:bountyboard" in block for block in blocks[1]):
        errors.append("Level 1 onboarding no longer requires the Bounty Board")
    if not any("kubejs:copper_coin" in block for block in blocks[1]):
        errors.append("Level 1 onboarding no longer proves the player completed a first sale")

    # World-generation luck must never hard-lock a required crop.
    crop_shop = CROP_SHOP.read_text(encoding="utf-8")
    for recovery_item in ("corn_delight:corn_seeds", "pineapple_delight:pineapple_crop"):
        if recovery_item not in crop_shop:
            errors.append(f"missing deterministic crop recovery trade for {recovery_item}")

    # The pre-iron processing tier must actually use cutting-board outputs.
    recipes = RECIPES.read_text(encoding="utf-8")
    for processed_input in (
        "farmersdelight:cooked_chicken_cuts",
        "farmersdelight:cooked_cod_slice",
        "farmersdelight:cooked_salmon_slice",
        "farmersdelight:beef_patty",
    ):
        if processed_input not in recipes:
            errors.append(f"Level 8 processing can bypass required input {processed_input}")
    if not any(
        "farmersdelight:cutting_board" in block and "farmersdelight:flint_knife" in block
        for block in blocks[8]
    ):
        errors.append("Level 8 no longer establishes Cutting Board and flint-knife infrastructure")

    # Promotion currency follows an explicit doubling-style industrial curve.
    promotion_costs = {
        10: [("kubejs:iron_coin", 48), ("minecraft:charcoal", 32), ("minecraft:copper_ingot", 24)],
        11: [("kubejs:iron_coin", 96), ("create:andesite_alloy", 48)],
        12: [("kubejs:iron_coin", 192), ("pineapple_delight:pineapple_pie", 64)],
        13: [("kubejs:gold_coin", 48), ("pineapple_delight:pineapple_pie", 128)],
        14: [("kubejs:gold_coin", 96), ("corn_delight:taco", 128), ("pineapple_delight:pineapple_pie", 128)],
        15: [("kubejs:gold_coin", 192), ("corn_delight:taco", 256), ("pineapple_delight:pineapple_pie", 256)],
    }
    for level, costs in promotion_costs.items():
        promotion = quests[level].get(LEVEL_STAGE_IDS[level], "")
        if not promotion:
            errors.append(f"Level {level} promotion block is missing")
            continue
        for item, count in costs:
            if not has_consumed_item(promotion, item, count):
                errors.append(f"Level {level} promotion lost automation-scale cost {count}x {item}")

    # Slice and Dice must be a used progression tool, not a dead namespace unlock.
    if not any("sliceanddice:slicer" in block for block in blocks[11]):
        errors.append("Level 11 no longer requires Slice and Dice infrastructure")

    # Infrastructure is retained; market orders consume renewable throughput instead.
    level12_market = quests[12].get(FINAL_MARKET_IDS[12], "")
    for infrastructure in (
        "createaddition:electric_motor",
        "createaddition:alternator",
        "createaddition:accumulator",
    ):
        if has_consumed_item(level12_market, infrastructure):
            errors.append(f"Level 12 Market Order consumes infrastructure {infrastructure}")
    for item, count in (
        ("minecraft:wheat", 256),
        ("corn_delight:taco", 128),
        ("pineapple_delight:pineapple_fried_rice", 128),
    ):
        if not has_consumed_item(level12_market, item, count):
            errors.append(f"Level 12 Market Order lost industrial shipment {count}x {item}")

    level14_market = quests[14].get(FINAL_MARKET_IDS[14], "")
    if has_consumed_item(level14_market, "alexscaves:cave_tablet"):
        errors.append("Level 14 Market Order consumes the Cave Tablet instead of retaining infrastructure")
    for item, count in (
        ("farmersdelight:chicken_sandwich", 256),
        ("pineapple_delight:pineapple_pie", 256),
        ("corn_delight:taco", 128),
    ):
        if not has_consumed_item(level14_market, item, count):
            errors.append(f"Level 14 no longer reconnects farm throughput through {count}x {item}")

    level15_market = quests[15].get(FINAL_MARKET_IDS[15], "")
    if has_consumed_item(level15_market, "twilightforest:magic_map"):
        errors.append("Level 15 Market Order consumes the Magic Map instead of retaining navigation infrastructure")
    for item, count in (
        ("corn_delight:taco", 512),
        ("pineapple_delight:pineapple_pie", 512),
        ("farmersdelight:chicken_sandwich", 256),
        ("ends_delight:chorus_fruit_pie", 128),
    ):
        if not has_consumed_item(level15_market, item, count):
            errors.append(f"Level 15 peak shipment lost {count}x {item}")

    # End's Delight is intentionally a real final-tier branch, not a dead namespace gate.
    if not any(
        block != level15_market and has_item(block, "ends_delight:chorus_fruit_pie", 64)
        for block in blocks[15]
    ):
        errors.append("Level 15 no longer establishes the End's Delight chorus-fruit production branch")

    # Repeatable orders scale geometrically on renewable goods after Create arrives.
    bounty = BOUNTIFUL.read_text(encoding="utf-8")
    expected_bulk_scale = {10: 4, 11: 8, 12: 16, 13: 32, 14: 64, 15: 128}
    for level, scale in expected_bulk_scale.items():
        if not re.search(rf'^\s*{level}:\s*{scale},?\s*$', bounty, re.MULTILINE):
            errors.append(f"Bountiful bulk scale for Level {level} must remain {scale}x")
    if "const bulk =" not in bounty:
        errors.append("Bountiful renewable-demand scaling helper is missing")

    for item in ("twilightdelight:glowstew", "ends_delight:chorus_fruit_pie"):
        if not re.search(
            rf"content:\s*'{re.escape(item)}'[\s\S]{{0,120}}amount:\s*bulk\(15,\s*1,\s*4\)",
            bounty,
        ):
            errors.append(f"Level 15 repeatable market no longer scales renewable {item} at 128x")

    stages = STAGES.read_text(encoding="utf-8")
    if not re.search(r'createModRestriction\("ends_delight",\s*"level_15"\)', stages):
        errors.append("End's Delight must remain gated to Level 15 while its chorus-fruit branch is active")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(
        "Economy curve OK: branched onboarding, recovery, processor use, retained infrastructure, "
        "4x-128x automation pressure, and the Level 15 frontier branches are protected."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
