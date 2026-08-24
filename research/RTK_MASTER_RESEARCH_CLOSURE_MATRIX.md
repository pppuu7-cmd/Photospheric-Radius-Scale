# RTK master research closure matrix

**Role:** authoritative high-level stopping/closure checklist for the autonomous RTK research loop.

This file does **not** override frozen protocol targets, `research/state/current.json`, branch-specific live state files, result JSON artifacts, the reproducibility lock, or theorem-specific acceptance gates.

Status semantics:

- 🟡 **RUNNING** — an admissible proof calculation is active or a former best-known claim has been reopened by stronger evidence.
- ✅ **SUBGATE CLOSED** — a meaningful scoped sub-question is reproducibly settled while its parent remains open.
- 🔴 **OPEN** — internally testable work remains.
- 🚀 **MAJOR CLOSED** — all declared proof requirements for that major item are satisfied.
- `EXTERNAL_BLOCKER` — closure requires independent external input.

## A. Matched numerical cosmology

| ID | Major item | Status | Current evidence / strict next gate |
|---|---|---|---|
| A1 | Frozen matched objective/common likelihood | 🚀 MAJOR CLOSED | `matched-ultra-linstep2+dense-BOSS`; production mapping `eff`; exact-float success-only semantics; recenter tolerance `0.005`; fingerprint `754edb2ff5380eff314867b0ecb1a23a8b861a69f7e46070c4b8251c98573666`. |
| A2 | ΛCDM local dense reference / best-known basin | 🟡 RUNNING | Historical exact score `1049.966118347761` remains reproducible, but its accepted-score point is **not** Hessian-certified: the historical PD Hessian center differs by exactly one base `Ob` step. Exact old→new line profile finds descent already at `t=0.01` by `0.013049143579337397`. The independently replayed `t=1` seed `1049.400976604194` is itself superseded by exact `t=1.1`, `1049.3633203461363`, improving `t=1` by `0.03765625805772288 > 0.005`. Mandatory gate: forward continuation/recenter from exact `t=1.1`, then full stationarity at the exact surviving center. |
| A3 | RTK Stage-4D3 interior local minimum | 🚀 MAJOR CLOSED (local) | Symmetric score-point/Hessian audit passes. Accepted score/params and final base+half Hessian centers are identical at `S=1050.249912429787`; both final stencils have best improvement `0.0` and PD curvature (min eig base `0.0002539372582019114`, half `0.0002755537750933801`). No global claim. |
| A4 | Independent clean-room reproduction | 🚀 MAJOR CLOSED (historical exact points) | Run `32148894768` reproduces historical LCDM/RTK exact scores with zero error. Later four-point cross-basin replay also reproduces historical points plus B9-derived seeds with zero error. Fresh-tree score reproduction does not transfer a Hessian certificate between nonidentical parameter points. |
| A5 | Best-known matched raw ΔS | 🟡 RUNNING | Historical exact pair delta `+0.2837940820259064` is retained only as historical raw-objective bookkeeping. Using certified RTK and the current best exact LCDM navigation sample `t=1.1` gives provisional navigation-only `ΔS=+0.886592083650612`; do **not** freeze it until ΛCDM recenter/stationarity + fresh-tree + common paired replay pass. The old preregistered `t=1` replacement replay is blocked as scientifically stale. |
| A6 | Formal model-selection statistics | 🟡 REOPENED / WAITING ON A5 | Historical AIC-like calculations remain conditional on the superseded historical pair. No current AIC/BIC/Bayes/sigma/Wilks statement until A5 is re-frozen under separately preregistered statistic-specific conventions. |

## B. Likelihood, observables, and robustness

