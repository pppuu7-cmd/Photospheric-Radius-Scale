"""Resumable process-level engine for one heavy RTK workload on a home node."""

from __future__ import annotations

import hashlib
import importlib
import inspect
import os
import signal
import time
from multiprocessing import Pool

from .checkpoint import load_checkpoint, run_dir, save_checkpoint
from .config import (
    CHECKPOINT_INTERVAL,
    PROGRESS_INTERVAL,
    RESET_CHECKPOINT,
    RUN_KEY,
    TASK_MODULE,
    TOTAL_TASKS,
    resolve_chunksize,
    resolve_workers,
)
from .progress import emit_event, write_progress

_STOP_REQUESTED = False


def _signal_handler(signum, _frame):
    global _STOP_REQUESTED
    _STOP_REQUESTED = True
    print(f"[RTK] graceful stop requested by signal {signum}", flush=True)


def _load_calculate():
    module = importlib.import_module(TASK_MODULE)
    calculate = getattr(module, "calculate", None)
    if not callable(calculate):
        raise RuntimeError(f"{TASK_MODULE}.calculate is not callable")
    return module, calculate


def _fingerprint(module) -> str:
    explicit = os.getenv("RTK_INPUT_FINGERPRINT", "").strip()
    if explicit:
        return explicit
    digest = hashlib.sha256()
    digest.update(f"task_module={TASK_MODULE}\ntotal={TOTAL_TASKS}\n".encode())
    path = inspect.getsourcefile(module)
    if path and os.path.exists(path):
        with open(path, "rb") as handle:
            digest.update(handle.read())
    else:
        digest.update(repr(module).encode())
    return digest.hexdigest()


def main() -> int:
    global _STOP_REQUESTED
    _STOP_REQUESTED = False
    signal.signal(signal.SIGTERM, _signal_handler)
    signal.signal(signal.SIGINT, _signal_handler)

    module, calculate = _load_calculate()
    fingerprint = _fingerprint(module)
    logical_cpus = max(1, os.cpu_count() or 1)
    workers = resolve_workers(logical_cpus)
    start_index = load_checkpoint(
        RUN_KEY,
        total_tasks=TOTAL_TASKS,
        fingerprint=fingerprint,
        reset=RESET_CHECKPOINT,
    )
    remaining = max(0, TOTAL_TASKS - start_index)
    chunksize = resolve_chunksize(remaining, workers)
    state = run_dir(RUN_KEY)
    state.mkdir(parents=True, exist_ok=True)

    metadata = {
        "workers": workers,
        "logical_cpus": logical_cpus,
        "chunksize": chunksize,
        "task_module": TASK_MODULE,
        "pid": os.getpid(),
        "fingerprint": fingerprint,
    }
    emit_event(
        RUN_KEY,
        f"START tasks={TOTAL_TASKS} resume={start_index} logical_cpus={logical_cpus} "
        f"workers={workers} chunksize={chunksize} task={TASK_MODULE} "
        f"checkpoint={state / 'checkpoint.json'}",
        notify_wall=True,
    )

    session_start = time.time()
    write_progress(
        run_key=RUN_KEY,
        done=start_index,
        total=TOTAL_TASKS,
        session_start_done=start_index,
        session_start_time=session_start,
        workers=workers,
        status="running",
    )

    if start_index >= TOTAL_TASKS:
        emit_event(RUN_KEY, "COMPLETE checkpoint already covers all tasks", notify_wall=True)
        write_progress(
            run_key=RUN_KEY,
            done=TOTAL_TASKS,
            total=TOTAL_TASKS,
            session_start_done=start_index,
            session_start_time=session_start,
            workers=workers,
            status="complete",
        )
        return 0

    next_index = start_index
    pool = Pool(processes=workers)
    try:
        iterator = pool.imap(
            calculate,
            range(start_index, TOTAL_TASKS),
            chunksize=chunksize,
        )
        for index, _result in enumerate(iterator, start=start_index):
            # Ordered imap means every task before next_index has completed successfully.
            next_index = index + 1

            if next_index % PROGRESS_INTERVAL == 0 or next_index == TOTAL_TASKS:
                write_progress(
                    run_key=RUN_KEY,
                    done=next_index,
                    total=TOTAL_TASKS,
                    session_start_done=start_index,
                    session_start_time=session_start,
                    workers=workers,
                    status="running",
                )

            if next_index % CHECKPOINT_INTERVAL == 0 or next_index == TOTAL_TASKS:
                path = save_checkpoint(
                    RUN_KEY,
                    next_index=next_index,
                    total_tasks=TOTAL_TASKS,
                    fingerprint=fingerprint,
                    metadata={**metadata, "status": "running"},
                )
                emit_event(
                    RUN_KEY,
                    f"CHECKPOINT next_index={next_index}/{TOTAL_TASKS} path={path}",
                    notify_wall=(next_index != TOTAL_TASKS),
                )

            if _STOP_REQUESTED:
                save_checkpoint(
                    RUN_KEY,
                    next_index=next_index,
                    total_tasks=TOTAL_TASKS,
                    fingerprint=fingerprint,
                    metadata={**metadata, "status": "interrupted"},
                )
                write_progress(
                    run_key=RUN_KEY,
                    done=next_index,
                    total=TOTAL_TASKS,
                    session_start_done=start_index,
                    session_start_time=session_start,
                    workers=workers,
                    status="interrupted",
                )
                emit_event(
                    RUN_KEY,
                    f"INTERRUPTED safely at next_index={next_index}; resume is available",
                    notify_wall=True,
                )
                pool.terminate()
                pool.join()
                return 130

        pool.close()
        pool.join()
        save_checkpoint(
            RUN_KEY,
            next_index=TOTAL_TASKS,
            total_tasks=TOTAL_TASKS,
            fingerprint=fingerprint,
            metadata={**metadata, "status": "complete"},
        )
        write_progress(
            run_key=RUN_KEY,
            done=TOTAL_TASKS,
            total=TOTAL_TASKS,
            session_start_done=start_index,
            session_start_time=session_start,
            workers=workers,
            status="complete",
        )
        emit_event(RUN_KEY, "COMPLETE all tasks committed", notify_wall=True)
        return 0

    except BaseException as exc:
        pool.terminate()
        pool.join()
        save_checkpoint(
            RUN_KEY,
            next_index=next_index,
            total_tasks=TOTAL_TASKS,
            fingerprint=fingerprint,
            metadata={**metadata, "status": "error", "error": repr(exc)},
        )
        write_progress(
            run_key=RUN_KEY,
            done=next_index,
            total=TOTAL_TASKS,
            session_start_done=start_index,
            session_start_time=session_start,
            workers=workers,
            status="error",
        )
        emit_event(
            RUN_KEY,
            f"ERROR at next_index={next_index}: {type(exc).__name__}: {exc}",
            notify_wall=True,
        )
        raise


if __name__ == "__main__":
    raise SystemExit(main())
