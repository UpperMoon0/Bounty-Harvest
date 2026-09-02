#!/usr/bin/env python3
"""Stream one CurseForge author-API upload through curl.

The helper deliberately emits exactly one JSON object on stdout so the PowerShell
publisher can consume it reliably. It uses curl rather than buffering a large
multipart body in PowerShell's web cmdlets.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any


def emit(payload: dict[str, Any], code: int) -> int:
    print(json.dumps(payload, separators=(",", ":")))
    return code


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--metadata", required=True)
    parser.add_argument("--file", required=True)
    args = parser.parse_args()

    token = os.environ.get("CURSEFORGE_API_TOKEN", "").strip()
    if not token:
        return emit({"ok": False, "error": "CURSEFORGE_API_TOKEN is required."}, 2)

    archive = Path(args.file)
    if not archive.is_file():
        return emit({"ok": False, "error": f"Missing upload file: {archive}"}, 2)

    try:
        metadata = json.loads(args.metadata)
    except json.JSONDecodeError as exc:
        return emit({"ok": False, "error": f"Invalid metadata JSON: {exc}"}, 2)

    is_child = "parentFileID" in metadata
    max_attempts = 4

    with tempfile.TemporaryDirectory(prefix="curseforge-upload-") as temp_dir:
        temp = Path(temp_dir)
        metadata_path = temp / "metadata.json"
        response_path = temp / "response.json"
        metadata_path.write_text(
            json.dumps(metadata, separators=(",", ":")), encoding="utf-8"
        )

        for attempt in range(1, max_attempts + 1):
            response_path.unlink(missing_ok=True)
            command = [
                "curl",
                "--silent",
                "--show-error",
                "--location",
                "--connect-timeout",
                "30",
                "--max-time",
                "900",
                "--output",
                str(response_path),
                "--write-out",
                "%{http_code}",
                "--request",
                "POST",
                "--header",
                f"X-Api-Token: {token}",
                "--form",
                f"metadata=<{metadata_path}",
                "--form",
                f"file=@{archive};type=application/zip",
                args.url,
            ]

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
            )
            status_text = result.stdout.strip()
            body = response_path.read_text(encoding="utf-8", errors="replace") if response_path.exists() else ""

            try:
                status = int(status_text)
            except ValueError:
                status = 0

            if result.returncode == 0 and 200 <= status < 300:
                try:
                    response = json.loads(body)
                except json.JSONDecodeError as exc:
                    return emit(
                        {
                            "ok": False,
                            "error": f"CurseForge returned invalid JSON: {exc}",
                            "http_status": status,
                        },
                        1,
                    )
                file_id = response.get("id")
                if not file_id:
                    return emit(
                        {
                            "ok": False,
                            "error": "CurseForge returned no file ID.",
                            "http_status": status,
                            "body": body,
                        },
                        1,
                    )
                return emit({"ok": True, "id": str(file_id)}, 0)

            transient_http = (
                status in {408, 425, 429}
                or 500 <= status <= 599
                or (is_child and status == 404)
            )
            transient_transport = result.returncode != 0
            if attempt < max_attempts and (transient_http or transient_transport):
                time.sleep(5 * attempt)
                continue

            error = result.stderr.strip() or body or "CurseForge upload failed."
            return emit(
                {
                    "ok": False,
                    "error": error,
                    "curl_exit": result.returncode,
                    "http_status": status,
                    "body": body,
                },
                1,
            )

    return emit({"ok": False, "error": "CurseForge upload exhausted retries."}, 1)


if __name__ == "__main__":
    raise SystemExit(main())
