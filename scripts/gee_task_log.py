#!/usr/bin/env python3
"""Append Google Earth Engine task records to CSV and JSONL ledgers."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("G:/GEE")
TASK_DIR = ROOT / "tasks"
CSV_PATH = TASK_DIR / "tasks.csv"
JSONL_PATH = TASK_DIR / "tasks.jsonl"
FIELDS = [
    "created_at",
    "alias",
    "project_id",
    "task_id",
    "description",
    "dataset",
    "aoi",
    "date_range",
    "drive_folder",
    "output_prefix",
    "status",
    "notes",
]


def append_record(record: dict) -> None:
    TASK_DIR.mkdir(parents=True, exist_ok=True)
    exists = CSV_PATH.exists()
    with CSV_PATH.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        if not exists:
            writer.writeheader()
        writer.writerow({field: record.get(field, "") for field in FIELDS})
    with JSONL_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--alias", required=True)
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--task-id", default="")
    parser.add_argument("--description", required=True)
    parser.add_argument("--dataset", default="")
    parser.add_argument("--aoi", default="")
    parser.add_argument("--date-range", default="")
    parser.add_argument("--drive-folder", default="")
    parser.add_argument("--output-prefix", default="")
    parser.add_argument("--status", default="planned")
    parser.add_argument("--notes", default="")
    args = parser.parse_args()

    record = vars(args)
    record["project_id"] = record.pop("project_id")
    record["date_range"] = record.pop("date_range")
    record["drive_folder"] = record.pop("drive_folder")
    record["output_prefix"] = record.pop("output_prefix")
    record["task_id"] = record.pop("task_id")
    record["created_at"] = datetime.now(timezone.utc).isoformat()
    append_record(record)
    print(json.dumps(record, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
