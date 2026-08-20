from __future__ import annotations

from pathlib import Path
import hashlib
import json
import mimetypes

TEXT_EXTENSIONS = {".txt", ".md", ".csv", ".log", ".json", ".yml", ".yaml", ".py", ".ini", ".cfg"}

def is_text_file(path: Path) -> bool:
    if path.suffix.lower() in TEXT_EXTENSIONS:
        return True
    mime, _ = mimetypes.guess_type(str(path))
    return bool(mime and mime.startswith("text/"))

def read_text_safely(path: Path, max_bytes: int) -> str:
    data = path.read_bytes()[:max_bytes]
    return data.decode("utf-8", errors="replace")

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()

def json_dumps(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2, default=str)
