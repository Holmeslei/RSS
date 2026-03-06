from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path


def write_rss(report_dir: Path, items: list[dict]) -> Path:
    report_dir.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
    item_xml = []
    for it in items:
        link = it.get("url") or (f"https://doi.org/{it['doi']}" if it.get("doi") else "https://example.org")
        item_xml.append(
            f"<item><title>{it.get('title','')}</title><link>{link}</link><description>score={it.get('score')}</description></item>"
        )

    xml = (
        "<?xml version='1.0' encoding='UTF-8'?>"
        "<rss version='2.0'><channel>"
        "<title>Personal Literature Recommendations</title>"
        f"<lastBuildDate>{now}</lastBuildDate>"
        + "".join(item_xml)
        + "</channel></rss>"
    )
    out = report_dir / "feed.xml"
    out.write_text(xml, encoding="utf-8")
    return out
