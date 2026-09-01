from __future__ import annotations

import re
import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEST_ROOT = ROOT / "config" / "ftbquests" / "quests"
STAGE_SCRIPT = ROOT / "scripts" / "gen_item_stages.zs"

ID_RE = re.compile(r'\bid:\s*"([0-9A-Fa-f]{16})"')
DEPENDENCY_RE = re.compile(r"dependencies:\s*\[([^\]]*)\]", re.DOTALL)

# The questbook intentionally has exactly three entry points.
KNOWN_ROOTS = {
    "74402ecaffafaec4": "chapters/level_1.snbt",
    "e60381a75a8c4d21": "chapters/research.snbt",
    "74be872a1ffe8d25": "chapters/currencies_exchange.snbt",
}

LEVEL_STAGE_IDS = {1: '74402ecaffafaec4', 2: '7d3858343983b67a', 3: '573fe8ed65790a78', 4: '1003c2b79f710366', 5: '29747d157c7f8c88', 6: '7297a69487bee03d', 7: '0a53cc520f7826a3', 8: '4003bf6fe565761f', 9: 'c0b4aa32262bf02b', 10: '201fa0d785ef1770', 11: '1ffcfc4eaf71d122', 12: 'd147bb0fa78a2efa', 13: '14a6f09e58565c89', 14: '4bb6b303f8005d7e', 15: '2820c98f56814014'}
FINAL_MARKET_IDS = {1: 'a06092ae6ea56685', 2: '759303985a706218', 3: '9131a689d31728c8', 4: '284bda8ad6a1ee07', 5: '964e4e55a3efb49e', 6: '5ef6647a3bb43a42', 7: 'd9d29b504ce79600', 8: 'f3fbd0bed43c89cc', 9: '2a9904a355a5fe23', 10: 'c4f9e553b22e40cc', 11: '2507ab50f6ccd90e', 12: 'c249cfa083ab4179', 13: 'a48274d6a8ee43b3', 14: '250184a59ea4eba2', 15: '998d5fca54b02b56'}

LEVEL_7_QUEST = "0a53cc520f7826a3"
LEVEL_10_QUEST = "201fa0d785ef1770"
COPPER_QUEST = "6a5c20c31bd2649e"
COPPER_TOOLS_QUEST = "34b5df088e2f447e"
IRON_QUEST = "557852ffd6f4d560"
IRON_STAGE = "iron_age"

COPPER_TOOLS = (
    "bettercopper:copper_shovel",
    "bettercopper:copper_pickaxe",
    "bettercopper:copper_axe",
    "bettercopper:copper_hoe",
    "bettercopper:copper_sword",
)

IRON_SELECTORS = (
    "tag:items:minecraft:iron_ores",
    "item:minecraft:iron_nugget",
    "item:minecraft:raw_iron",
    "item:minecraft:raw_iron_block",
    "item:minecraft:iron_ingot",
    "item:minecraft:iron_block",
    "item:minecraft:iron_axe",
    "item:minecraft:iron_hoe",
    "item:minecraft:iron_pickaxe",
    "item:minecraft:iron_shovel",
    "item:minecraft:iron_sword",
    "item:minecraft:iron_helmet",
    "item:minecraft:iron_chestplate",
    "item:minecraft:iron_leggings",
    "item:minecraft:iron_boots",
    "item:minecraft:shield",
)


def extract_quest_blocks(content: str) -> list[str]:
    marker = re.search(r"\bquests\s*:\s*\[", content)
    if not marker:
        return []

    blocks: list[str] = []
    bracket_depth = 1
    brace_depth = 0
    block_start: int | None = None
    quoted = False
    escaped = False

    for index in range(marker.end(), len(content)):
        char = content[index]
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
        elif char == "[":
            bracket_depth += 1
        elif char == "]":
            bracket_depth -= 1
            if bracket_depth == 0:
                break
        elif char == "{":
            if brace_depth == 0 and bracket_depth == 1:
                block_start = index
            brace_depth += 1
        elif char == "}" and brace_depth:
            brace_depth -= 1
            if brace_depth == 0 and block_start is not None:
                blocks.append(content[block_start : index + 1])
                block_start = None

    return blocks


def dependencies_for(block: str) -> set[str]:
    match = DEPENDENCY_RE.search(block)
    if not match:
        return set()
    return {value.lower() for value in re.findall(r'"([0-9A-Fa-f]{16})"', match.group(1))}


