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
| A2 | ΛCDM local dense reference / best-known basin | 🟡 RUNNING | The t=1.1 half-scale stencil is PD (min eig `0.019510024973060546`) but found exact candidate `S=1049.3550570964142`, improving that center by `0.008263249722176624 > 0.005`. Mandatory recenter1 base/half targets were frozen before new scores. The recenter1 scientific result is not yet persisted; no fresh-tree/minimum claim is admissible. |
| A3 | RTK Stage-4D3 interior local minimum | 🚀 MAJOR CLOSED (local phenomenological implementation) | Accepted score/params and final base+half Hessian centers are identical at `S=1050.249912429787`; both final stencils have best improvement `0.0` and PD curvature. This certificate belongs to the current phenomenological CLASS implementation and is not silently transferred to the elliptic-completed action. |
| A4 | Independent clean-room reproduction | 🚀 MAJOR CLOSED (historical exact points) | Run `32148894768` reproduces historical LCDM/RTK exact scores with zero error. Later cross-basin replay also reproduces the historical points plus B9-derived seeds. |
| A5 | Best-known matched raw ΔS | 🟡 RUNNING | Historical exact pair `+0.2837940820259064` is provenance only. Certified RTK plus exact LCDM recenter1 navigation point gives navigation-only `ΔS=+0.8948553333727887`. Freeze only after recenter1 decision tree, independent fresh-tree and common paired replay. |
| A6 | Formal model-selection statistics | 🟡 REOPENED / WAITING ON A5 | No current AIC/BIC/Bayes/sigma/Wilks statement until A5 is re-frozen under separately preregistered statistic-specific conventions. |
| A7 | Matched alternative-model benchmark | 🟡 RUNNING / PROTOCOL FROZEN | `research/benchmarks/RTK_MATCHED_MULTI_MODEL_BENCHMARK_PROTOCOL_v1.json` is frozen. wCDM can be run on the identical objective after A5 refreeze. Full CPL requires a crossing-safe perturbation implementation because the pinned fluid solver rejects `w=-1` crossing. |

## B. Likelihood, observables, and robustness

| ID | Major item | Status | Current evidence / strict next gate |
|---|---|---|---|
| B1 | Planck+Pantheon+BOSS implementation consistency | 🚀 MAJOR CLOSED | Formula/unit/data ordering, component replay, covariance and objective provenance audits passed for the current production phenomenological implementation. |
| B2 | Linear RTK observable fingerprint | 🚀 MAJOR CLOSED | Reproducible background/CMB/P(k)/growth signature atlas exists under frozen current-production settings; completion observables must be rederived/replayed separately. |
| B3 | Source of present BOSS pressure | 🚀 MAJOR CLOSED | Correlated residual/PCA analysis identifies geometry/growth pressure; λ scans and prior linear mapping diagnostics do not explain it. |
| B4 | Minimal-neutrino robustness | 🟡 RUNNING | v4 half: `S_center=1050.5511025943172`, best improvement `4.9814518433777266e-05`, non-PD min eig `-4.7214683209037513e-05`. Exact full-eigenvector half rays remain frozen/launched; no persisted ray decision yet. |
| B5 | Survey-level/nonlinear RSD robustness | 🟡 RUNNING | B5-LIN remains frozen over `k=0.02…0.24 h/Mpc`, `z=0.38,0.51,0.61`; no persisted scientific result yet. B5-SURVEY (window/AP/nonlinear template/bias nuisance) is explicitly separate. |
| B6 | Early-universe / BBN robustness | 🟡 RUNNING | Differential pinned AlterBBN response is extremely small and that differential subgate is closed; absolute abundance/model-likelihood scope remains separate. |
| B7 | Tensor/GW propagation and standard-siren sector | 🚀 MAJOR CLOSED (scoped local/action and phenomenological sectors) | Implemented late-time tensor equation has standard propagation speed under the pinned phenomenological model. The fixed U(1)+DBI representative independently has principal-TT `c_T^2=1`; completion source implementation must be control-replayed before claiming one unified production action. |
| B8 | Nonlinear/local-gravity/compact-object phenomenology | 🔴 OPEN with weak-field PPN subgate closed | The local frozen U(1)+RTK representative has `gamma_PPN=1`, `beta_PPN=1`, `alpha1_PPN=0`, `alpha2_PPN=0`, and `G_N=G` on its certified branch. Nonlinear static bare lapse gives `N=1`. Strong-field rotation, nonlinear galaxies, compact objects/universal horizons and same-completion PPN replay remain mandatory. |
| B9 | Planck standalone-lensing robustness | 🚀 MAJOR CLOSED (local protocol v1) | Final paired replay: `S_LCDM=1058.2173424114785`, `S_RTK=1059.2719553175134`, `ΔS_B9=+1.0546129060348903`, exact individual replays. Do not repeat v1 absent a new frozen question. |
| B10 | Finite-λ versus dust-tail identifiability | 🚀 MAJOR CLOSED (protocol v1) | finite `1050.249912429787`; factor-16384 tail `1050.2490169939647`; tail-finite `-0.0008954358222581504`, hence `|ΔS|<0.005`. No compact-object inference from the older bare-lapse diagnostic. |

