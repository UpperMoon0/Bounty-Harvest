from __future__ import annotations

import re
import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEST_ROOT = ROOT / "config" / "ftbquests" / "quests"
LEVEL_COUNT = 23

ID_RE = re.compile(r'\bid:\s*"([0-9A-Fa-f]{16})"')
DEPENDENCY_RE = re.compile(r"dependencies:\s*\[([^\]]*)\]", re.DOTALL)
TITLE_RE = re.compile(r'\btitle:\s*"([^"]+)"')

KNOWN_ROOTS = {
    "74402ecaffafaec4": "chapters/level_1.snbt",
    "e60381a75a8c4d21": "chapters/research.snbt",
    "74be872a1ffe8d25": "chapters/currencies_exchange.snbt",
}


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


def title_for(block: str) -> str:
    match = TITLE_RE.search(block)
    return match.group(1) if match else "<untitled>"


def reaches(start: str, target: str, dependents: dict[str, set[str]], allowed: set[str]) -> bool:
    seen = {start}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node == target:
            return True
        for child in dependents.get(node, set()):
            if child in allowed and child not in seen:
                seen.add(child)
                queue.append(child)
    return False


def main() -> int:
    errors: list[str] = []
    graph: dict[str, set[str]] = {}
    blocks_by_id: dict[str, str] = {}
    source_by_id: dict[str, Path] = {}

    for path in sorted(QUEST_ROOT.rglob("*.snbt")):
        for block in extract_quest_blocks(path.read_text(encoding="utf-8")):
            match = ID_RE.search(block)
            if not match:
                errors.append(f"quest without ID in {path.relative_to(QUEST_ROOT)}")
                continue
            quest_id = match.group(1).lower()
            if quest_id in graph:
                errors.append(
                    f"duplicate quest ID {quest_id.upper()} in "
                    f"{source_by_id[quest_id].relative_to(QUEST_ROOT)} and {path.relative_to(QUEST_ROOT)}"
                )
                continue
            graph[quest_id] = dependencies_for(block)
            blocks_by_id[quest_id] = block
            source_by_id[quest_id] = path

    for quest_id, dependencies in graph.items():
        for dependency in dependencies:
            if dependency not in graph:
                errors.append(
                    f"{quest_id.upper()} ({source_by_id[quest_id].relative_to(QUEST_ROOT)}) "
                    f"depends on missing quest {dependency.upper()}"
                )

    state: dict[str, int] = {}
    stack: list[str] = []

    def visit(node: str) -> None:
        state[node] = 1
        stack.append(node)
        for dependency in graph[node]:
            if dependency not in graph:
                continue
            if state.get(dependency, 0) == 0:
                visit(dependency)
            elif state.get(dependency) == 1:
                start = stack.index(dependency)
                errors.append(
                    "dependency cycle: " + " -> ".join(value.upper() for value in stack[start:] + [dependency])
                )
        stack.pop()
        state[node] = 2

    for node in graph:
        if state.get(node, 0) == 0:
            visit(node)

    actual_roots = {node for node, dependencies in graph.items() if not dependencies}
    for root, expected_source in KNOWN_ROOTS.items():
        if root not in graph:
            errors.append(f"missing declared root {root.upper()} ({expected_source})")
        elif source_by_id[root].relative_to(QUEST_ROOT).as_posix() != expected_source:
            errors.append(f"declared root {root.upper()} moved from {expected_source}")
    for unexpected in sorted(actual_roots - set(KNOWN_ROOTS)):
        errors.append(
            f"undeclared dependency-free root {unexpected.upper()} "
            f"({source_by_id[unexpected].relative_to(QUEST_ROOT)})"
        )

    global_dependents: dict[str, set[str]] = {node: set() for node in graph}
    for node, dependencies in graph.items():
        for dependency in dependencies:
            if dependency in global_dependents:
                global_dependents[dependency].add(node)
    reachable = {root for root in KNOWN_ROOTS if root in graph}
    queue = deque(reachable)
    while queue:
        node = queue.popleft()
        for child in global_dependents[node]:
            if child not in reachable:
                reachable.add(child)
                queue.append(child)
    for node in sorted(set(graph) - reachable):
        errors.append(
            f"quest {node.upper()} ({source_by_id[node].relative_to(QUEST_ROOT)}) is unreachable from the book roots"
        )

    previous_market: str | None = None

    for level in range(1, LEVEL_COUNT + 1):
        path = QUEST_ROOT / "chapters" / f"level_{level}.snbt"
        if not path.exists():
            errors.append(f"missing Level {level} chapter")
            continue
        content = path.read_text(encoding="utf-8")
        if "&" in content:
            errors.append(f"Level {level} contains literal '&'; FTB Quests interprets it as formatting")

        level_ids = {quest_id for quest_id, source in source_by_id.items() if source == path}
        level_blocks = {quest_id: blocks_by_id[quest_id] for quest_id in level_ids}

        if level == 1:
            promotion_candidates = [qid for qid in level_ids if qid == "74402ecaffafaec4"]
        else:
            promotion_candidates = [
                qid for qid, block in level_blocks.items()
                if re.search(rf'\bstage:\s*"level_{level}"', block)
            ]
        if len(promotion_candidates) != 1:
            errors.append(f"Level {level} has {len(promotion_candidates)} promotion milestones; expected exactly one")
            continue
        promotion = promotion_candidates[0]

        market_candidates = [
            qid for qid, block in level_blocks.items()
            if re.search(rf'\btitle:\s*"Level {level} Market Order"', block)
        ]
        if len(market_candidates) != 1:
            errors.append(f"Level {level} has {len(market_candidates)} Market Orders; expected exactly one")
            continue
        market = market_candidates[0]

        if level >= 2:
            if previous_market is None or graph[promotion] != {previous_market}:
                errors.append(
                    f"Level {level} promotion must depend only on Level {level - 1} Market Order; "
                    f"found {[value.upper() for value in sorted(graph[promotion])]}"
                )
            promotion_block = level_blocks[promotion]
            if "autoclaim: 1b" not in promotion_block:
                errors.append(f"Level {level} promotion must auto-claim its stage")
            expected_decree = f'\\"ids\\":[\\"level_{level}\\"]'
            if expected_decree not in promotion_block:
                errors.append(f"Level {level} promotion does not reward the matching level_{level} decree")

        market_block = level_blocks[market]
        if not graph[market]:
            errors.append(f"Level {level} Market Order has no production dependency")
        if promotion in graph[market]:
            errors.append(f"Level {level} Market Order depends directly on promotion instead of production")
        if market_block.count("consume_items: true") < 2:
            errors.append(f"Level {level} Market Order must consume at least two production outputs")

        level_dependents: dict[str, set[str]] = {qid: set() for qid in level_ids}
        for qid in level_ids:
            for dependency in graph[qid]:
                if dependency in level_dependents:
                    level_dependents[dependency].add(qid)

        mastery_ids = {
            qid for qid, block in level_blocks.items()
            if "Mastery" in title_for(block)
        }
        legal_terminals = {market} | mastery_ids
        for qid in sorted(level_ids):
            if not level_dependents[qid] and qid not in legal_terminals:
                errors.append(
                    f"Level {level} disconnected terminal {qid.upper()} ({title_for(level_blocks[qid])}); "
                    "connect it to the Market Order or an explicit Mastery node"
                )

        for qid, block in level_blocks.items():
            if qid in legal_terminals:
                continue
            optional = "Optional" in block
            if optional:
                if not mastery_ids or not any(reaches(qid, mastery, level_dependents, level_ids) for mastery in mastery_ids):
                    errors.append(
                        f"Level {level} optional quest {qid.upper()} ({title_for(block)}) must reconnect through Mastery"
                    )
            elif not reaches(qid, market, level_dependents, level_ids):
                errors.append(
                    f"Level {level} core quest {qid.upper()} ({title_for(block)}) does not feed the Market Order"
                )

        direct_branches = level_dependents[promotion]
        if level >= 6 and len(direct_branches) > 3:
            errors.append(
                f"Level {level} promotion opens {len(direct_branches)} direct branches; cap is 3. "
                "Sequence related products/processors downstream instead of unlocking them all at once"
            )
        if level >= 2 and len(direct_branches) < 1:
            errors.append(f"Level {level} promotion opens no progression branch")

        previous_market = market

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(
        "Quest graph OK: 23-level spine is reachable and acyclic; every core quest reaches its Market Order, "
        "optional branches reconnect through Mastery, and promotions avoid unlock dumps."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
