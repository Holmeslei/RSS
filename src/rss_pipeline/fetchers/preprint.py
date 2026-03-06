from __future__ import annotations


def fetch_biorxiv() -> list[dict]:
    return [
        {
            "id": "biorxiv:sample-1",
            "title": "BioRxiv candidate on biomedical recommendation",
            "authors": ["Ng, C."],
            "venue": "bioRxiv",
            "year": 2026,
            "abstract": "A biorxiv-like sample candidate.",
            "doi": "",
            "source": "biorxiv",
            "citation_count": 1,
            "sjr": 0.0,
        }
    ]


def fetch_medrxiv() -> list[dict]:
    return [
        {
            "id": "medrxiv:sample-1",
            "title": "medRxiv candidate on clinical literature ranking",
            "authors": ["Wang, D."],
            "venue": "medRxiv",
            "year": 2026,
            "abstract": "A medrxiv-like sample candidate.",
            "doi": "",
            "source": "medrxiv",
            "citation_count": 1,
            "sjr": 0.0,
        }
    ]
