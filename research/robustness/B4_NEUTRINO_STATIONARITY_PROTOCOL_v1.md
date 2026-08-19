# B4 minimal-neutrino multiscale stationarity protocol v1

Status: **FROZEN BEFORE CONSUMING NEUTRINO HESSIAN RESULTS**.

This protocol is downstream of `RTK_MINIMAL_NEUTRINO_REOPTIMIZATION_PROTOCOL_v1.md` and the paired seed run `32190997977`. It is a separate robustness proof and must not modify the already frozen massless A1-A5 result.

## Frozen objective and targets

Objective: `matched-ultra-linstep2+dense-BOSS+nu0p06-additive-v1`.

Production mapping: `eff`; record `k01` separately. Recenter tolerance: `0.005`.

The exact candidate centers, seed scores, artifact IDs/digests, neutrino convention and proof steps are frozen in `research/robustness/b4_neutrino_stationarity_targets_v1.json` before any neutrino Hessian is consumed.

## Base Hessian

For RTK use coordinates `[loglam,h,Ob,Om,As,ns,zre]`; for LCDM use `[h,Ob,Om,As,ns,zre]`. The base physical finite-difference steps are deliberately inherited from the already frozen massless stationarity proof for the corresponding model; they are not tuned after seeing the neutrino curvature.

Every likelihood point uses the same pinned CLASS/Pantheon/Planck/runtime environment as the massless comparison, with only the frozen minimal-neutrino block changed. Exact-float success-only evaluation and identical-point retries are mandatory.

## Decision rules

1. At each full Hessian scale, compute exact center, complete symmetric Hessian stencil, exact best point among all evaluated stencil/Newton-trust candidates, Hessian eigenvalues/eigenvectors, and `best_improvement = S_center-S_best_exact`.
2. If `best_improvement > 0.005`, the current center is not accepted. Recenter to the exact best point and restart the model's coordinate-poll -> base-Hessian chain under the same neutrino objective.
3. If a Hessian is non-PD, it is not an interior-minimum proof. Every strictly negative mode must be falsified with the exact frozen likelihood along that same-scale physical eigenray before descending to a smaller stencil.
4. If the base Hessian is recenter-clear and PD, calculate the `1/2` Hessian. Two adjacent recenter-clear PD Hessian scales are required for the model's local interior-minimum stationarity certification.
5. If the base is non-PD but same-scale exact negative rays are recenter-clear, calculate the `1/2` Hessian and use the same adaptive adjacent-scale ladder logic as Stage4D3 (`1`, `1/2`, `1/4`, `1/8`) if necessary. A ray-clear non-PD scale by itself never proves a minimum.
6. `eff` is the production objective. `k01` is reported independently and must not select an `eff` center.
7. Artifact identity must match the exact frozen B4 target center/objective/model/stencil scale and locked runtime/upstream provenance before parsing.

## B4 closure after stationarity

Even if both model stationarity gates pass, B4 remains open until a paired fresh-tree replay of both final neutrino robustness accepted-score parameter points reproduces each score within `2e-6`. Only then may `Delta S_nu0p06 = S_RTK_nu0p06 - S_LCDM_nu0p06` be frozen.

No global-minimum, Bayes, sigma/Wilks, or replacement-of-massless-baseline claim follows from this robustness proof.
