# RTK Distributed Compute Architecture

Version: 2026-08-21
Status: canonical compute-method document

## 1. Design goal

GitHub is the single dispatcher, provenance store and research-history authority. Compute nodes are replaceable workers. The present topology is:

- GitHub-hosted Ubuntu runners for short/medium independent workflows;
- `RTK-HOME-PC`, labels `[self-hosted, Linux, X64, rtk-home3]`, for long CPU-heavy work;
- future nodes may be added by a new unique routing label without changing scientific code.

The home node is not a second source of truth. Scientific inputs, formulas, protocols and acceptance criteria live in the repository. Only transient/resumable execution state lives on the node.

## 2. Observed home-node hardware

Observed on 2026-08-21 during the first live runner connection:

- CPU: 12th Gen Intel Core i5-1235U;
- physical cores: 10;
- logical processors: 12;
- Windows host RAM: approximately 7.7 GiB;
- WSL-visible RAM during the observation: approximately 5.9 GiB;
- virtualization enabled;
- runner connected successfully with Actions runner 2.336.0.

The earlier documentation that called this a ten-logical-CPU node was wrong. The correct maximum outer process width is 12 when WSL exposes the complete CPU set.

## 3. One heavy job, all useful CPU

A heavy RTK workflow owns the home node through the GitHub Actions concurrency group:

`rtk-home3-exclusive`

Only one such workflow may execute at a time. Inside that job, `rtk_engine.parallel_engine` uses a process pool.

Resource controls:

- `RTK_WORKERS=auto`: use all logical CPUs visible to Linux after reserve;
- `RTK_RESERVE_CPUS=0`: maximum-throughput mode; currently expected to resolve to 12 workers;
- `RTK_RESERVE_CPUS=2`: ten-worker headroom mode when desktop responsiveness matters;
- `RTK_CHUNKSIZE=auto`: adapt multiprocessing IPC batching to task granularity;
- `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, `NUMEXPR_NUM_THREADS=1` for outer-process-parallel task families.

The inner-thread limits prevent nested oversubscription. Twelve worker processes each independently spawning twelve BLAS/OpenMP threads would create roughly 144 runnable threads and usually reduce throughput.

### Why the first live `parallel` job showed only about 30% Windows CPU

At 2026-08-21 13:20 UTC the runner accepted a legacy `parallel` job. The observed Windows Task Manager showed about 30% CPU and Linux `top` showed about 78.6% idle.

That result is explained by the old engine design, not by a hardware limit:

1. Engine v1 used `workers=min(cpu_count()-2, 8)`. With 12 logical processors this evaluates to exactly 8 workers.
2. The placeholder worker performed only a few hundred Python arithmetic operations per task.
3. `Pool.imap(..., chunksize=1)` sent those tiny tasks through multiprocessing IPC individually.
4. The parent process therefore spent substantial time dispatching/receiving tasks instead of keeping every CPU continuously busy.

Engine v2.1 removes the eight-worker cap, uses all 12 logical CPUs in max-throughput mode, and adds adaptive IPC batching. The bootstrap uses a dedicated long-enough CPU-bound saturation worker so resource utilization can be measured independently of queue overhead.

### Two supported parallelism modes

1. **Independent indexed evaluations** — preferred for scans, stencil points, likelihood evaluations and Monte Carlo-like task families. Use `RTK_WORKERS=auto`, adaptive chunksize, and inner BLAS/OMP threads = 1.
2. **One native threaded solver** — if the scientific executable itself owns the parallel decomposition, run one outer task/process and explicitly give the native solver the desired OMP/MKL thread count. Do not nest both forms at full width.

## 4. Adaptive task granularity

`RTK_CHUNKSIZE=auto` targets roughly sixteen dispatch batches per worker and caps one batch at 1024 indexed items. This only changes transport granularity; each scientific task keeps its own deterministic index and identity.

For a small number of expensive scientific evaluations, auto mode naturally yields chunksize 1. For hundreds of thousands of tiny independent operations it batches many indices into each IPC message, avoiding the parent-process bottleneck observed in the first legacy test.

Checkpoint correctness is unchanged: only the contiguous ordered prefix already returned to the parent advances `next_index`. If the machine is hard-stopped, completed work still buffered inside an unfinished multiprocessing chunk may be recomputed after resume, but no unfinished item is incorrectly marked complete.

## 5. Stable task identity

Every resumable computation has a stable `run_key` and an input fingerprint.

A safe task family must satisfy:

- deterministic index space `0 .. total_tasks-1`;
- `calculate(index)` is idempotent or writes to an index-unique output;
- the same `run_key` is reused only for the same scientific workload;
- the checkpoint fingerprint must match the task module/input lock;
- a changed scientific input must use a new `run_key` or an explicit checkpoint reset.

If fingerprint or `total_tasks` differs, the engine refuses to resume. This is deliberate fail-closed behavior.

## 6. Persistent checkpoint protocol

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
- logical CPU count, worker count and effective chunksize;
- task metadata and terminal/running status.

The critical invariant is:

`next_index = last_successfully_committed_index + 1`.

The file is written to a temporary file, flushed/fsynced and atomically renamed. A power loss or process interruption therefore cannot expose a partially written JSON checkpoint under normal filesystem semantics.

On SIGINT/SIGTERM, the engine commits the last contiguous completed prefix and exits with status `interrupted`. A rerun with the same `run_key` and fingerprint resumes from `next_index`.

The checkout itself may be deleted or refreshed; checkpoint state survives because it is under `$HOME`, not under the Git working tree.

## 7. Progress and Ubuntu notifications

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
$HOME/.local/bin/rtk-runner-start
```

For the first bootstrap handshake, the official existing command is sufficient:

```bash
./run.sh
```

## 8. Bootstrap saturation gate

The canonical bootstrap workflow is `.github/workflows/rtk-home3-bootstrap.yml`.

It now requires:

- `nproc == 12` and `os.cpu_count() == 12`;
- `RTK_WORKERS=auto` and zero reserved CPUs;
- a 12-process-compatible CPU-bound synthetic workload (`rtk_engine.saturation_worker`);
- checkpoint schema v2 completion;
- progress completion with 12 workers;
- a sampled `/proc/stat` CPU-utilization artifact.

Mean aggregate CPU busy fraction >=80% is recorded as the saturation target. Falling below that target produces a warning and triggers investigation of WSL scheduling, Windows power policy, thermal throttling, or workload granularity; it is not converted into a scientific model result.

The saturation worker is infrastructure-only and must never be interpreted as RTK evidence.

## 9. GitHub state snapshot

At the end of every heavy engine job, even after failure where possible, the workflow copies the relevant persistent state into `results/runner-state/` inside the ephemeral checkout and uploads it with `actions/upload-artifact@v4`.

This artifact is a recovery/audit snapshot, not the primary live checkpoint. The primary resume path is the persistent node-local checkpoint because it avoids downloading an artifact on every restart.

## 10. Scientific integration contract

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

A real heavy research workflow must freeze its scientific input/protocol before dispatch. Placeholder or saturation workers exist only for infrastructure validation and must never be interpreted as model evidence.

## 11. Adding future compute nodes

For each additional computer:

1. register a GitHub self-hosted runner;
2. assign a unique role/routing label, e.g. `rtk-home4`;
3. record CPU/RAM/toolchain in `docs/COMPUTE_LOG.md`;
4. give node-specific heavy workflows a concurrency group;
5. keep the same checkpoint/progress contract;
6. partition independent task ranges between nodes only when scientific task identity is deterministic and merge rules are explicit.

Do not point two computers at the same writable node-local checkpoint. Distributed runs use disjoint shards/run keys and a deterministic repository-side merge protocol.

## 12. Provenance rules

Every research computation must record:

- UTC start/end time;
- Git commit SHA;
- workflow/run ID;
- runner label/node;
- scientific input fingerprint;
- task module/protocol version;
- visible logical CPU count;
- worker count/thread environment/chunksize;
- checkpoint key;
- result artifact hashes where applicable;
- acceptance/rejection rule and interpretation.

Scientific conclusions are copied into `research/RESEARCH_LEDGER.md`, formulas/derivations into `research/methods/RTK_FORMULA_BIBLE.md`, and model-development chronology into `research/RTK_MODEL_CHRONOLOGY.md`.

## 13. Current migration (2026-08-21)

Legacy home workflows referenced `rtk-home`; the actually configured node uses `rtk-home3`. The migration changes home workflows to `rtk-home3`, removes automatic push execution from benchmark workflows, and serializes heavy jobs through `rtk-home3-exclusive`.

The old engine kept checkpoints inside the checkout, hard-capped the worker pool at eight and used one-item multiprocessing dispatch. Engine v2/v2.1 moves state to `$HOME/.rtk-runner-state`, adds compatibility fingerprints, atomic checkpointing, signal-safe resume, heartbeat/ETA, explicit resource controls, 12-logical-CPU max-throughput operation, adaptive IPC batching and GitHub state snapshots.
