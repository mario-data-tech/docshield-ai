from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable
from .patterns import DEFAULT_PATTERNS, PatternRule
from .entities import EntityDetector, EntityMatch
from .utils import is_text_file, read_text_safely, sha256_text

@dataclass
class Match:
    kind: str
    label: str
    text: str
    start: int
    end: int
    weight: int
    source: str

@dataclass
class FileScanResult:
    path: str
    sha256: str
    size_bytes: int
    matches: list[Match] = field(default_factory=list)
    entities: list[EntityMatch] = field(default_factory=list)

class Scanner:
    def __init__(self, patterns: dict[str, PatternRule] | None = None, enable_nlp: bool = True, max_file_size_mb: int = 10):
        self.patterns = patterns or DEFAULT_PATTERNS
        self.detector = EntityDetector(enable_nlp=enable_nlp)
        self.max_file_size_bytes = max_file_size_mb * 1024 * 1024

    def scan_path(self, path: str | Path) -> list[FileScanResult]:
        p = Path(path)
        results: list[FileScanResult] = []
        if p.is_file():
            results.extend(self.scan_file(p))
        else:
            for f in self._walk(p):
                results.extend(self.scan_file(f))
        return results

    def _walk(self, folder: Path) -> Iterable[Path]:
        for p in folder.rglob("*"):
            if p.is_file():
                yield p

    def scan_file(self, path: Path) -> list[FileScanResult]:
        if not path.exists() or not path.is_file():
            return []
        size_bytes = path.stat().st_size
        if size_bytes > self.max_file_size_bytes or not is_text_file(path):
            return []
        text = read_text_safely(path, self.max_file_size_bytes)
        matches: list[Match] = []
        for rule in self.patterns.values():
            for m in rule.regex.finditer(text):
                matches.append(Match(
                    kind="pattern",
                    label=rule.name,
                    text=m.group(0),
                    start=m.start(),
                    end=m.end(),
                    weight=rule.risk_weight,
                    source="regex",
                ))
        entities = self.detector.detect(text)
        return [FileScanResult(path=str(path), sha256=sha256_text(text), size_bytes=size_bytes, matches=matches, entities=entities)]
