# RTK Distributed Compute Architecture

Version: 2026-08-21
Status: canonical compute-method document

## 1. Design goal

GitHub is the single dispatcher, provenance store and research-history authority. Compute nodes are replaceable workers. The present topology is:

- GitHub-hosted Ubuntu runners for short/medium independent workflows;
- `RTK-HOME-PC`, labels `[self-hosted, Linux, X64, rtk-home3]`, for long CPU-heavy work;
- future nodes may be added by a new unique routing label without changing scientific code.

The home node is not a second source of truth. Scientific inputs, formulas, protocols and acceptance criteria live in the repository. Only transient/resumable execution state lives on the node.

## 2. One heavy job, all useful CPU

A heavy RTK workflow owns the home node through the GitHub Actions concurrency group:

`rtk-home3-exclusive`

Only one such workflow may execute at a time. Inside that job, `rtk_engine.parallel_engine` uses a process pool.

Resource controls:

- `RTK_WORKERS=auto`: use all available logical CPUs after reserve;
- `RTK_RESERVE_CPUS=0`: maximum-throughput mode;
- `RTK_RESERVE_CPUS=2` or `RTK_WORKERS=8`: interactive/headroom mode on the current ten-logical-CPU node;
- `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, `NUMEXPR_NUM_THREADS=1` for process-parallel task families.

The inner-thread limits prevent oversubscription. Ten worker processes each spawning ten BLAS threads would create roughly one hundred runnable threads and usually reduce throughput.

### Two supported parallelism modes

1. **Independent indexed evaluations** — preferred for scans, stencil points, likelihood evaluations and Monte Carlo-like task families. Use `RTK_WORKERS=auto` and inner BLAS/OMP threads = 1.
2. **One native threaded solver** — if the scientific executable itself owns the parallel decomposition, run a single outer task/process and explicitly give the native solver the desired OMP/MKL thread count. Do not nest both forms at full width.

## 3. Stable task identity

Every resumable computation has a stable `run_key` and an input fingerprint.

A safe task family must satisfy:

- deterministic index space `0 .. total_tasks-1`;
- `calculate(index)` is idempotent or writes to an index-unique output;
- the same `run_key` is reused only for the same scientific workload;
- the checkpoint fingerprint must match the task module/input lock;
- a changed scientific input must use a new `run_key` or an explicit checkpoint reset.

If fingerprint or `total_tasks` differs, the engine refuses to resume. This is deliberate fail-closed behavior.

## 4. Persistent checkpoint protocol

Node-local state root:

`$HOME/.rtk-runner-state`

Per-run state:

`$HOME/.rtk-runner-state/<run_key>/checkpoint.json`

Checkpoint schema v2 records at least:

- schema version;
- sanitized run key;
- `next_index`;
- completed count;
- total task count;
- input fingerprint;
- UTC timestamp;
- worker/task metadata and terminal/running status.

The critical invariant is:

`next_index = last_successfully_committed_index + 1`.

The file is written to a temporary file, flushed/fsynced and atomically renamed. A power loss or process interruption therefore cannot expose a partially written JSON checkpoint under normal filesystem semantics.

On SIGINT/SIGTERM, the engine commits the last contiguous completed prefix and exits with status `interrupted`. A rerun with the same `run_key` and fingerprint resumes from `next_index`.

The checkout itself may be deleted or refreshed; checkpoint state survives because it is under `$HOME`, not under the Git working tree.

## 5. Progress and Ubuntu notifications

Each run maintains:

- `<run>/progress.json` — machine-readable current state;
- `<run>/live.log` — per-run event stream;
- `$HOME/.rtk-runner-state/live.log` — global event stream across jobs.

Progress records include:

- completed/total;
- percent;
- session elapsed time;
- throughput;
- ETA when measurable;
- worker count;
- status.

The engine emits lifecycle events to stdout and to `live.log`. Start, interruption, failure and completion additionally attempt a local `wall` notification. The runner-console wrapper tails the global log in the Ubuntu terminal.

After the bootstrap job installs the wrapper, start the node from the already configured Actions runner directory with:

```bash
~/.local/bin/rtk-runner-start
```

If the shell cannot find it, use:

```bash
$HOME/.local/bin/rtk-runner-start
```

For the first bootstrap handshake, use the official existing command in the configured runner directory:

```bash
./run.sh
```

## 6. GitHub state snapshot

At the end of every heavy engine job, even after failure where possible, the workflow copies the relevant persistent state into `results/runner-state/` inside the ephemeral checkout and uploads it with `actions/upload-artifact@v4`.

This artifact is a recovery/audit snapshot, not the primary live checkpoint. The primary resume path is the persistent node-local checkpoint because it avoids downloading an artifact on every restart.

## 7. Scientific integration contract

`RTK_TASK_MODULE` names a repository Python module exporting:

```python
def calculate(index):
    ...
```

The engine itself must not contain model-specific equations. Scientific modules define task index -> exact calculation. This separates:

- scientific formula/protocol;
- orchestration;
- resource scheduling;
- checkpoint/progress infrastructure.

A real heavy research workflow must freeze its scientific input/protocol before dispatch. Placeholder `rtk_engine.worker` exists only for infrastructure validation and must never be interpreted as model evidence.

## 8. Adding future compute nodes

For each additional computer:

1. register a GitHub self-hosted runner;
2. assign a unique role/routing label, e.g. `rtk-home4`;
3. record CPU/RAM/toolchain in `docs/COMPUTE_LOG.md`;
4. give node-specific heavy workflows a concurrency group;
5. keep the same checkpoint/progress contract;
6. partition independent task ranges between nodes only when scientific task identity is deterministic and merge rules are explicit.

Do not point two computers at the same writable node-local checkpoint. Distributed runs use disjoint shards/run keys and a deterministic repository-side merge protocol.

## 9. Provenance rules

Every research computation must record:

- UTC start/end time;
- Git commit SHA;
- workflow/run ID;
- runner label/node;
- scientific input fingerprint;
- task module/protocol version;
- worker count/thread environment;
- checkpoint key;
- result artifact hashes where applicable;
- acceptance/rejection rule and interpretation.

Scientific conclusions are copied into `research/RESEARCH_LEDGER.md`, formulas/derivations into `research/methods/RTK_FORMULA_BIBLE.md`, and model-development chronology into `research/RTK_MODEL_CHRONOLOGY.md`.

## 10. Current migration (2026-08-21)

Legacy home workflows referenced `rtk-home`; the actually configured node uses `rtk-home3`. The migration therefore changes home workflows to `rtk-home3`, removes automatic push execution from benchmark workflows, and serializes heavy jobs through `rtk-home3-exclusive`.

The old engine also kept checkpoints inside the checkout and hard-capped the worker pool. Engine v2 moves state to `$HOME/.rtk-runner-state`, adds compatibility fingerprints, atomic checkpointing, signal-safe resume, heartbeat/ETA, explicit resource controls and GitHub state snapshots.
