# RTK master research closure matrix

**Role:** authoritative high-level stopping/closure checklist for the autonomous RTK research loop.

This file does **not** override the frozen matched comparison protocol, `research/state/current.json`, branch-specific live state files, the reproducibility lock, or any theorem-specific acceptance gate. It records what must be true before a major item may be called closed.

Status semantics:

- 🟡 **RUNNING** — an admissible proof calculation is currently in progress or a previously closed best-known claim has been reopened by stronger evidence.
- ✅ **SUBGATE CLOSED** — a meaningful local sub-question is reproducibly settled, but the parent major claim is not complete.
- 🔴 **OPEN** — internally testable work remains.
- 🚀 **MAJOR CLOSED** — all predeclared proof requirements for this major item are satisfied. Do not use this mark for partial evidence.
- `EXTERNAL_BLOCKER` — closure intrinsically requires an independent group, new observations, peer review, or other input not derivable from the current repository/model.

## A. Matched numerical cosmology

| ID | Major item | Status | Strict closure condition | Current evidence / next gate |
|---|---|---|---|---|
| A1 | Frozen matched objective and common likelihood definition | 🚀 MAJOR CLOSED | RTK and ΛCDM use the same named dense-ultra objective, exact-float success-only evaluation semantics, fixed production mapping, and frozen recenter rule | `matched-ultra-linstep2+dense-BOSS`; production `eff`; recenter tolerance 0.005; objective fingerprint `754edb2ff5380eff314867b0ecb1a23a8b861a69f7e46070c4b8251c98573666` remains unchanged |
| A2 | ΛCDM local dense reference minimum / best-known basin | 🟡 RUNNING | preserve the historical certified local minimum, but any independently reproduced lower basin must itself pass the frozen recenter → multiscale stationarity → fresh-tree replay chain before becoming the new reference | Historical `S=1049.966118347761` remains a valid local certificate. New cross-basin seed `S=1049.400976604194` independently replayed with error `0.0` and improves the same objective by `0.5651417435669828`. Formal base-scale gate also replayed the center with error `0.0`, found exact improvement `0.0`, but one soft negative eigenvalue `-0.002467341536255588`; frozen exact eigenmode rays are now active. |
| A3 | RTK Stage-4D3 interior local minimum | 🚀 MAJOR CLOSED | current center recenter-clear; all negative coarse modes exact-ray falsified if present; two adjacent accepted stencil scales PD and each best improvement ≤0.005 | historical/current A5 RTK center `S=1050.249912429787` remains certified under the unchanged objective. Strip-lensing inspection of all 101 B9 base and all 101 B9 half-scale RTK points finds no baseline score below the B9 RTK center `1050.2560245726381`, so the B9 neighborhood does not supersede the historical RTK point. |
| A4 | Independent clean-room reproduction of historical accepted minima | 🚀 MAJOR CLOSED (historical pair) | fresh-tree paired RTK+ΛCDM replay at exact accepted-score params, locked environment, each score reproduced within 2e-6 and target fingerprint validated | run `32148894768` reproduced the historical local pair exactly. This certificate remains true for those points; it does **not** prove there is no deeper basin. New cross-basin audit independently reproduced both historical points and both B9-derived seeds with zero score error. |
| A5 | Best-known matched raw ΔS | 🟡 RUNNING | after A2 new-basin chain either fails or passes, freeze a paired score only from the then-current certified reference points and independently replay them under the unchanged objective | Historical local-pair `ΔS=+0.2837940820259064` is now historical/conditional. Using the still-certified historical RTK point and the independently reproduced new LCDM seed gives provisional best-known mixed `ΔS=+0.8489358255928892`, but it must **not** be frozen until the new LCDM stationarity + fresh-tree chain passes. The two B9-derived seeds instead give `+0.8550479684440688`. |
| A6 | Formal model-selection statistics | 🟡 REOPENED / WAITING ON A5 | only after current A5 best-known paired reference is re-frozen, under separately preregistered statistic-specific parameter/prior/sample conventions | Historical post-freeze `ΔAIC=+2.2837940820259064` remains a result conditional on the superseded historical A5 local pair. Do not use it as the current best-known AIC until A5 is re-frozen. BIC still needs defensible composite-likelihood `N_eff`; Bayes still needs preregistered normalized priors/evidence integration; no sigma/Wilks conversion authorized. |

## B. Likelihood, observables, and robustness