def check_cycles(graph: dict[str, set[str]], errors: list[str]) -> None:
    state: dict[str, int] = {}
    stack: list[str] = []
    reported: set[tuple[str, ...]] = set()

    def visit(node: str) -> None:
        state[node] = 1
        stack.append(node)
        for dependency in graph[node]:
            if dependency not in graph:
                continue
            dependency_state = state.get(dependency, 0)
            if dependency_state == 0:
                visit(dependency)
            elif dependency_state == 1:
                start = stack.index(dependency)
                cycle = tuple(stack[start:] + [dependency])
                signature = tuple(sorted(cycle[:-1]))
                if signature not in reported:
                    reported.add(signature)
                    errors.append("dependency cycle: " + " -> ".join(value.upper() for value in cycle))
        stack.pop()
        state[node] = 2

    for node in graph:
        if state.get(node, 0) == 0:
            visit(node)


def check_reachability(
    graph: dict[str, set[str]], quest_sources: dict[str, Path], errors: list[str]
) -> None:
    declared_roots = set(KNOWN_ROOTS)
    actual_roots = {node for node, dependencies in graph.items() if not dependencies}

    for root, expected_source in KNOWN_ROOTS.items():
        if root not in graph:
            errors.append(f"missing declared quest root {root.upper()} ({expected_source})")
            continue
        source = quest_sources[root].relative_to(QUEST_ROOT).as_posix()
        if source != expected_source:
            errors.append(f"declared quest root {root.upper()} moved to {source}; expected {expected_source}")
        if graph[root]:
            errors.append(
                f"declared quest root {root.upper()} unexpectedly has dependencies: "
                + ", ".join(value.upper() for value in sorted(graph[root]))
            )

    unexpected_roots = sorted(actual_roots - declared_roots)
    if unexpected_roots:
        preview = ", ".join(
            f"{value.upper()} ({quest_sources[value].relative_to(QUEST_ROOT).as_posix()})"
            for value in unexpected_roots[:8]
        )
        suffix = " ..." if len(unexpected_roots) > 8 else ""
        errors.append(
            "undeclared dependency-free quest roots detected; connect them to the graph "
            f"or add them to KNOWN_ROOTS intentionally: {preview}{suffix}"
        )

    dependents: dict[str, set[str]] = {node: set() for node in graph}
    for node, dependencies in graph.items():
        for dependency in dependencies:
            if dependency in graph:
                dependents[dependency].add(node)

    roots = [root for root in declared_roots if root in graph]
    reachable = set(roots)
    queue = deque(roots)
    while queue:
        node = queue.popleft()
        for dependent in dependents[node]:
            if dependent not in reachable:
                reachable.add(dependent)
                queue.append(dependent)

    unreachable = sorted(set(graph) - reachable)
    if unreachable:
        preview = ", ".join(
            f"{value.upper()} ({quest_sources[value].relative_to(QUEST_ROOT).as_posix()})"
            for value in unreachable[:8]
        )
        suffix = " ..." if len(unreachable) > 8 else ""
        errors.append(f"quests unreachable from declared roots: {preview}{suffix}")


def check_level_spine(
    graph: dict[str, set[str]], quest_blocks: dict[str, str], quest_sources: dict[str, Path], errors: list[str]
) -> None:
    for level in range(1, 16):
        stage_id = LEVEL_STAGE_IDS[level]
        market_id = FINAL_MARKET_IDS[level]
        expected_file = f"chapters/level_{level}.snbt"
        for quest_id, label in ((stage_id, "level milestone"), (market_id, "market order")):
            if quest_id not in graph:
                errors.append(f"Level {level} missing {label} {quest_id.upper()}")
                continue
            actual = quest_sources[quest_id].relative_to(QUEST_ROOT).as_posix()
            if actual != expected_file:
                errors.append(f"Level {level} {label} is in {actual}; expected {expected_file}")

        if market_id in quest_blocks:
            block = quest_blocks[market_id]
            if "Market Order" not in block:
                errors.append(f"Level {level} final milestone is not labelled as a Market Order")
            if block.count("consume_items: true") < 2:
                errors.append(f"Level {level} Market Order must consume at least two production outputs")

        if level >= 2 and stage_id in graph:
            expected_dep = {FINAL_MARKET_IDS[level - 1]}
            if graph[stage_id] != expected_dep:
                errors.append(
                    f"Level {level} milestone dependencies are "
                    f"{sorted(value.upper() for value in graph[stage_id])}; expected "
                    f"{sorted(value.upper() for value in expected_dep)}"
                )
            block = quest_blocks[stage_id]
            if "autoclaim: 1b" not in block or f'stage: "level_{level}"' not in block:
                errors.append(f"Level {level} milestone must auto-claim stage level_{level}")


