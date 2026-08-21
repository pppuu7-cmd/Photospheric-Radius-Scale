# RTK Formula Bible — C8 Auxiliary / Dirac-Degeneracy Appendix

Iteration start: 2026-08-21 23:32:00 UTC+03:00 / 2026-08-21 20:32:00 UTC
Status: mixed GREEN / BLACK scoped / YELLOW constructive

## Purpose

This appendix records the constraint-architecture search that follows the exact but zero-H-singular minimal EH+clock+grad-K representation. The goal is to determine which auxiliary mechanisms can reproduce the RTK one-pole scalar response without introducing an extra physical mode or hiding the `H^-2` behavior inside a singular constraint matrix.

The statements here are quadratic and scoped. They do not constitute a final covariant completion.

## 1. Starting regularity problem

For the exact minimal grad-K scalar representation,

`U=(6H^2 M_*^2-K_clock)^2/(8 K_clock M_K^2 H^2)`.

For finite positive `K_clock/M_K^2`,

`U ~ H^-2`.

With the production identity

`K_clock=2 M_cosm^2 M_K^2`,

`lim_{H->0} H^2 U=M_cosm^2/4`.

CI: run `32522407137`, artifact `9461010370`.

Interpretation guard: the divergence of this unitary-gauge coefficient is not by itself a physical strong-coupling theorem. A field normalization `X=H chi` can make `(u/H^2)X^2=u chi^2` for `H!=0`, although that transformation itself loses invertibility at `H=0`. Physical regularity must ultimately be tested by canonical kinetic eigenvalues, the complete Dirac constraint algebra and the cutoff in a representation that remains well-defined at the static boundary.

## 2. Regular algebraic auxiliary — BLACK scoped

For one algebraic auxiliary,

`L_aux = 1/2 A(H)y^2 + B(H)yX + 1/2 C(H)X^2`.

Exact elimination gives

`C_eff=C-B^2/A`.

If `A(0)!=0` and `A,B,C` remain finite, `C_eff` remains finite. If `B~H^m`, `m>=0`, while one requires

`B^2/A ~ H^-2`,

then

`A ~ H^(2m+2) -> 0`.

Thus the algebraic auxiliary Hessian loses uniform rank at the static boundary.

For multiple algebraic auxiliaries,

`C_eff=C-b^T M^{-1}b`.

Finite `b,C` and a finite nonsingular `M(0)` imply finite `C_eff`; an `H^-2` reduced coefficient requires either a divergent unreduced coefficient or an eigenvalue of `M` approaching zero.

CI:

- run `32523115561`;
- artifact `9461246849`;
- digest `sha256:de8b3b6c49d7eb48321ed964059a048a168a818e5b7a521c66f0b8e4ddc84bc6`.

Status: BLACK only for regular algebraic auxiliaries with nonsingular static Hessian.

## 3. Pure `K^2` / Hořava-lambda deformation — BLACK scoped

Take

`M_*^2/2 [K_ij K^ij-K^2+eta K^2]`

with unchanged clock sector and completely general grad-K scalar `(U,V,W)`.

After exact lapse/shift elimination, demanding

`K_eff(p^2)=K_clock/H^2 (1+p^2/M_K^2)`

for all `p^2` produces a cubic polynomial identity. Its constant coefficient is

`-K_clock^2 M_*^2 M_K^2 eta`.

For finite nonzero physical scales exact matching forces

`eta=0`

independently of `(U,V,W)`.

Corrected CI:

- run `32524954554`;
- artifact `9461843454`;
- digest `sha256:48a693ffb07afd02d0de5c93b05892c0449c33f39c205fa3ce67ac9fe3972de1`;
- PASS marker `RTK_ROUTE_B_GRADK_K2_DEFORMATION_GATE_PASS`.

The initial red CI was an implementation-only contradiction: `eta` had been declared `nonzero=True` while the theorem asks for the solution `eta=0`. The analytic coefficient identity was unchanged.

Status: BLACK only for this pure `K^2` deformation with unchanged clock sector.

## 4. Single nondegenerate dynamical auxiliary — BLACK scoped

For

`L = 1/2 K0 X^2 + b X y + 1/2(A-Z omega^2)y^2`,

elimination gives

`K_eff=K0-b^2/(A-Z omega^2)`.

For finite nonzero `b,Z`, an additional frequency-plane pole occurs at

`omega_aux^2=A/Z`,

with reduced-kernel pole residue

`b^2/Z`.

If one tries to obtain `b^2/A~H^-2` with finite `b,Z` by taking `A~H^2`, then

`omega_aux^2 ~ H^2 -> 0`.

Thus the extra excitation becomes light at the static boundary rather than disappearing.

Corrected CI:

- run `32524978316`;
- artifact `9461850988`;
- digest `sha256:9b009bf05fa7f6e4cff7806294ed67e3326dac1980345b987644c82bf64160d3`;
- marker `RTK_ROUTE_B_GRADK_DYNAMIC_AUXILIARY_POLE_GATE_PASS`.

