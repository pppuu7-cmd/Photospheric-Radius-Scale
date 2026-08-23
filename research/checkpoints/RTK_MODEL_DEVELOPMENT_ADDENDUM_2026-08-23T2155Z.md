# RTK model development checkpoint — 2026-08-23 21:55 UTC

Status: **CURRENT DURABLE CHECKPOINT**

This checkpoint records the latest verified state so continuation does not depend on chat history.

## Newly closed scoped gates

1. **Finite-Mc O(4) one-resolvent source support**
   - run `32667262375` — GREEN
   - artifact `9500369775`
   - digest `sha256:1238b071d5f1b90b4d0bc454eb727bb92c5c0fd813590420fd7cdc4a1447b340`
   - result: the new finite-Mc O(4) nonlocal source is governed by a single resolvent derivative `delta f=-(1/M_c^2)L^-1 delta(D^2)L^-1`; the filtered-stress metric term is O(6) for nonrelativistic PN matter.

2. **Exact P(X)-only partial-wave/phase-space unitarity**
   - run `32667382107` — GREEN after CI-only type fix
   - artifact `9500404197`
   - digest `sha256:68df8cb62ed305166e3579ca1a63b677a366b975b27c61d678d8bcfedd2f88ee`
   - generalized identical-scalar factor `g=k^2/(2 omega^2 v_g)`
   - first-channel cutoff values:
     - `k_unit(0)=2.7822563629876347e-9 eV`
     - `k_unit(1100)=1.5205675937379003e-6 eV`
     - early plateau `1.9807199478328038e-4 eV`
   - transition overshoot near `z=3.9810617e5`, `k_unit~=2.5951398e-4 eV`.

3. **B9 k-window safety margin**
   - final run `32667878699` — GREEN
   - artifact `9500535634`
   - digest `sha256:de1d06623970ca6e423f31d4f662af7e89de4ac98efca454cc85e3fd6707e64c`
   - with the entire configured `5 h/Mpc` envelope conservatively redshifted to every epoch through `z=1e9`, minimum `k_unit/k_phys,max = 8.963423475287682e15`.
   - B6 AlterBBN has no perturbation Fourier-k demand.

4. **Higher-spatial UV quadratic window**
   - run `32667427647` — GREEN
   - artifact `9500415622`
   - digest `sha256:3fc674f1c6da348deb4c1ebf215de4ae82fc8681d053517b7ceb886ad61f1318`
   - family `omega_n^2=c_a^2 k^2[1+(k/M_U)^(2n)]/[1+k^2/M_K^2]`
   - symbolic window `k_obs eps^(-1/(2n)) <= M_U <= k_unit`.

5. **Intrinsic-curvature UV carrier**
   - run `32667654954` — GREEN
   - artifact `9500478779`
   - digest `sha256:a425cb249d43b3f2a6bb8539ef9641a80c52fe27e4cd26c413481c47dee9659d`
   - `(R3)^2` gives p^4 numerator completion;
   - `D_i R3 D^i R3` gives p^6 numerator completion;
   - both leave the flat-FLRW quadratic TT dispersion unchanged because `R3^(1)=0` on TT perturbations;
   - no new time derivatives enter the quadratic velocity Hessian.

6. **Curvature-carrier UV power counting**
   - run `32667760220` — GREEN
   - artifact `9500500639`
   - digest `sha256:3a920a81583a8abd08537812f4b4517cddf754a6cda57e7bc31ca099170d527b`
   - for `[D^(n-1)R3]^2`, `g a_l ~ k^(1-n)`;
   - n=1 is marginal/constant;
   - n=2 gives `k^-1` and is the current preferred minimal candidate for deeper testing.

## Current preferred UV candidate

Do not promote it yet, but the leading candidate for the next same-action test is

`Delta S_UV = integral N sqrt(gamma) alpha6(X,H) D_i R3 D^i R3`,

with quadratic matching

`alpha6 = -G/[32 H^2 M_U^4]`, `G=rho+p=2 X P_X`,

which gives

`omega^2 = c_a^2 y(1+y^2/M_U^4)/(1+y/M_K^2)`.

This candidate is preferred only because:

- it is purely spatial at the tested level;
- it leaves the known rational kinetic denominator intact;
- it does not shift flat-FLRW quadratic tensor dispersion;
- its asymptotic partial-wave power counting is softer than n=1.

It is **not yet a complete UV completion**.

## Current O(4) PPN reduction

The full finite-Mc O(4) problem is now organized as:

`parent/local O(4) source + diagonal f(k) filtering + one new delta f/delta g convolution`.

The next task is to insert this decomposition into the parent projectable O(4) coefficient equations and solve for the full PPN set rather than treating the resolvent piece as a standalone observable.

## Current scientific status table

| Sector | Status |
|---|---|
| Corrected auxiliary Dirac order | GREEN |
| Flat-FLRW punctured low-k leading rank | GREEN scoped |
| Full classical rank on general backgrounds | YELLOW |
| Static O(2) finite-Mc Newton transfer | GREEN |
| O(3) alpha1 + preferred-frame combination | GREEN scoped |
| Full O(4) PPN coefficient solve | YELLOW |
| P(X)-only exact tree amplitude | GREEN scoped |
| P(X)-only partial-wave cutoff | GREEN scoped |
| B9 momentum safety margin | GREEN |
| Quadratic intrinsic-curvature UV carrier | GREEN scoped |
| n=2 UV asymptotic power counting | GREEN scoped |
| Exact reduced n=2 cubic/quartic amplitude | YELLOW |
| Mixed C(X)+metric/U1/auxiliary unitarity | YELLOW |
| Technical naturalness / RG protection | RED / open |
| Compact objects / universal horizons | RED / open |

## Immediate continuation queue

1. Exact cubic and quartic scalar expansion of `D_i R3 D^i R3` on the conformally-flat rolling patch.
2. Add lapse/shift dependence and perform nonlinear constraint reduction.
3. Exact 2->2 P(X)+n=2 carrier partial-wave scan, including interference.
4. Full projectable finite-Mc O(4) source equation and PPN coefficient solve in parallel.
5. Intersect rank, PPN and UV scale windows symbolically; do not choose `M_c` or `M_U` by fit before the structural gates close.
6. Technical-naturalness/RG and compact-object gates remain mandatory before calling the theory complete.

Canonical detailed formulas are in `research/methods/RTK_FORMULA_BIBLE_C9_UV_O4_FRONTIER_2026-08-23T2155Z.md`.
