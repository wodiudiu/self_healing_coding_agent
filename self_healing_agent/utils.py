from __future__ import annotations

import re
import subprocess
from pathlib import Path
from datetime import datetime


def clean_code_block(text: str) -> str:
    """Remove Markdown code fences if the model returns them."""
    text = text.strip()
    match = re.search(r"```(?:python)?\s*(.*?)```", text, flags=re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return text


def timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def ensure_dir(path: str | Path) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def run_python_file(file_path: str | Path, timeout: int = 15) -> tuple[int, str, str]:
    """Run a Python file and return returncode, stdout, stderr."""
    result = subprocess.run(
        ["python", str(file_path)],
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr
