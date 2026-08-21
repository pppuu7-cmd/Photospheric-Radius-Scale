# RTK Compute Log

## 2026-08-21

### Earlier baseline

- Self-hosted runner: `RTK-HOME-PC`.
- Baseline single-process benchmark recorded before parallel-engine migration.
- Parallel Engine v1 introduced multiprocessing, simple progress reporting and checkout-local checkpoints.
- Original policy used `MAX_WORKERS=8`, reserved 2 logical CPUs and routed workflows to legacy label `rtk-home`.

### Engine v2 / distributed-compute migration

- Actual configured routing label recovered as `rtk-home3`; platform Linux/X64.
- Current home node has 10 logical CPUs.
- Home workflows migrated from `rtk-home` to `rtk-home3`.
- Automatic push execution removed from the home scientific benchmark; home compute is dispatched deliberately.
- All heavy home jobs share concurrency group `rtk-home3-exclusive`, preventing two heavyweight workflows from oversubscribing the same PC.
- `RTK_WORKERS=auto` + `RTK_RESERVE_CPUS=0` is the maximum-throughput mode; on the current node this resolves to 10 outer worker processes.
- `RTK_RESERVE_CPUS=2` or explicit `RTK_WORKERS=8` remains available when desktop responsiveness is preferred.
- For process-parallel scientific workloads, inner `OMP/OPENBLAS/MKL/NUMEXPR` thread counts are pinned to 1 to prevent nested oversubscription.
- Persistent execution state moved to `$HOME/.rtk-runner-state/<run_key>/`.
- Checkpoint schema v2 records `next_index`, total task count, fingerprint, UTC time and metadata; writes are atomic.
- Resume refuses a changed fingerprint or changed total task count unless reset is explicit.
- SIGINT/SIGTERM produces a safe interrupted checkpoint at the last contiguous completed task prefix.
- Progress now records percent, throughput, ETA, worker count and status in `progress.json` plus an Ubuntu-visible `live.log`.
- Lifecycle events use stdout and best-effort local `wall` notification.
- Added console launcher `scripts/rtk_home_runner_console.sh`; bootstrap installs it as `$HOME/.local/bin/rtk-runner-start`.
- Heavy workflow uploads an end-of-job checkpoint/progress snapshot as a GitHub Actions artifact.

Canonical architecture: `docs/RTK_COMPUTE_ARCHITECTURE.md`.

Next validation gate:

1. bring `RTK-HOME-PC` online with its existing `./run.sh`;
2. allow the queued `rtk-home3` bootstrap/handshake job to verify labels, CPU count, persistent state and multiprocessing;
3. after bootstrap PASS, use the installed `rtk-runner-start` wrapper for future sessions and route the next suitable frozen heavy scientific workload to the node;
4. record observed scaling and actual worker count from the bootstrap artifact before deciding whether a scientific workload should use 10 processes, 8 processes, or one native multithreaded solver.
