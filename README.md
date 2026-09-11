# GEE

`GEE` is a Codex skill for Google Earth Engine workflows.

It helps Codex:

- switch authorized Earth Engine / Google Cloud projects by alias;
- run Earth Engine Python API jobs;
- export results to Google Drive;
- track batch tasks in CSV and JSONL ledgers;
- organize outputs under a local workspace such as `G:\GEE`;
- handle AOIs from GeoJSON, Shapefile, bounding boxes, or Earth Engine Asset IDs;
- search the official Earth Engine Data Catalog before recommending datasets.

## Install

Copy this folder into your Codex skills directory:

```text
D:\.Codex\skills\gee
```

Then invoke it in Codex:

```text
$gee 检查 Earth Engine 环境
```

## Configure Projects

Copy the example config:

```text
config\projects.example.json
```

to your local workspace as:

```text
G:\GEE\config\projects.local.json
```

Do not commit `projects.local.json`; it contains your real project IDs.

## Authenticate

Install or upgrade the Earth Engine Python API:

```powershell
python -m pip install --upgrade earthengine-api
```

Authenticate:

```powershell
python "D:\.Codex\skills\gee\scripts\gee_auth.py" --force
```

Verify:

```powershell
python "D:\.Codex\skills\gee\scripts\gee_check.py" --project default
```

## Notes

Project switching is for authorized project organization, not quota evasion. The skill asks before submitting 50 or more export tasks, overwriting files, deleting files, deleting Earth Engine assets, or making irreversible cloud changes.
