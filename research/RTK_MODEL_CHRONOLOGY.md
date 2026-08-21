# RTK Model Development Chronology

Version: 2026-08-21
Status: canonical append-only chronology

## Purpose

This file records how the RTK model, its numerical implementation and its theoretical interpretation evolved. It is deliberately separate from `RESEARCH_LEDGER.md`: the ledger tracks the current scientific frontier and individual gates, while this chronology records why the project changed direction and which earlier conclusions were superseded.

Rules:

1. Use UTC timestamps whenever a precise repository/workflow time is available.
2. Never rewrite an old score as if it belonged to a newer objective.
3. Record negative results with their exact scope.
4. Record formula corrections explicitly rather than silently replacing old expressions.
5. Every major change must point to a repository file, workflow/run, commit, or archived restore point.

---

## 2026-08-17 — Stage 4D3 dense-production consolidation

Archived restore point: `rtk/RESTORE_POINT_2026-08-17_STAGE4D3_DENSE.md` on `rtk-class-build`.

The project moved from an earlier sparse Stage4D3 objective to the matched-ultra + dense-BOSS production objective. The restore point explicitly froze the dense redshift grid, CLASS precision overrides, Planck/Pantheon/BOSS harness, exact-float cache semantics and the `0.005` recenter tolerance.

Important methodological correction: the old sparse RTK score `S_eff=1050.0338294787382` must not be compared numerically with a dense-objective LCDM score. This established the project's continuing rule that only contemporaneous, matched-objective scores may enter model comparisons.

The Stage4D3 work also established the local-stationarity workflow pattern now reused throughout the project: exact center replay -> axis/ray gate -> recenter only if improvement exceeds frozen tolerance -> Hessian/local-minimum certification -> matched comparison.

---

## 2026-08-18 to 2026-08-19 — robustness expansion

The research frontier broadened beyond a single cosmological minimum. Separate gates were introduced for neutrino robustness, primordial abundances, lensing, GW/PPN constraints and lambda identifiability.

The computational methodology increasingly separated:

- infrastructure success from scientific PASS/FAIL;
- fixed-center diagnostics from reoptimized comparisons;
- local stationarity from global evidence/posterior statements;
- phenomenological success from a covariant/UV completion.

This separation remains mandatory in all current reporting.

---

## 2026-08-20 — theoretical carrier boundary program

The project explicitly stopped treating one failed carrier as a failure of RTK itself. A family of scoped theoretical gates was developed around lapse-only ADM, U-DHOST/Route-B, PPN restrictions, compact-object boundaries and FLRW constraint structure.

Key scoped results now retained in the Formula Bible include:

- the weak-field transition-radius dimensional correction `r_C ~ (r_M/M_K^2)^(1/3)`;
- the exact-rational finite-positive-pole boundary `alpha = 2h/(3C+h) > 0` for `0<h<1` under the stated assumptions;
- the two-derivative lapse-only carrier obstruction caused by momentum dependence of the RTK target ratio;
- the minimal Route-B / beta1=0 PPN obstruction under the pinned closure;
- the fact that a fixed-action Minkowski obstruction does not automatically globalize to FLRW because background `H(a)` enters the constraint kernel.

Interpretation rule established here: BLACK/scoped no-go means only the named ansatz/assumptions are excluded.

---

## 2026-08-21 — frozen numerical frontier

The canonical frozen dense replay records:

- LCDM `S_eff = 1049.966118347761`;
- RTK `S_eff = 1050.249912429787`;
- local raw-objective gap `Delta S_eff = +0.2837940820259064`.

This is a reproducible local raw-objective result, not a Bayes factor, significance, global optimum or final model preference.

### B4 neutrino sector

A negative-mode ray around the parent neutrino RTK center found an exact improvement

`Delta S = 0.10990987029822463 > 0.005`,

therefore the parent center failed stationarity and required recentering. A fresh exact ray-recenter replay was launched rather than treating an unrepresented historical workflow state as proof.

### B6 primordial abundances

The paired AlterBBN pipeline initially passed frozen input/source/build checks but its first long abundance execution was externally cancelled, so no scientific abundance conclusion was inferred from that attempt.

The exact rerun, GitHub Actions run `32285359564` attempt 2, subsequently completed all six paired network executions and full-precision parsing. Its artifact showed `max |R_H-1| = 2.422446243599552e-09`. The only numerically resolved primary abundance shift was `delta Yp = +1.4314660568004456e-12`; the primary D/H shift and the other listed nuclide shifts remained below the preregistered numerical-resolution threshold with conservative bounds.

