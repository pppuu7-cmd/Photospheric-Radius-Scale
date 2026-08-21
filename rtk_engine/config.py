"""Runtime configuration for the RTK self-hosted compute engine."""

from __future__ import annotations

import os
from pathlib import Path


def _env_int(name: str, default: int, minimum: int = 0) -> int:
    value = int(os.getenv(name, str(default)))
    if value < minimum:
        raise ValueError(f"{name} must be >= {minimum}, got {value}")
    return value


STATE_ROOT = Path(
    os.getenv("RTK_STATE_ROOT", str(Path.home() / ".rtk-runner-state"))
).expanduser()
RUN_KEY = os.getenv("RTK_RUN_KEY", "manual-heavy").strip() or "manual-heavy"
TOTAL_TASKS = _env_int("RTK_TOTAL_TASKS", 1_000_000, 0)
REQUESTED_WORKERS = os.getenv("RTK_WORKERS", "auto").strip().lower()
RESERVE_CPUS = _env_int("RTK_RESERVE_CPUS", 0, 0)
CHECKPOINT_INTERVAL = _env_int("RTK_CHECKPOINT_INTERVAL", 100, 1)
PROGRESS_INTERVAL = _env_int("RTK_PROGRESS_INTERVAL", 25, 1)
MONITOR_INTERVAL_SECONDS = float(os.getenv("RTK_MONITOR_INTERVAL_SECONDS", "30"))
CHUNKSIZE = _env_int("RTK_CHUNKSIZE", 1, 1)
TASK_MODULE = os.getenv("RTK_TASK_MODULE", "rtk_engine.worker").strip()
RESET_CHECKPOINT = os.getenv("RTK_RESET_CHECKPOINT", "false").lower() in {
    "1", "true", "yes", "on"
}


def resolve_workers(cpu_count: int | None = None) -> int:
    """Resolve process count while allowing either max-throughput or headroom mode.

    RTK_WORKERS=auto and RTK_RESERVE_CPUS=0 means use all logical CPUs.
    On the current 10-thread home node this resolves to 10 workers.
    Set RTK_RESERVE_CPUS=2 (or RTK_WORKERS=8) when desktop responsiveness matters.
    """
    cpus = max(1, cpu_count or (os.cpu_count() or 1))
    available = max(1, cpus - min(RESERVE_CPUS, cpus - 1))
    if REQUESTED_WORKERS == "auto":
        return available
    requested = max(1, int(REQUESTED_WORKERS))
    return min(requested, available)
