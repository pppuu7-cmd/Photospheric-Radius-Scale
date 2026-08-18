# RTK master research closure matrix

**Role:** authoritative high-level stopping/closure checklist for the autonomous RTK research loop.

This file does **not** override the frozen matched comparison protocol, `research/state/current.json`, the reproducibility lock, or any theorem-specific acceptance gate. It records what must be true before a major item may be called closed.

Status semantics:

- 🟡 **RUNNING** — an admissible proof calculation is currently in progress.
- ✅ **SUBGATE CLOSED** — a meaningful local sub-question is reproducibly settled, but the parent major claim is not complete.
- 🔴 **OPEN** — internally testable work remains.
- 🚀 **MAJOR CLOSED** — all predeclared proof requirements for this major item are satisfied. Do not use this mark for partial evidence.
- `EXTERNAL_BLOCKER` — closure intrinsically requires an independent group, new observations, peer review, or other input not derivable from the current repository/model.

## A. Matched numerical cosmology

| ID | Major item | Status | Strict closure condition | Current evidence / next gate |
|---|---|---|---|---|
| A1 | Frozen matched objective and common likelihood definition | 🚀 MAJOR CLOSED | RTK and ΛCDM use the same named dense-ultra objective, exact-float success-only evaluation semantics, fixed production mapping, and frozen recenter rule | `matched-ultra-linstep2+dense-BOSS`; production `eff`; recenter tolerance 0.005; protocol and invariants committed |
| A2 | ΛCDM local dense reference minimum | 🚀 MAJOR CLOSED | recenter-clear exact stencil, positive-definite local Hessian, accepted-score point explicitly frozen | accepted local score `1049.966118347761`; repeated dense Hessian PD and recenter-clear |
| A3 | RTK Stage-4D3 interior local minimum | 🚀 MAJOR CLOSED | current center recenter-clear; all negative coarse modes exact-ray falsified if present; two adjacent accepted stencil scales PD and each best improvement ≤0.005 | current base and half stencils are both recenter-clear and PD; `N5_BASE_AND_HALF_STENCIL_PASS`; half run `32133215190`, artifact `9328770791` |
| A4 | Independent clean-room reproduction of both accepted minima | 🚀 MAJOR CLOSED | fresh-tree paired RTK+ΛCDM replay at exact accepted-score params, locked environment, each score reproduced within 2e-6 and target fingerprint validated | run `32148894768`, artifact `9329042339`; RTK, ΛCDM and delta replay errors are exactly `0.0` in the recorded doubles; `INDEPENDENT_FRESH_TREE_REPLAY_PASS` |
| A5 | Final frozen matched raw ΔS | 🚀 MAJOR CLOSED | A3 + A4 pass, then freeze `S_RTK - S_LCDM` from validated accepted points/replay; no stale target | `S_RTK=1050.249912429787`, `S_LCDM=1049.966118347761`, final raw local `ΔS=+0.2837940820259064`; replayed identically |
| A6 | Formal model-selection statistics | 🔴 OPEN | only after A5 and separately preregistered statistic-specific parameter/prior/sample conventions | ✅ A6a AIC is closed under `POSTFREEZE_MODEL_SELECTION_PROTOCOL_v1`: `ΔAIC=+2.2837940820259064`; BIC awaits a defensible composite-likelihood `N_eff`; Bayes awaits preregistered normalized priors/evidence integration; no sigma/Wilks conversion authorized |

## B. Likelihood, observables, and robustness

