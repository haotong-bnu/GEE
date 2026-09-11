#!/usr/bin/env python3
"""Check Earth Engine Python API authentication and initialization."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path("G:/GEE")
CONFIG = ROOT / "config" / "projects.local.json"


def load_project(alias_or_id: str | None) -> tuple[str, str]:
    if not CONFIG.exists():
        if alias_or_id:
            return alias_or_id, alias_or_id
        raise SystemExit(f"Missing config: {CONFIG}")
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    projects = config.get("projects", {})
    alias = alias_or_id or config.get("default")
    if not alias:
        raise SystemExit("No project alias supplied and no default set.")
    if alias in projects:
        return alias, projects[alias]
    if alias in projects.values():
        matched_alias = next(k for k, v in projects.items() if v == alias)
        return matched_alias, alias
    return alias, alias


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", help="Project alias or project ID. Defaults to configured default.")
    parser.add_argument("--install-hint", action="store_true", help="Print install/auth commands on failure.")
    args = parser.parse_args()

    try:
        import ee  # type: ignore
    except Exception as exc:
        print(f"earthengine-api import failed: {exc}")
        if args.install_hint:
            print("Install: python -m pip install --upgrade earthengine-api")
            print("Authenticate: earthengine authenticate")
        return 2

    alias, project_id = load_project(args.project)
    print(f"alias: {alias}")
    print(f"project_id: {project_id}")
    print(f"ee_version: {getattr(ee, '__version__', 'unknown')}")

    try:
        ee.Initialize(project=project_id)
        value = ee.String("hello from earth engine").getInfo()
        print(f"server: {value}")
        return 0
    except Exception as exc:
        print(f"ee.Initialize failed: {exc}")
        if args.install_hint:
            print("Try: earthengine authenticate")
            print(f"Then retry: python {Path(__file__).name} --project {alias}")
            try:
                result = subprocess.run(["earthengine", "--help"], check=False, capture_output=True, text=True)
                print(f"earthengine_cli_exit: {result.returncode}")
            except Exception as cli_exc:
                print(f"earthengine CLI check failed: {cli_exc}")
        return 3


if __name__ == "__main__":
    sys.exit(main())
