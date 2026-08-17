# RTK quantum / EFT consistency frontier v4

Date: 2026-08-18

Status: **Route A1 nonlinear scalar program advanced beyond v3; full coupled RT + metric + Khronon ghost/constraint theorem, finite-k nonlinear completion and physical strong-coupling scale remain open.**

This checkpoint inherits the quadratic-EFT, strong-coupling non-identifiability and Route-A1 cubic-basis evidence recorded in v2/v3 and adds the long-wave P(X), D4-identifiability and D5-dispersive results established since then. It is not a UV-completion claim.

## 1. Quadratic baseline inherited from v2/v3

The implemented scalar dispersion admits the constructive local preferred-frame quadratic action

`L2 = K/2 dot(pi)^2 + K/(2 M^2) (grad dot(pi))^2 - G/2 (grad pi)^2`,

with `G=rho+p>0`, `K=(rho+p)/c_a^2>0`, `M=k_star>0`.

The Fourier kinetic operator is `K(1+q^2/M^2)>0` and reproduces the implemented finite-k sound speed. This remains a reduced-scalar existence theorem, not the unique fundamental nonlinear action.

## 2. Explicit nonlinear research class — Route A1

Route A1 freezes a preferred-frame, spatial-translation/rotation invariant, parity-even, constant-shift-symmetric reduced scalar EFT. Lorentz invariance and time reversal are not assumed. Coefficients may vary adiabatically with cosmological background time.

Through cubic order and total derivative order `D<=4`, the complete basis modulo spatial integration by parts is

- `O1 = dot(pi)^3`,
- `O2 = dot(pi) (grad pi)^2`,
- `O3 = dot(pi)^2 Laplacian(pi)`,
- `O4 = (grad pi)^2 Laplacian(pi)`.

The velocity Hessian contains no higher time derivatives and remains invertible perturbatively while its kinetic operator does not cross zero. Thus the reduced scalar sector has one canonical pair through this cubic truncation.

## 3. Long-wave P(X) subsector fixes D3 coefficients

For the conditional shift-symmetric barotropic `P(X)` long-wave subsector, exact symbolic identities establish

`x d rho/dx = rho+p`,

`dp/d rho = c_a^2`,

`d ln X/d ln x = 2 c_a^2`,

with quadratic matching `G=rho+p`, `K=(rho+p)/c_a^2`.

Consequently

`c1 = (dK/dlnX - K)/3 = ((dK/dlnx)/(2 c_a^2)-K)/3`,

`c2 = -(K-G)/2`.

Machine theorem provenance: workflow run `32074936280`, job `95525982737`, artifact `9303072040`, SHA256 `4d51c32d2a1537c013746a1dfe56074ed05d348f7d5117a11d6f4fb8434d7a73`.

## 4. DBI dust-limit asymptotics

Let `L=sqrt(lambda_D)` and take the large-x branch. Exact algebra gives

`x w -> 1/[L(L+1)]`,

`x^2 c_a^2 -> 1/[L^2(L+1)]`,

`K/x^3 -> C L(L+1)^2`,

`d ln K/d ln x -> 3`,

`c_a^2 (c1/K) -> 1/2`,

`c2/K -> -1/2`.

Thus very large `c1/K` on the dust-like cosmological branch is an analytic small-`c_a^2` effect, not by itself evidence of finite-difference failure.

## 5. D4 coefficient identifiability no-go

`c3` and `c4` multiply operators that vanish on a homogeneous background and first enter at cubic perturbative order. The transformation

`c3 -> c3 + alpha`, `c4 -> c4 + beta`

leaves the entire background and quadratic action unchanged while changing the cubic theory.

Therefore **background thermodynamics plus the complete linear CLASS target cannot determine c3 or c4**. Their values require an additional nonlinear postulate or a deeper fundamental derivation.

Science code: `rtk/quantum_route_a1_d4_identifiability.py`.

## 6. D5 dispersive identifiability no-go

The quadratic dispersive term

`K/(2 M^2) (grad dot(pi))^2`

has total derivative order D=4. A valid shift-symmetric preferred-frame nonlinear completion can contain

`alpha K/(2 M^2) dot(pi) (grad dot(pi))^2`,

which is cubic derivative order D=5. Different `alpha` give exactly the same quadratic `K,M` but different nonlinear scattering.

Therefore:

- the closed cubic basis at `D<=4` is not sufficient for a physical strong-coupling analysis at `q~M`;
- linear `M_K/k_star` cannot identify the first nonlinear dispersive coupling;
- `M_K/k_star` cannot be promoted to a physical cutoff from the linear target.

Science code: `rtk/quantum_route_a1_d5_dispersive_nogo.py`.

## 7. Canonical D3 coefficient proxies

At `q<<M`, with `pi_c=sqrt(K_phys) pi`, the D3 coefficient-suppression proxies satisfy

`Lambda_i^2 = K_phys^(3/2)/|c_i,phys| = Mpl_bar sqrt(K_8piG)/|c_i/K|`.

These `Lambda_1,Lambda_2` are useful bookkeeping scales for the long-wave D3 coefficients only. They are **not** declared strong-coupling cutoffs because small sound speed, momentum-dependent normalization and unknown D4/D5 nonlinear interactions remain relevant.

A pinned one-point background diagnostic at the current RTK center has already solved the RT root `gamma=0.05166338653500` to printed precision. The first run failed only while opening a missing output directory after the background calculation had succeeded; the workflow was fixed and hardened to report coefficient proxies with an explicit non-cutoff interpretation boundary.

## 8. RT nonlocal sector theorem boundary

The RT sector is defined by a causal/retarded nonlocal equation. Its published formulation does not supply a closed local fundamental action analogous to the RR action. Localizing auxiliary variables must not automatically be counted as arbitrary propagating fields.

The project therefore separates:

1. reduced Khronon nonlinear completion;
2. causal RT nonlocal DOF prescription with fixed homogeneous auxiliary data;
3. coupled metric + RT + Khronon constraint/response consistency.

## 9. Closure map

🚀 Closed: explicit nonlinear Route A1 symmetry class selected.

🚀 Closed: complete Route A1 cubic basis through D<=4.

✅ Closed: reduced-scalar cubic one-canonical-pair statement under invertible velocity Hessian.

✅ Closed conditionally: long-wave P(X) reconstruction of c1 and c2.

✅ Closed as an identifiability result: c3,c4 cannot be inferred from background + linear target alone.

✅ Closed as a methodology result: linear dispersive M/k_star does not determine the D5 nonlinear coupling or physical cutoff.

🔴 Open: choose/derive the finite-k nonlinear completion, including the D5 dispersive layer relevant near q~M.

🔴 Open: physical strong-coupling scale using the full momentum-dependent canonical normalization.

🔴 Open: full coupled metric/lapse/shift + causal RT + Khronon constraint algebra and total physical DOF count.

🔴 Open: radiative stability/counterterm closure/naturalness.

🔴 Open: UV completion.

## 10. Next valid theory step

The next non-redundant theorem layer is to enumerate the cubic `D=5` preferred-frame basis relevant to the dispersive quadratic operator and then choose or derive a concrete nonlinear dispersive subroute. Only after that should interaction scales be promoted beyond the present long-wave D3 coefficient proxies.
