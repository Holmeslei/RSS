from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from rss_pipeline.io_utils import read_json, read_jsonl, write_json, write_jsonl


def sync_chat(data_dir: Path, full: bool = False) -> list[dict]:
    state_path = data_dir / "state" / "chat_state.json"
    raw_path = data_dir / "raw" / "chat_items.jsonl"

    state = read_json(state_path, {"last_sync": None})
    existing = [] if full else read_jsonl(raw_path)

    now = datetime.now(timezone.utc).isoformat()
    sample = {
        "message_id": f"chat-{now}",
        "timestamp": now,
        "role": "user",
        "content": "Interested in retrieval augmented generation, scholarly recommender systems, and biomedical preprints.",
        "topics": ["RAG", "recommender", "biomedical"],
        "source": "chat",
    }

    merged = [sample] + [r for r in existing if r.get("message_id") != sample["message_id"]]
    write_jsonl(raw_path, merged)
    state["last_sync"] = now
    write_json(state_path, state)
    return merged
