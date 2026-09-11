# GEE Workflow Guide

This document explains a local Google Earth Engine setup for future Codex chats and projects. Treat it as the canonical guide for using the `$gee` skill, then adapt paths and project aliases to the user's machine.

## Current State

The Codex skill is installed at:

```text
D:\.Codex\skills\gee
```

The default working root for Google Earth Engine jobs is:

```text
G:\GEE
```

After authentication, verify one authorized project with `gee_check.py`. A successful check prints a server response like:

```text
server: hello from earth engine
```

Do not ask the user to authenticate every time. Re-authenticate only when Earth Engine reports credential errors such as `Please authorize access`, `invalid_grant`, expired credentials, revoked credentials, or a Google account change.

## Project Aliases

Use this local config file for project aliases:

```text
G:\GEE\config\projects.local.json
```

Example aliases:

```text
default     -> your-earth-engine-project-id
research-a  -> another-authorized-project-id
research-b  -> third-authorized-project-id
```

Real project IDs are personal local configuration. Do not commit `projects.local.json`; commit only `projects.example.json`.

Useful commands:

```powershell
python "D:\.Codex\skills\gee\scripts\gee_project.py" list
python "D:\.Codex\skills\gee\scripts\gee_project.py" resolve default
python "D:\.Codex\skills\gee\scripts\gee_project.py" add alias-name project-id
python "D:\.Codex\skills\gee\scripts\gee_project.py" set-default alias-name
```

## Authentication

Normal use does not require repeated authorization.

If credentials fail, run:

```powershell
python "D:\.Codex\skills\gee\scripts\gee_auth.py" --force
```

Then verify a project:

```powershell
python "D:\.Codex\skills\gee\scripts\gee_check.py" --project default
```

The `earthengine.exe` command may not be on PATH, so prefer `gee_auth.py` and Python scripts over direct `earthengine authenticate` unless PATH has been fixed.

## Workspace Layout

Use this layout under `G:\GEE`:

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

For a new work item, create or use:

```text
G:\GEE\outputs\<alias>\<YYYYMMDD>_<task-slug>
```

Keep generated scripts, parameter files, AOI copies, small result tables, logs, and notes in that task folder.

## Drive Export Convention

The first supported cloud export target is Google Drive.

Use project-aware Drive folders:

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

Do not assume that exporting to Drive automatically downloads files to `G:\GEE`. Automatic Drive-to-local sync is intentionally not part of the first setup. If needed later, add a separate Drive API or rclone workflow.

## Task Ledger

Every planned or submitted batch task should be logged to:

```text
G:\GEE\tasks\tasks.csv
G:\GEE\tasks\tasks.jsonl
```

Use:

```powershell
python "D:\.Codex\skills\gee\scripts\gee_task_log.py" --alias default --project-id your-earth-engine-project-id --description "task description"
```

Recommended fields to include when known:

```text
alias
project_id
task_id
description
dataset
aoi
date_range
drive_folder
output_prefix
status
notes
```

For long-running jobs, record task IDs and tell the user they can later ask:

```text
$gee 检查任务状态
```

or run:

```powershell
python "D:\.Codex\skills\gee\scripts\gee_tasks.py" --project default
```

## Risk Gates

Ask the user before:

- submitting 50 or more export tasks;
- overwriting local files;
- deleting local files;
- deleting Earth Engine assets;
- making irreversible cloud changes;
- switching from Drive export to Google Cloud Storage or another billed service;
- using project switching as a quota-bypass strategy.

Project switching is allowed for authorized project organization and explicit user choice. Do not frame it as a way to evade Google or Earth Engine quota limits.

## AOI Handling

Accept these AOI forms:

- GeoJSON file;
- Shapefile folder or `.zip`;
- bounding box coordinates;
- Earth Engine Asset ID;
- user-described region, when a reliable boundary source can be identified.

Default decision:

- Small one-off AOI: use local geometry directly.
- Large or frequently reused AOI: suggest uploading or referencing a GEE Asset.
- Ambiguous place names: ask for confirmation or use an authoritative boundary source.

Keep a copy of local AOI input in the task folder when possible.

## Dataset Selection

If the user names a dataset, use it.

If the user asks which dataset to use, search the official Earth Engine Data Catalog first:

```text
https://developers.google.com/earth-engine/datasets
```

Return candidate datasets with:

- dataset ID;
- provider;
- temporal coverage;
- spatial resolution;
- key bands;
- update frequency if relevant;
- known limitations;
- fit for the user's analysis.

Let the user choose before submitting a large workflow.

## Common Invocation Patterns

Use default project:

```text
$gee 下载 2020-2024 年黄河流域 Sentinel-2 NDVI 月均值，导出到 Drive
```

Use explicit alias:

```text
$gee 用 default 下载 2020-2024 年 Sentinel-2 NDVI，导出到 Google Drive
```

Find dataset first:

```text
$gee 我想做降雨趋势分析，先帮我查 GEE 里适合的数据集，再让我选
```

Check tasks:

```text
$gee 检查 default 的 Earth Engine 任务状态
```

Add a new project alias:

```text
$gee 把 newproj 这个别名绑定到 my-project-id-123
```

## What Another Chat Should Do First

When another Codex chat needs to continue GEE work:

1. Load `$gee`.
2. Read this file.
3. Run:

```powershell
python "D:\.Codex\skills\gee\scripts\gee_project.py" list
```

4. If the task needs live GEE access, run:

```powershell
python "D:\.Codex\skills\gee\scripts\gee_check.py" --project default
```

5. If credentials fail, ask the user to run:

```powershell
python "D:\.Codex\skills\gee\scripts\gee_auth.py" --force
```

6. Continue with the user's requested dataset, AOI, date range, export target, and task logging.

## Official References

Use official Google documentation when checking behavior:

- Earth Engine authentication and initialization: https://developers.google.com/earth-engine/guides/auth
- Earth Engine Python installation: https://developers.google.com/earth-engine/guides/python_install
- Earth Engine Data Catalog: https://developers.google.com/earth-engine/datasets
