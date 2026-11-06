#!/usr/bin/env python3
"""Run the two trusted-main pack validators and emit Jenkins-readable evidence.

No Minecraft server, publishing credentials, or local game data are needed.
Each failure remains visible in JUnit and causes a nonzero process exit.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "ci-evidence"
CHECKS = [
    ("quest-graph", ROOT / "tools" / "validate_quests.py"),
    ("pack-invariants", ROOT / "tools" / "validate_pack.py"),
]


def run() -> int:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    suite = ET.Element("testsuite", name="bounty-harvest-validation", tests=str(len(CHECKS)))
    results = []
    failures = 0

    for name, path in CHECKS:
        case = ET.SubElement(suite, "testcase", name=name, classname="BountyHarvest")
        try:
            completed = subprocess.run(
                [sys.executable, str(path)], cwd=ROOT, text=True,
                capture_output=True, timeout=120, check=False,
            )
            stdout, stderr, code = completed.stdout, completed.stderr, completed.returncode
        except subprocess.TimeoutExpired as exc:
            stdout = str(exc.stdout or "")
            stderr = str(exc.stderr or "") + "\nValidation timed out."
            code = 124

        print(f"[{name}] exit={code}", flush=True)
        if stdout:
            print(stdout, end="" if stdout.endswith("\n") else "\n", flush=True)
        if stderr:
            print(stderr, file=sys.stderr, flush=True)

        ET.SubElement(case, "system-out").text = stdout
        ET.SubElement(case, "system-err").text = stderr
        if code != 0:
            failures += 1
            ET.SubElement(case, "failure", message=f"Validation {name} exited {code}").text = stderr or stdout
        results.append({"name": name, "exit_code": code})

    suite.set("failures", str(failures))
    tree = ET.ElementTree(suite)
    tree.write(EVIDENCE / "validation-tests.xml", encoding="utf-8", xml_declaration=True)

    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True,
        capture_output=True, check=True,
    ).stdout.strip()
    (EVIDENCE / "validation-receipt.json").write_text(
        json.dumps(
            {
                "schema": 1,
                "commit": head,
                "checked_at": datetime.now(timezone.utc).isoformat(),
                "checks": results,
                "all_passed": failures == 0,
            },
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(run())