## C. Theory / EFT consistency

| ID | Major item | Status | Current evidence / strict next gate |
|---|---|---|---|
| C1 | Classical background sign/stability domain | 🚀 MAJOR CLOSED | Declared DBI background sign/margin scan passed in its frozen scope. |
| C2 | Healthy local quadratic preferred-frame scalar representative | 🚀 MAJOR CLOSED (rolling branch) | Exact implemented cosmological linear dispersion has a positive local quadratic representative on the rolling branch. This does not override the exact local-rest rank-enhancement surface. |
| C3 | Route-A1 nonlinear EFT symmetry class | 🚀 MAJOR CLOSED | Symmetry/derivative assumptions explicitly frozen as a research postulate. |
| C4 | Route-A1 cubic operator basis through D≤4 | 🚀 MAJOR CLOSED | Complete IBP-reduced four-operator basis symbolically audited. |
| C5 | Long-wave conditional P(X) thermodynamic/cubic reconstruction | 🚀 MAJOR CLOSED | Exact conditional identities/relations proved with scope restrictions. |
| C6 | Finite-k nonlinear coefficient identifiability | 🚀 MAJOR CLOSED | No-go: dispersive nonlinear coefficients are not fixed by background+linear target without an added nonlinear completion hypothesis. |
| C7 | Full coupled metric + causal RT + Khronon nonlinear DOF/ghost theorem | 🟡 RUNNING with major FLRW rank subgates closed | Local weak-field fixed-action closure is strong: exact static scalar EOM/variation, `N=1`, core PPN quartet and O(v^3) scalar-silence pass. Elliptic-compensator current-lineage replay passes exact auxiliary Dirac projection and homogeneous source cancellation. Finite-k consolidation now provides a constructive flat-FLRW all-`q>0` rank-safe domain for `lambda_HL>1`, nonnegative-pressure barotropic matter and frozen UV-sign conditions. Generic inhomogeneous/all-background constraint rank, massive-neutrino anisotropic stress, compact objects and local-rest/rolling phase relation remain open. |
| C8 | Physical strong-coupling scale / EFT cutoff | 🟡 RUNNING / LOCAL-REST CANONICAL-RANK WARNING | At exact local rest `X_U=X_star`, full constraints give `S2_reduced=0`. The first nonzero constrained action is positive quartic and spatial; the first time-dependent term is quintic and linear in `dot(phi)`; canonical symplectic rank scales as `Omega~epsilon^3->0`. A single `(D^2 Sigma)^2` rescue is insufficient after full lapse elimination and its cosmological contamination requires `eta4<1.68e-11` for 1% at the tested production worst case. Do not call this a ghost/infinite strong coupling until nonlinear Dirac rank/cutoff is completed. |
| C9 | Radiative stability / counterterm closure / naturalness | 🔴 OPEN with existing-symmetry rescue NEGATIVELY CLOSED | Current `U(1) x Diff(M,F)` plus internal Sigma shift does not protect `sigma1=sigma2=0`; allowed marginal operators are expected to be regenerated. Requires an additional Ward symmetry, counterterm-stable degeneracy, RG fixed surface, or quantitative tuning control below a demonstrated EFT cutoff. |
| C10 | Same-full-action production cosmology completion bridge | 🟡 RUNNING / IMPLEMENTATION PROTOCOL FROZEN | `RTK_ROUTE_B_U1_ELLIPTIC_BRIDGE_CURRENT_LINEAGE_REPLAY_PASS` closes auxiliary projection and homogeneous bridge. `RTK_ROUTE_B_U1_FINITE_K_RANK_DOMAIN_CURRENT_LINEAGE_REPLAY_PASS` gives a constructive all-q rank-safe FLRW domain. `RTK_ROUTE_B_U1_HISTORY_WIDE_MC_WINDOW_PASS` gives `max(99 k_cos^2,3(3lambda_HL-1)H_EFT^2/(64eta0)) <= M_c^2 <= k_local^2/99` before isolated-root buffering, with explicit EFT onset. Production code audit shows current `khr_params` has `lambda_D` but no `lambda_HL`/`M_c`, and current perturbations are effective-fluid equations. Implementation protocol is frozen: `lambda_HL` must remain distinct from `lambda_D`; no completed-action likelihood score before shadow/source/constraint controls. Shadow-interface and linear-FLRW-source gates are active. |

