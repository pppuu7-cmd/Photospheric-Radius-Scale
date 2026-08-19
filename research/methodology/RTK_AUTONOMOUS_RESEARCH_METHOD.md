# RTK / DBI-Khronon — canonical autonomous research methodology

Status: **CANONICAL PROCESS DOCUMENT**  
Canonical state branch: `rtk-class-build`  
Repository: `pppuu7-cmd/Photospheric-Radius-Scale`

<!-- AUTO-ITERATION-METADATA:BEGIN -->
Last methodology synchronization: `2026-08-19T20:55:02Z` / `2026-08-19T23:55:02+03:00 Europe/Helsinki`  
Last synchronized iteration: `133` (`research/iterations/000133_20260819T205502Z.json`)  
Scientific source HEAD before iteration commit: `ed64586043f75bdf2177b808c960a97c9b692477`  
Objective: `matched-ultra-linstep2+dense-BOSS`  
Objective configuration SHA256: `754edb2ff5380eff314867b0ecb1a23a8b861a69f7e46070c4b8251c98573666`  
Explicit frozen objective fingerprint, if available: `754edb2ff5380eff314867b0ecb1a23a8b861a69f7e46070c4b8251c98573666`  
Chronology source: `research/chronology/RTK_RESEARCH_CHRONOLOGY.jsonl`
<!-- AUTO-ITERATION-METADATA:END -->

## 1. Purpose

This document defines how RTK / DBI-Khronon research is continued, audited, accepted, rejected, and handed off. Chat history is a discovery source only. Scientific state must survive complete loss of all chats.

The repository is authoritative. A result from an old conversation may be useful, but it cannot override a newer repository state, a frozen protocol, an objective fingerprint, a reproducibility lock, or a validated artifact.

## 2. Mandatory source-of-truth order

When records disagree, use this hierarchy:

1. `research/state/current.json` on `rtk-class-build` — live numerical/control state.
2. Frozen protocols in `research/robustness/`, `rtk/*PROTOCOL*.md`, and the reproducibility lock.
3. Validated workflow artifacts and exact run IDs.
4. `research/iterations/*.json` — deterministic per-iteration journal.
5. `research/chronology/RTK_RESEARCH_CHRONOLOGY.jsonl` — append-only cross-iteration chronology.
6. `research/chronology/RTK_RESEARCH_CHRONOLOGY.md` — human-readable milestone chronology.
7. Historical checkpoints / recovered chats — provenance and rediscovery only.

Never promote an older number merely because it is lower or appeared in a later-written chat message.

## 3. Mandatory chronology rule for every iteration

Every autonomous research iteration must persist all of the following before its state commit:

- integer iteration number;
- UTC timestamp in ISO-8601;
- Europe/Helsinki timestamp with explicit offset;
- stage before/after the decision when available;
- exact action list and observations from `research/iterations/...json`;
- Git commit SHA of the scientific source tree used by the iteration;
- objective name and objective fingerprint when available;
- referenced GitHub Actions run IDs / workflow names when present;
- whether a run failure is computational/infrastructure or scientific;
- which acceptance gates changed state;
- next dispatch/request, if any;
- warnings that restrict interpretation.

Chronology is **append-only**. Existing historical entries must not be silently rewritten. Corrections are added as later entries that identify the superseded claim.

The methodology itself must also be touched on every iteration by updating the auto-metadata block above. This makes a stale methodology mechanically detectable.

## 4. Scientific claim classes

A question is closed only by one of these classes:

1. **Analytic closure** — derivation/theorem with assumptions and domain stated.
2. **Numerical closure** — regression-tested result with precision/domain/provenance controls.
3. **Observational closure** — inference on one frozen common objective with matched model treatment.
4. **Negative closure** — rigorous demonstration that a requested extension/claim is inconsistent, non-identifiable, or outside the validated domain.

A lower objective or chi-squared alone closes none of these.

## 5. Numerical acceptance rules

### 5.1 Common rules

- Never recenter without an **exact** objective improvement beyond the frozen recenter threshold.
- Keep `eff` and `k01` distinct. One mapping cannot certify the other.
- Do not equate workflow `success` with scientific `PASS`; parse the result artifact.
- Do not advance from failed/incomplete runs.
- Compute/infrastructure failure is not scientific falsification.
- Never claim a global minimum from a local optimizer or Hessian.
- Never make AIC/BIC/Bayes/Wilks/sigma/preference claims before the corresponding matched objective and minimum requirements are frozen and satisfied.

### 5.2 Stage4D1 / fixed-lambda profile protocol

For each fixed `lambda_D` and independently for `eff` and `k01`:

1. use exact full-precision cache identity or no cache;
2. run deterministic correlated starts when recentering is required;
3. run two exact coordinate-poll levels;
4. any exact downhill gain beyond threshold => recenter and repeat;
5. only a stabilized center proceeds to the 73-point gradient/Hessian stencil;
6. require explicit gradient tolerance and positive-definite local Hessian before a local-minimum claim;
7. independently test correlated descent/ray directions when prescribed by the frozen protocol.

### 5.3 Stage4D3 multiscale local-minimum protocol

A strong local interior-minimum certificate requires adjacent scales:

1. base-scale exact improvement `<= 0.005` after any necessary recentering;
2. base Hessian positive definite;
3. independent half-scale (`0.5`) stencil;
4. half-scale exact improvement `<= 0.005`;
5. half-scale Hessian positive definite and qualitatively consistent;
6. configured gradient gate passes;
7. only then may the tested point be called an interior local minimum on the tested multiscale stencil.

