# RT nonlocal action / DOF framework audit

Date: 2026-08-18

Status: **methodology corrected and source implementation audited; full coupled RTK ghost/DOF theorem remains open.**

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

The full consistency problem must be split into three logically distinct layers.

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

### Background auxiliary initial-condition defect discovered

The pinned `source/input.c` contains

```
pba->U_ini_nlde = 0.;
pba->U_prime_ini_nlde = 0.;
pba->V_ini_nlde = 0.;
pba->U_prime_ini_nlde = 0.;
```

The fourth assignment is a copy/paste duplicate. `pba->V_prime_ini_nlde` is declared in `background.h` and subsequently used by `background.c` as the initial value of `index_bi_V_prime_nlde`, but is not explicitly assigned in this upstream block.

This is a source-level reproducibility defect even if a particular runner happens to provide zero-valued memory.

Research patch:

`rtk/upgrade_rtk_nonlocal_initial_conditions.py`

replaces only the duplicated fourth assignment by

`pba->V_prime_ini_nlde = 0.;`

and refuses to patch if the exact audited upstream block is not present.

An exact old-vs-fixed likelihood A/B control is running separately before this source hardening is allowed to alter the frozen production/stationarity interpretation.

## 4. What is now established

✅ The correct RT model branch is `model=2`; `model=1` is RR. The opposite comment in one upstream parser location is stale.

✅ The RT equation uses a retarded inverse operator in the published model definition.

✅ A closed-form RT action is not known in the primary model paper; full local-action Hamiltonian methods therefore cannot simply be assumed available.

✅ The pinned CLASS perturbation auxiliaries have explicitly fixed zero initial conditions.

✅ A background source bug/ambiguity affecting `V_prime_ini_nlde` initialization has been identified and a fail-closed one-line patch has been written.

✅ The research methodology will no longer count localized RT auxiliary variables as independent physical DOF merely because they appear as local ODE variables in CLASS.

## 5. What remains open

🔴 Exact score equivalence of the historical uninitialized-`V_prime` tree and the explicit-zero tree is pending the A/B control.

🔴 A first-principles causal/retarded DOF count for the complete nonlinear RT equation on cosmological backgrounds is not yet derived by this project.

🔴 No closed fundamental RT action has been reconstructed.

🔴 Coupled metric + RT + Route-A1 Khronon nonlinear DOF/constraint consistency is not yet proved.

🔴 The physical cubic Khronon coefficients and strong-coupling scale remain unknown.

## 6. Decision consequence

The full-theory consistency frontier is no longer formulated as the naive task

`localize RT -> count every U,V,Z variable as a free canonical field`.

The correct frontier is

`causal RT equation with fixed inverse-operator prescription`

`+ explicit Khronon nonlinear completion`

`-> coupled response/constraint/DOF analysis`.

This avoids a false ghost/DOF conclusion generated solely by over-enlarging the solution space during localization.
