from __future__ import annotations

import re
import sys

from validate_quests import ID_RE, QUEST_ROOT, extract_quest_blocks

DESCRIPTION_RE = re.compile(r"description:\s*\[(.*?)\]", re.DOTALL)
STRING_RE = re.compile(r'"((?:\\.|[^"\\])*)"')


def main() -> int:
    errors: list[str] = []
    checked = 0

    for path in QUEST_ROOT.rglob("*.snbt"):
        content = path.read_text(encoding="utf-8")
        for block in extract_quest_blocks(content):
            checked += 1
            id_match = ID_RE.search(block)
            quest_id = id_match.group(1).upper() if id_match else "UNKNOWN"
            description = DESCRIPTION_RE.search(block)
            lines = STRING_RE.findall(description.group(1)) if description else []
            if not any(line.strip() for line in lines):
                errors.append(
                    f"quest {quest_id} in {path.relative_to(QUEST_ROOT)} has no non-empty description"
                )

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"Quest descriptions OK: {checked} quests all have non-empty descriptions.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