| ID | Major item | Status | Strict closure condition | Current evidence / next gate |
|---|---|---|---|---|
| B1 | Planck+Pantheon+BOSS implementation consistency | 🚀 MAJOR CLOSED | formulas/units/data ordering independently audited; exact component replay reproducible; BOSS conventions externally cross-checked | component replay and BOSS convention/unit audits passed |
| B2 | Linear RTK observable fingerprint | 🚀 MAJOR CLOSED | reproducible background/CMB/P(k)/growth signature atlas at matched current centers with hardened primordial inputs and exact requested redshifts | signature atlas + cross-anchor decomposition completed |
| B3 | Source of present BOSS pressure | 🚀 MAJOR CLOSED | correlated residual analysis identifies geometry/growth directions and rules out λ_D and linear RSD-scale mapping as dominant explanations | BOSS PCA mode identified; λ_D scan and fσ8(k) grid show negligible explanatory power |
| B4 | Minimal-neutrino robustness | 🟡 RUNNING | separate paired, explicitly non-frozen robustness comparison with mν=0.06 eV and matched reoptimization for both models after massless freeze | ✅ fixed-current-center sensitivity is closed (run `32144865816`); first paired seed run `32173665110` failed before science because reusable core inherited worker argv as Planck path; module-safe fix and bounds hardening landed; paired rerun `32190997977` currently performs exact RTK+ΛCDM seed reoptimization after both import smoke tests passed |
| B5 | Survey-level/nonlinear RSD robustness | 🔴 OPEN | model-specific survey-window/AP/nonlinear-template treatment or a justified bound showing compressed BOSS likelihood is adequate at required precision | linear k-dependence is tiny, but survey-template robustness remains open |
| B6 | Early-universe / BBN robustness | 🟡 RUNNING | demonstrate valid background/perturbation behavior and abundance/expansion constraints through relevant early epochs under a declared data/protocol set | final-center same-parameter RTK/LCDM background diagnostic reaches very high redshift and converges strongly; abundance-level protocol is frozen, but a pinned BBN network/self-test + RTK H(T) injection + abundance refinement + preregistered observational comparison are still required |
| B7 | Tensor/GW propagation and standard-siren sector | 🚀 MAJOR CLOSED | derive/verify implemented late-time tensor propagation equation and propagation observables; execute reproducible diagnostic at the final frozen RTK center; explicitly exclude unsupported primordial-tensor claims | pinned model=2 source gives standard `k^2 h` term (`cT=c`) and modified friction; final-center run `32149794234`, artifact `9329259757`, predicts `dL_GW/dL_EM=0.95719` at z=0.51 and `0.94423` at z=1; primordial tensor generation is outside this closure |
| B8 | Nonlinear/local-gravity/compact-object phenomenology | 🔴 OPEN | derive applicable regime and pass declared local/nonlinear consistency tests | open |

## C. Theory / EFT consistency

| ID | Major item | Status | Strict closure condition | Current evidence / next gate |
|---|---|---|---|---|
| C1 | Classical background sign/stability domain | 🚀 MAJOR CLOSED | required background algebraic signs and DBI margins positive over declared physical scan | Q1 audit passed |
| C2 | Healthy local quadratic preferred-frame scalar EFT representative | 🚀 MAJOR CLOSED | exact implemented linear dispersion reconstructed by local quadratic representative; kinetic/gradient Hamiltonian positive over tested physical domain; no higher time derivative in representative | constructive Q3 audit passed |
| C3 | Route-A1 nonlinear EFT symmetry class | 🚀 MAJOR CLOSED | symmetry/derivative assumptions explicitly selected as a research postulate rather than inferred from linear CLASS | Route A1 frozen and documented |
| C4 | Route-A1 cubic operator basis through D≤4 | 🚀 MAJOR CLOSED | complete IBP-reduced basis enumerated and symbolically audited | four-operator basis; CI passed |
| C5 | Long-wave conditional P(X) thermodynamic/cubic reconstruction | 🚀 MAJOR CLOSED | exact thermodynamic identities and conditional c1,c2 relations proved symbolically with scope restrictions explicit | theorem CI passed |
| C6 | Finite-k nonlinear coefficient identifiability | 🚀 MAJOR CLOSED | prove whether c3,c4 / dispersive nonlinear coefficients are derivable from background+linear target | no-go proved: they are not identifiable without an added nonlinear completion hypothesis; D5 basis enumerated |
| C7 | Full coupled metric + causal RT + Khronon nonlinear DOF/ghost theorem | 🔴 OPEN | explicit valid nonlinear formulation for the coupled system plus constraint/DOF analysis showing absence (or presence) of unwanted propagating modes; causal nonlocal auxiliaries must not be miscounted as free local fields | reduced scalar result is insufficient; RT sector lacks a standard closed-form local action in the present implementation |
| C8 | Physical strong-coupling scale / EFT cutoff | 🔴 OPEN | choose/derive a nonlinear completion, canonically normalize full relevant interactions, identify lowest physical breakdown scale and verify hierarchy with cosmological modes | linear M_K/k_star is proven not to determine the cutoff |
| C9 | Radiative stability / counterterm closure / naturalness | 🔴 OPEN | declared nonlinear EFT/operator content plus loop power counting and stability of required hierarchies | open |

