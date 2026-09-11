---
name: gee
description: Google Earth Engine workflow for switching authorized Cloud Projects by alias, running Earth Engine Python jobs, exporting to Google Drive, tracking batch tasks, and organizing outputs in a local GEE workspace. Use when the user mentions GEE, Google Earth Engine, Earth Engine datasets, AOI, NDVI, Landsat, Sentinel, MODIS, ERA5, Drive exports, batch export, or checking Earth Engine task status.
---

# GEE

Use this skill for Google Earth Engine work.

The user's settled preferences:

- Codex invocation name: `$gee`.
- Local workspace root: `G:\GEE` by default; adapt if the user configures another root.
- Project selection: use aliases from `G:\GEE\config\projects.local.json`; default alias is allowed.
- Do not design workflows to bypass Google or Earth Engine quota limits. Project switching is for authorized projects and clear organization only.
- Authentication: default to ordinary user authentication; leave room for service-account support later.
- Export target: Google Drive first. Do not assume automatic Drive-to-local download is configured yet.
- Task tracking: log every submitted or planned batch task to both CSV and JSONL under `G:\GEE\tasks`.
- Risk gates: ask before submitting 50 or more export tasks, overwriting local outputs, deleting files, deleting Earth Engine assets, or making irreversible cloud changes.
- AOI support: accept GeoJSON, Shapefile, bbox, Earth Engine Asset IDs, and user-described regions. Prefer local geometry for small temporary AOIs and Earth Engine Assets for large or reusable AOIs.
- Dataset selection: use the dataset the user names. If they ask what dataset to use, search the official Earth Engine Data Catalog first, summarize candidate dataset IDs with time range, spatial resolution, bands, limitations, and ask the user to choose.

## Workflow

If the user asks how this personal GEE setup works, how to switch projects, whether authorization is needed again, how batch exports are organized, or how another chat should continue the workflow, read [references/user-guide.md](references/user-guide.md) before answering.

1. Resolve the project alias with `scripts/gee_project.py list` or `scripts/gee_project.py resolve <alias>`.
2. Check the Python/GEE environment with `scripts/gee_check.py --project <alias-or-id>`.
3. For new work, create a task folder under the configured workspace, for example `G:\GEE\outputs\<alias>\<YYYYMMDD>_<task-slug>`, and log planned tasks before or immediately after submission.
4. Generate Earth Engine Python scripts that call `ee.Initialize(project="<project-id>")`.
5. For Drive exports, use project-aware Drive folder names. Prefer `GEE_<alias>` as the top-level folder and task-specific filename prefixes.
6. For short jobs, submit and poll status. For long jobs, record task IDs and tell the user to ask `$gee check tasks`.

## Scripts

- `scripts/gee_project.py`: manage project aliases in `G:\GEE\config\projects.local.json`.
- `scripts/gee_auth.py`: run user authentication without relying on `earthengine.exe` being on PATH.
- `scripts/gee_check.py`: check package installation, credentials, selected project initialization, and basic server response.
- `scripts/gee_task_log.py`: append task records to CSV and JSONL.
- `scripts/gee_tasks.py`: list current Earth Engine task status for a selected project.

## Required Local Config

The user-specific config is outside the skill folder:

```text
G:\GEE\config\projects.local.json
```

Keep real project IDs local. If this skill is later published, include only `projects.example.json` and ignore `projects.local.json`.

## Official References

When behavior may have changed, verify against official Google documentation:

- Earth Engine authentication and initialization: `https://developers.google.com/earth-engine/guides/auth`
- Earth Engine Python installation: `https://developers.google.com/earth-engine/guides/python_install`
- Earth Engine Data Catalog: `https://developers.google.com/earth-engine/datasets`
