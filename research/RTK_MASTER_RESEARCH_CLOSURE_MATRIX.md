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
| A2 | ΛCDM local dense reference / best-known basin | 🟡 RUNNING | The t=1.1 half-scale stencil is PD (min eig `0.019510024973060546`) but found an exact Newton candidate `S=1049.3550570964142`, improving the t=1.1 center by `0.008263249722176624 > 0.005`. The mandatory recenter1 target was frozen before new scores at that exact point and its base stationarity workflow is active. No fresh-tree or minimum claim is admissible yet. |
| A3 | RTK Stage-4D3 interior local minimum | 🚀 MAJOR CLOSED (local) | Symmetric score-point/Hessian audit passes. Accepted score/params and final base+half Hessian centers are identical at `S=1050.249912429787`; both final stencils have best improvement `0.0` and PD curvature (min eig base `0.0002539372582019114`, half `0.0002755537750933801`). No global claim. |
| A4 | Independent clean-room reproduction | 🚀 MAJOR CLOSED (historical exact points) | Run `32148894768` reproduces historical LCDM/RTK exact scores with zero error. Later four-point cross-basin replay also reproduces historical points plus B9-derived seeds with zero error. Fresh-tree score reproduction does not transfer a Hessian certificate between nonidentical parameter points. |
| A5 | Best-known matched raw ΔS | 🟡 RUNNING | Historical exact pair delta `+0.2837940820259064` is retained only as historical bookkeeping. Using certified RTK and the current exact LCDM recenter1 navigation point gives navigation-only `ΔS=+0.8948553333727887`. Do not freeze it until the recenter1 base/conditional-half decision tree is resolved, any further recenter/rays are completed, an independent fresh-tree replay passes, and a common paired replay is frozen and reproduced. |
| A6 | Formal model-selection statistics | 🟡 REOPENED / WAITING ON A5 | Historical AIC-like calculations remain conditional on the superseded historical pair. No current AIC/BIC/Bayes/sigma/Wilks statement until A5 is re-frozen under separately preregistered statistic-specific conventions. |

## B. Likelihood, observables, and robustness

| ID | Major item | Status | Current evidence / strict next gate |
|---|---|---|---|
| B1 | Planck+Pantheon+BOSS implementation consistency | 🚀 MAJOR CLOSED | Formula/unit/data ordering, component replay, covariance and objective provenance audits passed. |
| B2 | Linear RTK observable fingerprint | 🚀 MAJOR CLOSED | Reproducible background/CMB/P(k)/growth signature atlas exists under frozen settings; center-specific tables may be refreshed without reopening implementation consistency. |
| B3 | Source of present BOSS pressure | 🚀 MAJOR CLOSED | Correlated residual/PCA analysis identifies geometry/growth pressure; λ scans and prior linear mapping diagnostics do not explain it. |
| B4 | Minimal-neutrino robustness | 🟡 RUNNING | Later v3→v4 lineage supersedes stale target-v2 state. v4 half run `32587822698`: `S_center=1050.5511025943172`, best improvement `4.9814518433777266e-05`, non-PD min eig `-4.7214683209037513e-05`. Exact full-eigenvector half rays are frozen/launched. Only a persisted no-descent classification may permit the preregistered quarter Hessian. |
| B5 | Survey-level/nonlinear RSD robustness | 🟡 RUNNING | B5-LIN is frozen over the actual BOSS Fourier interval `k=0.02…0.24 h/Mpc` at `z=0.38,0.51,0.61`, comparing the production `fσ8_eff=dσ8/dln a` with scale-dependent `f(k,z)σ8`. `B5_SURVEY_AP_NONLINEAR_SCOPE_PROTOCOL_2026-08-24.md` explicitly separates the still-open survey-window/AP/nonlinear-template/bias-nuisance problem. A B5-LIN PASS cannot close B5-SURVEY. |
| B6 | Early-universe / BBN robustness | 🟡 RUNNING | Differential pinned AlterBBN response is extremely small and that differential subgate is closed; absolute abundance/model-likelihood scope remains separate and prevents major closure. |
| B7 | Tensor/GW propagation and standard-siren sector | 🚀 MAJOR CLOSED (scoped) | Implemented late-time tensor equation has standard propagation speed with modified friction under the pinned model; unsupported primordial-tensor claims excluded. The same fixed U(1)+DBI IR representative independently passes an explicit principal-TT action theorem: `S_mix` vanishes in pure TT on homogeneous rolling `Sigma(t)` and the exact kinetic/gradient coefficients give `c_T^2=1`. |
| B8 | Nonlinear/local-gravity/compact-object phenomenology | 🔴 OPEN | The weak-field static zero-shift branch now has exact same-action Newton normalization, `gamma_PPN=1`, `beta_PPN=1`, and a nonlinear bare-lapse uniqueness theorem `N=1` throughout the regular real-DBI interior. This is a substantial Solar-System subgate, but moving-source preferred-frame, nonlinear galaxy, compact-object/universal-horizon and `X_U->0` behavior remain mandatory; therefore B8 is not closed. |
| B9 | Planck standalone-lensing robustness | 🚀 MAJOR CLOSED (local protocol v1) | Final paired replay PASS: `S_LCDM=1058.2173424114785`, `S_RTK=1059.2719553175134`, `ΔS_B9=+1.0546129060348903`; individual replay errors `0`, delta error `9.77e-15`; RTK fresh-tree PASS. Do not repeat v1 absent a newly frozen question. |
| B10 | Finite-λ versus dust-tail identifiability | 🚀 MAJOR CLOSED (protocol v1) | finite `1050.249912429787`; factor-16384 tail `1050.2490169939647`; tail-finite `-0.0008954358222581504`, so `|ΔS|<0.005`; classification `LAMBDA_NOT_NUMERICALLY_IDENTIFIABLE_AGAINST_PREREGISTERED_DUST_TAIL_AT_0P005`. Separate static DBI-domain work shows the formal `lambda_D->infinity` limit is not uniformly admissible at fixed nonzero local lapse; this does not reopen the frozen cosmological B10 result. |

