# RTK projectable-U(1) C9 architecture checkpoint — 2026-08-23 20:07 UTC

Status: **PROJECTABLE BRANCH STRUCTURALLY GREEN IN SCOPED C8/C9 GATES; FULL FINITE-Mc PPN, PRODUCTION COSMOLOGY, STRONG COUPLING AND STRONG FIELD REMAIN OPEN.**

This checkpoint is append-only and does not delete the nonprojectable lambda_HL>1 branch.  It records the first completed structural alternative to the technically unnatural nonprojectable eta1=eta2=0 surface.

## 1. Why this branch was opened

The nonprojectable U(1) Hamiltonian theorem of Mukohyama-Namba-Saitou-Watanabe (arXiv:1504.07357) removes the gravity scalar exactly only on eta1=eta2=0.  The two allowed operators `eta1 a_i a^i sigma` and `eta2 D_i a^i sigma` are marginal and expected to be regenerated.  A dedicated executable gate now classifies numerical tuning alone as insufficient protection of an **exact** 3-DOF claim:

- run `32660638335`: SUCCESS;
- artifact `9498643095`;
- digest `sha256:709190039cd3941dff36a498422afd0075950ffc5a4de02b708cee11823bacb0`;
- classification `RTK_C9_U1_RADIATIVE_TUNING_ONLY_NOGO_PASS`.

This does not exclude an exact Ward identity/RG surface or a different constraint architecture.

## 2. Projectability is a structural rather than tuning-based escape

For `N=N(t)`,

`a_i=D_i ln N=0`

identically on the projectable configuration space.  Consequently the two nonprojectable C9 counterterms vanish structurally rather than by choosing small coefficients.

The intended RTK scalar does not disappear: `D_i dot(pi)` remains a valid spatial derivative and the fixed quadratic kinetic operator still gives

`omega^2 = c_a^2 k^2/(1+k^2/M_K^2)`.

The elliptic Q/Lambda matter compensator is also purely spatial and survives projectability.

Compatibility gate:

- run `32660732873`: SUCCESS;
- artifact `9498666913`;
- digest `sha256:33b4e378790699ae10c2dda3bdc3f6f1e4b85a05d282d8c06b72ad8506fdc2b9`;
- classification `RTK_C9_PROJECTABLE_U1_RTK_COMPATIBILITY_PASS`.

## 3. Scoped coupled all-q carrier DOF certificate

Published projectable parent count in d=3:

- phase-space dimension 22;
- 8 first-class constraints;
- 2 second-class constraints;
- 2 physical gravity DOF (tensor polarizations).

Add the intended RTK scalar canonical pair: +2 phase dimensions and +1 intended physical DOF.

Add Q,Lambda: +4 phase dimensions and +4 second-class constraints, hence +0 propagating DOF.

Total carrier count:

`dim P=28`, `C1=8`, `C2=6`,

`N_phys=(28-2*8-6)/2=3`.

Within the certified flat homogeneous/isotropic barotropic lambda_HL>1 domain, the surviving projectable second-class pair `(Jhat,phihat)` has bracket `d(q)>0` for all q>0 under the already-certified source/Mc bound.  The auxiliary block remains invertible for `ell=1+q/M_c^2>0`.

- run `32660949364`: SUCCESS;
- artifact `9498725463`;
- digest `sha256:8765d8a73e2c6636473eae055538c9e123eb88e5837d0b8ada6c2ddac5240066`;
- classification `RTK_C9_PROJECTABLE_U1_COUPLED_DOF_ALLQ_PASS`.

Scope: ordinary matter physical DOF are not included in the 3 carrier DOF count.

## 4. Homogeneous A-source and global Friedmann equation

The elliptic auxiliary constraint gives at k=0:

`Q=H0`.

Therefore the matter+auxiliary source in the A constraint is exactly

`Q-H0=0`.

The old evolving-rho family-I flat-FLRW A-source obstruction is absent.  The `N H0` Hamiltonian source is not cancelled, so the homogeneous projectable global Hamiltonian equation remains sourced:

`(3/2)(3 lambda_HL-1) M_Pl^2 H^2 = rho_total + M_Pl^2 Lambda`.

Thus, relative to the local Newton normalization of the parent frame,

`G_cos/G_N = 2/(3 lambda_HL-1)`.

For a declared fractional normalization tolerance eps_G on the lambda_HL>1 side,

`lambda_HL <= 1 + 2 eps_G/[3(1-eps_G)]`.

Initial CI run `32661003460` was theorem-PASS but workflow-red only because a post-check required exact equality of a result string that contained an explanatory suffix.  The assertion was hardened without changing the theorem.  Rerun `32661224585`: SUCCESS; artifact `9498795593`; digest `sha256:f0810f592a3b0ff9ab9220fb74c7818eea3b8438f760bd9d810604fd0f1b41c2`.

## 5. Finite-Mc static O(2) source transfer

Using the published projectable O(2) equations (Lin-Mukohyama-Wang-Zhu, arXiv:1310.6666, Sec. VI), the parent GR branch `a1=1,a2=0,g1=-1` has gamma=1 from the spatial dynamical equation.  After Q/Lambda elimination the A-source is filtered by

`f(k)=a_eff=k^2/(M_c^2+k^2)`.

At O(2), the spatial-metric variation of the filtered A-H0 interaction starts at O(4), so the spatial equation remains unchanged while the A constraint becomes

`1 = kappa f(k)`, with `kappa=G/G_N(k)`.

Hence

