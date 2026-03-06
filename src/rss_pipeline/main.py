from __future__ import annotations

import argparse
from pathlib import Path

import json

from rss_pipeline.fetchers.arxiv import fetch_arxiv
from rss_pipeline.fetchers.crossref import fetch_crossref
from rss_pipeline.fetchers.preprint import fetch_biorxiv, fetch_medrxiv
from rss_pipeline.io_utils import write_jsonl
from rss_pipeline.profile.build_profile import build_profile
from rss_pipeline.publish.html import write_html
from rss_pipeline.publish.rss import write_rss
from rss_pipeline.rank.dedup import dedup_candidates
from rss_pipeline.rank.scorer import score_candidates
from rss_pipeline.sync.chat_sync import sync_chat
from rss_pipeline.sync.zotero_sync import sync_zotero


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run recommendation pipeline")
    p.add_argument("--config", default="configs/config.example.json")
    p.add_argument("--data-dir", default="data")
    p.add_argument("--report-dir", default="reports")
    p.add_argument("--full", action="store_true")
    return p.parse_args()


def load_config(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    data_dir = Path(args.data_dir)
    report_dir = Path(args.report_dir)

    sync_zotero(data_dir, full=args.full)
    sync_chat(data_dir, full=args.full)
    profile = build_profile(data_dir)

    hot_journals = profile.get("hot_journals", [])
    candidates = []
    if config.get("sources", {}).get("crossref", True):
        candidates.extend(fetch_crossref(hot_journals))
    if config.get("sources", {}).get("arxiv", True):
        candidates.extend(fetch_arxiv())
    if config.get("sources", {}).get("biorxiv", False):
        candidates.extend(fetch_biorxiv())
    if config.get("sources", {}).get("medrxiv", False):
        candidates.extend(fetch_medrxiv())

    deduped = dedup_candidates(candidates)
    scored = score_candidates(deduped, profile, config)
    top_k = int(config.get("run", {}).get("top_k", 20))
    final = scored[:top_k]

    write_jsonl(data_dir / "output" / "recommendations.jsonl", final)
    write_rss(report_dir, final)
    write_html(report_dir, final)


if __name__ == "__main__":
    main()
