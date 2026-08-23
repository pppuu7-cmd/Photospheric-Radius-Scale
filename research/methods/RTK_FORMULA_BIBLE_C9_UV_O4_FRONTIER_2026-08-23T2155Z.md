# RTK Formula Bible — C9 UV + finite-Mc O(4) current frontier

Updated: 2026-08-23 21:55 UTC
Status: **CURRENT FRONTIER — use together with the current pointer before older C8/C9 notes**

## 0. Scope and reading rule

This addendum records the current research state after the finite-Mc U(1) source-transfer work, the exact P(X) 2->2 tree benchmark, the generalized Lorentz-breaking partial-wave normalization, and the intrinsic-spatial-curvature UV-carrier gates.

It does **not** supersede the corrected C8 Dirac-order addenda.  The physical coupled-constraint order remains:

1. genuine auxiliary pair `(p_Q,C_Lambda)`;
2. exact auxiliary Dirac projection;
3. reduced chain `(pi_N,Jhat,Hperp_hat,phi_hat)`;
4. punctured low-k rank rather than exact k=0 rank;
5. finite-Mc source transfer and PPN;
6. scalar strong-coupling / UV completion;
7. technical naturalness and strong-field gates.

C9 is **not globally GREEN**.  The results below are scoped theorems that narrow the remaining work.

---

## 1. Frozen finite-Mc matter filter

The exact reduced ordinary-matter filter is

`f(k)=a_eff=k^2/(M_c^2+k^2)`.

The neutral RTK scalar is not part of the filtered ordinary-matter `H0` source.

Static O(2) projectable PPN transfer on the parent branch `a1=1,a2=0,g1=-1` gives

`gamma_PPN=1`,

`G_N(k)=G f(k)`.

The exact local deficit is

`1-G_N/G=M_c^2/(M_c^2+k^2)`.

At O(3), after exact auxiliary reduction and continuity,

`alpha1=8(1/f-1)=8 M_c^2/k^2`,

`alpha2-zeta1+2 xi = 2 M_c^2(2 lambda_HL-1)/[k^2(lambda_HL-1)]`.

Therefore a symbolic local alpha1 tolerance `|alpha1|<=eps1` gives

`M_c^2 <= eps1 k_local^2/8`.

Combined with the 1% cosmology-side filter requirement,

`M_c^2 >= 99 k_cos^2`,

an allowed symbolic window exists iff

`99 k_cos^2 <= eps1 k_local^2/8`.

The corrected alpha1/cosmology gate rerun is GREEN.

---

## 2. O(4) nonlocality reduces to one new resolvent derivative

After exact auxiliary elimination the matter Hamiltonian can be organized as

`H_m = N H0 + N^i H_i - A f_g H0`,

where `f_g` is the metric-dependent elliptic filter.

At fourth PN order,

`[f_g H0]_(4) = f0 H0^(4) + delta f[h^(2)] H0^(2)`.

The metric variation of the filtered interaction is

`delta_g(-A f_g H0) = -A[(delta f/delta g)H0 + f(delta H0/delta g)]`.

For nonrelativistic PN matter the term `A f delta H0/delta g` starts at O(6), so the **new finite-Mc O(4) nonlocal metric source** is controlled by the same operator that already appears in the filtered A-source:

`delta f = -(1/M_c^2) L^{-1} delta(D^2) L^{-1}`.

Thus the new nonlocal O(4) problem requires one resolvent-derivative convolution kernel, not two independent nonlocal kernels.  Ordinary stress terms remain in the parent/local source sector.

Provenance:

- run `32667262375` GREEN;
- artifact `9500369775`;
- digest `sha256:1238b071d5f1b90b4d0bc454eb727bb92c5c0fd813590420fd7cdc4a1447b340`.

The full O(4) coefficient solve for `beta,alpha2,zeta_i,xi` is still pending.

---

## 3. Exact P(X)-only elastic 2->2 tree amplitude

For the low-k canonically normalized P(X) scalar with

`Z(k)=1+k^2/M_K^2`,

`omega^2=c_a^2 k^2/Z(k)`,

the exact elastic equal-|k| COM P(X)-only tree amplitude is

`M_P = [24 C4t omega^4 - 8 C4ts k^2 omega^2 + 8 C4s k^4(1+2 cos^2 theta) + 4(C3s k^2-3 C3t omega^2)^2]/Z(k)^2`.

The t/u cubic P(X) exchange vertices vanish exactly for equal-|k| elastic kinematics; the s-channel survives.

This is a same-sector tree theorem only.  Mixed C(X), metric/U(1)/auxiliary exchange, loops and inelastic channels remain outside this statement.

