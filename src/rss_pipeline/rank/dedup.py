from __future__ import annotations


def dedup_candidates(rows: list[dict]) -> list[dict]:
    seen = set()
    out = []
    for r in rows:
        key = r.get("doi") or r.get("id") or r.get("title", "").strip().lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(r)
    return out