The RTK perturbation changes the frozen observational standardized residual by only about `1.10e-9 sigma` for Yp and `6.76e-9 sigma` for D/H. Therefore B6 was closed as **differential abundance robustness**, not as absolute BBN goodness-of-fit. The frozen reference calculation itself remains about `-4.706 sigma` from the selected D/H central value when only the quoted observational sigma is used.

Canonical result: `research/robustness/RTK_B6_ALTERBBN_RESULT_2026-08-21.md`.

### B9 Planck lensing

At frozen centers, standalone lensing gave

`Delta(-2 ln L) = -0.015658249008452`

for RTK minus LCDM. This is retained only as a fixed-center diagnostic; matched reoptimization remains open.

### B10 lambda identifiability

Base-stencil stationarity at tail factors 64 and 16384 retained the center as best exact point and gave positive-definite Hessians. Per preregistered protocol this did not close B10; a half-scale validation was required and launched.

---

## 2026-08-21 — C8 full FLRW Schur-complement gate

The theoretical frontier was sharpened from matching only a constraint-pole location to matching the complete rational remainder after lapse/shift elimination.

For nondynamical scalar constraints `x=(delta N, chi)`, define

`M=[[A,C],[C,B]]` and `J=(P,R)`.

Exact elimination gives

`K_eff = K0 - (B P^2 - 2 C P R + A R^2)/(A B - C^2)`.

For coefficients linear in Fourier variable `q`,

`A=a0+a1 q`, `B=b0+b1 q`, `C=c0+c1 q`,

the determinant has

`D2 = a1 b1 - c1^2`.

A strict single-linear-pole target therefore has the necessary algebraic gate

`a1 b1 - c1^2 = 0`.

This is not called a DHOST degeneracy condition without an explicit action map. C8 now requires one fixed action to match pole and residue at multiple epochs and then pass stability, DOF, cutoff, PPN/GW and observational consistency gates.

Canonical protocol: `research/RTK_C8_FLRW_SCHUR_MATCHING_PROTOCOL_2026-08-21.md`.

---

## 2026-08-21 — distributed-compute architecture transition

The project moved from GitHub-hosted-only/experimental home computation to a defined hybrid architecture.

Recovered hardware/runner state:

- runner name: `RTK-HOME-PC`;
- platform: Linux/X64 under the already configured Ubuntu/WSL environment;
- routing label: `rtk-home3`;
- current node: ten logical CPUs.

Legacy workflows still referenced `rtk-home`, so they could not reliably route to the configured node. The architecture was migrated to `rtk-home3` and heavy jobs were serialized through `rtk-home3-exclusive`.

The old engine used a hard eight-worker cap, reserved two CPUs and wrote a simple checkpoint inside the Git checkout. Engine v2 introduced:

- `RTK_WORKERS=auto` maximum-throughput mode;
- optional CPU reserve/headroom mode;
- one heavy GitHub job at a time with internal process parallelism;
- inner BLAS/OpenMP thread caps to prevent oversubscription;
- persistent `$HOME/.rtk-runner-state/<run_key>/checkpoint.json`;
- atomic writes and `next_index` resume semantics;
- input fingerprint/total-task compatibility checks;
- SIGINT/SIGTERM graceful checkpointing;
- heartbeat, throughput and ETA reporting;
- global Ubuntu-visible `live.log` and lifecycle notifications;
- GitHub artifact snapshots of execution state.

Canonical architecture: `docs/RTK_COMPUTE_ARCHITECTURE.md`.

Bootstrap workflow: `.github/workflows/rtk-home3-bootstrap.yml`, armed by commit `ee0b42f8594235f41db8aaecb61bfbbe63df3d94`. It installs the persistent Ubuntu launcher and verifies max-throughput multiprocessing plus checkpoint/progress contracts when the home runner comes online.

---

## Continuing rule

Every subsequent research iteration must update, as applicable:

1. `research/RESEARCH_LEDGER.md` — current gate/result/next action;
2. `research/methods/RTK_FORMULA_BIBLE.md` — formulas, derivations, assumptions, scope;
3. `research/RTK_MODEL_CHRONOLOGY.md` — why the model/research architecture changed;
4. `docs/COMPUTE_LOG.md` and compute artifacts — execution provenance for material numerical runs.
