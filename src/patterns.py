from __future__ import annotations

import re
from dataclasses import dataclass

@dataclass(frozen=True)
class PatternRule:
    name: str
    regex: re.Pattern
    risk_weight: int

def _compile(pattern: str) -> re.Pattern:
    return re.compile(pattern, re.IGNORECASE | re.MULTILINE)

EMAIL = PatternRule(
    name="email",
    regex=_compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"),
    risk_weight=10,
)

SSN = PatternRule(
    name="ssn",
    regex=_compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    risk_weight=35,
)

CREDIT_CARD_VISA = PatternRule(
    name="credit_card_visa",
    regex=_compile(r"\b4[0-9]{12}(?:[0-9]{3})?\b"),
    risk_weight=45,
)

CREDIT_CARD_MASTERCARD = PatternRule(
    name="credit_card_mastercard",
    regex=_compile(r"\b5[1-5][0-9]{14}\b"),
    risk_weight=45,
)

DNI_AR = PatternRule(
    name="dni_ar",
    regex=_compile(r"\b(?:\d{1,2}\.\d{3}\.\d{3}|\d{7,8})\b"),
    risk_weight=30,
)

IBAN = PatternRule(
    name="iban",
    regex=_compile(r"\b[A-Z]{2}\d{2}(?:[A-Z0-9]{1,30})\b"),
    risk_weight=40,
)

PHONE = PatternRule(
    name="phone",
    regex=_compile(r"\b(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{2,4}\)?[-.\s]?){2,4}\d{2,4}\b"),
    risk_weight=15,
)

DEFAULT_PATTERNS = {
    r.name: r for r in [
        EMAIL,
        SSN,
        CREDIT_CARD_VISA,
        CREDIT_CARD_MASTERCARD,
        DNI_AR,
        IBAN,
        PHONE,
    ]
}
