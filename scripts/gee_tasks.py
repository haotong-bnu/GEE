#!/usr/bin/env python3
"""List Earth Engine task status for a configured project."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path("G:/GEE")
CONFIG = ROOT / "config" / "projects.local.json"


def load_project(alias_or_id: str | None) -> tuple[str, str]:
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    projects = config.get("projects", {})
    alias = alias_or_id or config.get("default")
    if alias in projects:
        return alias, projects[alias]
    if alias in projects.values():
        matched_alias = next(k for k, v in projects.items() if v == alias)
        return matched_alias, alias
    return alias, alias


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", help="Project alias or project ID.")
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()

    try:
        import ee  # type: ignore
    except Exception as exc:
        print(f"earthengine-api import failed: {exc}")
        return 2

    alias, project_id = load_project(args.project)
    ee.Initialize(project=project_id)
    tasks = ee.batch.Task.list()[: args.limit]
    print(f"alias: {alias}")
    print(f"project_id: {project_id}")
    for task in tasks:
        status = task.status()
        print(json.dumps(status, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
