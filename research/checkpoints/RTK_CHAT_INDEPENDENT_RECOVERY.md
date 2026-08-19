# RTK / DBI-Khronon — chat-independent research recovery guide

Last reconciled: 2026-08-19.

## Purpose

This file is the first recovery document to read when continuing the RTK / DBI-Khronon research without access to any previous ChatGPT conversation. It consolidates the useful scientific and numerical invariants recovered from earlier research chats, archived methodology documents, Stage4D1/Stage4D3 checkpoints, and the live production state.

Do not use a chat transcript as the source of truth. The repository is authoritative.

## 1. Source-of-truth hierarchy

Use this order when two records disagree:

1. `rtk-class-build:research/state/current.json` — live machine-readable production state and objective provenance.
2. `rtk-class-build:research/runtime/actions_index.json` — recent monitored GitHub Actions runs.
3. Frozen protocol/result files under `research/robustness/`, `research/protocols/`, `research/checkpoints/`, and workflow artifacts.
4. This recovery guide — human-readable index and safety rules.
5. Historical Stage4D1/Stage4D3 checkpoints — provenance/navigation only when superseded by the production state.

`main` is currently the control-plane/documentation branch used to launch many workflows. Numerical production workflows commonly check out `rtk-class-build`. Never mix absolute scores from different source trees, objective fingerprints, precision presets, or sparse/dense BOSS definitions.

## 2. Current frozen comparison baseline

The production objective is:

- name: `matched-ultra-linstep2+dense-BOSS`
- production BOSS mapping: `eff`
- objective fingerprint: `754edb2ff5380eff314867b0ecb1a23a8b861a69f7e46070c4b8251c98573666`
- exact-float cache semantics: `clean-room-exact-float-v2`
- CLASS upstream commit: `36cf283628c4a3330ec9fd3d84239bf775f77317`
- dense BOSS redshift grid: `0.,0.25,0.30,0.34,0.36,0.37,0.38,0.39,0.40,0.42,0.47,0.49,0.50,0.51,0.52,0.53,0.55,0.57,0.59,0.60,0.61,0.62,0.63,0.65,0.70,0.75,1.0`
- recenter tolerance in the local proof protocol: `0.005` in `S`.

Independent fresh-tree replay of the frozen matched local minima passed exactly:

### LCDM accepted score point

- `S_eff = 1049.966118347761`
- `S_k01 = 1049.9661585330177`
- `h = 0.6782837587382693`
- `Omega_b = 0.04858764689799632`
- `Omega_m = 0.2611722579449536`
- `A_s = 2.1054040998203598e-9`
- `n_s = 0.9653185632254442`
- `z_re = 7.788312934950947`

### RTK accepted score point

- `S_eff = 1050.249912429787`
- `S_k01 = 1050.2501979467324`
- `lambda_D = 219457.5727136581`
- `h = 0.691103719964454`
- `Omega_b = 0.046800730927437424`
- `Omega_m = 0.2522864064078236`
- `A_s = 2.0877827951474356e-9`
- `n_s = 0.9645577770978523`
- `z_re = 7.328459220286924`

Current matched-local raw difference:

`Delta S_eff = S_RTK - S_LCDM = +0.2837940820259064`.

This is a reproducible **local raw-objective comparison only**. It is not evidence of a global optimum, significance, AIC/BIC preference, posterior preference, or Bayes factor.

## 3. Superseded numbers that must not be promoted back to current status

- Sparse-objective Stage4D3 value `S_eff ~= 1050.0338294787` is historical navigation only and must never be compared directly with the dense production LCDM score.
- Older v4/v5/v6 Stage4D3 values around `lambda_D ~ 2.8-3.0e5` are valuable provenance for locating the basin, but they are not the current frozen dense matched minimum.
- Old fixed-lambda Stage4D1 Powell convergence/stationarity claims were invalidated by a rounded-`A_s` cache bug. The individual expensive exact evaluations remain valid observations; optimizer convergence claims do not.
- Any absolute score lacking branch/source SHA, objective fingerprint, precision preset, and BOSS sampling provenance is non-comparable by default.

## 4. Numerical acceptance rules recovered from earlier methodology

A strong statement that a tested point is a local interior minimum requires the multiscale stationarity gate, not merely a low score:

1. If an exact poll/stencil finds improvement `> 0.005`, recenter at the improved exact point and rerun the base Hessian.
2. Base Hessian must be positive definite.
3. Repeat independently at half stencil scale (`scale = 0.5`).
4. Half-stencil exact improvement must be `<= 0.005`.
5. Half-stencil Hessian must remain positive definite and qualitatively consistent.
6. Only after the base + half gates pass may the repository label the point a local interior minimum on the tested multiscale stencil.
7. If a small negative `log(lambda_D)` curvature mode repeats, do not force a minimum claim; widen/profile the lambda direction.
8. A local optimizer or local Hessian can never establish a global minimum.

For fixed-lambda acceptance, keep `eff` and `k01` independent. Use exact full-precision cache keys, deterministic correlated starts when recentering is needed, a two-level coordinate poll, and a 73-point Hessian/gradient stencil before stationarity claims.

## 5. Critical implementation invariants recovered from older work

These are requirements, not optional historical notes:

