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

Recovered runner state:

- runner name: `RTK-HOME-PC`;
- platform: Linux/X64 under the already configured Ubuntu/WSL environment;
- routing label: `rtk-home3`.

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

### 2026-08-21 13:20 UTC — first live home-runner connection and correction

The existing Actions runner 2.336.0 connected at `13:20:08Z` and accepted a queued job named `parallel` at `13:20:14Z`.

The live Windows/WSL observation corrected an earlier hardware assumption:

- Intel Core i5-1235U;
- 10 physical cores;
- **12 logical processors**, not 10.

During the accepted legacy `parallel` job Windows showed roughly 30% aggregate CPU and WSL `top` roughly 78.6% idle. This was traced to the old engine formula `min(cpu_count()-2, 8)` plus a tiny placeholder task and `imap(..., chunksize=1)`. With 12 logical processors, the old formula creates only eight workers, and the tiny task shape makes parent/IPC overhead dominate.

This observation changed the compute architecture again without changing any scientific conclusion. Engine v2.1 therefore added:

- true 12-logical-CPU max-throughput mode;
- adaptive multiprocessing chunksize for fine-grained indexed tasks;
- checkpoint metadata for logical CPU count and effective chunksize;
- a dedicated synthetic saturation worker that keeps each process CPU-bound for a controlled interval;
- bootstrap verification of `nproc=12`, `os.cpu_count()=12`, `workers=12` and checkpoint/progress completion;
- `/proc/stat` CPU-utilization sampling with an 80% mean-busy target used as an infrastructure diagnostic.

Canonical implementation commits in this correction chain include `f14fe68997f9df42906b0bd72ba53da91e49c12d` (resource/chunksize policy), `22b6cabd9154a682e8299f6bba28bd44579ceda8` (engine metadata/batching), `945f308168d2309c30c00d531fa630671629d278` (saturation worker), and `632e2c1b5f9545d897a43aacc96881d975c3dd7f` (12-CPU bootstrap gate).

The legacy ~30% observation is retained as a failed infrastructure configuration, not as a benchmark of the redesigned engine.

---

## 2026-08-21 14:30 UTC — B10 lambda-tail identifiability closes

Independent half-scale fixed-lambda stationarity run `32482153752` completed at both preregistered dust-tail anchors after the earlier base T3 pass.

- factor 64: `S_tail=1050.249062546245`, zero exact base/half improvement, positive-definite Hessians;
- factor 16384: `S_tail=1050.2490169939647`, zero exact base/half improvement, positive-definite Hessians.

The corresponding base/half eigenmodes remained qualitatively aligned. Against the frozen finite-lambda local score `1050.249912429787`, the best tail difference is

`Delta_tail=-0.0008954358222581504`.

Since its absolute magnitude is below the preregistered `0.005` identifiability convention, B10 closes as

`LAMBDA_NOT_NUMERICALLY_IDENTIFIABLE_AGAINST_PREREGISTERED_DUST_TAIL_AT_0P005`.

This is explicitly not a confidence interval, posterior, Bayes factor, mathematical redundancy theorem or global-minimum statement.

Canonical result: `research/robustness/RTK_B10_FINAL_TAIL_IDENTIFIABILITY_RESULT_2026-08-21.md`.

---

## 2026-08-21 18:42 UTC — constructive C8 direct FLRW scalar carrier

The project crossed an important conceptual boundary: C8 no longer asks only whether a rational RTK pole can be mimicked. A fixed local spatially covariant action was shown to reproduce the complete controlled quadratic FLRW scalar kinetic kernel directly.

For

`S = integral N sqrt(gamma)[M_*^2/2(R3+KijKij-K^2)+F+C_acc a_i a^i]`,

the production DBI background obeys the exact identity

`K_8piG=(rho_8piG+p_8piG)/c_a^2=2 M_K^2`.

Exact lapse/shift elimination gives

`S2 = 1/2 integral a^3/H^2 [K_phys(1+p^2/M_K^2) dot(zeta)^2-G_phys p^2 zeta^2]`,

hence

`omega^2=c_a^2 p^2/(1+p^2/M_K^2)`.

Run `32514697064`, artifact `9458330218`, confirmed the executable theorem.

