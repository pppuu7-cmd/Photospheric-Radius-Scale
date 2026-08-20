# RTK / DBI-Khronon — canonical autonomous research methodology

Status: **CANONICAL PROCESS DOCUMENT**  
Canonical state branch: `rtk-class-build`  
Repository: `pppuu7-cmd/Photospheric-Radius-Scale`

<!-- AUTO-ITERATION-METADATA:BEGIN -->
Last methodology synchronization: `2026-08-20T21:55:02Z` / `2026-08-21T00:55:02+03:00 Europe/Helsinki`  
Last synchronized iteration: `172` (`research/iterations/000172_20260820T215502Z.json`)  
Scientific source HEAD before iteration commit: `d2f77147ac8b80cb3cf116a80c0b4626c76f1e74`  
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

## 13. Route-B quadratic-completion methodology (added 2026-08-20)

The Route-B BPS/healthy-Horava completion program must preserve these additional invariants:

1. **Use the production RTK scale dictionary, not a parameter-name guess.** From `rtk/khronon_background.c`, the physical rational-pole target is `C(a)=c_a^2(a)` and `Mdisp(a)=M_K(a)`, with the comoving transition `k_*(a)=a M_K(a)`. `lambda_D` affects these quantities through the background closure and must never be identified directly with `Mdisp`.
2. **Use the same positive full-CLASS gamma root as the frozen cosmological point.** A stand-alone guessed or silently floored gamma is not valid scale provenance.
3. **Keep unconstrained and constrained strong-coupling statements separate.** The unconstrained inverse family may maximize `Lambda_p` at order-one `alpha` or `lambda-1`; this cannot be promoted to a phenomenologically allowed completion until explicit low-energy caps are applied.
4. **For abstract caps `0<alpha<=alpha_cap<2` and `0<ell=lambda-1<=ell_cap`, use the exact cap inversion** `h_alpha=3 alpha_cap C/(2-alpha_cap)` and `h_ell=3 ell_cap/(2+3 ell_cap)`. The capped optimum is `min(h0(C),h_alpha,h_ell)`, where `h0(C)` is the previously derived unconstrained optimum. Do not replace this analytic gate by an avoidable parameter scan.
5. **Finite-range accuracy is evaluated in physical momentum.** For a CLASS comoving mode `k`, use `p=k/a`. The frozen matched likelihood harness uses `P_k_max_h/Mpc=5.0`; a coverage gate spanning the production dense grid therefore evaluates the physical maximum separately at every redshift.
6. **Separate hierarchy requirement from Planck-unit convention.** First compute the dimensionless required `M_P/M_K` implied by the exact BPS cutoff theorem. Only a separate, sourced convention/unit audit may insert a numerical Planck hierarchy.
7. **Workflow launch is never theorem validation.** SymPy theorem workflows and state-driven scale workflows remain `CANDIDATE` until their completed artifacts/logs contain the expected classification and all fail-closed checks pass.
8. **Keep completion non-claims explicit.** Quadratic pole matching plus low-energy cutoff control does not establish off-shell source/residue equivalence, nonlinear constraint/DOF closure, radiative stability, or matter-sector Lorentz safety.

Manual theory checkpoint for this addition: `research/checkpoints/RTK_ROUTE_B_ITERATION_20260820T011619Z.md`.

## 14. Route-B matter-normalization and low-energy phenomenology guards (added 2026-08-20)

1. **Distinguish the bare BPS `M_P` from the scale inferred from measured `G_N`.** The BPS strong-coupling formulas use the bare coefficient in the gravitational action. Once a matter metric is selected, the relation to measured Newton gravity depends on low-energy couplings. Never multiply a bare-`M_P` cutoff by a numerical Planck mass without this normalization step.
2. **The pure-gravity pole embedding does not fix the matter-metric parameter `beta`.** Generic physical-cutoff statements therefore require a separate matter-coupling dictionary. Any `beta=0` result is conditional and must be labeled as such.
3. **For the conditional `beta=0` minimal/universal branch**, use `Mbar_N=(8 pi G_N)^(-1/2)=M_P sqrt(1-alpha/2)`. Reoptimizing at fixed measured `G_N` changes the unconstrained cutoff regime boundary from the bare-`M_P` value `C=1/3` to the physical value `C=1/5`.
4. **For fixed `G_N` plus abstract alpha/ell caps**, use `h_opt=min(h0_Newton(C),h_alpha,h_ell)`, with `h_alpha=3 alpha_cap C/(2-alpha_cap)` and `h_ell=3 ell_cap/(2+3 ell_cap)`. Do not reuse the bare-`M_P` optimizer after inserting measured-Newton normalization.
5. **Production RTK satisfies `0<C=c_a^2<1` analytically.** With `C=x/[s^2(s+x)]`, `s=sqrt(1+lambda_D x^2)`, the positive denominator margin is `s^3+lambda_D x^3`. This domain fact should be used before any numerical scan.
6. **When using the sourced generic low-energy benchmark** summarized by Barausse arXiv:1907.05958 (`|beta|~<=1e-15`, `|alpha|~<=1e-7` for the generic branch, positive `lambda` only weakly bounded around `0.01--0.1`), keep it distinct from the alternative tuned branch. For production `0<C<1`, the `alpha=1e-7` benchmark is analytically the active cap before either `ell=0.01` or `0.1`.
7. **Do not convert the tuned relation into an exact exclusion.** Treating `lambda≈alpha/(1-2alpha)` as equality makes the selected inverse family intersect the central curve only at `C=1`, while production has `C<1`; however the observational relation is approximate, so only the exact central equality is excluded, not its allowed finite band.
8. **Compact-object regularity is a separate UV-sensitive gate.** The selected finite-h rational family has `alpha>0`; its only `alpha->0` limit is `h->0`, where the low-energy cutoff collapses. This does not prove the higher-spatial-derivative completion has pathological black holes. It requires a dedicated selected-UV-operator compact-object calculation.
9. **Keep convention mapping explicit.** On the `beta=0` branch, comparison of the ADM actions gives `ell=lambda_BPS-1=lambda_modern`; do not mix the old BPS `lambda` with the modern low-energy parameter without subtracting the GR value.

Manual checkpoint: `research/checkpoints/RTK_ROUTE_B_MATTER_NORMALIZATION_20260820T013203Z.md`.
