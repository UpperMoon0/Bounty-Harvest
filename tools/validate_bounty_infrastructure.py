from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOUNTIFUL = ROOT / "kubejs" / "server_scripts" / "bountiful_data.js"

FORBIDDEN_REPEATABLE_INFRASTRUCTURE = (
    "createaddition:electric_motor",
    "createaddition:alternator",
    "createaddition:accumulator",
    "alexscaves:cave_tablet",
    "twilightforest:magic_map",
)


def main() -> int:
    bounty = BOUNTIFUL.read_text(encoding="utf-8")
    leaked = [item for item in FORBIDDEN_REPEATABLE_INFRASTRUCTURE if item in bounty]
    if leaked:
        for item in leaked:
            print(f"ERROR: repeatable Bountiful pool contains retained infrastructure {item}")
        return 1

    print("Repeatable Bountiful pools contain renewable/market goods, not retained infrastructure.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
