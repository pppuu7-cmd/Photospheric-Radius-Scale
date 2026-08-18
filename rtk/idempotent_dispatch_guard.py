#!/usr/bin/env python3
"""Crash-consistent exactly-once guard for state-driven heavy workflow dispatch.

A dispatch request is satisfied by an Actions-bot workflow_dispatch run of the
requested workflow/ref created at or after the request timestamp. Because RTK
heavy workers are state-driven, such a run is semantically equivalent to
issuing a second dispatch for the same request. Requiring the Actions bot actor
prevents a coincident user-initiated manual replay from consuming an autonomous
request. This closes the crash window where `gh workflow run` succeeded but
`dispatch_request.json` was not yet consumed.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REQUEST = ROOT / "research/state/dispatch_request.json"
DEFAULT_STATE = ROOT / "research/state/current.json"
REPO = os.environ.get("GITHUB_REPOSITORY", "pppuu7-cmd/Photospheric-Radius-Scale")
AUTOMATION_ACTOR = "github-actions[bot]"


def parse_utc(value: str) -> dt.datetime:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("dispatch request created_at is missing")
    value = value.strip()
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    out = dt.datetime.fromisoformat(value)
    if out.tzinfo is None:
        out = out.replace(tzinfo=dt.timezone.utc)
    return out.astimezone(dt.timezone.utc)


def run_created_at(run: dict) -> dt.datetime:
    return parse_utc(run["created_at"])


def actor_login(run: dict) -> str | None:
    actor = run.get("actor")
    return actor.get("login") if isinstance(actor, dict) else None


def satisfying_run(run: dict, request: dict) -> bool:
    try:
        requested_at = parse_utc(request["created_at"])
        created_at = run_created_at(run)
    except (KeyError, TypeError, ValueError):
        return False
    return (
        run.get("event") == "workflow_dispatch"
        and run.get("head_branch") == request.get("ref", "main")
        and actor_login(run) == AUTOMATION_ACTOR
        and created_at >= requested_at
    )


def select_existing_run(runs: list[dict], request: dict) -> dict | None:
    matches = [r for r in runs if satisfying_run(r, request)]
    if not matches:
        return None
    # The earliest qualifying automation run is the one most tightly
    # associated with the request and avoids preferring later replays.
    return min(matches, key=run_created_at)


def gh_json(endpoint: str) -> dict:
    env = os.environ.copy()
    token = env.get("GH_TOKEN") or env.get("GITHUB_TOKEN")
    if token:
        env["GH_TOKEN"] = token
    cp = subprocess.run(
        ["gh", "api", endpoint], text=True, capture_output=True, env=env
    )
    if cp.returncode:
        raise RuntimeError(cp.stderr.strip() or f"gh api failed: {endpoint}")
    return json.loads(cp.stdout)


def recent_runs(workflow: str) -> list[dict]:
    payload = gh_json(
        f"repos/{REPO}/actions/workflows/{workflow}/runs?per_page=30"
    )
    return list(payload.get("workflow_runs", []))


def find_existing(request: dict) -> dict | None:
    # Fail closed on malformed timestamps: silently dispatching would defeat
    # the crash-consistency guarantee.
    parse_utc(request["created_at"])
    return select_existing_run(recent_runs(request["workflow"]), request)


def issue_dispatch(request: dict) -> None:
    env = os.environ.copy()
    token = env.get("GH_TOKEN") or env.get("GITHUB_TOKEN")
    if token:
        env["GH_TOKEN"] = token
    cmd = [
        "gh", "workflow", "run", request["workflow"],
        "--repo", REPO, "--ref", request.get("ref", "main"),
    ]
    cp = subprocess.run(cmd, text=True, capture_output=True, env=env)
    if cp.returncode:
        raise RuntimeError(cp.stderr.strip() or "gh workflow run failed")


def wait_for_dispatched_run(request: dict, attempts: int = 15, delay: float = 2.0) -> dict | None:
    for _ in range(attempts):
        found = find_existing(request)
        if found is not None:
            return found
        time.sleep(delay)
    return None


def consume(request_path: Path, state_path: Path, run: dict, disposition: str) -> None:
    state = json.loads(state_path.read_text())
    dispatch = state.setdefault("dispatch", {})
    dispatch.update({
        "status": "submitted",
        "run_id": int(run["id"]),
        "html_url": run.get("html_url"),
        "idempotency_disposition": disposition,
        "idempotency_guard": "workflow_ref_created_at_actor_v2",
    })
    state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")
    request_path.unlink(missing_ok=True)


def main() -> int:
    request_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_REQUEST
    state_path = Path(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_STATE
    if not request_path.exists():
        print("RTK_IDEMPOTENT_DISPATCH_NO_REQUEST")
        return 0
    request = json.loads(request_path.read_text())
    for key in ("workflow", "created_at"):
        if not request.get(key):
            raise RuntimeError(f"dispatch request missing {key}")

    existing = find_existing(request)
    if existing is not None:
        consume(request_path, state_path, existing, "reused_existing_run")
        print("RTK_IDEMPOTENT_DISPATCH_REUSED", int(existing["id"]), request["workflow"])
        return 0

    issue_dispatch(request)
    created = wait_for_dispatched_run(request)
    if created is None:
        # Keep request intact. On the next orchestrator iteration the run should
        # be visible and will be consumed rather than duplicated.
        raise RuntimeError(
            "workflow dispatch accepted but automation run not visible yet; request retained for crash-safe reconciliation"
        )
    consume(request_path, state_path, created, "new_dispatch")
    print("RTK_IDEMPOTENT_DISPATCH_NEW", int(created["id"]), request["workflow"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