---

## 4. Generalized identical-scalar phase-space factor

For an isotropic Lorentz-breaking dispersion `omega=omega(k)`, identical final scalars give

`Phi_2 = k^2/[8 pi omega(k)^2 v_g(k)]`,

where `v_g=d omega/dk`.

Define

`g(k)=k^2/[2 omega(k)^2 v_g(k)]`.

With the standard angular convention

`a_l=(1/32pi) integral_{-1}^{1} dcos(theta) P_l M`,

the elastic eigen-amplitudes are

`tilde a_l = g(k) a_l`,

and the tree-level elastic perturbative bound is

`|Re tilde a_l| <= 1/2`.

For linear dispersion `omega=u k`, this reduces exactly to

`g=1/(2u^3)`,

matching the known Lorentz-breaking partial-wave normalization.

For the production rational RTK dispersion,

`g(k)=(1+k^2/M_K^2)^(5/2)/(2 c_a^3)`.

The l=0 mode is the first P(X)-only channel to reach the tree bound on the frozen trajectory.

Provenance:

- run `32667382107` GREEN;
- artifact `9500404197`;
- digest `sha256:68df8cb62ed305166e3579ca1a63b677a366b975b27c61d678d8bcfedd2f88ee`.

---

## 5. Single-channel P(X) momentum cutoff

The certified first-crossing values include

`k_unit(z=0)=2.7822563629876347e-9 eV`,

`k_unit(z=1100)=1.5205675937379003e-6 eV`.

The cutoff is not strictly monotonic in redshift.  It has a transition overshoot near

`z ~= 3.9810617e5`,

`k_unit ~= 2.5951398e-4 eV`,

and approaches the early plateau

`k_unit,early = 1.9807199478328038e-4 eV`.

The early-edge analytic result is

`k_unit^4 = 24 pi M_Pl^2 mu_K^2 sqrt(sqrt(lambda_D)+1)/(29 lambda_D)`.

This is **not** an all-sector EFT cutoff.  It is a certified P(X)-only elastic tree partial-wave boundary that localizes where UV completion / the omitted channels must be treated explicitly.

---

## 6. B9 momentum demand is far below the P(X)-only cutoff

The production likelihood input uses

`P_k_max_h/Mpc = 5.0`,

with frozen `h=0.691103719964454`.

A deliberately excessive safety envelope treats the full configured comoving maximum as physical at every epoch through `z=1e9`:

`k_phys,max(z)=5 h (1+z) Mpc^-1`.

The minimum ratio on the dense redshift scan is

`k_unit/k_phys,max = 8.963423475287682e15`

at `z=1e9`.

Therefore the finite single-channel cutoff does not threaten the explicit B9 production k-range over this conservative envelope.

Provenance:

- final run `32667878699` GREEN;
- artifact `9500535634`;
- digest `sha256:de1d06623970ca6e423f31d4f662af7e89de4ac98efca454cc85e3fd6707e64c`.

B6 AlterBBN is a homogeneous H(T)+nuclear-network gate and has no perturbation Fourier-k requirement.

---

## 7. Higher-spatial quadratic completion window

Consider the quadratic family

`omega_n^2 = c_a^2 k^2 [1+(k/M_U)^(2n)]/[1+k^2/M_K^2]`.

At high momentum,

`g(k) ~ M_U^(3n) k^(3-3n)/(2 n c_a^3 M_K^3)`.

Hence

- `n=1`: phase space approaches a constant;
- `n=2`: `g~k^-3`;
- `n=3`: `g~k^-6`.

If the allowed fractional quadratic correction at the maximum observational momentum is `eps`, then a scale window exists when

`k_obs eps^(-1/(2n)) <= M_U <= k_unit`.

The present B9-to-cutoff hierarchy leaves an enormous symbolic window; no numerical `M_U` is selected.

Provenance:

- run `32667427647` GREEN;
- artifact `9500415622`;
- digest `sha256:3fc674f1c6da348deb4c1ebf215de4ae82fc8681d053517b7ceb886ad61f1318`.

---

## 8. Natural carrier inside the existing spatial-covariant RTK architecture

Use the already certified flat-FLRW scalar metric

`gamma_ij=a^2 exp(2 zeta) delta_ij`.

At linear scalar order

`R3^(1)=-4 a^-2 Delta zeta=4 y zeta`, `y=k^2/a^2`.

Therefore

`(R3)^2 -> 16 y^2 zeta^2`,

`D_i R3 D^i R3 -> 16 y^3 zeta^2`.

Adding

