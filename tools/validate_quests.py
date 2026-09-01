from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEST_ROOT = ROOT / "config" / "ftbquests" / "quests"


def main() -> int:
    ids: dict[str, Path] = {}
    dependencies: list[tuple[str, Path]] = []
    errors: list[str] = []

    for path in QUEST_ROOT.rglob("*.snbt"):
        content = path.read_text(encoding="utf-8")
        for raw_id in re.findall(r'\bid:\s*"([0-9A-Fa-f]{16})"', content):
            quest_id = raw_id.lower()
            if quest_id in ids:
                errors.append(f"duplicate ID {raw_id} in {path} (first in {ids[quest_id]})")
            else:
                ids[quest_id] = path
        for block in re.findall(r"dependencies:\s*\[([^\]]*)\]", content, re.DOTALL):
            dependencies.extend((dep, path) for dep in re.findall(r'"([0-9A-Fa-f]{16})"', block))

    for dependency, path in dependencies:
        if dependency.lower() not in ids:
            errors.append(f"dangling dependency {dependency} in {path}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"Quest graph OK: {len(ids)} unique IDs and {len(dependencies)} valid dependencies.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