If a repeatable negative/flat `log(lambda_D)` mode appears, trace/profile that direction instead of forcing a minimum classification.

## 6. Implementation invariants recovered from earlier RTK Research Loop / Auto-Continue / Auto-Advance work

These are permanent guardrails unless an explicit later theorem/implementation supersedes them:

- Cache keys must use the full-precision parameter tuple; never round dimensional `A_s` to 12 decimal places.
- Use modern primordial inputs `A_s` and `n_s`. Historical `A_s_ad` / `n_s_ad` amplitude results are not production-valid.
- Physical RTK/Khronon branch has `Omega_cdm = 0`; any old CDM slot used as storage must be explicitly documented as non-physical storage.
- Khronon `gamma` normalization uses a positive bracketed root. No silent `gamma > 0 ? gamma : tiny` fallback.
- Preserve Khronon perturbation variables when CLASS reconstructs perturbation vectors at approximation switches.
- Nonlocal RT synchronous-gauge support must not be claimed unless actually implemented and regression-tested.
- Unsupported Khronon isocurvature modes must fail closed; they are not silently replaced by CDM modes.
- RT auxiliary fields represent the intended retarded history and are not a freely adjustable dark-energy fluid.
- Reusable likelihood modules must never inherit a worker's arbitrary `sys.argv` as the Planck path; use explicit `RTK_PLANCK_DATA` / frozen path semantics.
- Out-of-bounds optimization proposals are rejected and logged, never silently clipped into a different physical point.
- Failure results are not inserted into the success cache.

## 7. Preserved analytic results / corrections

- Correct transition-radius estimate: `r_C ~= (r_M / M_K^2)^(1/3)`.
- The older `[M_K^2 r_M]^(1/3)` expression is dimensionally wrong and must not be resurrected.
- `r_C ∝ M_b^(1/6)`.
- Early DBI branch: `r_C(a) ∝ a^3`, equivalently `r_C(z) ~= r_C0 (1+z)^(-3)` in that regime.
- Controlled stationary weak-field limit gives small leading slip (`Phi ~= Psi`); this is not a substitute for a full lensing likelihood/cluster analysis.
- Leading controlled external-condition sensitivity: `d ln g / d p_ext ~= -(1/6)(r/r_C)^3`; a 1% criterion gives approximately `r < 0.391 r_C`.
- Linear cosmological environment cannot be inserted directly as a galaxy's external field without filtering/nonlinear environmental modeling.

## 8. Current frozen matched comparison

Production objective: `matched-ultra-linstep2+dense-BOSS`  
Production mapping: `eff`  
Objective fingerprint from independent replay: `754edb2ff5380eff314867b0ecb1a23a8b861a69f7e46070c4b8251c98573666`

Fresh-tree replay-certified accepted local score points:

- LCDM: `S_eff = 1049.966118347761`.
- RTK: `S_eff = 1050.249912429787`.
- Raw local matched difference: `Delta S_eff = +0.2837940820259064` (`RTK - LCDM`).
- Independent replay run: `32148894768`, recorded replay error `0.0`.

Interpretation: reproducible **matched local raw-objective comparison only**. Not global optimality and not significance/evidence/model-preference by itself.

## 9. Current robustness frontier

### B4 — minimal standard neutrino robustness

Frozen sector includes `N_ur=2.0328`, `N_ncdm=1`, `m_ncdm=0.06 eV`, `T_ncdm=0.71611`, `deg_ncdm=1.0`.

Required closure chain: paired reoptimization -> exact poll/recenter logic -> matched multiscale stationarity -> independent paired replay. A seed optimizer endpoint is never a certificate.

### B6 — BBN

Background/`H(T)` mapping evidence is not the same as abundance closure. Required chain: pinned AlterBBN source -> standard self-test -> explicit RTK `H(T)` injection -> paired reference/RTK nuclear network -> numerical refinement -> preregistered observational abundance comparison.

### B9 — Planck standalone lensing

The chosen B9-v1 lensing product and adapter contract are frozen before cosmological scoring. Required chain: adapter contract -> paired RTK/LCDM reoptimization -> stationarity -> independent replay.

### B10 — lambda-tail identifiability

Fixed-shared tail flatness is diagnostic only. Lambda identifiability requires the preregistered profiled nuisance reoptimization at the frozen tail factors and the subsequent decision gates.

## 10. Parallel research allocation

While expensive jobs run, do not duplicate them. Use spare work for:

- source/provenance audits;
- analytic consistency checks;
- protocol freezing before seeing results;
- regression tests;
- EFT/PPF/khronometric translation derivations;
- DOF/stability/strong-coupling analysis;
- observable signature/derivative atlas preparation.

## 11. Recovery after total chat loss

1. Read this methodology.
2. Read `research/state/current.json`.
3. Read the newest `research/iterations/*.json`.
4. Read `research/chronology/RTK_RESEARCH_CHRONOLOGY.jsonl` and the human milestone chronology.
5. Inspect live/just-completed Actions and their artifacts.
6. Read only the frozen protocol relevant to the next gate.
7. Never infer a result from a launch message or workflow conclusion alone.
8. Update chronology and this methodology metadata in the same iteration that changes state.

## 12. Change-control rule

Any future change to objective, dataset, precision preset, source tree, cache semantics, parameter mapping, stationarity threshold, or interpretation rule must be entered in chronology with timestamp and must create a new explicit provenance/fingerprint boundary. Cross-boundary absolute scores are non-comparable by default.
