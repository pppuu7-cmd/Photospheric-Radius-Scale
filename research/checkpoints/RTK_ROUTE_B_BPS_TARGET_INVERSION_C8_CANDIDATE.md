# RTK Route-B — BPS target inversion + C8 cutoff composition candidate

Created: 2026-08-20T01:02:00Z / 2026-08-20T04:02:00+03:00 Europe/Helsinki
Status: **CANDIDATE — pending GitHub Actions validation artifact**
Research worker commit: `e98f0eb1b03486adaf884e102e6486ff3438e263`
Launch commit: `efc6813e52d3f9f147aa4cedc68f5fdd03339087`
Frozen target-inversion workflow: `main:.github/workflows/rtk-route-b-bps-target-inversion.yml`

## Purpose

Compose the already exact healthy-BPS inverse map for an arbitrary positive RTK rational target

`omega^2 = C p^2 / (1 + p^2/Mdisp^2)`, with `C>0`, `Mdisp>0`,

with the exact BPS low-energy strong-coupling cutoffs and the independently checked C8 accuracy/crossover window. The goal is to replace an open numerical scan over the inverse-family tuning parameter `h` with a closed-form optimum and an exact hierarchy criterion.

## Inverse family

For `0<h<1`:

- `z = h/(3C)`
- `ell = lambda-1 = 2h/[3(1-h)]`
- `alpha = 2h/(3C+h)`
- `s = alpha`
- `M_* = Mdisp`

This keeps `c_s^2=C` and `Mdisp` exactly fixed.

The exact branch ratio is

`ell/alpha = (3C+h)/[3(1-h)]`.

## Exact BPS cutoff composition

Using the BPS low-energy cutoffs already encoded in `rtk/c8_bps_low_energy_cutoff_map.py`:

- if `ell <= alpha`,
  `Lambda_p/M_P = ell^(3/4) alpha^(-1/4)`;
- if `ell >= alpha`,
  `Lambda_p/M_P = alpha^(3/4) ell^(-1/4)`.

The branch switch is

`h_bal = 3(1-C)/4`

when this lies in `(0,1)`.

The fourth powers used for exact differentiation are

- low branch: `F_low^4 = 4 h^2 (3C+h) / [27(1-h)^3]`;
- high branch: `F_high^4 = 12 h^2 (1-h) / (3C+h)^3`,

where `F = Lambda_p/M_P`.

## Closed-form global optimum candidate

The high-branch stationary point is

`h_star = 6C/(9C+1)`.

The relation

`h_star - h_bal = 3(3C-1)(3C+1) / [4(9C+1)]`

makes `C=1/3` the exact regime boundary.

Therefore the candidate global optimum over `0<h<1` is:

### Regime A: `0<C<=1/3`

- `h_opt = 3(1-C)/4`
- `alpha_opt = ell_opt = 2(1-C)/(1+3C)`
- `z_opt = (1-C)/(4C)`
- `Lambda_p,max/M_P = sqrt[2(1-C)/(1+3C)]`
- `Lambda_omega/Lambda_p = 1`

### Regime B: `C>=1/3`

- `h_opt = 6C/(9C+1)`
- `alpha_opt = 4/[3(3C+1)]`
- `ell_opt = 4C/(3C+1)`
- `z_opt = 2/(9C+1)`
- `Lambda_p,max/M_P = [16/(27 C (3C+1)^2)]^(1/4)`
- `Lambda_omega/Lambda_p = sqrt(3C)`

The two branches agree continuously at `C=1/3`.

## Composed C8 hierarchy criterion candidate

For requested accuracy `0<epsilon<1` through `p_max`, define

`p_req = max(Mdisp, p_max epsilon^(-1/6))`.

The C8 condition requires a strict crossover momentum satisfying

`p_req < p_UV < Lambda_p`.

After maximizing over `h`, the candidate exact existence criterion is

`p_req < M_P Fmax(C)`,

with

- `Fmax(C) = sqrt[2(1-C)/(1+3C)]` for `0<C<=1/3`;
- `Fmax(C) = [16/(27 C (3C+1)^2)]^(1/4)` for `C>=1/3`.

Equivalently,

`M_P/Mdisp > max(1, (p_max/Mdisp) epsilon^(-1/6)) / Fmax(C)`.

At the same `h_opt`, the sufficient frequency guard is automatically weaker than the momentum condition:

- for `C<=1/3`, `Lambda_omega=Lambda_p` and `sqrt(2C)<1`;
- for `C>=1/3`, `Lambda_omega/Lambda_p=sqrt(3C)>sqrt(2C)`.

Thus one hierarchy inequality controls both the strict momentum window and the stated sufficient frequency guard.

## Interpretation

This would sharpen the earlier result considerably: taking `h -> 0` can make `alpha` and `ell` arbitrarily small, but it simultaneously collapses the BPS low-energy cutoffs. The phenomenologically relevant question is therefore not whether low-energy Lorentz-violating parameters can be made arbitrarily small, but whether the target scales fit below the **maximum available cutoff** of the exact inverse family. The formulas above identify that maximum analytically.

## Non-claims / guards

This candidate does **not** establish:

- off-shell source/residue equivalence;
- full nonlinear constraint/degree-of-freedom closure;
- radiative stability;
- matter-sector Lorentz-violation safety;
- a numerical phenomenological pass until actual `C`, `Mdisp`, `p_max`, `epsilon`, and the intended physical `M_P` convention are inserted;
- a scientific PASS until the GitHub Actions theorem run completes successfully and its artifact is validated.

## Next gate

1. Validate the composed SymPy theorem in GitHub Actions and inspect the artifact, not merely workflow launch status.
2. If PASS, promote these formulas into the chat-independent recovery/methodology frontier.
3. Insert the phenomenological RTK target values and evaluate the hierarchy margin.
4. Continue with the remaining nonlinear/radiative/matter-sector consistency gates.
