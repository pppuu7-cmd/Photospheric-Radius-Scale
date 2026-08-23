# RTK Formula Bible — C9 projectable-U(1) addendum

Date: 2026-08-23 20:07 UTC

Canonical use: read this addendum after the current C8 U(1) low-k/rank addenda and before interpreting the old nonprojectable C9 naturalness gate as the only completion route.

## A. Branch split

There are now two distinct U(1) carrier branches under active test.

### A1. Nonprojectable branch

`N=N(t,x)`, hence `a_i=D_i ln N` is nonzero in general.

Exact absence of the parent gravity scalar requires the special nonlinear surface

`eta1=eta2=0`

(`sigma1=sigma2=0` in the PPN dictionary).  Since the corresponding operators are allowed marginal terms, tuning them merely small does not protect an **exact** 3-DOF count.

Current useful classical domain:

`lambda_HL>1`, `beta24=beta2+beta4<=0`, `beta8<0`, together with the certified matter/Mc bound.

### A2. Projectable branch

`N=N(t)`.

Therefore

`D_i N=0`,

`a_i=0`

identically, and the nonprojectable C9 counterterms

`eta1 a_i a^i sigma`,

`eta2 D_i a^i sigma`

vanish on the entire projectable configuration space.  This is a structural branch property, not a small-coefficient tuning.

## B. Intended RTK scalar survives projectability

On flat rolling background, write

`Sigma=q t+pi`.

Projectability removes spatial lapse gradients, but not

`D_i dot(pi)`.

The fixed quadratic RTK scalar action keeps

`L2 = Akin/2 dot(pi)^2 + C0 (D_i dot(pi))^2 - P_X/2 (D_i pi)^2`,

with

`2 C0/Akin = 1/M_K^2`,

`P_X/Akin = c_a^2`.

Hence

`omega^2 = c_a^2 k^2/(1+k^2/M_K^2)`

exactly as in the production rational dispersion.

## C. Elliptic matter filter

Define

`ell(k)=1+k^2/M_c^2`,

`Q=H0/ell`,

`a_eff(k)=k^2/(M_c^2+k^2)`.

After auxiliary reduction,

`J_A^(m+aux)=Q-H0=-a_eff H0`.

Limits:

- `k=0`: `Q=H0`, `J_A^(m+aux)=0`;
- `k>>M_c`: `Q->0`, `J_A^(m+aux)->-H0`.

The `N H0` source remains in the Hamiltonian.  Therefore cancelling the homogeneous local A source does **not** erase the ordinary homogeneous energy density from the projectable global Hamiltonian equation.

## D. Projectable carrier DOF count

In d=3 the published projectable U(1) parent count is

`dim P_g=22`, `C1=8`, `C2=2`,

so

`N_g=(22-16-2)/2=2`.

Add the intended RTK scalar:

`+2` phase dimensions, `+1` physical DOF.

Add Q,Lambda auxiliary sector:

`+4` phase dimensions, `+4` second-class constraints, `+0` DOF.

Thus

`dim P=28`, `C1=8`, `C2=6`,

and

`N_carrier=(28-16-6)/2=3`.

Within the certified flat/barotropic `lambda_HL>1` domain, the surviving projectable second-class pair `(Jhat,phihat)` has nonzero bracket `d(q)>0` for every `q=k^2>0`.  The auxiliary block is invertible for `ell>0`.

## E. Homogeneous projectable background

At k=0:

`Q=H0`,

so the ordinary-matter-plus-auxiliary A source vanishes exactly.

On flat FLRW the A constraint fixes the geometric constant `Omega=0` on this branch, while the global homogeneous Hamiltonian gives

`(3/2)(3 lambda_HL-1) M_Pl^2 H^2 = rho_total + M_Pl^2 Lambda`.

Therefore

`G_cos/G_N = 2/(3 lambda_HL-1)`

when `G_N` denotes the local parent-frame Newton normalization.

For `lambda_HL>1` and a declared tolerance

`1-G_cos/G_N <= eps_G`,

the exact upper interval is

`lambda_HL <= 1 + 2 eps_G/[3(1-eps_G)]`.

Do not identify `lambda_HL` with production `lambda_D`.

