#!/usr/bin/env python3
"""Authenticate Google Earth Engine for the current Windows user."""

from __future__ import annotations

import argparse
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="Force refresh credentials.")
    parser.add_argument("--auth-mode", default=None, help="Optional ee.Authenticate auth_mode.")
    args = parser.parse_args()

    try:
        import ee  # type: ignore
    except Exception as exc:
        print(f"earthengine-api import failed: {exc}")
        print("Install: python -m pip install --upgrade earthengine-api")
        return 2

    kwargs = {"force": args.force}
    if args.auth_mode:
        kwargs["auth_mode"] = args.auth_mode

    print("Starting Earth Engine authentication. Follow the browser or URL instructions.")
    ee.Authenticate(**kwargs)
    print("Authentication finished. Run gee_check.py with a project alias to verify initialization.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