| ID | Major item | Status | Strict closure condition | Current evidence / next gate |
|---|---|---|---|---|
| B1 | Planck+Pantheon+BOSS implementation consistency | 🚀 MAJOR CLOSED | formulas/units/data ordering independently audited; exact component replay reproducible; BOSS conventions externally cross-checked | component replay and BOSS convention/unit audits passed; BOSS 9x9 covariance was independently checked SPD/well-conditioned (reported correlation condition number ≈13.95) |
| B2 | Linear RTK observable fingerprint | 🚀 MAJOR CLOSED | reproducible background/CMB/P(k)/growth signature atlas at matched current centers with hardened primordial inputs and exact requested redshifts | signature atlas + cross-anchor decomposition completed; any future best-known-center refresh should regenerate center-specific presentation tables without reopening the implementation theorem |
| B3 | Source of present BOSS pressure | 🚀 MAJOR CLOSED | correlated residual analysis identifies geometry/growth directions and rules out λ_D and linear RSD-scale mapping as dominant explanations | BOSS PCA mode identified; λ_D scan and fσ8(k) grid show negligible explanatory power |
| B4 | Minimal-neutrino robustness | 🟡 RUNNING | separate paired, explicitly non-frozen robustness comparison with mν=0.06 eV; both models reoptimized, stationarity-certified and independently replayed after massless freeze | existing B4 chain remains separate from the A5 cross-basin audit; do not compare absolute scores across objectives |
| B5 | Survey-level/nonlinear RSD robustness | 🔴 OPEN | model-specific survey-window/AP/nonlinear-template treatment or a justified bound showing compressed BOSS likelihood is adequate at required precision | linear k-dependence is tiny, but survey-template robustness remains open |
| B6 | Early-universe / BBN robustness | 🟡 RUNNING | demonstrate valid background/perturbation behavior and abundance/expansion constraints through relevant early epochs under a declared data/protocol set | pinned AlterBBN differential chain has strong partial closure; keep absolute-abundance/model-likelihood scope separate |
| B7 | Tensor/GW propagation and standard-siren sector | 🚀 MAJOR CLOSED | derive/verify implemented late-time tensor propagation equation and propagation observables; execute reproducible diagnostic at the final frozen RTK center; explicitly exclude unsupported primordial-tensor claims | pinned model=2 source gives standard `k^2 h` term (`cT=c`) and modified friction; historical final-center diagnostic remains a scoped propagation result |
| B8 | Nonlinear/local-gravity/compact-object phenomenology | 🔴 OPEN | derive applicable nonlinear/local regime and pass declared solar-system/galaxy/compact-object consistency tests | necessary-condition negative subgate remains: current implemented linear static RTK closure cannot by itself generate the asymptotic logarithmic potential needed for flat galaxy curves; nonlinear isolated-system/compact-object tests remain open |
| B9 | Planck standalone-lensing robustness | 🚀 MAJOR CLOSED (local protocol v1) | separately preregistered matched lensing objective; paired reoptimization; both local stationarity chains; independent RTK fresh-tree certification; final paired exact replay | All frozen gates passed. `S_LCDM=1058.2173424114785`, `S_RTK=1059.2719553175134`, final local `ΔS_B9=+1.0546129060348903`; both center replay errors `0.0`, delta replay error `9.769962616701378e-15`; RTK fresh-tree run `32704596153` reproduced the center exactly with PD Hessian and zero exact improvement. Canonical closure: `research/robustness/B9_FINAL_LOCAL_ROBUSTNESS_CLOSURE_2026-08-24.md`. No global/model-selection claim. |
| B10 | Finite-λ_D versus dust-boundary / tail identifiability | 🚀 MAJOR CLOSED (protocol v1) | preregistered finite-versus-tail chain resolves numerical identifiability at the declared `0.005` scale; posterior/Bayes/global questions remain separately scoped | Canonical v1 result: finite `1050.249912429787`; factor-16384 tail `1050.2490169939647`; best tail-finite difference `-0.0008954358222581504`, hence `|ΔS|<0.005`; classification `LAMBDA_NOT_NUMERICALLY_IDENTIFIABLE_AGAINST_PREREGISTERED_DUST_TAIL_AT_0P005`. Do not reopen v1 merely for posterior/Bayes/global questions. |

## C. Theory / EFT consistency