## F. Finite-Mc static O(2) projectable transfer

Published projectable O(2) equations on the parent GR branch `a1=1,a2=0,g1=-1` give

`gamma_PPN=1`

from the spatial dynamical equation.

After the elliptic auxiliary reduction, the A-source is multiplied by `a_eff(k)`.  At O(2), its metric variation is O(4), so the spatial equation is unchanged, while the A constraint becomes

`1 = kappa a_eff(k)`,

with `kappa=G/G_N(k)`.

Therefore

`G_N(k)=G a_eff(k)=G k^2/(M_c^2+k^2)`,

`gamma_PPN=1`.

The exact local Newton deficit is

`1-G_N/G = M_c^2/(M_c^2+k^2)`.

This is **not** yet a finite-Mc theorem for `beta_PPN`, `alpha1`, or `alpha2`.

## G. Dual-tolerance scale window

For independently declared `0<eps_cos,eps_local<1`, require

`a_eff(k_cos)<=eps_cos`,

`1-a_eff(k_local)<=eps_local`.

Then

`M_c^2 >= [(1-eps_cos)/eps_cos] k_cos^2`,

`M_c^2 <= [eps_local/(1-eps_local)] k_local^2`.

The interval is nonempty iff

`k_local/k_cos >= sqrt[(1-eps_cos)(1-eps_local)/(eps_cos eps_local)]`.

Special symmetric 1% case:

`k_local/k_cos>=99`.

No Mc is selected by this theorem.

## H. Lambda>1 weak-anisotropy response margin

For the certified isotropic response `X0` with

`||X0_TF||=sqrt(2/3) A`,

`|tr X0|<=2A`,

the DeWitt quadratic form is

`X G X = ||X_TF||^2 - (tr X)^2/[3(3 lambda_HL-1)]`.

A sufficient perturbative positivity condition is

`||Delta X_TF|| + |tr Delta X|/sqrt[3(3lambda_HL-1)]`

`< A/sqrt(3) [sqrt(2)-2/sqrt(3lambda_HL-1)]`.

The right side is strictly positive for `lambda_HL>1` and vanishes at `lambda_HL=1`.

For pure traceless response `||Delta X_TF||<=rA`,

`lambda_HL > [1+4/(sqrt(2)-sqrt(3)r)^2]/3`,

and at small r

`lambda_min-1=(2sqrt(6)/3)r+O(r^2)`.

This is an open-neighborhood theorem, not yet a Bianchi-I solution.

## I. Cosmology-versus-anisotropy compatibility target

Eliminating lambda_HL between the homogeneous Newton-normalization tolerance and the conservative traceless-response margin yields

`r < sqrt(2/3) [1-sqrt(1-eps_G)]`.

At small eps_G,

`r_max=eps_G/sqrt(6)+O(eps_G^2)`.

The physical next step is to derive r from shear/anisotropic stress rather than treating it as a free tolerance.

## J. Projectable integration-constant warning

A locally integrated projectable Friedmann equation may admit

`rho_int=C_int/a^3`.

At the background level this is exactly amplitude-degenerate with particle CDM and an exact RTK dust tail.  If `C_int` is retained as a free sector, background data alone cannot identify the separate amplitudes.

Acceptable routes are:

1. freeze a principled global state/boundary condition with `C_int=0` before fitting;
2. retain `C_int` and distinguish it with perturbations/growth/lensing;
3. fit only a combined dust sector and abandon separate background amplitude identification.

Do not silently set `C_int=0` merely for convenience.

## K. Current architecture rule

The nonprojectable lambda_HL>1 branch remains the stronger weak-field benchmark because its scoped `gamma`, `beta`, `alpha1`, `alpha2` gates are already complete.

The projectable branch is currently the stronger **C9 structural candidate** because it eliminates the eta1/eta2 detuning mechanism by configuration-space structure rather than tuning.

No final branch selection is allowed before:

- projectable finite-Mc O(3)/O(4) PPN recertification;
- projectable perturbation/global-integration-constant audit;
- intended RTK scalar strong-coupling/cutoff;
- production BBN/CMB with `lambda_HL` separate from `lambda_D`;
- generic anisotropic/curved and strong-field gates.
