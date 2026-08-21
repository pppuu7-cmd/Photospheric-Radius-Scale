# RTK C8 constraint frontier — 2026-08-21 20:24 UTC

Purpose: preserve the current C8 reasoning independently of chat history. All statements below are scoped to the stated quadratic flat-FLRW constructions unless explicitly noted.

## 1. Corrected full TT-safe grad-K basis — GREEN

CI run `32522247851`, artifact `9460955420`, digest `sha256:b1923d26260050b6992549fc2c03e733efd500b1f382137da040ff9711edfecc`.

The allowed TT-null scalar operators

- `O_K = D_i K D^i K -> (U,V,W)=(9,3,1)`;
- `O_D = D_i K^i_j D_k K^{kj} -> (1,1,1)`;
- `O_X = D_i K D_j K^{ij} -> (3,2,1)`

have map determinant `-4` and span arbitrary scalar `(U,V,W)`. On the exact RTK rank-one branch `r=V/W`, `U=r^2 W`, the complete pointwise correction is

`W [ ((r-1)/2) D_i K + ((3-r)/2) D_j K^j_i ]^2`.

It vanishes for strictly static `K_ij=0` and for TT perturbations. The earlier `R=2` condition remains valid only for the restricted basis that omitted `O_X`; it is not a full grad-K obstruction.

## 2. Minimal grad-K zero-H regularity — BLACK in scope

CI run `32522407137`, artifact `9461010370`, digest `sha256:11cfcf0d22834f3c6e23b400d83202568e768ab34a93549a2cd239b6ab547b81`.

Required exact coefficients are

- `U=(6H^2 M_*^2-K_clock)^2/(8 K_clock M_K^2 H^2)`;
- `V=M_*^2(6H^2 M_*^2-K_clock)/(2 K_clock M_K^2)`;
- `W=2H^2 M_*^4/(K_clock M_K^2)`.

For finite positive `K_clock/M_K^2`, `U~H^-2`. Under the production DBI identity `K_clock=2 M_cosm^2 M_K^2`,

`lim_{H->0} H^2 U = M_cosm^2/4`.

Thus the minimal EH+clock grad-K carrier has no finite-coefficient zero-H continuation. This does not exclude a deliberately branch-changing theory, an auxiliary/dynamical constraint completion, or nonlocal/retarded structure.

## 3. Algebraic auxiliary rank gate — launched

Research source commit `4d8a93f902da53d0a51886080865d353151ccd60`; trigger commit `e7a4cc05df1f6162499dfd8ca66766d84231f6a3`.

For one nondynamical auxiliary,

`L_aux = 1/2 A(H)y^2 + B(H)yX + 1/2 C(H)X^2`,

elimination gives `C_eff=C-B^2/A`. If `A(0)!=0` and all unreduced coefficients are finite, `C_eff` is finite. If `B~H^m` while `B^2/A~H^-2`, then `A~H^(2m+2)->0`: the auxiliary Hessian loses uniform rank at `H=0`.

For several algebraic auxiliaries, `C_eff=C-b^T M^{-1}b`; a finite nonsingular `M(0)` and finite `b,C` likewise cannot generate an `H^-2` pole. Therefore a purely algebraic auxiliary can move the singularity into a vanishing constraint eigenvalue, but cannot remove it while preserving a regular nonsingular static constraint matrix.

Do not promote this to a no-go for dynamical auxiliaries or intentionally branch-changing static limits until CI artifact is inspected.

## 4. Pure K^2 / Hořava-lambda base deformation — launched exact gate

Research source commit `b3ac1334d1b5271a9e4af86603e762ab002342da`; trigger commit `5a49acedbb867f7e1cd792305980d08cd6da9611`.

Test action deformation:

`M_*^2/2 [K_ij K^ij-K^2+eta K^2]`

with unchanged clock coefficient and completely general scalar grad-K `(U,V,W)`.

Using `A=dot(zeta)-Hn`, `q=p^2 psi`,

- EH scalar kinetic: `-6A^2-4Aq`;
- `(delta K)^2=9A^2+6Aq+q^2`.

After exact lapse+shift elimination and demanding

`K_eff(p^2)=K_clock/H^2 (1+p^2/M_K^2)`

for all `p^2`, the cleared equality is cubic in `p^2`. Its constant coefficient is

`-K_clock^2 M_*^2 M_K^2 eta`.

For finite nonzero physical scales exact matching therefore forces `eta=0`, independently of `(U,V,W)`. If CI confirms the symbolic gate, a simple K^2/Hořava-lambda deformation cannot regularize the zero-H issue while preserving the same exact RTK scalar target and clock sector.

## 5. Numerical branches still running

At this checkpoint:

- B4 target-v2 half Hessian run `32514077002`: exact Hessian step still in progress.
- B9 RTK recenter base Hessian run `32518496348`: exact Hessian step still in progress.
- B9 LCDM interrupted-recenter base Hessian run `32522002655`: exact Hessian step still in progress.

No scientific conclusion is to be inferred from elapsed run time.

## 6. Next decision tree

1. Inspect auxiliary-rank and K^2-deformation CI artifacts before promoting either theorem.
2. If both pass, stop spending time on algebraic auxiliaries with regular nonsingular static Hessians and on pure K^2 deformation.
3. Next local completion candidates must genuinely alter the constraint architecture: a dynamical/degenerate auxiliary, a distinct regular branch, or a controlled nonlocal/retarded completion.
4. Every surviving candidate must be tested with the same fixed action/parameter tuple for DOF count, scalar/tensor stability, PPN/Newton, GW, compact objects and EFT cutoff.
5. Independently advance B4 and B9 according to their frozen stationarity protocols as soon as artifacts appear.