| ID | Major item | Status | Strict closure condition | Current evidence / next gate |
|---|---|---|---|---|
| C1 | Classical background sign/stability domain | 🚀 MAJOR CLOSED | required background algebraic signs and DBI margins positive over declared physical scan | Q1 audit passed |
| C2 | Healthy local quadratic preferred-frame scalar EFT representative | 🚀 MAJOR CLOSED | exact implemented linear dispersion reconstructed by local quadratic representative; kinetic/gradient Hamiltonian positive over tested physical domain; no higher time derivative in representative | constructive Q3 audit passed |
| C3 | Route-A1 nonlinear EFT symmetry class | 🚀 MAJOR CLOSED | symmetry/derivative assumptions explicitly selected as a research postulate rather than inferred from linear CLASS | Route A1 frozen and documented |
| C4 | Route-A1 cubic operator basis through D≤4 | 🚀 MAJOR CLOSED | complete IBP-reduced basis enumerated and symbolically audited | four-operator basis; CI passed |
| C5 | Long-wave conditional P(X) thermodynamic/cubic reconstruction | 🚀 MAJOR CLOSED | exact thermodynamic identities and conditional c1,c2 relations proved symbolically with scope restrictions explicit | theorem CI passed |
| C6 | Finite-k nonlinear coefficient identifiability | 🚀 MAJOR CLOSED | prove whether c3,c4 / dispersive nonlinear coefficients are derivable from background+linear target | no-go proved: they are not identifiable without an added nonlinear completion hypothesis; D5 basis enumerated |
| C7 | Full coupled metric + causal RT + Khronon nonlinear DOF/ghost theorem | 🔴 OPEN | explicit valid nonlinear formulation for the coupled system plus constraint/DOF analysis showing absence (or presence) of unwanted propagating modes; causal nonlocal auxiliaries must not be miscounted as free local fields | route-B/U(1) completion work supplies scoped subgates; full coupled nonlinear constraint theorem remains open |
| C8 | Physical strong-coupling scale / EFT cutoff | 🔴 OPEN | choose/derive a nonlinear completion, canonically normalize full relevant interactions, identify lowest physical breakdown scale and verify hierarchy with cosmological modes | linear `M_K/k_star` alone is proven not to determine the physical cutoff |
| C9 | Radiative stability / counterterm closure / naturalness | 🔴 OPEN | declared nonlinear EFT/operator content plus loop power counting and stability of required hierarchies | open; must be applied to the same fixed action that survives completion/phenomenology gates |

## D. Reproducibility and software proof chain

| ID | Major item | Status | Strict closure condition | Current evidence / next gate |
|---|---|---|---|---|
| D1 | Locked production environment | 🚀 MAJOR CLOSED | CLASS/Pantheon commits, Planck archive SHA, NumPy/SciPy/Python/likelihood version, gauge, nonlocal branch mapping, neutrino baseline and IC semantics recorded | `rtk/reproducibility_lock.json` schema 8; clean-room Python is explicitly pinned to 3.12.3 |
| D2 | Failure/cache/retry safety | 🚀 MAJOR CLOSED | failed/transient evaluations never memoized as successful objective walls; deterministic exact retries and regression tests pass | success-only cache and retries audited/CI-tested |
| D3 | Crash-idempotent heavy dispatch | 🚀 MAJOR CLOSED | serialized control-plane and tested no-duplicate behavior across dispatch crash window | idempotent dispatch guard + tests; heavy new gates use explicit frozen targets and branch-separated trigger/compute semantics |
| D4 | Proof-artifact identity/provenance | 🚀 MAJOR CLOSED | active RTK/ΛCDM proof families require exact center/objective/scale fingerprints and locked upstream/runtime provenance; historical frozen proof artifacts are independently covered when they predate the validator | the A5/B9 four-point cross-basin replay used the same locked CLASS/Pantheon/Planck/runtime provenance and reproduced all four target scores with zero error |
| D5 | Autonomous decision-tree regression coverage | 🚀 MAJOR CLOSED | negative-eigenray, half/quarter, final replay and dispatch transitions covered by synthetic regression tests; no known logical acceptance race | new B9 and cross-basin workflows preserve fail-closed separation: workflow failure is not automatically scientific failure; result routers advance only after explicit persisted PASS classifications |

## E. External scientific validation

| ID | Item | Status | Exact external closure condition |
|---|---|---|---|
| E1 | Independent implementation/reproduction by another group/codebase | `EXTERNAL_BLOCKER` | an independent team reproduces core RTK equations and matched observational results without using this repository as its executable implementation |
| E2 | Peer-reviewed publication | `EXTERNAL_BLOCKER` | manuscript accepted after external peer review |
| E3 | Prospective observational discrimination | `EXTERNAL_BLOCKER` | a preregistered distinctive RTK prediction is tested by independent new/held-out observations |

## Current high-priority execution order

1. Complete the new A5 ΛCDM cross-basin chain: inspect the frozen base eigenmode rays; if no exact descent exceeds `0.005`, run the unchanged-center half-scale Hessian; if recenter is required, freeze the best ray point and repeat the multiscale chain. Only after local stationarity is resolved run an independent fresh-tree baseline replay before re-freezing A5.
2. Re-freeze the best-known A5 matched pair only after item 1 is certified; then independently replay the pair and refresh any A6 statistic that depended on the historical A5 pair.
3. B9 and B10 protocol-v1 local robustness questions are closed; do not spend compute repeating them without a new explicitly frozen question.
4. Continue remaining B4/B5/B6 and fixed-action C7-C9 theory gates without mixing their objectives or claims.

## Autonomous stopping rule

The autonomous research loop must **not** stop because a single workflow, paper draft, or local fit completes. It may declare the internally achievable research frontier exhausted only when every internally achievable major row above is 🚀, or when a remaining row has been rigorously reclassified as `EXTERNAL_BLOCKER` with a precise external closure condition.

Whenever `research/state/current.json` or a branch-specific live state materially changes a major proof status, update this matrix conservatively. A valid historical local result remains valid at its frozen point even if a deeper independent basin is later discovered; only the best-known/global interpretation changes.