- Never round dimensional `A_s` in a likelihood cache key. Use a full-precision serialized/binary parameter tuple or no cache.
- Primordial inputs in the RTK CLASS path are the modern `A_s` and `n_s`. Historical use of `A_s_ad` / `n_s_ad` produced incorrect amplitudes/likelihoods and required reruns.
- Physical RTK/Khronon branch has `Omega_cdm = 0`; any reused upstream CDM slot must be explicitly documented as storage rather than physical CDM.
- Solve the Khronon `gamma` normalization with a positive bracketed root. Do not use a silent `gamma > 0 ? gamma : tiny` fallback.
- Preserve Khronon perturbation variables when CLASS recreates perturbation vectors during approximation switches.
- Do not claim full synchronous-gauge support for the nonlocal RT model unless explicitly implemented and tested.
- Khronon isocurvature modes are not silently replaced by CDM isocurvature modes; unsupported modes must fail closed.
- RT auxiliary fields encode retarded history with the intended deep-radiation initial conditions; they are not a freely tunable dark-energy fluid.

## 6. Recovered analytic/physical facts worth preserving

- Correct transition-radius estimate:
  `r_C ~= (r_M / M_K^2)^(1/3)`.
  The older expression `[M_K^2 r_M]^(1/3)` is dimensionally wrong and must not be reused.
- Scaling: `r_C proportional to M_b^(1/6)`.
- Early DBI scaling: `r_C(a) proportional to a^3`, equivalently `r_C(z) ~= r_C0 (1+z)^(-3)` in that regime.
- In the controlled stationary weak-field limit, the leading gravitational slip is small (`Phi ~= Psi`), so the lensing potential inherits the same leading MOND + mass structure. This does **not** replace a full galaxy-galaxy/cluster lensing fit.
- Leading external-condition sensitivity in the controlled stationary regime:
  `d ln g / d p_ext ~= -(1/6) (r/r_C)^3`; a 1% criterion gives approximately `r < 0.391 r_C`.
- A linear cosmological environmental field cannot simply be inserted as the external field of an individual galaxy; spatial filtering, nonlinear environment, and environmental statistics are required.

## 7. Research frontier on 2026-08-19

### Closed / established

- Planck 2018 baseline likelihood runtime and component self-tests are operational.
- Exact-float cache-safe objective is operational.
- Pantheon covariance and BOSS covariance/convention checks are established.
- Matched local dense minima passed multiscale local certification and an independent fresh-tree replay.
- AlterBBN v2.2 source/runtime interface was pinned and self-tested.
- B6 entropy-aware RTK `H(T)` mapping completed successfully: the expansion-ratio deviation over the mapped BBN range is extremely small (`max |R_H-1| ~= 2.17e-9`), with nominal-vs-refined mapping error `~1.73e-12`. This is an expansion-history result only, not yet an abundance constraint.
- B9 standalone Planck R3 lensing likelihood interface loads successfully under the pinned likelihood stack. This is an interface result only, not yet an RTK-vs-LCDM lensing score.
- B10 fixed-shared lambda-tail reconnaissance completed and preregistered an asymptotic onset factor of `64`; fixed-shared tail flatness alone does not establish profiled lambda identifiability.

### Active at reconciliation

- B4 paired minimal-neutrino base stationarity: independent RTK and LCDM exact Hessian jobs.
- B10 paired fixed-lambda T2 profiles at factors `64` and `16384`: independent six-dimensional profiling on the preregistered large-lambda tail.

### Immediate next gates

1. B4: if base stationarity passes, run/finish the paired half-stencil gate; compare robustness only after both models satisfy the same protocol.
2. B10: use T2 profiled scores to decide whether lambda becomes identifiable after nuisance reoptimization. Do not interpret fixed-shared T1 flatness as a profile result.
3. B6: patch the common AlterBBN Hubble-rate path with the frozen RTK `R_H(T)` table and run paired `R_H=1` vs RTK abundance/refinement tests. Only then discuss BBN abundance impact.
4. B9: freeze a matched standalone-lensing robustness protocol before evaluating the first cosmological lensing score; then score RTK and LCDM on identical lensing data/runtime/provenance.
5. After robustness packages close, move to modern-data/posterior work only on a single frozen objective and source fingerprint.

## 8. Research-utility roadmap that remains open

Highest-value open theory/community tasks after numerical robustness closure:

- explicit degree-of-freedom/constraint count and quadratic stability analysis;
- no-ghost/no-gradient/hyperbolicity conditions and EFT cutoff;
- EFT/PPF/khronometric translation dictionary (`mu`, `Sigma`, `eta`, transition scales);
- CMB/matter/lensing residual and derivative atlas;
- early-time initial-condition/attractor validity map;
- GW propagation/standard-siren sector;
- quasistatic/nonlinear/spherical-collapse and local-gravity feasibility;
- one-command reproducibility benchmark and immutable objective/source fingerprints.

## 9. Recovery procedure after any interrupted session

1. Read this file.
2. Read `rtk-class-build:research/state/current.json` and verify its iteration/objective fingerprint.
3. Read `rtk-class-build:research/runtime/actions_index.json` and inspect any in-progress or just-completed monitored workflows.
4. For every newly completed run, inspect the artifact JSON before deciding the next action.
5. Update this recovery guide only when a result changes the scientific frontier or an invariant/guardrail.
6. Never infer success from a workflow being launched. Only a completed successful run with validated artifact can close a gate.
7. Keep expensive calculations non-duplicated: while long jobs run, use spare effort for independent audits, protocol freezing, analytic checks, provenance, or low-cost validation.

## 10. Definition of "closed"

A research question is closed only by one of:

- an analytic derivation/theorem with assumptions explicit;
- a numerical result with regression tests, precision/domain controls, and provenance;
- an observational inference on a frozen common objective;
- a rigorous negative result delimiting inconsistency or domain of validity.

A lower chi-squared or objective score by itself closes none of these categories.
