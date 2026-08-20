from __future__ import annotations

from dataclasses import dataclass
from collections import Counter
from .scanner import FileScanResult

@dataclass(frozen=True)
class RiskReport:
    total_files: int
    total_matches: int
    risk_score: int
    severity: str
    breakdown: dict[str, int]
    files: list[dict]

class Classifier:
    def __init__(self):
        self.entity_weights = {
            "PERSON": 8,
            "ORG": 10,
            "GPE": 6,
            "DATE": 4,
            "MONEY": 12,
        }

    def score(self, results: list[FileScanResult]) -> RiskReport:
        total = 0
        breakdown = Counter()
        files_out = []
        for r in results:
            file_score = 0
            for m in r.matches:
                file_score += m.weight
                breakdown[m.label] += 1
            for e in r.entities:
                w = self.entity_weights.get(e.label, 2)
                file_score += w
                breakdown[e.label] += 1
            total += file_score
            files_out.append({
                "path": r.path,
                "sha256": r.sha256,
                "size_bytes": r.size_bytes,
                "match_count": len(r.matches),
                "entity_count": len(r.entities),
                "file_risk_score": file_score,
            })
        severity = "low" if total < 40 else "medium" if total < 100 else "high" if total < 200 else "critical"
        return RiskReport(
            total_files=len(results),
            total_matches=sum(len(r.matches) + len(r.entities) for r in results),
            risk_score=total,
            severity=severity,
            breakdown=dict(breakdown),
            files=files_out,
        )
