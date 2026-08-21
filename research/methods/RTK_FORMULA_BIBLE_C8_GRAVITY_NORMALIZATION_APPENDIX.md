# RTK Formula Bible — C8 Gravity-Normalization and Standard-Matter Appendix

Date: 2026-08-21
Status: mixed — GREEN exact FLRW scalar carrier and beta=0 normalization theorem; YELLOW for the newly launched general standard-matter BBN+PPN+GW theorem until its artifact is inspected.

## Purpose

This appendix corrects a normalization ambiguity that appeared immediately after the constructive C8 direct spatial-covariant FLRW exact-match theorem.

Three gravitational normalizations must be kept distinct until a matter frame/covariant carrier is fixed:

1. `M_*^2` — the bare coefficient in the low-energy gravitational action;
2. `M_cosm^2 = (8 pi G_cosm)^(-1)` — the Friedmann/background gravitational normalization;
3. `M_N^2 = (8 pi G_N)^(-1)` — the locally measured Newton normalization.

The production DBI formulas store quantities named `rho_8piG` and `p_8piG`. When mapping the production background to a standard universally coupled low-energy Horava carrier, the relevant `G` is the carrier's cosmological/Friedmann coupling `G_cosm`, not automatically its bare action coefficient.

This distinction prevents a false universal conclusion from the simpler same-normalization observation `alpha=2`.

---

## 1. Constructive direct FLRW result retained

The direct spatial-covariant benchmark action is

`S = integral N sqrt(gamma) [ M_*^2/2 (R3 + KijKij-K^2) + F + C_acc a_i a^i ]`,

with `a_i=D_i ln N`.

The production DBI identities imply exactly

`K_8piG = (rho_8piG+p_8piG)/c_a^2 = 2 M_K^2`.

After exact lapse/shift elimination the controlled single-clock FLRW scalar action has the RTK form

`S2 = 1/2 integral a^3/H^2 [ K_phys(1+p^2/M_K^2) dot(zeta)^2 - G_phys p^2 zeta^2 ]`,

hence

`omega^2 = c_a^2 p^2/(1+p^2/M_K^2)`.

CI provenance:

- run `32514697064`;
- artifact `9458330218`;
- digest `sha256:72fe15a918873ee0d7bf6af27f6eab51ef47dea48d4a4c3d7db9d65de9aeeb74`.

This exact scalar result is not revoked by the normalization analysis below.

---

## 2. Correct conversion of the production kinetic coefficient

If production `8 pi G` is identified with the cosmological gravitational coupling of the candidate carrier,

`K_phys = M_cosm^2 K_8piG = 2 M_cosm^2 M_K^2`.

The direct acceleration mechanism therefore requires

`C_acc,required = K_phys/(2 M_K^2) = M_cosm^2`.

This replaces the prematurely specialized statement `C_acc=M_*^2` when a covariant/matter-frame interpretation is attempted.

The statement `C_acc=M_*^2` remains true only in the special same-normalization identification `M_cosm=M_*`.

---

## 3. Standard low-energy Horava gravitational constants

In the standard universally coupled low-energy Horava parameterization used by Gumrukcuoglu, Saravani and Sotiriou, PRD 97, 024032 (2018), arXiv:1711.08845, Eqs. (7)-(12),

`G_cosm = 1/[4 pi M_*^2 (2+3 gamma+beta)]`

or equivalently

`M_cosm^2 = M_*^2 (2+3 gamma+beta)/2`,

while

`G_N = 1/[8 pi M_*^2 (1-alpha/2)]`,

so

`M_N^2 = M_*^2 (1-alpha/2)`.

The low-energy acceleration term has coefficient

`C_acc = M_*^2 alpha/2`.

Exact direct RTK matching to the production-normalized FLRW kernel therefore requires

`M_*^2 alpha/2 = M_cosm^2`,

hence the fixed relation

**`alpha = 2 + 3 gamma + beta`.**

This is an action/matter-frame relation, not an epoch-by-epoch fit.

---

## 4. Universal invariant on the exact-match hypersurface

Using the relation above,

`M_cosm^2 = M_*^2 alpha/2`.

Therefore

`G_cosm/G_N = M_N^2/M_cosm^2`

becomes

**`G_cosm/G_N = (2-alpha)/alpha`.**

This result is independent of how `3 gamma+beta` is partitioned once exact direct matching has been imposed.

In particular,

`G_cosm=G_N` exactly at `alpha=1`.

This explains why the earlier same-normalization shortcut `alpha=2` is not the general physical answer: `M_cosm` and the bare action coefficient need not be equal.

---

## 5. beta=0 exact no-solution theorem

For `beta=0`, use the older BPS notation `lambda_prime` for the corresponding kinetic coupling. The exact match becomes

`alpha = 2 + 3 lambda_prime`.

The standard beta=0 scalar has

`c_chi^2 = lambda_prime/alpha`.

The Newton normalization on the match surface is

`M_N^2 = -(3/2) M_*^2 lambda_prime`.

