from __future__ import annotations


def fetch_crossref(hot_journals: list[str]) -> list[dict]:
    venue = hot_journals[0] if hot_journals else "Nature"
    return [
        {
            "id": "doi:10.1000/sample1",
            "title": "Semantic recommender systems for literature triage",
            "authors": ["Smith, A."],
            "venue": venue,
            "year": 2026,
            "abstract": "A crossref-like sample candidate.",
            "doi": "10.1000/sample1",
            "source": "crossref",
            "citation_count": 10,
            "sjr": 4.0,
        }
    ]
