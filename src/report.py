from __future__ import annotations

from pathlib import Path
import csv
from .utils import json_dumps

class ReportWriter:
    @staticmethod
    def to_json(report) -> str:
        return json_dumps(report.__dict__)

    @staticmethod
    def to_html(report) -> str:
        rows = "".join(f"<tr><td>{f['path']}</td><td>{f['file_risk_score']}</td><td>{f['match_count']}</td><td>{f['entity_count']}</td></tr>" for f in report.files)
        breakdown = "".join(f"<li>{k}: {v}</li>" for k, v in report.breakdown.items())
        return f"""
        <html><head><meta charset="utf-8"><title>DocShield Report</title></head>
        <body>
        <h1>DocShield.ai Report</h1>
        <p>Severity: {report.severity}</p>
        <p>Risk Score: {report.risk_score}</p>
        <p>Total Files: {report.total_files}</p>
        <table border="1"><thead><tr><th>Path</th><th>Risk</th><th>Matches</th><th>Entities</th></tr></thead><tbody>{rows}</tbody></table>
        <h2>Breakdown</h2><ul>{breakdown}</ul>
        </body></html>
        """

    @staticmethod
    def to_csv(report, path: str | Path) -> Path:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["path", "sha256", "size_bytes", "match_count", "entity_count", "file_risk_score"])
            writer.writeheader()
            writer.writerows(report.files)
        return p
