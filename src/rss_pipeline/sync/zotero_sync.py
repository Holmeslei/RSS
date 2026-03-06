from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from rss_pipeline.io_utils import read_json, read_jsonl, write_json, write_jsonl


def sync_zotero(data_dir: Path, full: bool = False) -> list[dict]:
    state_path = data_dir / "state" / "zotero_state.json"
    raw_path = data_dir / "raw" / "zotero_items.jsonl"

    state = read_json(state_path, {"last_sync": None})
    existing = [] if full else read_jsonl(raw_path)

    now = datetime.now(timezone.utc).isoformat()
    sample = {
        "id": f"zotero-{now}",
        "title": "Sample Zotero Paper",
        "authors": ["Doe, Jane"],
        "year": 2025,
        "venue": "Nature",
        "abstract": "A sample record produced by local pipeline check.",
        "tags": ["sample", "pipeline"],
        "url": "https://example.org/zotero-sample",
        "source": "zotero",
        "updated_at": now,
    }

    merged = [sample] + [r for r in existing if r.get("id") != sample["id"]]
    write_jsonl(raw_path, merged)
    state["last_sync"] = now
    write_json(state_path, state)
    return merged
