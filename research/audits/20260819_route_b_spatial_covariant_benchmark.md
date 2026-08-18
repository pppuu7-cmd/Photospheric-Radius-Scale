# Route-B preferred-foliation spatially covariant benchmark — 2026-08-19

## Goal

Construct an explicit **local metric+Khronon nonlinear benchmark** that reproduces the already established RTK scalar quadratic target while keeping the lapse nondynamical in the preferred foliation. This is a Route-A1/Route-B bridge: it is more complete than the reduced scalar EFT, but it deliberately does not yet include the causal nonlocal RT sector.

## Benchmark action

Use ADM variables adapted to the physical preferred foliation,

`S_bench = ∫ dt d^3x N sqrt(gamma) [ M_Pl^2/2 (R3 + K_ij K^ij - K^2) + F(N) + C(N) a_i a^i ]`,

with

`a_i = D_i ln N`.

The clock Stückelberg dictionary is

`X = -(∇T)^2/2 = 1/(2N^2)` in unitary gauge,

so choose

`F(N) = P[X(N)]`,

where `P(X)` is the already established conditional barotropic long-wave reconstruction.

Primary Hamiltonian reference: X. Gao, arXiv:1409.6708. Its spatially covariant framework permits coefficients/potentials depending on `N` and arbitrary **spatial** derivatives, explicitly discusses `a_i=partial_i ln N`, and shows that when the lapse enters nonlinearly the lapse primary/secondary constraints become second class, giving the generic physical count `2 tensor + 1 scalar` for the no-lapse-velocity class.

## Exact scalar quadratic matching

Use the local Goldstone convention

`T = T_bar(t+pi)`

and normalize the local background so

`X = X0[(1+dot pi)^2-(grad pi)^2]`.

Expanding `P(X)` gives exactly

`L2_PX = K/2 dot(pi)^2 - G/2 (grad pi)^2`,

with

`G=2 X P_X=rho+p`,

`K=2 X P_X+4 X^2 P_XX=(rho+p)/c_a^2`.

For the lapse,

`N/N0 = sqrt(X0/X)`,

therefore

`delta ln N = -dot(pi) + O(pi^2)`.

Thus

`a_i = -partial_i dot(pi) + O(pi^2)`

and the acceleration potential contributes

`C_bg (grad dot(pi))^2`.

Choosing

`C_bg = K/(2 M^2)`

reproduces the exact established finite-k quadratic target

`L2 = K/2 dot(pi)^2 + K/(2M^2)(grad dot(pi))^2 - G/2(grad pi)^2`,

and hence

`omega^2 = (G/K) q^2/[1+q^2/M^2]`.

The benchmark can therefore use `M=M_K=k_star` on the background. Along the monotonic barotropic branch one may regard `C(N)` (equivalently `C(X)`) as the nonlinear coefficient function whose background value tracks `K(X)/(2M(X)^2)`.

## ADM velocity-Hessian check

At a local `N=1`, zero-shift patch, the Einstein-Hilbert velocity dependence is

`Q_EH = 1/4 [dot(gamma)_ij dot(gamma)^ij - (tr dot(gamma))^2]`.

The benchmark additions `F(N)` and `C(N)a_i a^i` contain **no `dot N`** and no new metric velocities. The exact symbolic Hessian with respect to the six independent `dot(gamma)_ij` components plus `dot N` has

- dimension `7`;
- rank `6`;
- one null vector, exactly the `dot N` direction.

On the transverse-traceless metric-velocity subspace the principal kinetic form remains the GR form. Thus the new acceleration sector does not alter the tensor principal kinetic operator at this level.

## Constraint-count scope

For the declared spatially covariant class:

- configuration variables: `gamma_ij(6), N(1), N^i(3)` → phase-space dimension 20;
- spatial diffeomorphisms give the three shift primaries plus three momentum constraints: six first-class constraints;
- nonlinear lapse with no lapse velocity gives the lapse primary/secondary second-class pair in the generic Gao class.

Therefore

`N_DOF = (20 - 2*6 - 2)/2 = 3`,

corresponding to two tensor modes and one scalar preferred-foliation mode.

This count is a theorem about the declared preferred-foliation spatially covariant benchmark class; it is not an assertion that an arbitrary unrestricted covariant scalar-tensor rewriting is a regular DHOST theory. The companion acceleration-degeneracy audit explains that distinction.

## Machine proof

`rtk/route_b_spatial_covariant_benchmark.py`

checks:

1. exact P(X) quadratic expansion;
2. `delta ln N=-dot(pi)` at first order;
3. exact coefficient `C_bg=K/(2M^2)`;
4. exact rational dispersion;
5. 7×7 ADM velocity-Hessian rank 6 with pure `dot N` null vector;
6. nondegenerate TT metric kinetic subspace;
7. the declared Hamiltonian constraint count `3` physical DOF.

## Scientific consequence

If the machine proof passes, the project has an explicit nonlinear **local preferred-foliation metric+Khronon benchmark** that reproduces all already frozen scalar quadratic data and has the intended local physical DOF count under the spatially covariant Hamiltonian theorem.

This is a substantial C7 subgate because the missing finite-k denominator no longer requires an unspecified operator: the operator is explicitly `a_i a^i` with a fixed background coefficient.

## Remaining C7 boundary

This does **not** yet close C7 because the actual production cosmology also contains the causal RT/nonlocal metric sector. Still required:

- formulate the coupled causal-RT + ADM-Khronon system consistently at nonlinear/constraint level;
- verify that the RT causal auxiliary prescription does not change the local metric/Khronon constraint count or activate an unwanted propagating mode;
- establish the full coupled nonlinear equations in the regime needed by the model.

C8 and C9 also remain open: `C(N)` beyond its background quadratic match and the rest of the nonlinear interaction functions determine the physical cutoff and radiative closure.