## C. Theory / EFT consistency

| ID | Major item | Status | Current evidence / strict next gate |
|---|---|---|---|
| C1 | Classical background sign/stability domain | 🚀 MAJOR CLOSED | Declared background DBI sign/margin scan passed. |
| C2 | Healthy local quadratic preferred-frame scalar representative | 🚀 MAJOR CLOSED | Exact implemented linear dispersion has a local quadratic representative with positive tested kinetic/gradient Hamiltonian and no higher time derivative in that representative. |
| C3 | Route-A1 nonlinear EFT symmetry class | 🚀 MAJOR CLOSED | Symmetry/derivative assumptions explicitly frozen as a research postulate. |
| C4 | Route-A1 cubic operator basis through D≤4 | 🚀 MAJOR CLOSED | Complete IBP-reduced four-operator basis symbolically audited. |
| C5 | Long-wave conditional P(X) thermodynamic/cubic reconstruction | 🚀 MAJOR CLOSED | Exact conditional identities/relations proved with scope restrictions. |
| C6 | Finite-k nonlinear coefficient identifiability | 🚀 MAJOR CLOSED | No-go: dispersive nonlinear coefficients are not fixed by background+linear target without an added nonlinear completion hypothesis. |
| C7 | Full coupled metric + causal RT + Khronon nonlinear DOF/ghost theorem | 🟡 RUNNING | Same-action U(1)+DBI weak-field progress is now much stronger: exact static scalar EOM PASS; exact variation bridge `C(X)(DTheta)^2 -> M_Pl^2 a_i a^i` PASS; O(2) Newton/gamma PASS; nonlinear elliptic theorem gives unique regular asymptotically-flat static `N=1` on the real-DBI interior; static O(v^4) inheritance gives `beta_PPN=gamma_PPN=1`. A separately frozen O(v^3) moving-source scalar-silence/vector gate is active, with a preferred-frame `alpha1,alpha2` target preregistered before its result. Full nonlinear/compact-object and all-background ghost/constraint closure remain outside these scoped PPN theorems. |
| C8 | Physical strong-coupling scale / EFT cutoff | 🔴 OPEN | Same-action TT principal propagation is healthy in its scoped two-derivative sector, but that does not determine the scalar/mixed strong-coupling cutoff. Several P(X), curvature-carrier and partial-wave subgates exist; full lapse/shift/U(1) interactions for the surviving fixed action and the lowest physical cutoff remain unresolved. |
| C9 | Radiative stability / counterterm closure / naturalness | 🔴 OPEN | `n=2` intrinsic-curvature carrier has exact nonlinear kernels, but soft-s channel invalidated the earlier optimistic all-hard UV sufficiency. The fixed representative sits on the exceptional `sigma1=sigma2=0` surface, whose radiative protection remains mandatory. The exact static RTK reduction and PPN successes do not supply that protection. Full mixed-sector unitarity and technical naturalness remain open. |

