from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class EntityMatch:
    label: str
    text: str
    start: int
    end: int
    source: str = "nlp"

class EntityDetector:
    def __init__(self, enable_nlp: bool = True):
        self.enable_nlp = enable_nlp
        self._nlp = None
        if enable_nlp:
            self._load()

    def _load(self):
        try:
            import spacy
            try:
                self._nlp = spacy.load("en_core_web_sm")
            except Exception:
                try:
                    self._nlp = spacy.load("es_core_news_sm")
                except Exception:
                    self._nlp = spacy.blank("en")
        except Exception:
            self._nlp = None

    def detect(self, text: str) -> list[EntityMatch]:
        if not self._nlp:
            return self._fallback(text)
        doc = self._nlp(text)
        allowed = {"PERSON", "ORG", "GPE", "DATE", "MONEY"}
        return [
            EntityMatch(label=ent.label_, text=ent.text, start=ent.start_char, end=ent.end_char)
            for ent in doc.ents
            if ent.label_ in allowed and ent.text.strip()
        ]

    def _fallback(self, text: str) -> list[EntityMatch]:
        import re
        results: list[EntityMatch] = []
        for m in re.finditer(r"\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)+\b", text):
            results.append(EntityMatch("PERSON", m.group(), m.start(), m.end(), source="fallback"))
        for m in re.finditer(r"\b(?:Argentina|Buenos Aires|Rosario|Córdoba|Madrid|Barcelona|Paris|London|New York)\b", text, re.I):
            results.append(EntityMatch("GPE", m.group(), m.start(), m.end(), source="fallback"))
        return results
