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

LEVEL_7_QUEST = "0a53cc520f7826a3"
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


def check_reachability(graph: dict[str, set[str]], errors: list[str]) -> None:
    roots = [node for node, dependencies in graph.items() if not dependencies]
    dependents: dict[str, set[str]] = {node: set() for node in graph}
    for node, dependencies in graph.items():
        for dependency in dependencies:
            if dependency in graph:
                dependents[dependency].add(node)

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
        preview = ", ".join(value.upper() for value in unreachable[:8])
        suffix = " ..." if len(unreachable) > 8 else ""
        errors.append(f"unreachable quests from dependency roots: {preview}{suffix}")


def check_progression_invariants(
    graph: dict[str, set[str]], quest_blocks: dict[str, str], errors: list[str]
) -> None:
    required = {
        LEVEL_7_QUEST: "Level 7",
        COPPER_QUEST: "Copper",
        COPPER_TOOLS_QUEST: "Copper Tools",
        IRON_QUEST: "Iron",
    }
    missing = [name for quest_id, name in required.items() if quest_id not in graph]
    if missing:
        errors.append("missing critical progression quests: " + ", ".join(missing))
        return

    expected_dependencies = {
        COPPER_QUEST: {LEVEL_7_QUEST},
        COPPER_TOOLS_QUEST: {COPPER_QUEST},
        IRON_QUEST: {COPPER_TOOLS_QUEST},
    }
    for quest_id, expected in expected_dependencies.items():
        if graph[quest_id] != expected:
            errors.append(
                f"critical quest {quest_id.upper()} dependencies are "
                f"{sorted(value.upper() for value in graph[quest_id])}; expected "
                f"{sorted(value.upper() for value in expected)}"
            )

    copper_tools = quest_blocks[COPPER_TOOLS_QUEST]
    if 'autoclaim: 1b' not in copper_tools or f'stage: "{IRON_STAGE}"' not in copper_tools:
        errors.append("Copper Tools must auto-claim the iron_age (Ironworking) stage")
    for item in COPPER_TOOLS:
        if item not in copper_tools:
            errors.append(f"Copper Tools milestone is missing {item}")

    stages = STAGE_SCRIPT.read_text(encoding="utf-8")
    for selector in IRON_SELECTORS:
        expected = f'ItemStages.restrict(<{selector}>, "{IRON_STAGE}");'
        if expected not in stages:
            errors.append(f"{selector} is not gated by Ironworking")
        leaked = f'ItemStages.restrict(<{selector}>, "level_7");'
        if leaked in stages:
            errors.append(f"{selector} bypasses Ironworking through level_7")


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
    check_reachability(graph, errors)
    check_progression_invariants(graph, quest_blocks, errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    dependency_count = sum(len(dependencies) for dependencies in graph.values())
    print(
        f"Quest graph OK: {len(ids)} unique IDs / {dependency_count} quest dependencies; "
        "cycle, reachability, and critical progression invariants valid."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
