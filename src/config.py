from __future__ import annotations

from pathlib import Path
from pydantic import BaseModel, Field


class ScanConfig(BaseModel):
    min_risk_threshold: int = Field(default=30, ge=0, le=1000)
    max_file_size_mb: int = Field(default=10, ge=1, le=1024)
    include_hidden: bool = False
    recursive: bool = True
    redact_matches: bool = False
    enable_nlp: bool = True
    output_format: str = Field(default="json", pattern="^(json|html|csv)$")
    patterns_to_enable: list[str] = Field(default_factory=list)


class AppConfig(BaseModel):
    scan: ScanConfig = Field(default_factory=ScanConfig)

    @classmethod
    def from_yaml(cls, path: str | Path) -> "AppConfig":
        import yaml
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
        return cls.model_validate(data)
