# RTK C8 grad-K correction and regularity result

Date: 2026-08-21
Status: **MIXED — constructive quadratic FLRW escape, but minimal all-background regularity fails in scope**

## Scope

This note reconciles four consecutive C8 results for the spatially-covariant one-spatial-gradient extrinsic-curvature route. It is deliberately narrower than a no-go for RTK or for all covariant completions.

## 1. Pointwise scalar match exists

For flat FLRW scalar perturbations define

`A = dot(zeta)-H n`, `q=p^2 psi`, `y=p^2`.

A general grad-K scalar contribution has

`y [ U A^2 + 2 V A q + W q^2 ]`.

Exact elimination of lapse and shift matches the RTK kinetic target iff

- `U W = V^2`;
- `V/W = (6 H^2 M_*^2-K_clock)/(4 H^2 M_*^2)`;
- `W = 2 H^2 M_*^4/(K_clock M_K^2)`.

Thus a pointwise quadratic solution exists.

## 2. Constant-Wilson all-epoch realization fails

If `U,V,W` are constants of one simple fixed action, the exact ratio equation forces

`R=K_clock/(H^2 M_*^2)=6-4V/W`

to be constant, and the W equation then forces `M_K^2=2M_*^2/(R W)` constant.

Production instead has

`M_K=mu_K sqrt(s)(s+x)`, `s=sqrt(1+lambda_D x^2)`, `x=x0/a^3`,

with `dM_K/dx>0` for positive `x,lambda_D`; therefore `M_K(a)` is not constant.

CI: run `32521251025`, artifact `9460618747`, digest `sha256:3e7fdd10e8847483ce212472779ff06f518c7190be82150ded3e282701159f99`.

Classification: **BLACK only for constant-Wilson members of this grad-K scalar class**.

## 3. Correction to the earlier tensor-null interpretation

An intermediate restricted-basis theorem considered

- `O_T=D_l K^i_j D^l K^j_i`,
- `O_K=D_iK D^iK`,
- `O_D=D_iK^i_j D_kK^{kj}`

and found that the `O_T` coefficient vanishes on the exact scalar branch only at `R=2`.

That algebra is correct **inside that restricted representation**, but the broad interpretation was incomplete because it omitted the allowed cross contraction

`O_X=D_iK D_jK^{ij}`.

The corrected TT-safe scalar basis is

- `O_K -> (U,V,W)=(9,3,1)`;
- `O_D -> (1,1,1)`;
- `O_X -> (3,2,1)`.

The map determinant is `-4`, so these TT-safe operators alone span every scalar triple `(U,V,W)`.

The inverse map is

- `c_K=(U-2V+W)/4`;
- `c_D=(U-6V+9W)/4`;
- `c_X=(-U+4V-3W)/2`.

On the exact rank-one RTK branch `r=V/W`, `U=r^2W`, the entire correction is

`W [ ((r-1)/2) D_iK + ((3-r)/2) D_jK^j_i ]^2`.

For transverse-traceless tensors, `delta K=0` and `D_j delta K^j_i=0`, so this correction vanishes identically at quadratic flat-FLRW order. It also vanishes when `K_ij=0` exactly.

Correction CI: run `32522247851`, artifact `9460955420`, digest `sha256:b1923d26260050b6992549fc2c03e733efd500b1f382137da040ff9711edfecc`.

**Mandatory correction rule:** the old `R=2` statement must never again be quoted as a full grad-K tensor obstruction. It remains only a restricted `{O_T,O_K,O_D}` representation result.

## 4. Q_cosm dictionary and its corrected interpretation

The frozen-center CLASS dictionary evaluated

`Q_cosm(a)=2 M_K(a)^2/H(a)^2`.

Run `32521709199`, artifact `9460770879`, digest `sha256:322b75660ead7eb7420ef6000b94b273bb02d599c96506ea9d24ef24657a5690`.

On the frozen z=0..1 grid:

- `Q_min=51353307.766232975`;
- `Q_max=8679266917.145449`;
- `Q(z=1)/Q(z=0)=169.01086404510914`.

This proves that a constant gravitational normalization cannot hold the **restricted-basis** `R=2` surface over the grid. After the TT-safe basis correction, this is no longer a full tensor-safety exclusion.

## 5. Minimal grad-K zero-H regularity obstruction

The required scalar coefficients themselves obey

`U=(6H^2M_*^2-K_clock)^2/(8 K_clock M_K^2 H^2)`,

`V=M_*^2(6H^2M_*^2-K_clock)/(2 K_clock M_K^2)`,

`W=2H^2M_*^4/(K_clock M_K^2)`.

For finite positive `K_clock/M_K^2`,

`lim_{H->0} H^2 U = K_clock/(8 M_K^2) > 0`,

so `U~H^-2`.

With the production DBI identity

`K_clock=2 M_cosm^2 M_K^2`,

one obtains

`lim_{H->0} H^2 U = M_cosm^2/4`.

CI: run `32522407137`, artifact `9461010370`, digest `sha256:11cfcf0d22834f3c6e23b400d83202568e768ab34a93549a2cd239b6ab547b81`.

Interpretation: the **minimal EH+clock+grad-K representation of this exact cosmological scalar form** does not possess a finite-coefficient zero-H continuation at the same finite positive production clock state.

This is not a broad physical no-go. In particular it does not exclude:

- auxiliary constrained fields;
- a modified lapse/shift constraint structure;
- a different static Khronon branch where `K_clock/M_K^2=O(H^2)`;
- a deliberately cosmology-only EFT with a lower-H validity bound;
- a broader covariant completion whose unitary-gauge reduction is not the same finite grad-K `(U,V,W)` form.

## 6. Current C8 decision

The operator search should **not** continue by adding more linear combinations of the same minimal grad-K quadratic invariants. Tensor safety is already achievable; the remaining obstruction is regularity/fixed-action realization.

Highest-value next construction class:

1. auxiliary nondynamical/constrained fields that change the Schur complement without explicit singular Wilson coefficients;
2. modified base lapse/shift constraints with the same production scalar pole and residue;
3. only after a candidate is explicit: same-action DOF, ghost/gradient/hyperbolicity, Newton/PPN, GW, compact-object and EFT-cutoff tests.

A workflow PASS certifies only the exact algebra encoded above, not general UV completion viability.
