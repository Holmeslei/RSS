from __future__ import annotations

from collections import Counter
from pathlib import Path

from rss_pipeline.io_utils import read_jsonl, write_json


def _tokenize(text: str) -> list[str]:
    cleaned = "".join(c.lower() if c.isalnum() else " " for c in text)
    return [t for t in cleaned.split() if len(t) > 2]


def build_profile(data_dir: Path) -> dict:
    zotero = read_jsonl(data_dir / "raw" / "zotero_items.jsonl")
    chats = read_jsonl(data_dir / "raw" / "chat_items.jsonl")

    author_counter = Counter()
    journal_counter = Counter()
    token_counter = Counter()

    for item in zotero:
        author_counter.update(item.get("authors", []))
        venue = item.get("venue")
        if venue:
            journal_counter[venue] += 1
        token_counter.update(_tokenize(f"{item.get('title', '')} {item.get('abstract', '')}"))

    for msg in chats:
        token_counter.update(_tokenize(msg.get("content", "")))

    profile = {
        "top_authors": [{"name": k, "count": v} for k, v in author_counter.most_common(20)],
        "top_journals": [{"name": k, "count": v} for k, v in journal_counter.most_common(20)],
        "hot_journals": [k for k, _ in journal_counter.most_common(10)],
        "top_keywords": [{"term": k, "count": v} for k, v in token_counter.most_common(30)],
    }

    write_json(data_dir / "profile" / "top_authors.json", profile["top_authors"])
    write_json(data_dir / "profile" / "top_journals.json", profile["top_journals"])
    write_json(data_dir / "profile" / "hot_journals.json", profile["hot_journals"])
    write_json(data_dir / "profile" / "keywords.json", profile["top_keywords"])

    return profile
