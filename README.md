# Personal Academic Recommender RSS Pipeline

这是一个“基于 Zotero + ChatGPT 项目聊天记录”的**个人学术兴趣画像与每日文献推荐**流程设计。

目标：每天在 GitHub Actions 自动运行，抓取候选论文、完成去重与打分，并发布 RSS/HTML 报告。

## 功能总览

1. **Zotero 同步（增量）**
   - 通过 Zotero Web API 拉取文库条目。
   - 使用 `since` 或本地 `last_modified_version` 做增量更新。
   - 将条目标准化后写入本地缓存（JSON/SQLite）。

2. **ChatGPT 项目聊天同步（增量）**
   - 获取指定项目的最新聊天内容。
   - 提取与研究兴趣相关的关键词、主题、研究问题。
   - 写入“兴趣信号池”（可按天分片存储）。

3. **兴趣画像构建**
   - 对 Zotero 条目与聊天内容进行向量化。
   - 统计高频作者、高频期刊、近期上升主题。
   - 维护热门期刊列表（带时间窗口）。

4. **候选抓取**
   - 基础源：Crossref、arXiv。
   - 可选源：bioRxiv / medRxiv。
   - 针对热门期刊额外做精准抓取（ISSN / 期刊名）。

5. **去重与打分**
   - DOI / arXiv ID / 标题归一化去重。
   - 综合打分：
     - 语义相似度（与兴趣画像）
     - 时间衰减（越新权重越高）
     - 引用或 Altmetric 信号（可选）
     - SJR 期刊指标
     - 白名单加分（作者、期刊、关键词）

6. **输出发布**
   - 生成 `reports/feed.xml`（RSS 订阅）。
   - 生成 `reports/index.html`（可读报告）。
   - 用 GitHub Pages 发布。
   - 可选：把高分论文推送回 Zotero。

---

## 推荐目录结构

```text
.
├─ README.md
├─ config/
│  ├─ sources.yaml            # 数据源配置
│  ├─ scoring.yaml            # 打分权重配置
│  └─ whitelist.yaml          # 白名单配置
├─ data/
│  ├─ raw/                    # 原始抓取数据
│  ├─ cache/                  # 增量状态（since/version）
│  └─ profile/                # 画像快照
├─ reports/
│  ├─ feed.xml
│  └─ index.html
├─ src/
│  ├─ ingest/
│  │  ├─ zotero.py
│  │  ├─ chatgpt_project.py
│  │  └─ sources.py
│  ├─ profile/
│  │  ├─ normalize.py
│  │  ├─ embedding.py
│  │  └─ trend.py
│  ├─ rank/
│  │  ├─ dedup.py
│  │  ├─ score.py
│  │  └─ features.py
│  ├─ output/
│  │  ├─ rss.py
│  │  └─ html.py
│  └─ main.py
└─ .github/
   └─ workflows/
      └─ daily.yml
```

---

## 数据模型（建议）

### 1) 统一论文对象 `PaperRecord`

- `id`: 内部唯一 ID
- `source`: `crossref|arxiv|biorxiv|medrxiv|zotero`
- `doi`, `arxiv_id`
- `title`, `abstract`
- `authors[]`, `journal`, `issn`
- `published_at`, `updated_at`
- `url`, `pdf_url`
- `citations`, `altmetric`
- `sjr_score`
- `embedding`

### 2) 兴趣画像对象 `InterestProfile`

- `updated_at`
- `top_keywords[]`
- `top_authors[]`
- `top_journals[]`
- `recent_hot_journals[]`
- `centroid_embedding`

### 3) 排名结果对象 `RankedItem`

- `paper_id`
- `final_score`
- `score_breakdown`
  - `semantic`
  - `freshness`
  - `impact`
  - `journal_quality`
  - `whitelist_bonus`

---

## 关键流程（每日）

1. 读取本地增量游标（Zotero version、聊天 last_id、各源时间戳）。
2. 拉取并标准化新数据。
3. 更新兴趣画像（增量向量化 + 统计）。
4. 抓取候选文献（基础源 + 热门期刊精准源）。
5. 去重与过滤（语言、时间窗、主题阈值）。
6. 执行多因子打分并排序。
7. 生成 RSS/HTML 报告。
8. 提交 `reports/` 到仓库并由 Pages 发布。

---

## GitHub Actions（每日调度）

建议：
- `cron: '15 22 * * *'`（UTC，每天一次）
- 支持 `workflow_dispatch` 手动触发
- 缓存 `data/cache` 以减少 API 调用

需要的 Secrets（按你实际 API 调整）：
- `ZOTERO_USER_ID`
- `ZOTERO_API_KEY`
- `OPENAI_API_KEY`（如使用 embedding/LLM）
- `CHATGPT_PROJECT_TOKEN`（如有可用接口）
- `ALTMETRIC_API_KEY`（可选）

---

## 打分公式示例

可从线性加权开始：

```text
score =
  0.45 * semantic_similarity
+ 0.20 * freshness_decay
+ 0.15 * impact_signal
+ 0.10 * sjr_normalized
+ 0.10 * whitelist_bonus
```

并加入硬过滤：
- 低于语义阈值（如 `<0.55`）直接丢弃。
- 已在 Zotero 库中存在且近期无重大更新则降权或过滤。

---

## 实施优先级（MVP -> 增强）

### MVP（1-2 周）
- Zotero 增量同步
- Crossref + arXiv 候选抓取
- 基础向量检索与去重
- RSS 输出 + GitHub Actions 自动发布

### 增强（第 2 阶段）
- 聊天记录同步并纳入画像
- 引入 SJR / Altmetric 特征
- 热门期刊精准抓取
- HTML 报告可视化（主题趋势、来源分布）

### 进阶（第 3 阶段）
- 主动学习（收藏/点击反馈回流）
- 推送回 Zotero Collection
- 多画像模式（不同研究主题 Profile）

---

## 风险与注意事项

- **API 可用性与配额**：对每个数据源做好限频、重试和退避。
- **聊天数据隐私**：仅保留必要字段，敏感文本可做摘要或脱敏。
- **向量模型一致性**：统一模型版本，避免历史向量不可比。
- **可解释性**：在报告中展示 `score_breakdown`，便于人工审阅。

---

## 下一步建议

如果你愿意，我可以下一步直接为这个仓库补齐：
1. 可运行的 `src/` 骨架；
2. 一份 `daily.yml` 工作流模板；
3. `feed.xml`/`index.html` 生成脚手架；
4. 可配置的 `scoring.yaml` 示例。