| ID | Major item | Status | Current evidence / strict next gate |
|---|---|---|---|
| B1 | Planck+Pantheon+BOSS implementation consistency | 🚀 MAJOR CLOSED | Formula/unit/data ordering, component replay, covariance and objective provenance audits passed. |
| B2 | Linear RTK observable fingerprint | 🚀 MAJOR CLOSED | Reproducible background/CMB/P(k)/growth signature atlas exists under frozen settings; center-specific tables may be refreshed without reopening implementation consistency. |
| B3 | Source of present BOSS pressure | 🚀 MAJOR CLOSED | Correlated residual/PCA analysis identifies geometry/growth pressure; λ scans and prior linear mapping diagnostics do not explain it. |
| B4 | Minimal-neutrino robustness | 🟡 RUNNING | Later v3→v4 lineage was recovered and supersedes stale target-v2 state. v4 half run `32587822698`: `S_center=1050.5511025943172`, best improvement `4.9814518433777266e-05`, non-PD min eig `-4.7214683209037513e-05`. Exact full-eigenvector half rays are frozen/launched. If no descent `>0.005`, a quarter-scale target was preregistered before ray scores and may execute; PD quarter would still require independent fresh-tree replay. |
| B5 | Survey-level/nonlinear RSD robustness | 🟡 RUNNING | Frozen subgate now measures RTK `fσ8(k,z)` scale dependence over the BOSS DR12 analysis window `k=0.02…0.24 h/Mpc` at `z=0.38,0.51,0.61`, reproducing production `fσ8_eff=dσ8/dln a`. This can settle only linear scale dependence. Survey window, AP remapping, nonlinear RSD template, bias marginalization and full-shape/adequacy bound remain separate mandatory scope. |
| B6 | Early-universe / BBN robustness | 🟡 RUNNING | Differential pinned AlterBBN response is extremely small and that differential subgate is closed; absolute abundance/model-likelihood scope remains separate and prevents major closure. |
| B7 | Tensor/GW propagation and standard-siren sector | 🚀 MAJOR CLOSED (scoped) | Implemented late-time tensor equation has standard propagation speed with modified friction under the pinned model; unsupported primordial-tensor claims excluded. |
| B8 | Nonlinear/local-gravity/compact-object phenomenology | 🔴 OPEN | Linear static closure cannot by itself generate the desired asymptotic logarithmic galaxy potential; nonlinear isolated-system, solar-system and compact-object/universal-horizon gates remain mandatory. |
| B9 | Planck standalone-lensing robustness | 🚀 MAJOR CLOSED (local protocol v1) | Final paired replay PASS: `S_LCDM=1058.2173424114785`, `S_RTK=1059.2719553175134`, `ΔS_B9=+1.0546129060348903`; individual replay errors `0`, delta error `9.77e-15`; RTK fresh-tree PASS. Do not repeat v1 absent a newly frozen question. |
| B10 | Finite-λ versus dust-tail identifiability | 🚀 MAJOR CLOSED (protocol v1) | finite `1050.249912429787`; factor-16384 tail `1050.2490169939647`; tail-finite `-0.0008954358222581504`, so `|ΔS|<0.005`; classification `LAMBDA_NOT_NUMERICALLY_IDENTIFIABLE_AGAINST_PREREGISTERED_DUST_TAIL_AT_0P005`. |

## C. Theory / EFT consistency

| ID | Major item | Status | Current evidence / strict next gate |
|---|---|---|---|
| C1 | Classical background sign/stability domain | 🚀 MAJOR CLOSED | Declared background DBI sign/margin scan passed. |
| C2 | Healthy local quadratic preferred-frame scalar representative | 🚀 MAJOR CLOSED | Exact implemented linear dispersion has a local quadratic representative with positive tested kinetic/gradient Hamiltonian and no higher time derivative in that representative. |
| C3 | Route-A1 nonlinear EFT symmetry class | 🚀 MAJOR CLOSED | Symmetry/derivative assumptions explicitly frozen as a research postulate. |
| C4 | Route-A1 cubic operator basis through D≤4 | 🚀 MAJOR CLOSED | Complete IBP-reduced four-operator basis symbolically audited. |
| C5 | Long-wave conditional P(X) thermodynamic/cubic reconstruction | 🚀 MAJOR CLOSED | Exact conditional identities/relations proved with scope restrictions. |
| C6 | Finite-k nonlinear coefficient identifiability | 🚀 MAJOR CLOSED | No-go: dispersive nonlinear coefficients are not fixed by background+linear target without an added nonlinear completion hypothesis. |
| C7 | Full coupled metric + causal RT + Khronon nonlinear DOF/ghost theorem | 🔴 OPEN | Route-B/U(1) work supplies scoped prerequisites/obstructions, but one fixed nonlinear formulation still needs a complete coupled constraint/DOF analysis. |
| C8 | Physical strong-coupling scale / EFT cutoff | 🔴 OPEN | Several P(X), curvature-carrier and partial-wave subgates exist; full relevant interactions for a surviving fixed action and the lowest physical cutoff remain unresolved. |
| C9 | Radiative stability / counterterm closure / naturalness | 🔴 OPEN | `n=2` intrinsic-curvature carrier has exact nonlinear kernels, but soft-s channel invalidated the earlier optimistic all-hard UV sufficiency. Full lapse/shift completion, mixed-sector unitarity and technical naturalness remain open. |