Consequently:

- `lambda_prime>0` gives positive scalar gradient ratio but `alpha>2` and `M_N^2<0`;
- `lambda_prime=0` gives `alpha=2`, `M_N^2=0`, singular `G_N`, and vanishing scalar speed;
- `-2/3<lambda_prime<0` gives positive finite Newton normalization but `c_chi^2<0`;
- `lambda_prime<=-2/3` gives `alpha<=0`.

Thus there is no healthy positive-finite-Newton exact direct RTK realization in this minimal beta=0 universal matter branch.

Executable theorem:

- `rtk-class-build:rtk/route_b_spatial_covariant_cosmological_newton_gate.py`;
- source commit `2670aa4c5a53d55a5816abe03be3e8db856ffdc0`.

CI:

- run `32518243787` — success;
- artifact `9459582368`;
- digest `sha256:1250056abd3426d1b78a32d4c97272dd6fa7d609f954adcd2cdb2e8cb14235d9`;
- artifact marker `RTK_ROUTE_B_SPATIAL_COVARIANT_COSMOLOGICAL_NEWTON_GATE_PASS`.

Status: GREEN scoped negative theorem.

---

## 6. General standard-matter observational gate

The same 2018 standard universal matter frame gives the BBN bound

`|(alpha+3 gamma+beta)/(2+3 gamma+beta)| < 1/8`.

On the direct-match hypersurface

`3 gamma+beta = alpha-2`,

so the BBN expression simplifies exactly to

`|2(alpha-1)/alpha| < 1/8`.

For `alpha>0`, this is equivalent to

**`16/17 < alpha < 16/15`**, approximately

`0.941176 < alpha < 1.066667`.

The first translated preferred-frame PPN bound in the same source is

`|4(alpha-2 beta)/(1-beta)| <=~ 1e-4`.

Post-GW170817 tensor-speed phenomenology restricts the same standard low-energy `beta` to order

`|beta| <=~ 1e-15`.

Across the entire BBN-allowed alpha interval and the GW beta interval,

`|4(alpha-2 beta)/(1-beta)|`

has the rigorous triangle-inequality lower bound

`4[(16/17)-2*10^-15]/(1+10^-15) > 3.76`.

This exceeds the `1e-4` PPN benchmark by more than `3.7e4`.

Therefore, if the executable theorem passes CI, the direct acceleration-only exact RTK carrier has **no solution in this standard universal low-energy Horava matter frame** satisfying simultaneously:

1. exact direct FLRW RTK matching;
2. the cited cosmological/Newton BBN bound;
3. the post-GW170817 beta bound;
4. the first preferred-frame PPN bound.

Executable theorem launched:

- `rtk-class-build:rtk/route_b_spatial_covariant_standard_matter_no_go.py`;
- source commit `303e1922cc0950ece6cf77f24525ed3e564ccd07`;
- workflow `main:.github/workflows/rtk-route-b-spatial-covariant-standard-matter-no-go.yml`;
- launch commit `ad3ffff0870372e246f7d5e7606ad850e58c5ecc`.

Status at writing: YELLOW pending artifact inspection.

---

## 7. Scope: what is and is not excluded

These results do **not** exclude the exact spatial-covariant quadratic FLRW mechanism itself.

They exclude increasingly specific embeddings:

- same-normalization standard identification -> `alpha=2` Newton boundary;
- beta=0 universal standard matter frame with correct `G_cosm` normalization -> no healthy positive-Newton solution;
- general standard universal matter frame -> observational BBN+PPN+GW incompatibility if the launched theorem passes.

Still open are:

- nonminimal/disformal matter metrics;
- fixed companion operators that alter static/Newton/PPN response while leaving the cosmological `p^2 dot(zeta)^2` coefficient intact;
- auxiliary constrained fields whose elimination generates the RTK kinetic factor;
- broader spatially covariant theories not mapped to the standard three-parameter universal matter frame;
- covariant completions with additional degeneracy operators;
- higher-spatial-gradient UV operators important for compact objects while reducing to the verified cosmological EFT in its domain.

Therefore the scientific frontier is no longer “can a local action make the RTK rational scalar dispersion?” It can. The frontier is now “can a fixed companion/matter-frame completion retain that cosmological scalar kernel while escaping the standard low-energy PPN/GW/Newton obstruction?”

---

## 8. Required next gate

Construct the smallest fixed deformation with no epoch-dependent fitting and test, on one coefficient tuple:

1. exact/controlled recovery of the FLRW RTK kinetic kernel;
2. tensor speed / GW bound;
3. Newton and Friedmann normalization;
4. both PPN preferred-frame combinations;
5. scalar kinetic/gradient stability;
6. DOF and degeneracy/constraint structure;
7. compact-object/universal-horizon behavior;
8. EFT cutoff/strong coupling;
9. matter/source transfer functions.

Any escape that simply inserts a momentum-dependent source factor by hand fails the already-established C8 source-redefinition discipline.
