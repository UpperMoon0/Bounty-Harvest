from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    pack = json.loads((ROOT / "pack" / "pack.json").read_text(encoding="utf-8"))
    instance = json.loads((ROOT / "minecraftinstance.json").read_text(encoding="utf-8"))
    stem = f"{pack['artifactName']}-{pack['version']}"
    client_path = ROOT / "dist" / f"{stem}.zip"
    server_path = ROOT / "dist" / f"{stem}-server.zip"
    errors: list[str] = []

    for path in (client_path, server_path):
        if not path.is_file():
            errors.append(f"missing archive {path}")
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1

    # Build expected enabled addon set from instance metadata
    enabled_addons = {
        (int(addon["addonID"]), int(addon["installedFile"]["id"]))
        for addon in instance["installedAddons"]
        if addon.get("isEnabled", True)
    }

    with zipfile.ZipFile(client_path) as archive:
        names = set(archive.namelist())
        for required in (
            "manifest.json",
            "modlist.html",
            "overrides/scripts/gen_item_stages.zs",
            "overrides/resourcepacks/gen_bh_bounties.zip",
            "overrides/config/ftbquests/quests/chapters/research.snbt",
        ):
            if required not in names:
                errors.append(f"client archive lacks {required}")
        if any(name.startswith("overrides/mods/") for name in names):
            errors.append("client archive embeds launcher-managed mods")
        manifest = json.loads(archive.read("manifest.json"))
        if manifest["minecraft"]["modLoaders"][0]["id"] != f"forge-{pack['forgeVersion']}":
            errors.append("client manifest has the wrong Forge version")
        actual = {(int(item["projectID"]), int(item["fileID"])) for item in manifest["files"]}
        if actual != enabled_addons:
            missing = sorted(enabled_addons - actual)
            extra = sorted(actual - enabled_addons)
            errors.append(
                "client manifest project/file pairs differ from enabled minecraftinstance.json addons; "
                f"missing={missing}, extra={extra}"
            )

    client_only = {int(value) for value in pack["clientOnlyProjectIds"]}
    expected_server_mods = {
        addon["installedFile"]["fileName"]
        for addon in instance["installedAddons"]
        if addon.get("isEnabled", True)
        and int(addon["addonID"]) not in client_only
        and addon["installedFile"]["fileName"].lower().endswith(".jar")
    }
    with zipfile.ZipFile(server_path) as archive:
        names = set(archive.namelist())
        coordinate = f"{pack['minecraftVersion']}-{pack['forgeVersion']}"
        for required in (
            f"forge-{coordinate}-installer.jar",
            "start-server.bat",
            "start-server.sh",
            "user_jvm_args.txt",
            "SERVER-README.md",
            "scripts/gen_item_stages.zs",
            "resourcepacks/gen_bh_bounties.zip",
            "config/ftbquests/quests/chapters/research.snbt",
        ):
            if required not in names:
                errors.append(f"server archive lacks {required}")
        forbidden_prefixes = ("kubejs/assets/", "kubejs/client_scripts/", "config/jei/")
        for prefix in forbidden_prefixes:
            if any(name.startswith(prefix) for name in names):
                errors.append(f"server archive contains client-only path {prefix}")
        actual_server_mods = {Path(name).name for name in names if name.startswith("mods/") and name.endswith(".jar")}
        if actual_server_mods != expected_server_mods:
            missing = sorted(expected_server_mods - actual_server_mods)
            extra = sorted(actual_server_mods - expected_server_mods)
            errors.append(f"server mod split mismatch; missing={missing}, extra={extra}")

        # Validate server launcher metadata against pack.json
        for launcher_name, launcher_content in (
            ("start-server.bat", archive.read("start-server.bat").decode("utf-8")),
            ("start-server.sh", archive.read("start-server.sh").decode("utf-8")),
        ):
            if pack["minecraftVersion"] not in launcher_content:
                errors.append(f"{launcher_name} does not reference minecraftVersion {pack['minecraftVersion']}")
            if pack["forgeVersion"] not in launcher_content:
                errors.append(f"{launcher_name} does not reference forgeVersion {pack['forgeVersion']}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"Archives OK: {client_path.name} and {server_path.name}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
