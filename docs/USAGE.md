# RSS Pipeline 使用指南

本文档介绍如何在本地运行、配置、调试并同步到 GitHub。

## 1. 环境准备

- Python 3.11+
- Git
- （可选）GitHub CLI `gh`

建议先创建虚拟环境：

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .
```

> 如果你的环境不能联网，`pip install -e .` 可能失败。该项目目前仅依赖标准库，直接用 `PYTHONPATH=src` 也可运行。

## 2. 配置文件

复制示例配置并按需修改：

```bash
cp configs/config.example.json configs/config.local.json
```

关键配置项：

- `run.top_k`：输出推荐条目数量。
- `sources.*`：开关不同抓取源。
- `weights.*`：多因子打分权重。
- `whitelist_journals`：白名单期刊加分。

## 3. 本地运行

### 3.1 使用可执行命令（安装成功后）

```bash
rss-pipeline --config configs/config.local.json
```

### 3.2 不安装直接运行（推荐在受限环境）

```bash
PYTHONPATH=src python -m rss_pipeline.main --config configs/config.local.json
```

### 3.3 全量模式

```bash
PYTHONPATH=src python -m rss_pipeline.main --config configs/config.local.json --full
```

## 4. 输出目录说明

运行后将生成：

- `data/raw/`：同步后的原始条目（zotero/chat）。
- `data/profile/`：画像统计结果（关键词、作者、期刊）。
- `data/output/recommendations.jsonl`：最终推荐列表（含打分拆解）。
- `reports/feed.xml`：RSS 订阅文件。
- `reports/index.html`：HTML 报告页面。

## 5. GitHub Actions 每日运行

工作流文件：`.github/workflows/daily.yml`。

- 每日 UTC `02:15` 自动运行。
- 支持手动触发 `workflow_dispatch`。
- 产物目录 `reports/` 会部署到 GitHub Pages。

首次启用建议检查：

1. 仓库 `Settings -> Pages` 是否允许 GitHub Actions 部署。
2. 仓库 `Actions` 是否启用。
3. 若后续接入真实 API，需在 `Settings -> Secrets and variables -> Actions` 中配置对应密钥。

## 6. 同步到 GitHub

当前仓库若未绑定远程，先添加：

```bash
git remote add origin <your-repo-url>
```

提交并推送：

```bash
git add .
git commit -m "docs: add usage guide and github sync instructions"
git push -u origin <branch-name>
```

如果你使用 GitHub CLI，也可以创建 PR：

```bash
gh pr create --fill
```

## 7. 常见问题

### Q1: `pip install -e .` 失败，提示无法访问依赖源？
使用免安装方式运行：

```bash
PYTHONPATH=src python -m rss_pipeline.main --config configs/config.local.json
```

### Q2: 为什么默认数据看起来像样例？
当前是可跑通骨架版本，`sync` 和 `fetchers` 模块使用样例数据模拟，便于先验证流程。

### Q3: 如何切换成真实 API？
按模块替换：

- Zotero：`src/rss_pipeline/sync/zotero_sync.py`
- Chat：`src/rss_pipeline/sync/chat_sync.py`
- 数据源抓取：`src/rss_pipeline/fetchers/*.py`

并保留现有 I/O 与编排接口，即可无缝接入。
