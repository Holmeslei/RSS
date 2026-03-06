# RSS

基于 Zotero + Chat 兴趣画像的学术推荐流水线（最小可运行版本）。

## 功能覆盖（当前实现）
- Zotero/Chat 增量同步（本地样例数据模拟）
- 画像构建：关键词、高频作者/期刊、热门期刊
- 候选抓取：Crossref、arXiv、bioRxiv/medRxiv（可开关）
- 去重与多因子打分（语义、时效、引用、SJR、白名单）
- 输出 `reports/feed.xml` 与 `reports/index.html`
- GitHub Actions 每日执行并发布到 GitHub Pages

## 本地运行
```bash
python -m pip install -e .
rss-pipeline --config configs/config.example.json
```

运行后会生成：
- `data/output/recommendations.jsonl`
- `reports/feed.xml`
- `reports/index.html`

## GitHub Actions
工作流文件：`.github/workflows/daily.yml`。
- 每天 UTC 02:15 自动运行
- 支持手动触发 `workflow_dispatch`

> 注意：当前仓库为“可跑通骨架”，真实 API 接入（Zotero、ChatGPT、Crossref等）可在对应模块中替换样例抓取逻辑。


## 使用指南
详细操作请见：`docs/USAGE.md`。