## D. Reproducibility and software proof chain

| ID | Major item | Status | Current evidence / strict next gate |
|---|---|---|---|
| D1 | Locked production environment | 🚀 MAJOR CLOSED | CLASS/Pantheon commits, Planck SHA, Python/NumPy/SciPy/likelihood versions, precision and IC semantics are recorded. |
| D2 | Failure/cache/retry safety | 🚀 MAJOR CLOSED | Failed/transient evaluations are not success-cached; exact retry invariants tested. |
| D3 | Crash-idempotent heavy dispatch | 🚀 MAJOR CLOSED | Serialized/idempotent control-plane and frozen-target dispatch pattern established. |
| D4 | Proof-artifact identity/provenance | 🚀 MAJOR CLOSED | Active proof families carry center/objective/scale fingerprints and locked upstream/runtime provenance. |
| D5 | Autonomous decision-tree regression coverage | 🚀 MAJOR CLOSED | Workflow success is separated from scientific classification; result routers advance only from persisted eligible results. New A5 guard also forbids a stale `t=1` half result from dispatching final replay after later exact descent was discovered. |

## E. External scientific validation

| ID | Item | Status | Exact external closure condition |
|---|---|---|---|
| E1 | Independent implementation/reproduction | `EXTERNAL_BLOCKER` | Another group/codebase reproduces core equations and matched observational results without using this repository as its executable implementation. |
| E2 | Peer-reviewed publication | `EXTERNAL_BLOCKER` | Manuscript accepted after external peer review. |
| E3 | Prospective observational discrimination | `EXTERNAL_BLOCKER` | A preregistered distinctive prediction is tested by independent new/held-out observations. |

## Current high-priority execution order

1. **A5:** complete the frozen exact forward continuation from `t=1.1`. If any new point improves by `>0.005`, recenter at the best exact point; if the best lies at the upper boundary, preregister another extension. Only after this discovered direction is recenter-clear may a full Hessian be built at the exact current center.
2. **A5:** after the surviving LCDM center passes base/multiscale stationarity and fresh-tree replay, freeze a new common RTK/LCDM paired replay. Only then update `research/state/current.json` and A6.
3. **B4:** finish v4 half eigenmode rays; only a persisted no-descent result may route into the already-preregistered v4 quarter Hessian. Fresh-tree remains mandatory after a recenter-clear PD quarter.
4. **B5:** finish the frozen BOSS-window linear scale-dependence subgate, then address survey-window/AP/nonlinear-template propagation separately.
5. Continue B6 and fixed-action C7-C9 without mixing their objectives or claims. B9/B10 protocol-v1 remain closed and should not consume repeat compute.

## Mandatory score-point/Hessian-center guard

A Hessian certificate applies only to its exact parameter center. A neighboring `best_exact` or accepted score within recenter tolerance may be retained for score bookkeeping but does not inherit that Hessian certificate. Every future stationarity report must explicitly state whether Hessian center and accepted-score point are identical.

## Autonomous stopping rule

Do not stop because one workflow, local fit, or paper draft completes. The internally achievable frontier is exhausted only when every internally achievable major row is 🚀, or a remaining row is rigorously reclassified as `EXTERNAL_BLOCKER` with a precise external closure condition.