## D. Reproducibility and software proof chain

| ID | Major item | Status | Current evidence / strict next gate |
|---|---|---|---|
| D1 | Locked production environment | 🚀 MAJOR CLOSED | CLASS/Pantheon commits, Planck SHA, Python/NumPy/SciPy/likelihood versions, precision and IC semantics are recorded. |
| D2 | Failure/cache/retry safety | 🚀 MAJOR CLOSED | Failed/transient evaluations are not success-cached; exact retry invariants tested. |
| D3 | Crash-idempotent heavy dispatch | 🚀 MAJOR CLOSED | Serialized/idempotent control-plane and frozen-target dispatch pattern established. |
| D4 | Proof-artifact identity/provenance | 🚀 MAJOR CLOSED | Active proof families carry center/objective/scale fingerprints and locked upstream/runtime provenance. |
| D5 | Autonomous decision-tree regression coverage | 🚀 MAJOR CLOSED | Workflow success is separated from scientific classification. A5 recenter1, B4/B5 targets and the C8/C9 theorem chain follow frozen-before-result discipline. Completion history-window, shadow-interface and linear-source targets were likewise frozen before their executions. |

## E. External scientific validation

| ID | Item | Status | Exact external closure condition |
|---|---|---|---|
| E1 | Independent implementation/reproduction | `EXTERNAL_BLOCKER` | Another group/codebase reproduces core equations and matched observational results without using this repository as its executable implementation. |
| E2 | Peer-reviewed publication | `EXTERNAL_BLOCKER` | Manuscript accepted after external peer review. |
| E3 | Prospective observational discrimination | `EXTERNAL_BLOCKER` | A preregistered distinctive prediction is tested by independent new/held-out observations. |

## Current high-priority execution order

1. **A5:** inspect the recenter1 base result when persisted. Improvement `>0.005` -> freeze recenter2; recenter-clear/non-PD -> exact eigenmode rays; recenter-clear/PD -> only the already-preregistered identical-center half gate. Fresh-tree and paired replay remain mandatory.
2. **C10 completion bridge:** finish shadow-interface and linear-FLRW-source replays; then derive/freeze the reduced U1 metric-constraint mapping required by CLASS. Do **not** patch only effective-fluid `cs2/w`.
3. **C10 source/history:** audit the actual ordinary-source composition entering filtered `H0`, especially massive-neutrino anisotropic stress, and select no `M_c` until that audit plus the history-wide window is satisfied.
4. **C8 local rest:** determine whether the nonlinear primary relation removes the scalar or produces a finite-amplitude strong-coupling scale; keep higher-spatial rescue separate from the production-completion bridge unless a same-action target is frozen.
5. **B4:** finish v4 half eigenmode rays; only a persisted no-descent result may route into the preregistered quarter Hessian.
6. **B5:** finish B5-LIN, then freeze the separate survey/template adequacy target; linear scale-dependence alone cannot close B5-SURVEY.
7. **A7:** after A5 refreeze, launch wCDM on the identical objective. Full CPL waits for crossing-safe perturbations.
8. **C9:** seek one explicit additional protection/RG/tuning mechanism; existing declared symmetries are already ruled out as sufficient protection.
9. Continue B6 and compact-object/nonlinear work without mixing objectives. B9/B10 v1 remain closed.

## Mandatory score-point/Hessian-center guard

A Hessian certificate applies only to its exact parameter center. A neighboring `best_exact` or accepted score within recenter tolerance may be retained for score bookkeeping but does not inherit that Hessian certificate. Every future stationarity report must explicitly state whether Hessian center and accepted-score point are identical.

## Autonomous stopping rule

Do not stop because one workflow, local fit, or paper draft completes. The internally achievable frontier is exhausted only when every internally achievable major row is 🚀, or a remaining row is rigorously reclassified as `EXTERNAL_BLOCKER` with a precise external closure condition.
