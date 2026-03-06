from __future__ import annotations

from datetime import datetime


def _semantic_score(title: str, keywords: set[str]) -> float:
    words = {w.lower() for w in title.split()}
    if not words:
        return 0.0
    return len(words & keywords) / len(words)


def score_candidates(candidates: list[dict], profile: dict, config: dict) -> list[dict]:
    weights = config.get("weights", {})
    keywords = {k["term"] for k in profile.get("top_keywords", [])[:20]}
    white = set(config.get("whitelist_journals", []))
    now = datetime.now().year

    scored = []
    for c in candidates:
        semantic = _semantic_score(c.get("title", ""), keywords)
        recency = max(0.0, 1 - 0.2 * max(0, now - int(c.get("year", now))))
        citation = min(1.0, c.get("citation_count", 0) / 50)
        sjr = min(1.0, c.get("sjr", 0.0) / 5)
        whitelist = 1.0 if c.get("venue") in white else 0.0

        total = (
            weights.get("semantic", 0.55) * semantic
            + weights.get("recency", 0.2) * recency
            + weights.get("citation", 0.1) * citation
            + weights.get("sjr", 0.1) * sjr
            + weights.get("whitelist", 0.05) * whitelist
        )
        c2 = dict(c)
        c2["score"] = round(total, 4)
        c2["score_breakdown"] = {
            "semantic": round(semantic, 4),
            "recency": round(recency, 4),
            "citation": round(citation, 4),
            "sjr": round(sjr, 4),
            "whitelist": round(whitelist, 4),
        }
        scored.append(c2)

    return sorted(scored, key=lambda x: x["score"], reverse=True)
