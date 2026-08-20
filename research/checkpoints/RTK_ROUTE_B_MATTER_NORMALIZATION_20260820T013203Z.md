# RTK Route-B matter normalization / low-energy phenomenology checkpoint

Created: `2026-08-20T01:32:03Z` / `2026-08-20T04:32:03+03:00 Europe/Helsinki`  
Status: **analytic/source frontier advanced; newly launched theorem gates remain CANDIDATE until CI artifacts are validated**

## 1. Why this checkpoint exists

The earlier Route-B strong-coupling theorem optimized `Lambda_p/M_P`, where `M_P` is the bare gravitational coefficient in the BPS healthy-Horava action. That quantity cannot automatically be identified with the Planck scale inferred from the locally measured Newton constant once low-energy Lorentz-violating couplings and the matter metric are specified.

This checkpoint freezes the required distinction so it cannot be lost across chats.

## 2. Primary-source normalization facts

Primary theory source: Blas, Pujolas, Sibiryakov, arXiv:1007.3503.

- The healthy nonprojectable action uses `(M_P^2/2) integral N sqrt(gamma) [K_ij K^ij - lambda K^2 - V]`.
- Its low-energy scales satisfy `M_lambda^2=(lambda-1) M_P^2` and `M_alpha^2=alpha M_P^2`.
- The strong-coupling estimates in Eqs. (5.14)-(5.15) are expressed using that bare `M_P`.
- The matter/effective-metric sector introduces an additional parameter `beta`; the pure-gravity quadratic pole construction does not determine it.
- On the conditional `beta=0` minimally/universally coupled branch, the Newton normalization is

  `G_N = 1/[8 pi M_P^2 (1-alpha/2)]`.

Define the measured reduced Newton Planck scale

`Mbar_N = (8 pi G_N)^(-1/2)`.

Then for `beta=0`

`Mbar_N = M_P sqrt(1-alpha/2)`.

**Guard:** generic matter-coupled Route-B statements must not insert a numerical measured Planck scale into a bare-`M_P` cutoff until `beta` / matter metric is fixed. `beta=0` results below are explicitly conditional.

## 3. Fixed-measured-Newton cutoff theorem candidate

Research worker: `rtk/route_b_bps_beta0_newton_cutoff.py`  
Science commit: `6a0b84ec96cceafa2175eda44bf9331d7bf140dc`  
Workflow commit: `1442716660f97eedaab34beab2ce6949a23643b1`  
Launch commit: `51f04b8ba7f37d05929ffd3a4bffcf62bb26d1b4`

For the exact inverse family

- `alpha=2h/(3C+h)`;
- `ell=lambda_BPS-1=2h/[3(1-h)]`,

the beta=0 Newton factor is

`M_P/Mbar_N = sqrt[(3C+h)/(3C)]`.

The physical fixed-`G_N` momentum cutoff is therefore

### `ell<=alpha`

`(Lambda_p/Mbar_N)^4 = 4 h^2(3C+h)^3 / [243 C^2(1-h)^3]`.

### `ell>=alpha`

`(Lambda_p/Mbar_N)^4 = 4 h^2(1-h) / [3 C^2(3C+h)]`.

The global optimum changes relative to the bare-`M_P` theorem:

### `0<C<=1/5`

- `h_opt = 3(1-C)/4`;
- `alpha_opt=ell_opt=2(1-C)/(1+3C)`;
- `Lambda_p,max/Mbar_N = sqrt[(1-C)/(2C)]`.

### `C>=1/5`

- `h_opt = [1-9C+sqrt(81C^2+30C+1)]/4`;
- the optimum is on the `ell>=alpha` branch;
- insert this `h_opt` into the high-branch physical cutoff above.

Thus the physical regime boundary is **`C=1/5`**, not the bare-`M_P` boundary `C=1/3`.

This theorem is conditional on `beta=0` and remains **CANDIDATE** until its CI artifact passes.

## 4. Exact fixed-G_N cutoff with low-energy caps

Research worker: `rtk/route_b_bps_beta0_capped_newton_cutoff.py`  
Science commit: `a18d7313ff076224bdae26694aef18c700721649`  
Workflow commit: `e9e3caddcfb5ca32f876ed72acd77a4b8d4373b4`  
Launch commit: `dce55a6b314b8173681c1c515931d9134658aba4`

For abstract caps

`0<alpha<=alpha_cap<2`, `0<ell<=ell_cap`,

the exact h-bounds are

- `h_alpha = 3 alpha_cap C/(2-alpha_cap)`;
- `h_ell = 3 ell_cap/(2+3 ell_cap)`.

Let `h0(C)` be the fixed-Newton unconstrained optimum from Sec. 3. Then

`h_opt,cap = min[h0(C), h_alpha, h_ell]`.

No scan is needed.

The cap-dominance crossover is

`C_cross = ell_cap(2-alpha_cap)/[alpha_cap(2+3 ell_cap)]`.

The exact `ell` reached when the alpha cap saturates is

`ell(alpha_cap) = 2 alpha_cap C / [2-alpha_cap(1+3C)]`.

Small-cap scaling remains square-root:

- low branch, alpha active: `Lambda_p/Mbar_N ~ sqrt(alpha_cap) C^(3/4)`;
- low branch, ell active: `~ sqrt(ell_cap) C^(1/4)`;
- high branch, alpha active: `~ sqrt(alpha_cap) C^(-1/4)`;
- high branch, ell active: `~ sqrt(ell_cap) C^(-3/4)`.

Status: **CANDIDATE pending CI**.

## 5. Sourced low-energy phenomenology benchmark

Primary phenomenology source: E. Barausse, arXiv:1907.05958 v4, Introduction.

