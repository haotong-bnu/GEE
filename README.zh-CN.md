# GEE

[English README](README.md)

GEE 是一个面向 Google Earth Engine 的 Codex skill，用来把常见的 GEE 工作流固定下来：项目切换、Python API 检查、Google Drive 导出、批量任务记录、输出目录整理，以及跨聊天复用。

它适合经常用 Earth Engine 下载和处理遥感、气候、地理数据的人：不用每次重新想项目 ID、授权、导出命名、任务记录和文件夹结构。

## 能做什么

- 用别名切换已授权的 Earth Engine / Google Cloud Project。
- 用指定 project 初始化 Earth Engine Python API。
- 把栅格或表格结果导出到 Google Drive。
- 用 CSV 和 JSONL 同时记录计划任务和已提交任务。
- 按固定目录整理脚本、参数、AOI、日志和输出文件。
- 支持 GeoJSON、Shapefile、bbox、Earth Engine Asset ID、地名等 AOI 输入。
- 在用户没指定数据集时，优先检索官方 Earth Engine Data Catalog，再给候选数据集。
- 在大批量提交、覆盖、删除、不可逆云端操作前先确认。

## 为什么需要它

GEE 工作流出问题，往往不是算法本身，而是这些细节：

- 用错了 Google Cloud Project；
- 授权过期但没有及时发现；
- 批量导出后没有任务账本；
- Drive 文件夹和文件名混乱；
- AOI、脚本、日志和结果散落在不同地方；
- 一次性提交太多任务，事后不好追踪。

这个 skill 的作用是给 Codex 一套稳定的本地工作方式，让不同聊天、不同项目里都能按同一套规则处理 GEE 任务。

## 仓库结构

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

## 环境要求

- 已启用本地 skills 的 Codex。
- Python 3.10 或更新版本。
- 有 Earth Engine 权限的 Google 账号。
- 至少一个已经注册 Earth Engine 的 Google Cloud Project。
- `earthengine-api` Python 包。

安装或升级 Earth Engine Python API：

```powershell
python -m pip install --upgrade earthengine-api
```

## 安装

把这个文件夹复制到你的 Codex skills 目录。

Windows 示例：

```text
D:\.Codex\skills\gee
```

然后在 Codex 里调用：

```text
$gee 检查 Earth Engine 环境
```

## 配置 Project

复制示例配置：

```text
config\projects.example.json
```

到你的本地 GEE 工作目录：

```text
G:\GEE\config\projects.local.json
```

示例：

```json
{
  "default": "default",
  "projects": {
    "default": "your-earth-engine-project-id",
    "research-a": "another-authorized-project-id"
  }
}
```

不要把 `projects.local.json` 提交到 GitHub。它里面是真实 Project ID。

常用命令：

```powershell
python "D:\.Codex\skills\gee\scripts\gee_project.py" list
python "D:\.Codex\skills\gee\scripts\gee_project.py" resolve default
python "D:\.Codex\skills\gee\scripts\gee_project.py" add research-a your-project-id
python "D:\.Codex\skills\gee\scripts\gee_project.py" set-default research-a
```

## 授权

首次授权：

```powershell
python "D:\.Codex\skills\gee\scripts\gee_auth.py" --force
```

验证：

```powershell
python "D:\.Codex\skills\gee\scripts\gee_check.py" --project default
```

成功时会看到类似输出：

```text
server: hello from earth engine
```

不需要每次都授权。只有在 Earth Engine 报凭据过期、凭据无效、账号切换或权限撤销时，才需要重新授权。

## 常见用法

使用默认 project：

```text
$gee 下载 2020-2024 年黄河流域 Sentinel-2 NDVI 月均值，导出到 Google Drive
```

指定 project 别名：

```text
$gee 用 research-a 导出我的 AOI 的 Landsat LST
```

先找数据集：

```text
$gee 我想做降雨趋势分析，先查 GEE 官方数据目录，给我几个候选数据集再让我选
```

检查任务状态：

```text
$gee 检查 default 的 Earth Engine 任务状态
```

## 工作目录约定

默认本地工作目录：

```text
G:\GEE
```

推荐结构：

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

每个任务建议放在：

```text
G:\GEE\outputs\<alias>\<YYYYMMDD>_<task-slug>
```

里面保存生成脚本、参数文件、AOI 副本、日志和小型结果表。

## Google Drive 导出规则

默认导出到 Google Drive。

Drive 文件夹按 project 别名组织：

```text
GEE_<alias>
```

文件名前缀按任务组织：

```text
<YYYYMMDD>_<task-slug>_<dataset>_<date-range>_<index-or-band>
```

示例：

```text
Drive folder: GEE_default
File prefix: 20260911_yellowriver_s2_ndvi_2020_2024_monthly
```

注意：导出到 Drive 不等于自动下载到本地。后续如果需要自动同步，可以再接 Google Drive API 或 rclone。

## 任务账本

每个计划任务或已提交任务都建议记录到：

```text
G:\GEE\tasks\tasks.csv
G:\GEE\tasks\tasks.jsonl
```

添加一条记录：

```powershell
python "D:\.Codex\skills\gee\scripts\gee_task_log.py" --alias default --project-id your-earth-engine-project-id --description "monthly NDVI export"
```

查看 Earth Engine 任务：

```powershell
python "D:\.Codex\skills\gee\scripts\gee_tasks.py" --project default
```

## 安全边界

以下情况必须先问用户：

- 一次提交 50 个或更多导出任务；
- 覆盖本地文件；
- 删除本地文件；
- 删除 Earth Engine assets；
- 执行不可逆云端操作；
- 切换到可能计费的导出目标，例如 Google Cloud Storage；
- 把 project 切换包装成绕过额度限制的方案。

Project 切换只能用于已授权项目的组织和明确选择，不能用于规避 Google 或 Earth Engine 的额度规则。

## 开源注意事项

仓库应该包含：

- `config/projects.example.json`
- `.gitignore`
- 可复用脚本
- skill 指令
- 使用说明

仓库不应该包含：

- `projects.local.json`
- 真实 Google Cloud Project ID
- Earth Engine 凭据
- 任务账本
- 导出的数据
- 本地输出文件

## License

本项目采用 MIT License 开源。
