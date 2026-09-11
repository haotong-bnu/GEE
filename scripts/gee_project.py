#!/usr/bin/env python3
"""Manage local Google Earth Engine project aliases."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path("G:/GEE")
CONFIG = ROOT / "config" / "projects.local.json"


def load_config() -> dict:
    if not CONFIG.exists():
        raise SystemExit(f"Missing config: {CONFIG}")
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def save_config(config: dict) -> None:
    CONFIG.parent.mkdir(parents=True, exist_ok=True)
    CONFIG.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def resolve(config: dict, alias_or_id: str | None) -> tuple[str, str]:
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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="List configured aliases.")

    p_resolve = sub.add_parser("resolve", help="Resolve alias to project ID.")
    p_resolve.add_argument("alias", nargs="?")

    p_default = sub.add_parser("set-default", help="Set default alias.")
    p_default.add_argument("alias")

    p_add = sub.add_parser("add", help="Add or update a project alias.")
    p_add.add_argument("alias")
    p_add.add_argument("project_id")

    args = parser.parse_args()
    config = load_config()

    if args.cmd == "list":
        print(f"default: {config.get('default', '')}")
        for alias, project_id in sorted(config.get("projects", {}).items()):
            marker = "*" if alias == config.get("default") else " "
            print(f"{marker} {alias}: {project_id}")
        return

    if args.cmd == "resolve":
        alias, project_id = resolve(config, args.alias)
        print(json.dumps({"alias": alias, "project_id": project_id}, ensure_ascii=False))
        return

    if args.cmd == "set-default":
        if args.alias not in config.get("projects", {}):
            raise SystemExit(f"Unknown alias: {args.alias}")
        config["default"] = args.alias
        save_config(config)
        print(f"default: {args.alias}")
        return

    if args.cmd == "add":
        config.setdefault("projects", {})[args.alias] = args.project_id
        config.setdefault("default", args.alias)
        save_config(config)
        print(f"{args.alias}: {args.project_id}")


if __name__ == "__main__":
    main()
