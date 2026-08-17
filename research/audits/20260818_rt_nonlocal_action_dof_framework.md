# RT nonlocal action / DOF framework audit

Date: 2026-08-18

Status: **methodology corrected; causal/minimal auxiliary-IC implementation gate reproducibly closed; full coupled RTK ghost/DOF theorem remains open.**

## 1. Primary-theory boundary

The RT model used by the pinned nonlocal CLASS branch is defined by the effective equation of motion

`G_mn - (m^2/3) (g_mn Box^-1 R)^T = 8 pi G T_mn`,

with `Box^-1` defined through the retarded Green function. In Dirian et al., arXiv:1602.03558, the authors explicitly state that a closed-form action corresponding to the RT equation is not known. The related RR model instead has the nonlocal action `R - (m^2/6) R Box^-2 R`.

Therefore a Hassan-Rosen-style canonical Hamiltonian proof cannot simply be applied to the present RT equation as if a standard local fundamental action were already available.

Primary references:

- Y. Dirian et al., *Non-local gravity and comparison with observational datasets. II*, arXiv:1602.03558, especially the model definition and discussion around eqs. (1)-(2).
- S. Foffa, M. Maggiore, E. Mitsou, *Apparent ghosts and spurious degrees of freedom in non-local theories*, arXiv:1311.3421.

The second paper establishes the conceptual warning relevant here: auxiliary/localized ghost-looking modes in causal nonlocal equations need not correspond to actual independent propagating degrees of freedom.

## 2. Correct theorem strategy for RTK

The full consistency problem is split into three logically distinct layers.

### Layer A — Khronon reduced scalar completion

Route A1 is now explicitly frozen and its cubic reduced-scalar EFT basis has passed symbolic CI. This layer can use ordinary local Legendre/Hamiltonian reasoning because it is an explicit local preferred-frame EFT postulate.

### Layer B — RT causal nonlocal sector

The RT auxiliary variables are a localization/device for solving a retarded nonlocal equation. Their allowed homogeneous solutions/initial data must be fixed by the definition of the inverse operator and by the cosmological causal prescription; they must **not** automatically be counted as arbitrary new free particle initial data.

A valid RT DOF analysis must therefore preserve the retarded prescription and distinguish localizing variables from genuinely free propagating modes.

### Layer C — coupled RT + Khronon consistency

Only after A and B are well defined may one study whether coupling the reduced Khronon sector to the RT-modified metric equations activates an additional unwanted mode, creates a singular constraint/response operator, or otherwise violates the linear target.

## 3. Pinned CLASS implementation audit

Pinned upstream CLASS commit:

`36cf283628c4a3330ec9fd3d84239bf775f77317`

### Perturbation auxiliary initial conditions

`source/perturbations.c` explicitly sets the nonlocal scalar perturbation auxiliaries to zero for the adiabatic initial-condition routine:

- `deltaU_nlde = 0`,
- `deltaU_prime_nlde = 0`,
- `deltaV_nlde = 0`,
- `deltaV_prime_nlde = 0`,
- for RT/model 2 also `deltaZ_nlde = 0`,
- `deltaZ_prime_nlde = 0`.

This is consistent with a fixed minimal homogeneous nonlocal solution rather than arbitrary auxiliary-field initial data.

### Background auxiliary initial-condition defect and hardening

The pinned `source/input.c` contains

```
pba->U_ini_nlde = 0.;
pba->U_prime_ini_nlde = 0.;
pba->V_ini_nlde = 0.;
pba->U_prime_ini_nlde = 0.;
```

The fourth assignment is a copy/paste duplicate. `pba->V_prime_ini_nlde` is declared in `background.h` and subsequently used by `background.c` as the initial value of `index_bi_V_prime_nlde`, but is not explicitly assigned in this upstream block.

Research patch `rtk/upgrade_rtk_nonlocal_initial_conditions.py` replaces only the duplicated fourth assignment by

`pba->V_prime_ini_nlde = 0.;`

and refuses to patch if the exact audited upstream block is not present.

Exact old-vs-fixed likelihood control run `32073306866` returned zero reported difference in every compared quantity, including total eff/k01 score, Planck, Pantheon, BOSS and `r_d`. Therefore historical scores need not be invalidated solely by this source typo, while future production trees are required to use the explicit-zero patch.

## 4. Machine-verified causal/minimal auxiliary IC gate

A separate fail-closed audit now verifies the pinned source after the one-line background patch.

Audit source:

`rtk/audit_rt_retarded_auxiliary_ic.py`

Successful workflow evidence:

- workflow run `32073844769`, rerun attempt success;
- job `95522905671`;
- research checkout `14142d3ab9c42657fd7ca04f5eb9d2cae1651818`;
- artifact `rtk-retarded-auxiliary-ic-audit`, ID `9302714258`;
- artifact ZIP SHA256 `0b1130ead65b69c20315d6abd64243d5c835add0d31e8901a14f77ce0f4d5624`;
- emitted classification `RTK_RETARDED_AUX_IC_IMPLEMENTATION_PASS`.

The audit verifies:

1. exactly one explicit zero assignment for each background auxiliary initial datum `U`, `U'`, `V`, `V'`;
2. the upstream duplicated `U'` initialization has been removed;
3. `V'_ini` is declared and consumed by the background integrator;
4. direct zero assignments for `deltaU`, `deltaU'`, `deltaV`, `deltaV'`;
5. direct zero assignments for RT-only `deltaZ`, `deltaZ'` inside the `model==2` branch;
6. allocation of `Z,Z'` perturbation indices only in the RT/model-2 branch.

The first audit attempt failed because its regex simplified the nested CLASS workspace index syntax. The failure was an audit-code mismatch, not missing physical ICs. The corrected audit uses the exact pinned source form and passes.

## 5. What is now established

✅ The correct RT model branch is `model=2`; `model=1` is RR. The opposite comment in one upstream parser location is stale.

✅ The RT equation uses a retarded inverse operator in the published model definition.

✅ A closed-form RT action is not known in the primary model paper; full local-action Hamiltonian methods therefore cannot simply be assumed available.

✅ The pinned CLASS perturbation auxiliaries have explicitly fixed zero initial conditions.

✅ The background `V'_ini` source ambiguity is removed by a fail-closed explicit-zero patch.

✅ Historical current-point likelihood values are exactly reproduced by the explicit-zero patch in the A/B control.

✅ The complete background + perturbation minimal auxiliary-IC implementation contract is now machine-verified in CI.

✅ The research methodology will not count localized RT auxiliary variables as independent physical DOF merely because they appear as local ODE variables in CLASS.

## 6. What remains open

🔴 A first-principles causal/retarded DOF count for the complete nonlinear RT equation on cosmological backgrounds is not yet derived by this project.

🔴 No closed fundamental RT action has been reconstructed.

🔴 Coupled metric + RT + Route-A1 Khronon nonlinear DOF/constraint consistency is not yet proved.

🔴 The physical cubic Khronon coefficients and strong-coupling scale remain unknown.

## 7. Decision consequence

The full-theory consistency frontier is no longer formulated as the naive task

`localize RT -> count every U,V,Z variable as a free canonical field`.

The correct frontier is

`causal RT equation with fixed inverse-operator prescription`

`+ explicit Khronon nonlinear completion`

`-> coupled response/constraint/DOF analysis`.

This avoids a false ghost/DOF conclusion generated solely by over-enlarging the solution space during localization.
