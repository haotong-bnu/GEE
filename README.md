# GEE

[中文说明](README.zh-CN.md)

GEE is a Codex skill for practical Google Earth Engine work: project switching, Python API checks, Google Drive exports, batch task tracking, and repeatable workspace organization.

It is designed for researchers and analysts who use Earth Engine often enough to need a reliable workflow, but not enough to rebuild project setup, authentication checks, task logs, and export conventions every time.

## What It Does

- Switch between authorized Earth Engine / Google Cloud projects by alias.
- Initialize Earth Engine Python jobs with the selected project.
- Export raster and table results to Google Drive.
- Track planned and submitted batch jobs in CSV and JSONL ledgers.
- Organize generated scripts, logs, AOIs, and outputs under a local workspace such as `G:\GEE`.
- Support AOIs from GeoJSON, Shapefile, bounding boxes, Earth Engine Asset IDs, or named regions.
- Search the official Earth Engine Data Catalog before recommending datasets.
- Ask before high-risk actions such as large batch submissions, overwrites, deletions, and irreversible cloud changes.

## Why This Exists

Earth Engine workflows often fail for ordinary reasons:

- the wrong Cloud Project was used;
- credentials expired;
- export tasks were submitted without a record;
- Drive folders and file names became impossible to audit;
- AOIs, scripts, and output files were scattered across projects;
- a batch job was too large to submit casually.

This skill gives Codex a local operating pattern so it can behave consistently across chats and projects.

## Repository Layout

```text
.
|-- SKILL.md
|-- README.md
|-- README.zh-CN.md
|-- agents/
|   `-- openai.yaml
|-- config/
|   `-- projects.example.json
|-- references/
|   `-- user-guide.md
`-- scripts/
    |-- gee_auth.py
    |-- gee_check.py
    |-- gee_project.py
    |-- gee_task_log.py
    `-- gee_tasks.py
```

## Requirements

- Codex with local skills enabled.
- Python 3.10 or newer.
- A Google account with Earth Engine access.
- At least one Google Cloud Project registered for Earth Engine.
- `earthengine-api`.

Install or upgrade the Python API:

```powershell
python -m pip install --upgrade earthengine-api
```

## Installation

Copy this folder into your Codex skills directory.

Example on Windows:

```text
D:\.Codex\skills\gee
```

Then use it in Codex:

```text
$gee check my Earth Engine setup
```

or:

```text
$gee 检查 Earth Engine 环境
```

## Configure Projects

Copy the example config:

```text
config\projects.example.json
```

to your local GEE workspace:

```text
G:\GEE\config\projects.local.json
```

Example:

```json
{
  "default": "default",
  "projects": {
    "default": "your-earth-engine-project-id",
    "research-a": "another-authorized-project-id"
  }
}
```

Do not commit `projects.local.json`. It contains real project IDs.

Useful commands:

```powershell
python "D:\.Codex\skills\gee\scripts\gee_project.py" list
python "D:\.Codex\skills\gee\scripts\gee_project.py" resolve default
python "D:\.Codex\skills\gee\scripts\gee_project.py" add research-a your-project-id
python "D:\.Codex\skills\gee\scripts\gee_project.py" set-default research-a
```

## Authenticate

Authenticate once:

```powershell
python "D:\.Codex\skills\gee\scripts\gee_auth.py" --force
```

Then verify:

```powershell
python "D:\.Codex\skills\gee\scripts\gee_check.py" --project default
```

A successful check prints a server response:

```text
server: hello from earth engine
```

You do not need to authenticate every time. Re-authenticate only when Earth Engine reports expired, revoked, or invalid credentials.

## Typical Usage

Use the default project:

```text
$gee download monthly Sentinel-2 NDVI for the Yellow River Basin from 2020 to 2024 and export to Google Drive
```

Use a project alias:

```text
$gee use research-a to export Landsat LST for my AOI
```

Ask for dataset selection first:

```text
$gee I want to analyze rainfall trends. Search the Earth Engine Data Catalog and recommend candidate datasets before running anything.
```

Check current Earth Engine tasks:

```text
$gee check task status for default
```

## Workspace Convention

The default local workspace is:

```text
G:\GEE
```

Recommended layout:

```text
G:\GEE
  config\
    projects.local.json
    projects.example.json
  outputs\
    <alias>\
      <YYYYMMDD>_<task-slug>\
  tasks\
    tasks.csv
    tasks.jsonl
  downloads\
  tmp\
```

For each job, keep generated scripts, parameter files, AOIs, logs, and small result tables in:

```text
G:\GEE\outputs\<alias>\<YYYYMMDD>_<task-slug>
```

## Google Drive Exports

The default export target is Google Drive.

Use project-aware folders:

```text
GEE_<alias>
```

Use task-specific file prefixes:

```text
<YYYYMMDD>_<task-slug>_<dataset>_<date-range>_<index-or-band>
```

Example:

```text
Drive folder: GEE_default
File prefix: 20260911_yellowriver_s2_ndvi_2020_2024_monthly
```

Exporting to Drive does not automatically download files to your local disk. Add Google Drive API or rclone later if you need automatic Drive-to-local sync.

## Task Ledger

Every planned or submitted batch task should be logged to:

```text
G:\GEE\tasks\tasks.csv
G:\GEE\tasks\tasks.jsonl
```

Append a record:

```powershell
python "D:\.Codex\skills\gee\scripts\gee_task_log.py" --alias default --project-id your-earth-engine-project-id --description "monthly NDVI export"
```

List Earth Engine tasks:

```powershell
python "D:\.Codex\skills\gee\scripts\gee_tasks.py" --project default
```

## Safety Boundaries

The skill should ask before:

- submitting 50 or more export tasks;
- overwriting local files;
- deleting local files;
- deleting Earth Engine assets;
- making irreversible cloud changes;
- switching to a billed export target such as Google Cloud Storage;
- using project switching as a quota-bypass strategy.

Project switching is for authorized project organization and explicit user choice, not quota evasion.

## Publishing Notes

This repository intentionally includes:

- `config/projects.example.json`
- `.gitignore`
- reusable scripts
- skill instructions
- usage documentation

It intentionally excludes:

- `projects.local.json`
- real Google Cloud Project IDs
- Earth Engine credentials
- task ledgers
- exported data
- local output files

## License

No license has been selected yet. Add one before encouraging broad reuse.
