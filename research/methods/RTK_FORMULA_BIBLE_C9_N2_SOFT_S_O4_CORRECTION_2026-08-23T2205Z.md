# RTK Formula Bible — mandatory C9 n=2 soft-s / O(4) generalized-PPN correction

Updated: 2026-08-23 22:05 UTC
Status: **MANDATORY CURRENT CORRECTION — supersedes the optimistic n=2 interpretation in the earlier 21:55 UTC frontier addendum**

## 1. Why this correction exists

The earlier generic curvature-carrier power-count gate correctly showed that when **all relevant spatial legs are hard**, a family `[D^(n-1)R3]^2` has `g a_l ~ k^(1-n)` in the deepest `k>>M_K,M_U` regime.  That theorem remains algebraically correct in its scope.

The subsequent exact nonlinear conformal expansion exposed an exceptional elastic channel outside that assumption: in COM kinematics the s-channel internal **spatial** momentum is exactly zero, while the n=2 cubic curvature kernel is nonzero.  Therefore the internal leg is not hard-spatial and does not receive the same `Z(q)^(1/2)` normalization.

Hence the statement “n=2 is asymptotically sufficient because `g a_l~k^-1`” is **not a valid full-channel conclusion** and must not be used without the correction below.

---

## 2. Exact n=2 conformal expansion

For

`gamma_ij=a^2 exp(2 zeta) delta_ij`,

in d=3,

`R3=a^-2 exp(-2 zeta) F`,

`F=-4 Delta zeta-2(grad zeta)^2`.

Exactly,

`sqrt(gamma) D_iR3 D^iR3 = a^-3 exp(-3zeta)[partial_i F-2F partial_i zeta]^2`.

Define

`Z_i=partial_i zeta`,

`L=Delta zeta`,

`U_i=partial_i Delta zeta`,

`V_i=partial_j zeta partial_i partial_j zeta`,

`S=(grad zeta)^2`.

Then through quartic scalar order:

`Q2=16 U^2`,

`Q3=32 U.V-64 L U.Z-48 zeta U^2`,

`Q4=16 V^2-64 L V.Z+64 L^2 Z^2-32 S U.Z-96 zeta U.V+192 zeta L U.Z+72 zeta^2 U^2`.

For `k1+k2+k3=0`, `q_i=|k_i|^2`, the exact symmetric cubic Fourier kernel is

`K3=16[(q1+q2+q3)^3-7(q1+q2+q3)(q1q2+q1q3+q2q3)+12q1q2q3]`.

For equal-|k| elastic COM scattering, the bare quartic contact kernel is

`K4=320 k^6(9-2 cos^2 theta)`.

The cubic channel kernels are

`K3_s=-96 k^6`,

`K3_t=-32 k^6[4c^3+4c^2-31c+26]`,

`K3_u=32 k^6[4c^3-4c^2-31c-26]`,

with all three nonzero on `-1<=c<=1` in this bare conformal convention.

Provenance:

- run `32669082828` GREEN;
- artifact `9500857844`;
- digest `sha256:efec6f70955d98f4dffd725038e1818563d70c8273a1b039b4e8237450a39b31`.

This is a bare conformal theorem only; lapse/shift reduction and perturbations of the state-dependent carrier coefficient remain pending.

---

## 3. Exceptional soft-spatial s-channel warning

The n=2 completed quadratic dispersion is

`omega^2=c_a^2 k^2 N/Z`,

`N=1+k^4/M_U^4`,

`Z=1+k^2/M_K^2`.

For isotropic scattering the exact phase-space factor can be written

`g=Z^(3/2)/[2 c_a^3 N^(3/2) D]`,

where

`D=1+2 k^4/(M_U^4+k^4)-k^2/(M_K^2+k^2)`.

Because `q_s=0` but `K3_s=-96k^6`, the fixed-lapse conformal s-channel gives

`g a0_s = -9 H^2 k^10 sqrt(Z)/[128 pi K M_U^8 c_a N^(5/2) D]`.

Two important asymptotic regimes follow.

### Intermediate hierarchy `M_U << k << M_K`

`g a0_s -> -3 H^2 M_U^2/[128 pi K c_a]`.

Thus the soft-s contribution is **marginal/constant**, not `k^-1`.

### Formal deepest hierarchy `k >> M_K,M_U`

`g a0_s -> -9 H^2 M_U^2 k/[256 pi K c_a M_K]`.

Thus the bare soft-s contribution grows linearly with k.  Using the production identity `K=2 M_Pl^2 M_K^2`,