## D. Reproducibility and software proof chain

| ID | Major item | Status | Current evidence / strict next gate |
|---|---|---|---|
| D1 | Locked production environment | 🚀 MAJOR CLOSED | CLASS/Pantheon commits, Planck SHA, Python/NumPy/SciPy/likelihood versions, precision and IC semantics are recorded. |
| D2 | Failure/cache/retry safety | 🚀 MAJOR CLOSED | Failed/transient evaluations are not success-cached; exact retry invariants tested. |
| D3 | Crash-idempotent heavy dispatch | 🚀 MAJOR CLOSED | Serialized/idempotent control-plane and frozen-target dispatch pattern established. |
| D4 | Proof-artifact identity/provenance | 🚀 MAJOR CLOSED | Active proof families carry center/objective/scale fingerprints and locked upstream/runtime provenance. |
| D5 | Autonomous decision-tree regression coverage | 🚀 MAJOR CLOSED | Workflow success is separated from scientific classification. A5 recenter1 base and conditional half targets were frozen before recenter1 scores; the base workflow dispatches half only after a persisted recenter-clear PD result. The O(v^3) scalar-silence and conditional preferred-frame targets were likewise frozen before the O(v^3) result, and the preferred-frame workflow is gated on its persisted PASS. |

## E. External scientific validation

| ID | Item | Status | Exact external closure condition |
|---|---|---|---|
| E1 | Independent implementation/reproduction | `EXTERNAL_BLOCKER` | Another group/codebase reproduces core equations and matched observational results without using this repository as its executable implementation. |
| E2 | Peer-reviewed publication | `EXTERNAL_BLOCKER` | Manuscript accepted after external peer review. |
| E3 | Prospective observational discrimination | `EXTERNAL_BLOCKER` | A preregistered distinctive prediction is tested by independent new/held-out observations. |

## Current high-priority execution order

1. **A5:** inspect `A5_LCDM_T1P1_RECENTER1_BASE_RESULT_v1.json` when persisted. If improvement `>0.005`, freeze recenter2 before any further scale. If recenter-clear and non-PD, freeze exact eigenmode rays. If recenter-clear and PD, only the already-preregistered identical-center recenter1 half-scale workflow may proceed.
2. **A5:** if the admissible recenter1 half result is recenter-clear and PD, require independent fresh-tree replay at the identical center; only then freeze a new common RTK/LCDM paired replay and update `research/state/current.json`.
3. **C7 same-action:** finish the frozen O(v^3) moving-source scalar-silence/vector gate. Only a persisted PASS may authorize the already-preregistered preferred-frame inheritance check for `alpha1,alpha2`. Static `beta=gamma=1` is already closed on its stated branch and should not be redone.
4. **B4:** finish v4 half eigenmode rays; only a persisted no-descent result may route into the preregistered v4 quarter Hessian. Fresh-tree remains mandatory after a recenter-clear PD quarter.
5. **B5:** finish B5-LIN, then use `B5_SURVEY_AP_NONLINEAR_SCOPE_PROTOCOL_2026-08-24.md` to freeze a separate survey/template adequacy target; do not infer survey closure from linear scale dependence alone.
6. Continue B6 and C8-C9 without mixing their objectives or claims. B9/B10 protocol-v1 remain closed and should not consume repeat compute.

## Mandatory score-point/Hessian-center guard

A Hessian certificate applies only to its exact parameter center. A neighboring `best_exact` or accepted score within recenter tolerance may be retained for score bookkeeping but does not inherit that Hessian certificate. Every future stationarity report must explicitly state whether Hessian center and accepted-score point are identical.

## Autonomous stopping rule

Do not stop because one workflow, local fit, or paper draft completes. The internally achievable frontier is exhausted only when every internally achievable major row is 🚀, or a remaining row is rigorously reclassified as `EXTERNAL_BLOCKER` with a precise external closure condition.
