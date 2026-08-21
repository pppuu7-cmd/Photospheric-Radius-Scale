"""Heartbeat monitor for a running self-hosted RTK job."""

from __future__ import annotations

import json
import time

from .checkpoint import run_dir
from .config import MONITOR_INTERVAL_SECONDS, RUN_KEY

TERMINAL = {"complete", "error", "interrupted"}


def monitor(interval: float = MONITOR_INTERVAL_SECONDS) -> None:
    progress_path = run_dir(RUN_KEY) / "progress.json"
    print(f"[RTK MONITOR] run={RUN_KEY} path={progress_path}", flush=True)
    while True:
        if progress_path.exists():
            try:
                state = json.loads(progress_path.read_text(encoding="utf-8"))
                eta = state.get("eta_seconds")
                eta_text = "unknown" if eta is None else f"{float(eta)/60:.1f}min"
                print(
                    "[RTK MONITOR] "
                    f"{state.get('percent', 0):.2f}% "
                    f"{state.get('done', 0)}/{state.get('total', 0)} "
                    f"workers={state.get('workers')} "
                    f"rate={state.get('session_rate_tasks_per_second', 0):.3f}/s "
                    f"ETA={eta_text} status={state.get('status')}",
                    flush=True,
                )
                if state.get("status") in TERMINAL:
                    return
            except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
                print(f"[RTK MONITOR] transient read error: {exc}", flush=True)
        else:
            print("[RTK MONITOR] waiting for first progress snapshot", flush=True)
        time.sleep(max(1.0, interval))


if __name__ == "__main__":
    monitor()
