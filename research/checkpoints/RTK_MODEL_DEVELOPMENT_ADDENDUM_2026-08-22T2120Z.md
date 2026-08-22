# RTK model development addendum — 2026-08-22 21:20 UTC

This checkpoint supersedes any interpretation that the frozen elliptic compensator already has a completed full coupled 8x8 Dirac proof.  It preserves the successful algebraic results but records the corrected Dirac-Bergmann order discovered in this iteration.

## B9 Planck R3 lensing robustness

- Frozen LCDM recenter-v6 center remains unchanged.
- Base v6 run `32592618365` is SUCCESS with exact center replay, zero best improvement and a positive-definite effective Hessian.
- Independent half-scale stationarity run `32596694426` remains the active preregistered B9 calculation at the time of this checkpoint.
- No center/threshold retuning is allowed before that run finishes.

## Elliptic matter compensator — results closed in this iteration

### Conditional 8x8 Schur identity

Run `32597268677`: SUCCESS.

For an assumed old-four plus auxiliary-four constraint basis,

`det M = det E det(O + X E^{-1} X^T)`, with `det E=ell^4`.

This is retained as an exact matrix theorem, but it is now explicitly conditional: the Dirac algorithm does not automatically generate `C_Q` and the old `phi_A` as first-generation constraints once the coupled primary `G=p_nu+J_A_total` contains `Q`.

### Regular-slice cross support

Run `32597990939`, attempt 2: SUCCESS.

On `D_i nu=0`, the auxiliary Schur correction cannot touch the `pi_N` row.  The exact Pfaffian correction for the conditional 8x8 basis was reduced to the lower 3x3 old-sector support.  Artifact ID `9482103922`, digest `sha256:f8156e476e20f2f80f86f4d60ec3beccd52e82c12688d60cffb6edb4011661ea`.

### Effective coupling transfer

Run `32597994972`: SUCCESS.

After algebraic auxiliary elimination at source level,

`a1_eff(k)=k_phys^2/(M_c^2+k_phys^2)`.

Exact limits:

- `k=0`: `a1_eff=0`;
- `k=M_c`: `a1_eff=1/2`;
- `k >> M_c`: `a1_eff -> 1`.

The exact 1% scale-separation window exists iff `k_local/k_cos >= 99`.  No value of `M_c` is selected.  Artifact ID `9482083935`, digest `sha256:0e7355fd9895a9980e3f6e6493e763dd2335949f54a4a4366f190f7402247c40`.

## Critical coupled-Dirac correction

The frozen canonical source is

`J_A_total = J0 + Q`,

so the actual U(1) primary is

`G = p_nu + J_A_total`.

Therefore

`{G,p_Q}=+1`

(up to the fixed bracket orientation).  The first consistency equations consequently mix primary multipliers:

- `dot G = Phi + u_Q = 0` fixes `u_Q`; it does not by itself impose the old `phi_A=0`;
- `dot p_Q = -C_Q-u_G = 0` fixes `u_G`; it does not by itself impose `C_Q=0`;
- `p_Lambda` still generates the genuine secondary `C_Lambda=ell Q-H0`;
- `p_A` still generates `J_A_total`;
- on the frozen a2=0 regular slice, `p_N` still generates `H_perp`.

The primary-mixing theorem itself printed PASS in run `32598229839`; that workflow attempt was marked failure only by an overly literal post-result string assertion.  The assertion was corrected and a hardened rerun was launched.  The scientific result of the script was not the failing item.

## Corrected preferred Dirac architecture

The genuine pair

`(p_Q, C_Lambda=ell Q-H0)`

has bracket operator `ell` and is invertible for the positive elliptic branch.  This motivates the exact projected constraints

`Jhat = J_A_total - ell^{-1} C_Lambda`

and

`Ghat = G - ell^{-1} C_Lambda = p_nu + Jhat`.

In Fourier-symbol form this gives

`Jhat = J_A^(g) - (1-1/ell) H0 = J_A^(g)-a1_eff H0`.

The key point is that `Jhat` and `Ghat` commute with `p_Q` in the auxiliary canonical support algebra.  The reduced matter Hamiltonian is exactly

`H_red = N H0-a1_eff(A-Acal)H0`

plus the old gravity/RTK/shift terms.  After `C_Lambda=0`, the `Lambda` term drops from the reduced Hamiltonian and `p_Lambda` is expected to be a trivial first-class multiplier constraint in this reduced support.  Thus the preferred physical route is to eliminate `(p_Q,C_Lambda)` first and then recompute the remaining U(1) four-constraint rank.  A dedicated exact Dirac-projection CI gate has been launched.

This replaces the earlier plan to prove the frozen model directly with the conditional 8x8 matrix.

## Reduced-chain localization

A second launched gate checks the Fourier-symbol reduced matter sector.  For c-number `a1_eff` it has the original a2=0 canonical structure:

- `J_A^m=-a1_eff H0`;
- `p_nu^m=+a1_eff H0`;
- `p_nu^m+J_A^m=0`;
- `dJ_A^m/dN=0`;
- on `D_i nu=0`, `H_perp^m=H0` and is N-independent;
- the direct matter self-bracket `{J_A^m,H_m}_matter` vanishes because both are proportional to the same `H0`.

Therefore the remaining finite-k rank problem is localized to gravity/metric cross brackets and the functional metric dependence of the elliptic inverse, not a direct matter self-bracket or a new lapse/A Hessian.

## Elliptic resolvent metric variation

A separate operator gate has been launched for

`L=1-D^2/M_c^2 = 1+(-D^2)/M_c^2`.

Under boundary conditions where `-D^2` is nonnegative self-adjoint and `M_c>0`, the physical branch has no filter pole and `||L^{-1}||<=1`.  The exact variation identity is

`delta L^{-1}=-L^{-1}(delta L)L^{-1}`,

hence

`delta a_eff=L^{-1}(delta L)L^{-1}=-(1/M_c^2)L^{-1}[delta(D^2)]L^{-1}`.

This will be used to derive the actual metric-dependent corrections to the reduced U(1) Pfaffian and, if possible, a sufficient no-zero bound in a controlled geometry domain.

## Mandatory next gates

1. Finish the exact `(p_Q,C_Lambda)` Dirac-projection CI and validate the zero auxiliary physical-DOF count in the coupled basis.
2. Derive `H_perp_hat` and `phi_hat` from preservation of `pi_N` and `Ghat` in the reduced Hamiltonian.
3. Compute the actual reduced 4x4 U(1) Poisson matrix/Pfaffian with `L^{-1}` retained as an operator; do not import the conditional 8x8 result as a DOF proof.
4. Classify finite-k rank-loss loci before choosing `M_c`.
5. Only after the classical rank gate is green, confront the transition scale with cosmological perturbations, PPN/local tests, cutoff/strong-coupling and compact-object gates.
6. The existing C9 technical-naturalness warning remains mandatory: the exceptional `eta1=eta2=0` (`sigma1=sigma2=0`) gravity surface is not promoted to a technically natural completion without an additional protection/RG/tuning mechanism.

## Parameter-freeze rule

Keep `M_c>0` symbolic.  Do not fit or select `M_c`, and do not retune the B9 v6 center, until the corresponding preregistered structural/statistical gates close.