`gamma_PPN=1`,

`G_N(k)=G k^2/(M_c^2+k^2)`,

and

`1-G_N/G=M_c^2/(M_c^2+k^2)`.

- run `32661442475`: SUCCESS;
- artifact `9498850306`;
- digest `sha256:4c4ffddca743e542f8db5c2bcb16b6cb323e701ff5d3a50ce09ed9f7895842e5`.

Do **not** extend this to finite-Mc beta_PPN or alpha1,alpha2 yet.  The O(3)/O(4) projectable equations require a direct primary-equation/TeX audit and fresh auxiliary-response derivation.

## 6. Exact dual-tolerance Mc window

For

`a_eff(k)=k^2/(M_c^2+k^2)`,

require simultaneously

`a_eff(k_cos)<=eps_cos`,

`1-a_eff(k_local)<=eps_local`.

Then

`M_c^2 >= [(1-eps_cos)/eps_cos] k_cos^2`,

`M_c^2 <= [eps_local/(1-eps_local)] k_local^2`,

and the window exists iff

`k_local/k_cos >= sqrt[(1-eps_cos)(1-eps_local)/(eps_cos eps_local)]`.

- run `32660884728`: SUCCESS;
- artifact `9498708390`;
- digest `sha256:7f189c5b2471508c6d155e4a7a11abe25a888593ef8c29ca772bf2551a20305b`.

No numerical Mc or experimental eps_local is chosen.

## 7. Projectable integration-constant warning

A projectable local integrated Friedmann equation can contain `rho_int=C_int/a^3`.  At background level this is exactly degenerate with particle-CDM and any exact RTK dust tail:

`rho_dust=(D_cdm+D_RTK_tail+D_int)/a^3`.

The amplitude Jacobian has rank 1.  Therefore a free integration constant creates a new identifiability problem; it is not automatically a virtue of projectability.

- run `32661185227`: SUCCESS;
- artifact `9498786077`;
- digest `sha256:ba7150bfda42be1114e198f83fd405e7c15da79b12a488f18d0c62ea9ae5b71a`;
- status remains YELLOW.

This is consistent with, but does not reopen, B10: the already-closed B10 protocol found the finite RTK lambda_D solution numerically unseparated from the preregistered dust tail at the 0.005 raw-objective convention.

Resolution must be one of: freeze a principled global state with C_int=0 before fitting; retain C_int and distinguish it using perturbations/non-background observables; or fit only a combined dust sector and relinquish separate background identifiability.

## 8. Nonprojectable branch remains scientifically useful

The nonprojectable lambda_HL>1 branch is **not discarded**.  It currently has stronger same-action weak-field coverage:

- all-q flat/barotropic rank;
- exact weak-anisotropy margin;
- static Newton/gamma;
- scoped static beta_PPN=1;
- scoped moving-source alpha1=alpha2=0.

However its exact 3-DOF surface still has the C9 radiative tuning problem unless an additional protection mechanism is found.

The projectable branch currently has the opposite profile: structurally stronger C9 protection and simpler constraint count, but finite-Mc O(3)/O(4) PPN and projectable perturbation/global-integration-constant phenomenology remain open.

## 9. Current branch comparison

| Gate | Nonprojectable lambda_HL>1 | Projectable candidate |
|---|---|---|
| exact RTK rational scalar dispersion | GREEN | GREEN |
| elliptic homogeneous A-source cancellation | GREEN | GREEN |
| scoped all-q 3 carrier DOF | GREEN classical | GREEN classical |
| C9 eta1/eta2 radiative protection | BLACK for tuning-only; symmetry/RG open | GREEN structural candidate because a_i=0 |
| static O(2) gamma/Newton | GREEN | GREEN, finite-Mc Newton transfer explicit |
| static beta_PPN | GREEN scoped | YELLOW finite-Mc rederivation pending |
| alpha1,alpha2 | GREEN scoped regular lambda!=1 | YELLOW finite-Mc rederivation pending |
| homogeneous Friedmann source | GREEN lambda>1 | GREEN global homogeneous equation |
| integration-constant dust sector | not applicable in same way | YELLOW |
| anisotropic/curved generic backgrounds | YELLOW | YELLOW |
| intended RTK scalar strong coupling | OPEN | OPEN |
| strong-field/black holes | OPEN | OPEN |

## 10. Frozen research order after this checkpoint

1. Keep B9 v7 half-scale run `32657629806` untouched until completion and follow its frozen decision tree.
2. Complete the lambda_HL>1 cosmology-versus-anisotropy compatibility theorem and map the abstract response norm to an actual Bianchi-I/anisotropic-stress solution.
3. TeX-audit the projectable O(3) equations before any finite-Mc alpha1/alpha2 claim; then derive O(3) and O(4) source transfer from the same auxiliary-eliminated action.
4. Introduce `lambda_HL` as a **distinct** parameter from production `lambda_D` in a new projectable numerical background interface; use BBN/CMB to constrain `G_cos/G_N` rather than choosing lambda_HL by hand.
5. Derive the projectable integration-constant perturbation sector and compare it to RTK/CDM growth/lensing, or freeze a principled C_int=0 global branch.
6. Derive the cubic/quartic interaction coefficient dictionary and strong-coupling/cutoff of the intended RTK scalar. Projectability solves the unwanted-gravity-scalar C9 problem only; it does not solve intended-scalar EFT control.
7. Continue compact-object/X_U->0 and black-hole gates on whichever architecture survives the above comparison.
