# Stage4D3 multiscale stationarity readiness

Date: 2026-08-18

Status: **infrastructure ready; base RTK Hessian run 32065998894 still active at the time of this checkpoint.**

## Required decision chain

The project must not certify an RTK interior local minimum from a single stencil. The enforced chain is:

1. parse the base 7D RTK Hessian only after artifact identity/provenance validation;
2. require base best exact improvement <= 0.005 before advancing;
3. dispatch `rtk-autonomous-dense-rtk-half-stencil.yml` at `RTK_STENCIL_SCALE=0.5`;
4. attach a newly discovered half-stencil run but do not parse it in the same iteration;
5. on the next control iteration, validate artifact identity/provenance before parsing;
6. require half-stencil best exact improvement <= 0.005;
7. require both base and half-stencil Hessians to be positive definite;
8. only then set `N5_BASE_AND_HALF_STENCIL_PASS` and allow `local_dense_accepted` interior-minimum wording.

If the half-stencil contains an exact downhill improvement >0.005, the gate recenters and restarts the axis/Hessian chain. If either Hessian is non-PD, the state remains `N5_CURVATURE_UNRESOLVED`.

## Half-stencil worker audit

Workflow: `.github/workflows/rtk-autonomous-dense-rtk-half-stencil.yml`

The worker is `workflow_dispatch` only and therefore cannot start merely because this checkpoint or other repository files change.

Frozen execution settings include:

- timeout: 240 minutes;
- `RTK_STENCIL_SCALE=0.5`;
- CLASS commit `36cf283628c4a3330ec9fd3d84239bf775f77317`;
- Pantheon commit `7eb29dc87ba223b4ec8457cd3cccba1216c36fb7`;
- Planck baseline SHA256 `0b73171e3acc671c28184466a45485a2d1c1d93676b832abdfe688c7b04024e6`;
- NumPy `2.5.2`;
- SciPy `1.18.0`;
- clipy-like `0.15`;
- exact-float success-only cache preparation;
- explicit zero RT nonlocal background auxiliary initial conditions, including `V_prime_ini_nlde=0`.

The scientific worker writes `center_fingerprint`, `objective_fingerprint`, actual CLASS/Pantheon commits, NumPy version, stencil scale and source provenance. The artifact identity validator checks these before scientific parsing.

## Curvature-threshold context

The worker defines `positive_definite` by requiring every numerical Hessian eigenvalue to exceed `1e-8` in the dimensionless stencil coordinates.

Historically the weak RTK mode has not been a threshold-edge effect:

- first dense RTK Hessian minimum eigenvalue: approximately `-2.3476e-4`;
- next recentered dense RTK Hessian minimum eigenvalue: approximately `+3.7213e-4`.

Both magnitudes are more than four orders of magnitude above the `1e-8` technical cutoff. Therefore the current Stage4D3 question is the physical/numerical sign stability of the weak lambda-direction curvature under recentering and stencil halving, not a classification caused by an eigenvalue sitting at the code threshold.

## Closure status

✅ Stage4D3 control/infrastructure readiness is closed.

🔴 Base current-center 7D Hessian result is still pending.

🔴 Half-stencil result is not yet run for the current center.

🔴 Interior local-minimum certification is therefore not yet closed.
