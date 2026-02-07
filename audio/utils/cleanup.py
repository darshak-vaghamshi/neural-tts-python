import os
import time
from pathlib import Path
from typing import Iterable

def cleanup_files(files: list):
    for f in files:
        if os.path.exists(f):
            try:
                os.remove(f)
            except:
                pass


def cleanup_matching_files(directory: str | Path, candidates: Iterable[str], keep: Iterable[str] = ()) -> None:
    """Remove files within *directory* listed in *candidates* except those in *keep*."""
    base_path = Path(directory)
    if not base_path.exists():
        return

    keep_names = {Path(name).name for name in keep}
    for candidate in candidates:
        candidate_name = Path(candidate).name
        if candidate_name in keep_names:
            continue
        file_path = base_path / candidate_name
        if file_path.exists():
            try:
                file_path.unlink()
            except Exception:
                pass


def cleanup_old_files(root: str | Path, ttl_seconds: int) -> None:
    """Delete files older than *ttl_seconds* under *root* recursively."""
    base_path = Path(root)
    if not base_path.exists():
        return

    now = time.time()
    for dirpath, _, filenames in os.walk(base_path):
        for name in filenames:
            file_path = Path(dirpath) / name
            try:
                if now - file_path.stat().st_mtime > ttl_seconds:
                    file_path.unlink()
            except Exception:
                continue