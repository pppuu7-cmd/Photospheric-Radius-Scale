#!/usr/bin/env python3
"""Synchronize the canonical RTK methodology metadata and append-only chronology.

Run after the deterministic orchestrator and all gate-enforcement steps, but before
committing the iteration. The source iteration journal remains authoritative; this
script only builds durable cross-chat recovery metadata from it.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import subprocess
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "research/state/current.json"
METHOD = ROOT / "research/methodology/RTK_AUTONOMOUS_RESEARCH_METHOD.md"
CHRON = ROOT / "research/chronology/RTK_RESEARCH_CHRONOLOGY.jsonl"
BEGIN = "<!-- AUTO-ITERATION-METADATA:BEGIN -->"
END = "<!-- AUTO-ITERATION-METADATA:END -->"
HELSINKI = ZoneInfo("Europe/Helsinki")


def parse_utc(s: str) -> dt.datetime:
    x = dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
    if x.tzinfo is None:
        x = x.replace(tzinfo=dt.timezone.utc)
    return x.astimezone(dt.timezone.utc)


def git_head() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()


def objective_hash(state: dict) -> str:
    raw = json.dumps(state.get("objective", {}), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def explicit_objective_fingerprint(state: dict):
    fr = state.get("final_replay_result") or {}
    return fr.get("objective_fingerprint")


def load_iteration(state: dict) -> tuple[str, dict]:
    rel = state.get("last_iteration")
    if not rel:
        raise SystemExit("state has no last_iteration")
    p = ROOT / rel
    if not p.exists():
        raise SystemExit(f"last_iteration missing: {rel}")
    return rel, json.loads(p.read_text())


def append_chronology(event: dict) -> bool:
    CHRON.parent.mkdir(parents=True, exist_ok=True)
    existing = CHRON.read_text().splitlines() if CHRON.exists() else []
    event_id = event["event_id"]
    for line in existing:
        if not line.strip():
            continue
        try:
            if json.loads(line).get("event_id") == event_id:
                return False
        except json.JSONDecodeError as exc:
            raise SystemExit(f"invalid chronology JSONL line: {exc}") from exc
    with CHRON.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, sort_keys=True, separators=(",", ":")) + "\n")
    return True


def sync_methodology(block: str) -> None:
    text = METHOD.read_text()
    if BEGIN not in text or END not in text:
        raise SystemExit("canonical methodology metadata markers missing")
    before, rest = text.split(BEGIN, 1)
    _old, after = rest.split(END, 1)
    METHOD.write_text(before + BEGIN + "\n" + block.rstrip() + "\n" + END + after)


def main() -> None:
    state = json.loads(STATE.read_text())
    rel, iteration = load_iteration(state)
    number = int(iteration["iteration"])
    t_utc = parse_utc(iteration["time"])
    t_local = t_utc.astimezone(HELSINKI)
    source_sha = git_head()
    obj_hash = objective_hash(state)
    explicit_fp = explicit_objective_fingerprint(state)

    observations = iteration.get("observations", [])
    actions = iteration.get("actions", [])
    run_ids = sorted({
        int(v)
        for row in observations
        if isinstance(row, dict)
        for k, v in row.items()
        if k.endswith("_run") and isinstance(v, int)
    })
    dispatch = iteration.get("next_dispatch")
    if isinstance(dispatch, dict) and isinstance(dispatch.get("run_id"), int):
        run_ids = sorted(set(run_ids + [int(dispatch["run_id"])]))

    event = {
        "schema_version": 1,
        "event_id": f"iteration-{number:06d}",
        "kind": "autonomous_iteration",
        "iteration": number,
        "timestamp_utc": t_utc.isoformat().replace("+00:00", "Z"),
        "timestamp_europe_helsinki": t_local.isoformat(),
        "source": "research/iterations",
        "iteration_file": rel,
        "source_branch": "rtk-class-build",
        "source_head_sha": source_sha,
        "stage": iteration.get("stage"),
        "actions": actions,
        "observations": observations,
        "run_ids": run_ids,
        "next_dispatch": dispatch,
        "comparison": iteration.get("comparison"),
        "objective_name": (state.get("objective") or {}).get("name"),
        "objective_configuration_sha256": obj_hash,
        "explicit_objective_fingerprint": explicit_fp,
        "interpretation_warning": (
            "Chronology records deterministic control-state evolution. Workflow success alone is not a scientific PASS; validated artifacts and frozen gates remain authoritative."
        ),
    }
    appended = append_chronology(event)

    meta = (
        f"Last methodology synchronization: `{event['timestamp_utc']}` / "
        f"`{event['timestamp_europe_helsinki']} Europe/Helsinki`  \n"
        f"Last synchronized iteration: `{number}` (`{rel}`)  \n"
        f"Scientific source HEAD before iteration commit: `{source_sha}`  \n"
        f"Objective: `{event['objective_name']}`  \n"
        f"Objective configuration SHA256: `{obj_hash}`  \n"
        f"Explicit frozen objective fingerprint, if available: `{explicit_fp}`  \n"
        f"Chronology source: `research/chronology/RTK_RESEARCH_CHRONOLOGY.jsonl`"
    )
    sync_methodology(meta)

    print(
        "RTK_ITERATION_LEDGER_SYNC_PASS",
        json.dumps(
            {
                "iteration": number,
                "chronology_appended": appended,
                "timestamp_utc": event["timestamp_utc"],
                "timestamp_europe_helsinki": event["timestamp_europe_helsinki"],
                "source_head_sha": source_sha,
                "objective_configuration_sha256": obj_hash,
            },
            sort_keys=True,
        ),
    )


if __name__ == "__main__":
    main()