This result does not establish a viable universal matter frame or UV completion. It moves the frontier from “construct the RTK scalar kernel” to “preserve that kernel while satisfying Newton/PPN/GW/compact-object/cutoff constraints.”

---

## 2026-08-21 19:23 UTC — gravitational-normalization ambiguity resolved for beta=0

A normalization correction was made before promoting the direct carrier to a physical theory. Production `8 pi G` must not automatically be identified with the bare coefficient `M_*^-2` of a candidate covariant action. For a standard universally coupled low-energy Hořava mapping, the production background normalization corresponds to `G_cosm`.

With

`M_cosm^2=M_*^2(1+3 lambda_prime/2)`

and

`M_N^2=M_*^2(1-alpha/2)`,

exact matching requires

`alpha=2+3 lambda_prime`.

Run `32518243787`, artifact `9459582368`, proved that the beta=0 direct acceleration-only branch has no healthy positive-finite-Newton exact solution: positive scalar gradient requires `lambda_prime>0`, which makes `M_N^2<0`; the other lambda-prime intervals either make the scalar gradient negative or alpha nonpositive.

This is a scoped negative result for the standard beta=0 universal matter branch only.

Canonical derivation: `research/methods/RTK_FORMULA_BIBLE_C8_GRAVITY_NORMALIZATION_APPENDIX.md`.

---

## 2026-08-21 19:31 UTC — standard universal matter frame excluded for the direct carrier

The beta=0 restriction was then removed using the modern low-energy parameters `(alpha,beta,gamma)` and the same-source cosmological, Newton, PPN and post-GW170817 relations.

Exact direct matching gives

`alpha=2+3 gamma+beta`

and therefore

`G_cosm/G_N=(2-alpha)/alpha`.

The cited BBN bound reduces on this hypersurface to

`|2(alpha-1)/alpha|<1/8`,

which requires

`16/17 < alpha < 16/15`.

With the post-GW170817 benchmark `|beta|<=~1e-15`, the first preferred-frame PPN expression is bounded below by about `3.7647`, while the observational benchmark is `1e-4`. The minimum mismatch exceeds `3.7e4`.

Run `32518936616`, artifact `9459822043`, independently verified the exact rational theorem.

Therefore the direct acceleration-only exact RTK carrier cannot live in the cited **standard universal low-energy Hořava matter frame**. This does not exclude nonminimal/disformal matter maps, auxiliary fields, fixed companion operators or broader spatially covariant/covariant completions.

Canonical result: `research/RTK_C8_STANDARD_MATTER_NO_GO_RESULT_2026-08-21.md`.

---

## 2026-08-21 19:43 UTC — minimal static-safe mixed-gradient escape tested

The next carrier search was narrowed to operators that can contribute to the cosmological scalar kinetic sector but vanish in a strictly static `K_ij=0` configuration. The minimal quadratic basis tested is

`C a_i a^i + 2D a_i D^i K + B D_iK D^iK`.

Exact lapse/shift elimination and polynomial matching to

`K/(2H^2)[1+p^2/M_K^2]`

produce only two analytic branches: the pure acceleration solution and a rank-one mixed branch. On the mixed branch

`C/C_direct=[(6H^2M_*^2+K)/(6H^2M_*^2-K)]^2 > 1`.

Thus this smallest mixed-gradient deformation cannot lower the static `a_i a^i` coefficient; setting `C=0` gives no exact RTK solution in this operator basis.

Executable theorem: `rtk-class-build:rtk/route_b_mixed_gradient_static_safe_gate.py`, source commit `7aa3f26e3896baf69deb2c45d915f7b38ec50ba0`. CI was launched at this chronology update; promote only after artifact inspection.

This is again a scoped operator-basis result, not a no-go for auxiliary constraints, other extrinsic-curvature tensors, nonminimal matter coupling or higher-spatial-gradient completions.

---

## Continuing rule

Every subsequent research iteration must update, as applicable:

1. `research/RESEARCH_LEDGER.md` — current gate/result/next action;
2. `research/methods/RTK_FORMULA_BIBLE.md` and its index/appendices — formulas, derivations, assumptions, scope;
3. `research/RTK_MODEL_CHRONOLOGY.md` — why the model/research architecture changed;
4. `docs/COMPUTE_LOG.md` and compute artifacts — execution provenance for material numerical runs.