The initial red CI was only an overall-denominator-sign assertion; SymPy returned `-A+Z omega^2`, algebraically identical to `-(A-Z omega^2)`.

Status: BLACK only for the minimal single nondegenerate dynamical auxiliary.

## 5. Two ordinary positive dynamical auxiliaries — BLACK scoped

Let

`M(omega^2)=M0-omega^2 Z`

with real symmetric 2x2 matrices. Then

`det M = D0-D1 omega^2+D2 omega^4`,

where

- `D0=det M0`;
- `D1=tr(adj(M0) Z)`;
- `D2=det Z`.

Rank-one `Z` sets `D2=0`, but if

`M0>0`, `Z>=0`, `Z!=0`,

then `adj(M0)>0` and

`D1=tr(adj(M0)Z)>0`.

Therefore the determinant remains frequency dependent. A second ordinary healthy auxiliary does not provide an exact pole cancellation merely by making the kinetic matrix rank one inside this positive nondegenerate potential class.

CI:

- run `32524715584`;
- artifact `9461764440`;
- digest `sha256:b67497718867ecf565d944baba13b55a346edf209e9e2bac9b3f42f857047b68`.

Status: BLACK only for `M0>0`, `Z>=0` ordinary two-auxiliary frequency-denominator cancellation.

## 6. Constructive Dirac-degenerate rank-one kinetic system — YELLOW pending CI

The previous result does **not** exclude a genuinely degenerate theory in which constraints remove the would-be second mode.

Consider

`L = k/2 (dot X + a dot y)^2 - V(X,y)`,

with

`V=1/2 Omega^2 X^2+g X y+1/2 m^2 y^2`.

The velocity Hessian is

`K_vel=k v v^T`, `v=(1,a)`,

and has rank one.

The momenta obey

`p_X=k(dot X+a dot y)`,

`p_y=a p_X`,

so the primary constraint is

`phi1=p_y-a p_X=0`.

The canonical Hamiltonian is

`H_c=p_X^2/(2k)+V`.

Preserving `phi1` gives

`phi2=a V_X-V_y`

or

`phi2=(a Omega^2-g)X+(a g-m^2)y`.

Their Poisson bracket is

`{phi1,phi2}=m^2+a^2 Omega^2-2ag`.

For a positive-definite potential matrix

`Vmat=[[Omega^2,g],[g,m^2]]`,

this equals

`(a,-1)^T Vmat (a,-1)>0`.

Therefore the two constraints form a second-class pair. With two coordinates the original phase-space dimension is four, and

`N_DOF=(4-2)/2=1`.

### One-pole source response

At fixed spatial momentum,

`M(omega^2)=Vmat-k omega^2 v v^T`.

Define

`Q=v^T Vmat^{-1}v>0`.

The determinant lemma and Sherman-Morrison identity give exactly

`det M=det(Vmat)(1-kQ omega^2)`

and, for a source aligned with `v`,

`v^T M^{-1}v=Q/(1-kQ omega^2)`.

Thus the source channel has one finite pole

`omega_*^2=1/(kQ)>0`

and the response is

`(1/k)/(omega_*^2-omega^2)`.

Any positive single-pole target response

`R/(Omega_T^2-omega^2)`

can therefore be matched **pointwise** by

`k=1/R`,

`Q=R/Omega_T^2`.

This is a constructive structural escape: degeneracy can remove the extra physical DOF while retaining one healthy pole. It does not yet derive the required momentum/epoch dependence or source alignment from one RTK gravitational action.

Implementation:

- source `rtk/route_b_dirac_degenerate_one_dof_gate.py` on `rtk-class-build`;
- corrected source commit `d9de97a87c3b68fe3ea83789438cc544bb79854f`;
- workflow `.github/workflows/rtk-route-b-dirac-degenerate-one-dof.yml`;
- corrected trigger `7914d851c6931be450fd668d15b6173025daeec6`.

Status: YELLOW until the corrected GitHub artifact is inspected.

## 7. Current C8 decision tree

If the Dirac-degenerate gate passes CI, the preferred local path becomes:

1. embed the rank-one kinetic pair into the full FLRW lapse/shift scalar constraint block;
2. derive the source direction from the same action;
3. require one physical scalar DOF after the **full** Dirac count;
4. match RTK pole, residue and polynomial remainder for the same invariant-dependent coefficient functions over multiple epochs;
5. test whether the canonical kinetic eigenvalue and constraint brackets remain finite in the static limit, rather than judging `U~H^-2` alone;
6. apply no-ghost, gradient/hyperbolicity, Newton/PPN, GW, compact-object and EFT-cutoff gates to that same action.

If the full gravitational embedding fails, the remaining qualitatively distinct routes are a controlled branch-changing theory or retarded/nonlocal completion; repeating ordinary algebraic/positive auxiliary matrices is no longer useful.