It summarizes the low-energy khronometric constraints after GW170817/GRB170817A as:

- `|beta| <=~ 1e-15`;
- generic branch with `|lambda| >> 1e-7`: `|alpha| <=~ 1e-7`;
- on that generic branch, the remaining positive `lambda` is only weakly bounded at about `0.01--0.1`;
- alternative tuned branch: `|alpha| <=~ 0.25e-4` with `lambda approximately alpha/(1-2alpha)`.

For `beta=0`, comparison of the ADM conventions gives

`ell = lambda_BPS-1 = lambda_modern`.

Research worker: `rtk/route_b_bps_low_energy_phenomenology.py`  
Science commit: `7a07dc58518dbe21c8bf7dbb49de75a0443cc2b1`  
Workflow commit: `1f17cf204189c92410567542aec173fd70b85949`  
Launch commit: `f823114bf5da1d1776cb8821f0f332023e6ab3a6`

### Exact production-domain fact

Production RTK has

`C=c_a^2=x/[s^2(s+x)]`, `s=sqrt(1+lambda_D x^2)`, with `x>0`, `lambda_D>0`.

The denominator margin is

`s^2(s+x)-x = s^3 + lambda_D x^3 > 0`,

therefore

`0 < C < 1`

for the full production background domain.

### Generic benchmark consequence

Use the sourced benchmark `alpha_cap=1e-7` and bracket `ell_cap=0.01--0.1`.

The exact cap-crossover values are

- for `ell_cap=0.01`: `C_cross=19999999/203 ~= 98522.16`;
- for `ell_cap=0.1`: `C_cross=19999999/23 ~= 869565.17`.

Since production has `0<C<1`, the **alpha cap is always the active low-energy cap** across the entire production RTK domain. The loose `lambda/ell` cap never controls this optimization.

Moreover the unconstrained fixed-Newton optimum obeys `h0>=3/5` on `0<C<1`, while

`h_alpha <= 3/19999999 ~= 1.5e-7`.

Hence the sourced generic benchmark fixes

`h_opt = h_alpha`.

The exact physical cutoff simplifies to

`(Lambda_p/Mbar_N)^4 = 32 alpha_cap^2 C^3 / [(2-alpha_cap)^2 (2-alpha_cap(1+3C))^3]`.

This is the formula to combine with the pending current-state `C(a),M_K(a)` artifact.

### Tuned central curve

At alpha saturation the selected inverse family has

`ell = 2 alpha C/[2-alpha(1+3C)]`.

If the source's approximate tuned central relation is treated as an exact equality,

`ell = alpha/(1-2alpha)`,

then algebraically the intersection requires exactly

`C=1`.

Production has `C<1`, so no production RTK point lies exactly on that *central equality curve*. This is **not** an exclusion of the finite observational tuned band, because the source relation is approximate.

Status of the sourced theorem: **CANDIDATE pending CI**.

## 6. Compact-object regularity boundary

Research worker: `rtk/route_b_bps_compact_object_boundary.py`  
Science commit: `4ad0765234b2ecc541e9d4080202bc31379f53b9`  
Workflow commit: `c434521aacaea4fca481ffd4343dfad33ecfa142`  
Launch commit: `9d8cfc4693ea2cc98f9ee9569e810cc2eb567d7e`

The same phenomenology source summarizes the low-energy slowly-moving-black-hole result: avoiding the reported universal-horizon curvature pathology selects `alpha=beta=0` in that low-energy analysis.

The selected exact-rational BPS inverse family has, for every finite `0<h<1`,

- `alpha>0`;
- `ell>0`;
- `z>0`;
- `s=alpha>0`.

Therefore it has **no finite-h member with alpha=0**. The limit `alpha->0` occurs only as `h->0`, where `alpha,ell,z,s->0` and the low-energy cutoff also collapses to zero.

This is a rigorous **intersection boundary**, not a no-go theorem for the full higher-spatial-derivative completion. The UV operators may alter the universal-horizon region, which requires a dedicated compact-object calculation.

Status: **CANDIDATE pending CI**.

## 7. Current state-driven numerical gate

The current-scale dictionary gate remains active from the earlier checkpoint:

- research script commit `ce12bc4683266c9190b456157993edbdded3f6f6`;
- hardened workflow commit `397521d3142f3e2fe299a5dd634de49924c90c6a`;
- launch `a500c421d006cf2ff5332bed593aca5989e3c1e7`.

It must supply the replay-certified `gamma`, `C(a)`, `M_K(a)`, `k_*(a)` and hierarchy requirements across all 27 frozen dense redshifts. Do not substitute a guessed gamma.

Runtime snapshot refresh was triggered at main commit `9b81f755441d9dc7fdf42fceb52016137958b99b` to capture these and other active Route-B runs.

## 8. Immediate next decisions

1. Consume and validate completed CI artifacts for all Route-B theorem gates before promoting any CANDIDATE to PASS.
2. When the state-driven scale dictionary passes, combine `C(a),M_K(a)` with the exact alpha-limited fixed-`G_N` formula above and compute the worst hierarchy margin over the frozen dense-z grid.
3. Keep generic matter coupling separate from `beta=0`; derive the generic-beta measured-Newton normalization before any generic physical-cutoff claim.
4. Treat the low-energy compact-object result as a boundary condition requiring a dedicated selected-UV-operator black-hole analysis, not as an automatic full-theory exclusion.
5. Continue independent nonlinear DOF/constraint, radiative stability, matter-sector Lorentz percolation and off-shell source/residue gates.

## Non-claims

No result in this checkpoint establishes a global cosmological preference, a posterior/Bayes factor, generic matter-coupling viability, compact-object regularity of the UV theory, radiative stability, or a complete nonlinear completion. Workflow launch is not scientific PASS.
