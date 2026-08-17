# RTK quantum / EFT consistency frontier v2

Date: 2026-08-17

This checkpoint records the strongest reproducible statements currently justified for the implemented RTK/Khronon scalar sector. It is deliberately narrower than a UV-completion or nonlinear ghost-free theorem.

## Reproducible evidence

### Q1 — classical algebraic stability: PASS

Workflow run `31975991159` completed successfully.

Broad-grid checks retained positive `Q`, `rho`, `1+w`, non-negative/positive sound-speed quantities in their physical domains, and positive DBI margin. This is a classical algebraic sign audit, not a fundamental Hamiltonian proof.

### Q2 — original finite-difference quadratic proxy: SUPERSEDED NUMERICAL FAILURE

Workflow run `31978863354` is recorded as `failure`, but the physics grid itself retained positive gradient and kinetic proxies. The failed assertion was the relative numerical comparison of tiny quantities `c_a^2` and a finite-difference estimate of `dp/drho` at extreme scales (`c_a^2` reaching roughly 1e-15 ... 1e-22), where floating-point cancellation destroyed relative derivative accuracy.

This run is therefore retained as a useful numerical-audit failure, not evidence for a negative kinetic or gradient mode.

Its physical conclusion remains valid: because the implemented sector has explicit

`c_s^2(k) = c_a^2 / [1 + (k/k_*)^2]`,

a pure local two-derivative `P(X)` scalar is insufficient for the full finite-k implementation. Preferred-frame higher-spatial-derivative or auxiliary EFT structure is required.

### Q3 — constructive local quadratic EFT reconstruction: PASS

Workflow run `31982347734` completed successfully.
Artifact `rtk-quantum-local-quadratic-eft`, artifact ID `9272723493`, uploaded ZIP SHA256
`b8b45113e267825fdc9676a4f95f5839d157e8e80e7ec970bbed008050d429a4`.

The symbolic audit proves exactly

`c_a^2 = dp/drho`

for the coded background, replacing the unstable finite-difference test.

A local preferred-frame quadratic reconstruction exists:

`L2(q) = 1/2 K [1 + q^2/M^2] |pi_dot|^2 - 1/2 G q^2 |pi|^2`,

with

- `G = rho + p`,
- `K = (rho+p)/c_a^2`,
- `M = k_*`.

It gives exactly

`omega^2 = (G/K) q^2/[1+q^2/M^2]`,

matching the implemented finite-k dispersion.

The corresponding Fourier-mode Hamiltonian

`H = P^2/[2 K(1+q^2/M^2)] + G q^2 pi^2/2`

is positive for `G>0`, `K>0`, `M^2>0`. The CI run scanned 3430 points and found no sign violations, with minimum scanned `G=1.000000000001e-12`, minimum `K=1.0000000000020002`, and minimum mode kinetic coefficient `1.0000000000020002`.

The candidate contains higher spatial derivatives but no higher time derivative.

Classification:

`CONSTRUCTIVE_LOCAL_QUADRATIC_EFT_EXISTENCE_AT_LINEAR_LEVEL`.

This is an existence result for a healthy quadratic representative of the implemented linear sector. It is not a claim that this representative is the unique or fundamental nonlinear action.

### Q4 — strong-coupling identifiability theorem: PASS

Workflow run `31982495371` completed successfully.

The symbolic construction shows that arbitrary cubic and higher operators can leave the quadratic Hessian unchanged. Therefore the current linear CLASS implementation cannot determine a unique strong-coupling scale.

Consequences:

- `M_K` / `k_*` is a proven dispersive scale, not a proven strong-coupling cutoff;
- a strong-coupling scale is underdetermined by the current linear equations;
- new information is required: an explicit nonlinear EFT completion and its cubic/higher coefficients.

## Current theorem frontier

✅ Background algebraic sign stability over broad scans.

✅ Exact symbolic barotropic identity `c_a^2 = dp/drho`.

✅ Positive quadratic gradient coefficient `G=rho+p` on the tested physical domain.

✅ Positive quadratic kinetic coefficient `K=(rho+p)/c_a^2` on the tested physical domain.

✅ A local preferred-frame quadratic action reproducing the implemented dispersion exists.

✅ Its Fourier-mode quadratic Hamiltonian is positive under the implemented sign conditions.

✅ The reconstructed quadratic theory has no higher time derivatives.

✅ Pure two-derivative `P(X)` is insufficient for the full finite-k sector.

✅ Strong-coupling scale is proven **not identifiable** from the linear sector alone.

🔴 No unique fundamental nonlinear RTK/Khronon action has yet been selected/derived from this reconstruction.

🔴 Nonlinear constraint algebra has not yet been derived.

🔴 Cubic and higher operator coefficients are not fixed.

🔴 Physical strong-coupling scale is not yet determined.

🔴 One-loop/radiative stability is not established.

🔴 Counterterm closure/naturalness is not established.

🔴 UV completion is not claimed.

## Correct claim language

Allowed:

> The implemented RTK scalar sector admits a constructive healthy local quadratic preferred-frame EFT reconstruction at linear level, with positive quadratic Hamiltonian on the tested physical domain.

Not yet allowed:

> The fundamental RTK theory is ghost-free to all orders.

or

> The RTK strong-coupling cutoff is `M_K` / `k_*`.

## Next valid theoretical step

The next non-redundant theorem task is not another linear sign scan. It is to specify or derive an explicit nonlinear preferred-frame EFT completion whose quadratic expansion reduces to the established reconstruction, then:

1. derive the constraint/degree-of-freedom structure;
2. classify cubic operators compatible with the preferred-frame symmetries;
3. canonically normalize the propagating mode;
4. derive interaction scales and the actual strong-coupling bound;
5. only then study loop closure/radiative stability.

This is the precise remaining gap between the current RTK evidence and a Hassan-Rosen-style nonlinear ghost/constraint theorem.
