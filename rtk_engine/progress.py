"""Persistent progress reporting for GitHub logs and the Ubuntu runner console."""

from __future__ import annotations

import json
import os
import subprocess
import time
from pathlib import Path

from .config import STATE_ROOT
from .checkpoint import run_dir


def _atomic_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + f".tmp.{os.getpid()}")
    with tmp.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp, path)


def _append(path: Path, line: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(line.rstrip() + "\n")
        handle.flush()


def _eta_text(seconds: float | None) -> str:
    if seconds is None or seconds < 0:
        return "unknown"
    seconds = int(seconds)
    hours, rem = divmod(seconds, 3600)
    minutes, secs = divmod(rem, 60)
    if hours:
        return f"{hours}h{minutes:02d}m"
    if minutes:
        return f"{minutes}m{secs:02d}s"
    return f"{secs}s"


def emit_event(run_key: str, message: str, notify_wall: bool = False) -> str:
    stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    line = f"[{stamp}] [RTK:{run_key}] {message}"
    print(line, flush=True)
    _append(run_dir(run_key) / "live.log", line)
    _append(STATE_ROOT / "live.log", line)
    if notify_wall:
        try:
            subprocess.run(
                ["wall", f"RTK {run_key}: {message}"],
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=3,
            )
        except (FileNotFoundError, subprocess.SubprocessError):
            pass
    return line


def write_progress(
    *,
    run_key: str,
    done: int,
    total: int,
    session_start_done: int,
    session_start_time: float,
    workers: int,
    status: str = "running",
) -> dict:
    elapsed = max(0.0, time.time() - session_start_time)
    session_done = max(0, done - session_start_done)
    rate = session_done / elapsed if elapsed > 0 else 0.0
    remaining = max(0, total - done)
    eta = remaining / rate if rate > 0 and remaining else (0.0 if remaining == 0 else None)
    percent = (100.0 * done / total) if total else 100.0

    payload = {
        "run_key": run_key,
        "status": status,
        "done": int(done),
        "total": int(total),
        "percent": percent,
        "workers": int(workers),
        "session_elapsed_seconds": elapsed,
        "session_rate_tasks_per_second": rate,
        "eta_seconds": eta,
        "updated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    _atomic_json(run_dir(run_key) / "progress.json", payload)

    line = (
        f"progress={percent:6.2f}% {done}/{total} "
        f"rate={rate:.3f}/s ETA={_eta_text(eta)} workers={workers} status={status}"
    )
    emit_event(run_key, line, notify_wall=False)
    return payload


# Backwards-compatible name used by early engine code.
def show_progress(done: int, total: int, start_time: float) -> None:
    elapsed = max(0.0, time.time() - start_time)
    rate = done / elapsed if elapsed else 0.0
    eta = (total - done) / rate if rate else None
    percent = 100.0 * done / total if total else 100.0
    print(
        f"[RTK] {percent:6.2f}% {done}/{total} rate={rate:.3f}/s ETA={_eta_text(eta)}",
        flush=True,
    )