`g a0_s -> -9 H^2 M_U^2 k/[512 pi c_a M_Pl^2 M_K^3]`.

Provenance:

- run `32669380424` GREEN;
- artifact `9500930355`;
- digest `sha256:e3ad2e22dfb28e2d8e8a949b188f25115ab9067104c3caa9000428e3c6cd1f4b`.

### Correct interpretation

This is **not a final no-go for n=2**.  It is a mandatory warning that the generic all-hard-leg power count does not control the elastic soft-spatial s-channel.  The full lapse/shift and state-function expansion may modify or cancel `K3_s`.

Therefore n=2 is now **YELLOW / conditional**, not the preferred promoted UV completion.

The next decisive UV gate is specific: derive the full cubic constraint reduction and test whether the reduced `q_s=0` cubic vertex vanishes.  If it survives, n=2 must be reconsidered; likely options include a higher-derivative/symmetry-protected carrier or a structure that forbids the soft-s vertex.

---

## 4. O(4): one new generalized nonlocal potential

Published projectable PPN structure (Lin–Mukohyama–Wang–Zhu, arXiv:1310.6666v4) gives

`h00=2U-U^2+2 a1 A4+O(6)`

and the combined O(4) A-constraint + trace-dynamical equation contains A4 through

`-2 Delta A4`.

Define `S_res` as the additive finite-Mc single-resolvent O(4) source on the right-hand side, with parent/local terms held fixed.  Then exactly

`-2 Delta delta A4 = S_res`,

so

`delta A4=-(1/2)Delta^-1 S_res`.

On the current physical `a1=1` branch,

`delta h00=-Delta^-1 S_res`.

Define the new potential

`Psi_res := -Delta^-1 S_res`.

Thus `delta h00=Psi_res`.

The exact d=3 conformal resolvent-variation kernel is

`K_res/gamma=-m^2(3x^2-x cosTheta)/[(m^2+1)(m^2+x^2)]`,

`m=M_c/k`, `x=q/k`.

It is genuinely non-separable.  A separable `F(m)G(x,theta)` would have zero mixed log derivative, whereas here

`partial_m partial_x log|K_res| = 4 m x/(m^2+x^2)^2 >0`.

Equivalently the separability cross-product has numerator

`m1^2 m2^2 (m1^2-m2^2)(x1^2-x2^2)`.

Therefore, for arbitrary extended sources, `Psi_res` is true mode mixing and cannot generically be represented by a constant shift of a standard PPN coefficient such as beta.

It vanishes in the local-parent limit `M_c/k ->0`.

Provenance:

- run `32669251516` GREEN;
- artifact `9500899658`;
- digest `sha256:1cff1ef2e6d3af26af1640a3dcb31c8f4aa18a0091fd5e2a8f0ce1015a840810`.

### Correct O(4) interpretation

The finite-Mc problem is naturally a generalized/nonlocal PPN problem:

`standard parent/local potentials + diagonal filter pieces + Psi_res`.

Only after `Psi_res` is evaluated for a concrete source/support may one ask whether it is approximately degenerate with a constant beta/alpha2 shift over that experiment.

Do **not** obtain finite-Mc O(4) PPN parameters by the naive substitution `a1 -> f(k)` in the parent closed-form PPN formulas.  O(3) already contains a mixed filtered/unfiltered source structure, so that substitution is not the physical reduced theory.

---

## 5. Current corrected status

### GREEN scoped

- exact n=2 bare conformal Q2/Q3/Q4 expansion and momentum kernels;
- exact identification of the soft-spatial s-channel;
- exact fixed-lapse soft-s warning asymptotics;
- exact O(4) source-to-`A4`/`h00` map;
- exact nonseparability of the finite-Mc resolvent kernel and generalized potential `Psi_res`.

### YELLOW / decisive next gates

1. full cubic lapse/shift constraint reduction with the n=2 carrier;
2. specify/derive the nonlinear state-function completion of `alpha6` and include its perturbations;
3. test whether the reduced elastic `K3_s(q_s=0)` cancels;
4. only if it cancels or stays perturbative, build the exact reduced P(X)+curvature amplitude;
5. evaluate `Psi_res` for a controlled extended source and solve the modified O(4) `A4` equation rather than fitting a constant beta prematurely.

### RED / still open

- all-sector unitarity and loops;
- technical naturalness/RG protection;
- full general-background rank;
- compact objects/universal horizons and nonlinear strong-field sector.

No numerical `M_c` or `M_U` is selected here.