`alpha4 (R3)^2`,  `alpha4=-G/[32 H^2 M_U^2]`,

gives

`omega^2=c_a^2 y(1+y/M_U^2)/(1+y/M_K^2)`.

Adding

`alpha6 D_i R3 D^i R3`,  `alpha6=-G/[32 H^2 M_U^4]`,

gives

`omega^2=c_a^2 y(1+y^2/M_U^4)/(1+y/M_K^2)`.

Since `G=rho+p=2 X P_X`, the coefficient can be represented as a fixed state-function of the same clock rather than an epoch-by-epoch fitted number.

Neither carrier contains time derivatives, so the quadratic velocity Hessian is unchanged.

For TT perturbations on flat FLRW,

`R3^(1)=d_i d_j h_ij-Delta h=0`,

so these scalar-curvature invariants do not change the flat-FLRW quadratic tensor/GW dispersion.

Provenance:

- run `32667654954` GREEN;
- artifact `9500478779`;
- digest `sha256:a425cb249d43b3f2a6bb8539ef9641a80c52fe27e4cd26c413481c47dee9659d`.

---

## 9. Curvature-carrier UV power counting

For the family schematically `[D^(n-1)R3]^2`, the number of spatial derivatives in a bare m-point curvature vertex remains `2n+2`.

With the existing high-k external normalization `Z^(1/2)~k/M_K`,

`V3~k^(2n-1)`,

`V4~k^(2n-2)`.

For the completed dispersion `omega^2~k^(2n)`, contact and exchange amplitudes have the same asymptotic scaling

`M~k^(2n-2)`.

Combining with `g~k^(3-3n)` gives

`g a_l ~ k^(1-n)`.

Therefore

- `n=1`: `g a_l -> constant`; coefficient-level amplitude test still required;
- `n=2`: `g a_l ~ k^-1`;
- `n=3`: `g a_l ~ k^-2`.

This makes the minimal six-spatial-derivative carrier

`D_i R3 D^i R3`

the current preferred UV candidate **for further testing**, not yet a promoted final term.

Provenance:

- run `32667760220` GREEN;
- artifact `9500500639`;
- digest `sha256:3a920a81583a8abd08537812f4b4517cddf754a6cda57e7bc31ca099170d527b`.

---

## 10. Current scientific classification

### GREEN within explicit scope

- corrected auxiliary Dirac order and exact elliptic matter filter;
- flat-FLRW punctured low-k leading rank;
- finite-Mc static O(2) Newton transfer;
- finite-Mc O(3) alpha1 and preferred-frame combination;
- one-resolvent structure of the new O(4) nonlocal source;
- exact P(X)-only elastic tree amplitude;
- generalized isotropic phase-space / partial-wave normalization;
- finite P(X)-only tree momentum cutoff;
- huge B9-k safety margin relative to that cutoff;
- intrinsic-curvature quadratic UV carrier;
- favorable n>=2 curvature-carrier asymptotic power counting.

### YELLOW / open

- full finite-Mc O(4) coefficient solve and source-specific observables;
- nonlinear lapse/shift reduction with the n=2 curvature carrier;
- exact cubic/quartic reduced n=2 vertices and their interference with P(X);
- mixed C(X), metric/U(1)/auxiliary exchange in the unitarity matrix;
- inelastic channels and loops;
- intermediate/high-k full constraint rank beyond the controlled low-k branch;
- curved/anisotropic/inhomogeneous-lapse rank;
- compact objects / universal horizons;
- same-action strong-field and GW checks away from flat-FLRW quadratic TT;
- radiative stability / RG protection of the exceptional U(1) surface.

### RED / not solved

C9 technical naturalness is not solved.  The known parent U(1)-Hořava analysis indicates the exceptional scalar-graviton-free coupling surface is not technically natural without additional protection.

---

## 11. Immediate research order

1. Expand the preferred n=2 carrier `D_i R3 D^i R3` through cubic and quartic scalar order on the flat rolling patch.
2. Include lapse and shift perturbations and solve their constraints to obtain reduced cubic/quartic n=2 vertices.
3. Compute the exact P(X)+curvature 2->2 amplitude and partial waves; test whether `g a_l` actually decreases before promoting the carrier.
4. In parallel, assemble the complete finite-Mc O(4) parent + filtered source equation using the single resolvent derivative and solve the coefficient system for `beta,alpha2,zeta_i,xi`.
5. Only after 3-4 close, intersect the PPN `M_c` window, rank window and any UV `M_U` window without fitting either scale to data.
6. Then revisit technical naturalness/RG protection and strong-field constraints.

No numerical `M_c` or `M_U` is selected by these theorems.