## D. Reproducibility and software proof chain

| ID | Major item | Status | Strict closure condition | Current evidence / next gate |
|---|---|---|---|---|
| D1 | Locked production environment | 🚀 MAJOR CLOSED | CLASS/Pantheon commits, Planck archive SHA, NumPy/SciPy/Python/likelihood version, gauge, nonlocal branch mapping, neutrino baseline and IC semantics recorded | `rtk/reproducibility_lock.json` schema 8; clean-room Python is explicitly pinned to 3.12.3 |
| D2 | Failure/cache/retry safety | 🚀 MAJOR CLOSED | failed/transient evaluations never memoized as successful objective walls; deterministic exact retries and regression tests pass | success-only cache and retries audited/CI-tested |
| D3 | Crash-idempotent heavy dispatch | 🚀 MAJOR CLOSED | serialized control-plane and tested no-duplicate behavior across dispatch crash window | idempotent dispatch guard + tests; no duplicate base/half worker occurred |
| D4 | Proof-artifact identity/provenance | ✅ SUBGATE CLOSED | current proof artifacts require exact center/objective/stencil fingerprints and locked runtime provenance; all active proof families should be covered consistently | validator checks runtime sidecars when present: Python, NumPy, SciPy, clipy-like, Planck SHA in addition to canonical fingerprints and CLASS/Pantheon; active-main workflow/live-lock consistency audit added; eighth-scale eigenray proof family is now included |
| D5 | Autonomous decision-tree regression coverage | 🚀 MAJOR CLOSED | negative-eigenray, half/quarter, final replay and dispatch transitions covered by synthetic regression tests; no known logical acceptance race | generalized `1→1/2→1/4→1/8` fallback is now wired; every non-PD scale including 1/8 requires same-scale exact-ray falsification before progression/exhaustion; eighth-ray workflow and locked provenance validation added; synthetic terminal-ray/recenter/exhaustion/N5 regressions pass; static invariants lock the behavior; orchestrator runs `32194448452` and `32194624153` passed the complete control-plane suite |

## E. External scientific validation

| ID | Item | Status | Exact external closure condition |
|---|---|---|---|
| E1 | Independent implementation/reproduction by another group/codebase | `EXTERNAL_BLOCKER` | an independent team reproduces core RTK equations and matched observational results without using this repository as its executable implementation |
| E2 | Peer-reviewed publication | `EXTERNAL_BLOCKER` | manuscript accepted after external peer review |
| E3 | Prospective observational discrimination | `EXTERNAL_BLOCKER` | a preregistered distinctive RTK prediction is tested by independent new/held-out observations |

## Autonomous stopping rule

The autonomous research loop must **not** stop because a single workflow, paper draft, or local fit completes. It may declare the internally achievable research frontier exhausted only when every internally achievable major row above is 🚀, or when a remaining row has been rigorously reclassified as `EXTERNAL_BLOCKER` with a precise external closure condition.

Whenever `research/state/current.json` materially changes a major proof status, update this matrix conservatively. A weaker claim may be downgraded if later evidence invalidates an earlier gate.
