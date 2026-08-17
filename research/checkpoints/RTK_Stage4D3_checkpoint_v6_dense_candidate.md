# RTK Stage 4D3 — checkpoint v6 dense-candidate frontier

## Scope

This checkpoint records the transition from the sparse BOSS navigation objective to the candidate production objective using exact-float cache semantics, matched-ultra CLASS settings with `l_linstep=2`, and dense BOSS redshift-growth sampling. It is a provenance checkpoint, not a model-selection claim.

## Round5 sparse-objective local geometry

Current Round5 center:

- lambda_D = 217225.01601516694
- h = 0.6904831253428524
- Omega_b = 0.046836300417955265
- Omega_m = 0.25300743080221694
- A_s = 2.0837288833768707e-9
- n_s = 0.9643603115669437
- z_re = 7.21843542110055
- S_eff = 1050.0338294787382
- S_k01 = 1050.0482111660676

At ultrafine 7D scale=0.0625, both mappings had positive-definite Hessians. The center was the best exact point among the 99-point stencil plus Newton proposal; the Newton proposal worsened. The explicit finite-difference gradient gate remained above tolerance, so an independent correlated-ray gate was required.

Corrected dual-mapping correlated-ray run `31981199050` evaluated symmetric exact rays along the inferred descent direction. For both `eff` and `k01` the best exact point was the center itself, with exact improvement 0.0 against a recenter threshold of 0.005. Therefore no sparse-objective recenter is justified by the residual gradient.

## Dense BOSS current-center audit

Run `31981316837` completed successfully at matched-ultra CLASS precision.

Sparse center:

- S_eff = 1050.3892614534907
- S_k01 = 1050.4035848303351
- chi2_BOSS_eff = 7.55555472496795
- chi2_BOSS_k01 = 7.569878101812414

Dense center:

- S_eff = 1050.4261151803064
- S_k01 = 1050.4263548358153
- chi2_BOSS_eff = 7.592408451783703
- chi2_BOSS_k01 = 7.592648107292614

Dense minus sparse:

- Delta S_eff = +0.036853726815707
- Delta S_k01 = +0.022770005480197
- Delta Planck = 0
- Delta Pantheon = 0
- Delta r_d = 0

The production-objective change is therefore entirely in the BOSS growth term at this point and is larger than the 0.005 local acceptance tolerance. Sparse-objective local stationarity cannot be promoted directly to a final production-objective certificate.

## Candidate objective fingerprint

Workflow `31981568685` completed successfully. The candidate objective is fingerprinted with exact cache semantics, matched-ultra CLASS overrides, dense BOSS z-grid, CLASS/RTK source hashes, likelihood-core hashes, and data/covariance hashes. The objective remains a candidate freeze until RTK and LCDM are locally reoptimized on it.

## Dust-boundary coordinate

The symbolic CI audit proved the leading physical large-lambda deviation coordinate is

`u = 1/lambda_D`.

Thus finite-lambda versus dust-boundary classification must be performed as an approach to `u=0`, not merely by comparing two large lambda values.

A six-lambda matched-ultra+dense fixed-lambda nuisance-poll matrix is active at:

- 217225.01601516694
- 300000
- 1e6
- 1e7
- 1e8
- 1e9

The initial matrix exposed an argv/Planck-path interface bug, not a likelihood failure. The science script was fixed in `rtk-class-build` commit `0b411b293cf8897eb67c8024593052cadc8b5bfb`; the clean matrix relaunch is run `31981673256`.

## Matched LCDM control

A six-dimensional matched-ultra+dense local nuisance poll is active as run `31981604507` at the current production-branch LCDM partial-best point. This is required before any contemporaneous RTK-minus-LCDM score difference can be interpreted.

## Current acceptance status

- ✅ Exact Planck runtime/self-tests, Pantheon/BOSS covariance algebra, exact-float cache semantics and repeatability are established.
- ✅ Round5 sparse-objective ultrafine Hessians are positive definite in both mappings.
- ✅ Independent corrected correlated-ray gate found no exact descent and forbids sparse-objective recenter.
- ✅ Differential CLASS precision convergence is established for deep RTK descents.
- ✅ Dense BOSS systematic is directly measured at the current Round5 center.
- ✅ Candidate matched-ultra+dense objective is cryptographically fingerprinted.
- ✅ Physical dust-boundary coordinate `u=1/lambda_D` is symbolically verified.
- 🟡 Clean dense-objective dust-boundary nuisance poll is active.
- 🟡 Matched dense-objective LCDM nuisance poll is active.
- ❌ Dense-objective RTK local stationarity has not yet been re-certified after any nuisance recenter indicated by the current-lambda poll.
- ❌ Finite-lambda interior optimum versus `u=0` is not yet established.
- ❌ RTK and LCDM are not yet both locally reoptimized on one frozen final objective.
- ❌ No final significance, posterior preference, AIC/BIC interpretation, Bayes factor or observational model-preference claim is valid yet.

## Decision rule

1. Use the current-lambda dense nuisance poll to determine whether the Round5 center must be recentered under the candidate objective.
2. Compare the fixed-lambda nuisance-poll envelope as a function of `u=1/lambda_D` to determine whether the dust direction is improving, worsening, or flat.
3. If the current dense center changes materially (>0.005), recenter before launching a dense 7D Hessian/stationarity certificate.
4. Recenter/refine LCDM on the same fingerprinted objective.
5. Only after both models are locally certified on one objective may RTK-minus-LCDM score differences be used for model-comparison diagnostics.
