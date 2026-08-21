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
REQUESTED_CHUNKSIZE = os.getenv("RTK_CHUNKSIZE", "auto").strip().lower()
TASK_MODULE = os.getenv("RTK_TASK_MODULE", "rtk_engine.worker").strip()
RESET_CHECKPOINT = os.getenv("RTK_RESET_CHECKPOINT", "false").lower() in {
    "1", "true", "yes", "on"
}


def resolve_workers(cpu_count: int | None = None) -> int:
    """Resolve outer process count from logical CPUs visible to WSL/Linux.

    `RTK_WORKERS=auto` with `RTK_RESERVE_CPUS=0` uses every logical processor.
    The currently observed RTK-HOME-PC is a 10-core / 12-logical-processor
    i5-1235U, so max-throughput mode resolves to 12 worker processes when WSL
    exposes all processors. Use a reserve only when interactive responsiveness
    matters more than throughput.
    """
    cpus = max(1, cpu_count or (os.cpu_count() or 1))
    available = max(1, cpus - min(RESERVE_CPUS, cpus - 1))
    if REQUESTED_WORKERS == "auto":
        return available
    requested = max(1, int(REQUESTED_WORKERS))
    return min(requested, available)


def resolve_chunksize(remaining_tasks: int, workers: int) -> int:
    """Choose IPC batching without changing scientific task identity.

    Very small `calculate(index)` calls are dominated by multiprocessing queue
    traffic when chunksize=1. In auto mode we aim for roughly 16 dispatch
    chunks per worker and cap a chunk at 1024 items. Heavy scientific tasks
    naturally resolve to chunksize=1 because there are relatively few of them.

    Completed items inside an in-flight chunk may be recomputed after a hard
    interruption; correctness is preserved because checkpointing advances only
    over the contiguous ordered prefix already returned to the parent process.
    """
    remaining = max(0, int(remaining_tasks))
    workers = max(1, int(workers))
    if REQUESTED_CHUNKSIZE != "auto":
        return max(1, int(REQUESTED_CHUNKSIZE))
    if remaining <= workers * 16:
        return 1
    target_chunks = workers * 16
    return max(1, min(1024, (remaining + target_chunks - 1) // target_chunks))