def check_copper_iron_invariant(
    graph: dict[str, set[str]], quest_blocks: dict[str, str], quest_sources: dict[str, Path], errors: list[str]
) -> None:
    required = {
        LEVEL_7_QUEST: "Level 7",
        COPPER_QUEST: "Copper",
        COPPER_TOOLS_QUEST: "Copper Tools",
        LEVEL_10_QUEST: "Level 10",
        IRON_QUEST: "Iron Supply",
    }
    missing = [name for quest_id, name in required.items() if quest_id not in graph]
    if missing:
        errors.append("missing critical progression quests: " + ", ".join(missing))
        return

    expected_dependencies = {
        COPPER_QUEST: {LEVEL_7_QUEST},
        COPPER_TOOLS_QUEST: {COPPER_QUEST},
        IRON_QUEST: {LEVEL_10_QUEST},
    }
    for quest_id, expected in expected_dependencies.items():
        if graph[quest_id] != expected:
            errors.append(
                f"critical quest {quest_id.upper()} dependencies are "
                f"{sorted(value.upper() for value in graph[quest_id])}; expected "
                f"{sorted(value.upper() for value in expected)}"
            )

    copper_tools = quest_blocks[COPPER_TOOLS_QUEST]
    if f'stage: "{IRON_STAGE}"' in copper_tools:
        errors.append("Copper Tools must not grant Ironworking; copper must remain active through Level 9")
    for item in COPPER_TOOLS:
        if item not in copper_tools:
            errors.append(f"Copper Tools milestone is missing {item}")

    iron_grants = [quest_id for quest_id, block in quest_blocks.items() if f'stage: "{IRON_STAGE}"' in block]
    if iron_grants != [LEVEL_10_QUEST]:
        errors.append(
            "iron_age must be granted exactly once by the Level 10 promotion; found "
            + ", ".join(value.upper() for value in iron_grants)
        )

    level_10 = quest_blocks[LEVEL_10_QUEST]
    if level_10.count("autoclaim: 1b") < 2 or f'stage: "{IRON_STAGE}"' not in level_10:
        errors.append("Level 10 promotion must auto-claim both level_10 and iron_age")

    iron_source = quest_sources[IRON_QUEST].relative_to(QUEST_ROOT).as_posix()
    if iron_source != "chapters/level_10.snbt":
        errors.append(f"Iron Supply moved to {iron_source}; expected chapters/level_10.snbt")

    for level in (7, 8, 9):
        text = (QUEST_ROOT / "chapters" / f"level_{level}.snbt").read_text(encoding="utf-8")
        if f'stage: "{IRON_STAGE}"' in text:
            errors.append(f"Level {level} illegally grants Ironworking before Level 10")

    stages = STAGE_SCRIPT.read_text(encoding="utf-8")
    for selector in IRON_SELECTORS:
        expected = f'ItemStages.restrict(<{selector}>, "{IRON_STAGE}");'
        if expected not in stages:
            errors.append(f"{selector} is not gated by Ironworking")
        for early_stage in ("level_7", "level_8", "level_9"):
            if f'ItemStages.restrict(<{selector}>, "{early_stage}");' in stages:
                errors.append(f"{selector} bypasses Ironworking through {early_stage}")


def main() -> int:
    ids: dict[str, Path] = {}
    quest_blocks: dict[str, str] = {}
    quest_sources: dict[str, Path] = {}
    errors: list[str] = []

    for path in QUEST_ROOT.rglob("*.snbt"):
        content = path.read_text(encoding="utf-8")
        for raw_id in ID_RE.findall(content):
            value = raw_id.lower()
            if value in ids:
                errors.append(f"duplicate ID {raw_id} in {path} (first in {ids[value]})")
            else:
                ids[value] = path

        for block in extract_quest_blocks(content):
            match = ID_RE.search(block)
            if not match:
                errors.append(f"quest without a 16-digit ID in {path}")
                continue
            quest_id = match.group(1).lower()
            if quest_id in quest_blocks:
                errors.append(
                    f"duplicate quest ID {match.group(1)} in {path} "
                    f"(first in {quest_sources[quest_id]})"
                )
                continue
            quest_blocks[quest_id] = block
            quest_sources[quest_id] = path

    graph = {quest_id: dependencies_for(block) for quest_id, block in quest_blocks.items()}
    for quest_id, dependencies in graph.items():
        for dependency in dependencies:
            if dependency not in graph:
                errors.append(
                    f"dangling quest dependency {dependency.upper()} in {quest_sources[quest_id]} "
                    f"(quest {quest_id.upper()})"
                )

    check_cycles(graph, errors)
    check_reachability(graph, quest_sources, errors)
    check_level_spine(graph, quest_blocks, quest_sources, errors)
    check_copper_iron_invariant(graph, quest_blocks, quest_sources, errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    dependency_count = sum(len(dependencies) for dependencies in graph.values())
    print(
        f"Quest graph OK: {len(ids)} unique IDs / {dependency_count} quest dependencies; "
        "15 economic levels, market-order spine, 3 declared roots, cycles, reachability, "
        "and delayed Level 10 Ironworking invariants valid."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
