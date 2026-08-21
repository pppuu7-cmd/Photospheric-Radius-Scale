"""Persistent, atomic checkpoint handling for RTK self-hosted jobs."""

from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path

from .config import STATE_ROOT

SCHEMA_VERSION = 2


def safe_run_key(run_key: str) -> str:
    key = re.sub(r"[^A-Za-z0-9_.-]+", "_", run_key).strip("._")
    return key or "run"


def run_dir(run_key: str) -> Path:
    return STATE_ROOT / safe_run_key(run_key)


def checkpoint_path(run_key: str) -> Path:
    return run_dir(run_key) / "checkpoint.json"


def _atomic_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + f".tmp.{os.getpid()}")
    with tmp.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp, path)


def reset_checkpoint(run_key: str) -> Path | None:
    path = checkpoint_path(run_key)
    if not path.exists():
        return None
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    archived = path.with_name(f"checkpoint.reset-{stamp}.json")
    path.replace(archived)
    return archived


def save_checkpoint(
    run_key: str,
    next_index: int,
    total_tasks: int,
    fingerprint: str,
    metadata: dict | None = None,
) -> Path:
    """Save the *next* task index, so resume never repeats the last committed item."""
    payload = {
        "schema_version": SCHEMA_VERSION,
        "run_key": safe_run_key(run_key),
        "next_index": int(next_index),
        "completed": int(next_index),
        "total_tasks": int(total_tasks),
        "fingerprint": str(fingerprint),
        "updated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "metadata": metadata or {},
    }
    path = checkpoint_path(run_key)
    _atomic_json(path, payload)
    return path


def load_checkpoint(
    run_key: str,
    total_tasks: int,
    fingerprint: str,
    reset: bool = False,
) -> int:
    """Return the next task index after strict compatibility checks."""
    if reset:
        reset_checkpoint(run_key)
        return 0

    path = checkpoint_path(run_key)
    if not path.exists():
        return 0

    with path.open(encoding="utf-8") as handle:
        state = json.load(handle)

    if state.get("schema_version") != SCHEMA_VERSION:
        raise RuntimeError(
            f"Checkpoint schema mismatch at {path}; reset explicitly before reuse"
        )
    if state.get("fingerprint") != fingerprint:
        raise RuntimeError(
            f"Checkpoint fingerprint mismatch at {path}; refusing unsafe resume"
        )
    if int(state.get("total_tasks", -1)) != int(total_tasks):
        raise RuntimeError(
            f"Checkpoint total_tasks mismatch at {path}; refusing unsafe resume"
        )

    next_index = int(state.get("next_index", 0))
    if not 0 <= next_index <= total_tasks:
        raise RuntimeError(f"Invalid next_index={next_index} in {path}")
    return next_index
