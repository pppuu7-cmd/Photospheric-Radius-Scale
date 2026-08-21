# RTK Compute Log

## 2026-08-21

### Earlier baseline

- Self-hosted runner: `RTK-HOME-PC`.
- Baseline single-process benchmark recorded before parallel-engine migration.
- Parallel Engine v1 introduced multiprocessing, simple progress reporting and checkout-local checkpoints.
- Original policy used `MAX_WORKERS=8`, reserved 2 logical CPUs and routed workflows to legacy label `rtk-home`.

### Engine v2 / distributed-compute migration

- Actual configured routing label recovered as `rtk-home3`; platform Linux/X64.
- Home workflows migrated from `rtk-home` to `rtk-home3`.
- Automatic push execution removed from the home scientific benchmark; home compute is dispatched deliberately.
- All heavy home jobs share concurrency group `rtk-home3-exclusive`, preventing two heavyweight workflows from oversubscribing the same PC.
- Persistent execution state moved to `$HOME/.rtk-runner-state/<run_key>/`.
- Checkpoint schema v2 records `next_index`, total task count, fingerprint, UTC time and metadata; writes are atomic.
- Resume refuses a changed fingerprint or changed total task count unless reset is explicit.
- SIGINT/SIGTERM produces a safe interrupted checkpoint at the last contiguous completed task prefix.
- Progress records percent, throughput, ETA, worker count and status in `progress.json` plus an Ubuntu-visible `live.log`.
- Lifecycle events use stdout and best-effort local `wall` notification.
- Added console launcher `scripts/rtk_home_runner_console.sh`; bootstrap installs it as `$HOME/.local/bin/rtk-runner-start`.
- Heavy workflow uploads an end-of-job checkpoint/progress snapshot as a GitHub Actions artifact.

### First live connection and corrected hardware topology

At 2026-08-21 13:20:08Z the existing self-hosted runner connected successfully to GitHub using Actions runner `2.336.0`. At 13:20:14Z it accepted a queued job named `parallel`.

Observed host data supplied from Windows Task Manager and WSL `top`:

- CPU: 12th Gen Intel Core i5-1235U;
- physical cores: 10;
- logical processors: 12;
- Windows CPU utilization during the legacy test: about 30%;
- WSL aggregate CPU at the sample: 15.5% user, 4.9% system, 78.6% idle, 1.0% softirq;
- WSL load average at the sample: 2.45 / 1.07 / 0.41;
- Windows host memory: about 7.3 / 7.7 GiB used at the screenshot moment;
- WSL-visible memory: 5925.1 MiB total, 751.5 MiB used, 4473.7 MiB free, 889.3 MiB buffer/cache;
- WSL swap: 8192 MiB total, unused at the sample.

The earlier repository note that described the node as having ten logical CPUs was incorrect. The correct topology is **10 cores / 12 logical processors**.

### Diagnosis of the ~30% legacy CPU utilization

The active `parallel` job corresponded to the earlier engine behavior:

- old worker count: `min(cpu_count()-2, MAX_WORKERS)` with `MAX_WORKERS=8`;
- for 12 logical processors this resolves to 8 outer processes;
- the placeholder `calculate(index)` workload was extremely small;
- multiprocessing `imap` used `chunksize=1`.

The `top` snapshot showed the Python parent process consuming about 120% of one Linux CPU plus several worker processes at only about 10–20% each. This is characteristic of a parent/IPC dispatch bottleneck for tiny tasks rather than a CPU-capacity ceiling.

Therefore the observed ~30% is **not accepted as the target utilization** for the redesigned architecture.

### Engine v2.1 response

- Corrected max-throughput topology to 12 logical processors.
- `RTK_WORKERS=auto` + `RTK_RESERVE_CPUS=0` now resolves to all 12 processors visible to WSL.
- Ten-worker mode is available with `RTK_RESERVE_CPUS=2` when desktop headroom is needed.
- Added `RTK_CHUNKSIZE=auto` to batch tiny multiprocessing tasks and avoid parent/queue saturation.
- Auto chunksize targets approximately 16 dispatch batches per worker and caps a batch at 1024 indexed tasks.
- Engine metadata now records logical CPU count, worker count and effective chunksize in the persistent checkpoint.
- Added `rtk_engine.saturation_worker`, an infrastructure-only CPU-bound test that keeps each worker continuously busy for a controlled interval.
- Bootstrap v3 requires `nproc=12`, `os.cpu_count()=12`, 12 workers, valid checkpoint/progress completion, and records `/proc/stat` aggregate CPU utilization.
- Bootstrap saturation target: mean CPU busy >=80%; lower utilization generates an explicit warning for WSL/power/thermal/granularity investigation.
- For process-parallel scientific workloads, inner `OMP/OPENBLAS/MKL/NUMEXPR` threads remain pinned to 1 to prevent nested oversubscription.

### Second live connection: queued legacy benchmark

At 2026-08-21 13:43:41Z the runner connected again and at 13:43:46Z accepted another previously queued job named `benchmark`.

Observed approximately 27 seconds after start:

- Windows Task Manager: about 18% aggregate CPU at 1.70 GHz;
- Windows memory: about 6.4 / 7.7 GiB used (83%);
- WSL `top`: 10.1% user, 89.9% idle;
- one `python3` process at about 99.7% of one Linux logical CPU;
- WSL load average: 0.20 / 0.32 / 0.49;
- WSL-visible memory: 5925.1 MiB total, 666.2 MiB used, 4480.6 MiB free; swap unused.

Interpretation: this accepted `benchmark` is a stale legacy queued workload and is effectively single-core at the sampled moment. It is not a validation of engine v2.1 and its low utilization must not be used as the redesigned architecture benchmark.

The current repository `RTK Home Scientific Benchmark` workflow is now manual-only (`workflow_dispatch`), so new automatic push-triggered benchmark jobs should no longer be generated. The operational strategy is to let already accepted legacy queue entries drain while keeping the runner online, then validate the first `bootstrap` v3 run separately.

Canonical architecture: `docs/RTK_COMPUTE_ARCHITECTURE.md`.

Next validation gate:

1. leave `RTK-HOME-PC` connected while any already accepted legacy benchmark finishes;
2. do not interpret legacy benchmark CPU utilization as engine-v2.1 performance;
3. let the updated `rtk-home3` bootstrap v3 run when it reaches the runner;
4. inspect its artifact for exact `workers=12`, checkpoint/progress PASS and measured mean/median/max CPU busy fractions;
5. after bootstrap PASS, use `$HOME/.local/bin/rtk-runner-start` for future sessions;
6. route the next suitable frozen heavy scientific workload to the node and record whether its natural task granularity calls for 12 outer processes or one native threaded solver.
