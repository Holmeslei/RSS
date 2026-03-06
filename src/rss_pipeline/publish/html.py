from __future__ import annotations

from pathlib import Path


def write_html(report_dir: Path, items: list[dict]) -> Path:
    report_dir.mkdir(parents=True, exist_ok=True)
    rows = "\n".join(
        f"<tr><td>{i+1}</td><td>{it.get('title','')}</td><td>{it.get('venue','')}</td><td>{it.get('score','')}</td></tr>"
        for i, it in enumerate(items)
    )
    html = f"""<!doctype html>
<html><head><meta charset='utf-8'><title>Recommendation Report</title></head>
<body><h1>Daily Recommendation Report</h1>
<table border='1' cellpadding='6'>
<tr><th>#</th><th>Title</th><th>Venue</th><th>Score</th></tr>
{rows}
</table></body></html>"""
    out = report_dir / "index.html"
    out.write_text(html, encoding="utf-8")
    return out
