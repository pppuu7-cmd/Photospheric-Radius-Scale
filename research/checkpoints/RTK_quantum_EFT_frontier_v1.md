# RTK quantum / EFT consistency frontier v1

This checkpoint records what is and is not established for the implemented RTK/Khronon sector. It must not be read as a UV-completion or a full nonlinear quantum-gravity claim.

## 1. Classical algebraic stability baseline

Workflow run `31975991159` completed successfully. Across 1225 broad-grid points the implemented background/perturbation algebra retained positive `Q`, positive `1+w`, positive `c_a^2`, non-negative `c_s^2`, and positive DBI margin with no violations. The audit explicitly did **not** claim a ghost-free quadratic action, bounded Hamiltonian, strong-coupling scale, loop stability, or UV completion.

## 2. Earlier finite-k quadratic proxy audit

The proxy audit run `31978863354` intentionally tested whether the implemented finite-k sector could be identified with a pure local two-derivative `P(X)` scalar. It cannot: the implementation has explicit

`c_s^2(k) = c_a^2 / [1 + (k/k_*)^2]`.

The run's FAIL status was driven by floating-point finite-difference `dp/drho` loss of relative precision at extreme tiny sound speeds, while all scanned gradient and kinetic proxies remained positive. The finite-k conclusion is physical: a pure two-derivative `P(X)` description is insufficient and extra preferred-frame / higher-spatial-derivative EFT structure is required.

## 3. Exact background identity

A symbolic reconstruction now verifies exactly that the coded background quantity `c_a^2` equals `dp/drho` for the implemented equation of state. This removes the numerical finite-difference ambiguity in the earlier proxy audit.

## 4. Constructive local quadratic EFT existence result

Science code: `rtk/quantum_local_quadratic_eft_reconstruction.py`

Workflow run: `31982347734` — PASS.

A local preferred-frame quadratic action was constructed:

`L2(q) = 1/2 K [1 + q^2/M^2] |pi_dot|^2 - 1/2 G q^2 |pi|^2`,

corresponding in position space to a standard time kinetic term plus a higher-spatial-derivative kinetic operator, but no higher time derivatives.

With

- `G = rho + p`,
- `K = (rho+p)/c_a^2`,
- `M = k_*`,

the resulting dispersion relation

`omega^2 = (G/K) q^2 / [1 + q^2/M^2]`

exactly reproduces the implemented finite-k sound speed. The canonical Fourier-mode Hamiltonian is

`H = P^2/[2 K (1+q^2/M^2)] + G q^2 pi^2/2`,

which is positive when `G>0`, `K>0`, `M^2>0`. A 3430-point broad-grid sign audit found no violations; minimum scanned `G=1.000000000001e-12`, minimum `K=1.0000000000020002`, and minimum mode kinetic coefficient `1.0000000000020002`.

This is therefore a constructive **existence proof for a healthy local quadratic/linear preferred-frame EFT reconstruction of the implemented scalar dispersion**, not proof that this is the unique or fundamental nonlinear RTK action.

## 5. What remains open

✅ Classical broad-grid algebraic stability.

✅ Exact background barotropic identity `c_a^2 = dp/drho`.

✅ Positive gradient and kinetic coefficients on the scanned domain.

✅ Local quadratic preferred-frame EFT reconstruction exists.

✅ Implemented finite-k dispersion is reproduced exactly by that reconstruction.

✅ Quadratic Hamiltonian of the reconstructed scalar mode is positive under the implemented positivity conditions.

✅ The candidate quadratic reconstruction contains no higher time derivatives.

❌ Nonlinear constraint algebra has not been derived.

❌ Cubic and higher interaction operators have not been fixed from a nonlinear completion.

❌ A physical strong-coupling scale has not been derived; the dispersive scale `M_K`/`k_*` is not automatically the strong-coupling cutoff.

❌ One-loop/radiative stability has not been established.

❌ Counterterm closure/naturalness has not been established.

❌ UV completion is not claimed.

## 6. Decision rule

The next valid quantum step is to derive or choose an explicit nonlinear preferred-frame EFT completion whose quadratic expansion matches the proven reconstruction, then derive its constraint structure and cubic operators. Only after canonical normalization of those cubic operators may a strong-coupling scale be quoted. Until then `M_K` is a dispersive scale, not a proven quantum cutoff.
