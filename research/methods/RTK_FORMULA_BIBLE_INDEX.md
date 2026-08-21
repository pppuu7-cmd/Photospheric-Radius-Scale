# RTK Formula Bible Index

Updated: 2026-08-21 20:38 UTC
Status: canonical derivation/provenance map

## Purpose

Recovery index for RTK mathematics. Main formulas live in `research/methods/RTK_FORMULA_BIBLE.md`; detailed derivations and corrections live in appendices/result notes. A future session must reconstruct the current frontier without chat history.

Markers: GREEN validated in scope; YELLOW open gate; RED open; BLACK scoped excluded construction; SUPERSEDED means a broader interpretation was corrected while a narrower algebraic statement may remain true.

## Core

Canonical file: `research/methods/RTK_FORMULA_BIBLE.md`.

Maintain these invariants: exact-float `A_s`; physical RTK `Omega_cdm=0`; positive bracketed gamma root; production `eff` vs `k01` and sparse vs dense objectives are distinct; local Hessian/replay never implies a global minimum.

## Appendix A — C8 FLRW Schur/rank/residue

File: `research/methods/RTK_FORMULA_BIBLE_C8_SCHUR_APPENDIX.md`.

CI run `32490690248`, artifact `9449602889`, digest `sha256:1f2bfda3959e8b6c57866bd35e7279e7cb398460c1a6cd296d4b2d146e092dce`.

For `M(q)=M0+qM1`, a strict nonconstant linear determinant mechanism needs `det M1=0`; q-plane constraint residues are not automatically physical `omega^2` residues.

Status: GREEN scoped algebra.

## Appendix B — source/redefinition locality

File: `research/methods/RTK_FORMULA_BIBLE_C8_SOURCE_REDEFINITION_APPENDIX.md`.

CI run `32491666126`, artifact `9449986685`, digest `sha256:006d396c0bd686a76c1b76da2aaf3dd2c462b5ef696227b9ce5bf456134661d9`.

For `K_RTK=(1+r q^2)K_BPS`, exact scalar normalization requires `T=sqrt(1+r q^2)` and the source transforms with the same factor. The exact scalar-only finite-polynomial shortcut cannot keep a q-independent source unchanged.

Status: GREEN scoped theorem.

## Appendix C — direct spatial-covariant FLRW scalar match

File: `research/methods/RTK_FORMULA_BIBLE_C8_SPATIAL_COVARIANT_FLRW_APPENDIX.md`.

CI run `32514697064`, artifact `9458330218`, digest `sha256:72fe15a918873ee0d7bf6af27f6eab51ef47dea48d4a4c3d7db9d65de9aeeb74`.

Production identity `K_8piG=(rho_8piG+p_8piG)/c_a^2=2M_K^2`. Controlled flat-FLRW reduction gives

`omega^2=c_a^2 p^2/(1+p^2/M_K^2)`.

Status: GREEN exact quadratic scalar FLRW theorem; physical completion remains open.

## Appendix D — gravitational normalization and standard universal matter frame

File: `research/methods/RTK_FORMULA_BIBLE_C8_GRAVITY_NORMALIZATION_APPENDIX.md`.

Always distinguish bare `M_*^2`, `M_cosm^2=(8piG_cosm)^-1`, and local `M_N^2=(8piG_N)^-1`.

### D1 beta=0

Run `32518243787`, artifact `9459582368`: no healthy positive-finite-Newton exact solution in the standard beta=0 direct acceleration-only universal matter branch.

Status: BLACK scoped no-go.

### D2 general beta

Run `32518936616`, artifact `9459822043`, digest `sha256:07f9e3bb7e64139a5f35df9e7aa2d77a7bfe2b06b4578a545e14354c046aca02`.

Exact match gives `alpha=2+3gamma+beta`; the BBN/Newton window gives `16/17<alpha<16/15`, while GW plus PPN excludes this direct standard-universal branch by a minimum factor about `3.7647e4` against the `1e-4` PPN benchmark.

Canonical result: `research/RTK_C8_STANDARD_MATTER_NO_GO_RESULT_2026-08-21.md`.

Status: BLACK scoped no-go; nonminimal/disformal/auxiliary/companion completions remain open.

## Appendix E — minimal `{a_i,D_iK}` mixed-gradient basis

Source: `rtk/route_b_mixed_gradient_static_safe_gate.py`.

CI run `32519335082`, artifact `9459962141`, digest `sha256:2bde114d4aafb9f5758ff7107c8479c3112036ccf507755960ff5bad676d1809`.

For `C a_i a^i +2D a_iD^iK+B D_iK D^iK`, the nontrivial exact branch requires

`C/C_direct=[(6H^2M_*^2+K)/(6H^2M_*^2-K)]^2>1`.

Thus this minimal mixed-gradient basis cannot remove or reduce the direct static acceleration coefficient; `C=0` has no exact solution.

Status: BLACK scoped no-go.

## Appendix F — full scalar grad-K carrier, tensor correction, and regularity

Canonical reconciliation note:

`research/RTK_C8_GRADK_CORRECTION_AND_REGULARITY_RESULT_2026-08-21.md`.

### F1 pointwise scalar match

For `p^2[U A^2+2V A q+W q^2]`, exact RTK matching requires

- `UW=V^2`;
- `V/W=(6H^2M_*^2-K_clock)/(4H^2M_*^2)`;
- `W=2H^2M_*^4/(K_clock M_K^2)`.

Pointwise scalar solution exists.

### F2 constant-Wilson obstruction

Run `32521251025`, artifact `9460618747`, digest `sha256:3e7fdd10e8847483ce212472779ff06f518c7190be82150ded3e282701159f99`.

One constant `(U,V,W)` tuple forces constant `M_K`, incompatible with production `M_K(a)`.

Status: BLACK only for constant-Wilson members of this grad-K scalar class.

### F3 tensor-basis correction — IMPORTANT

An intermediate run `32521548678`, artifact `9460716295`, found `R=2` as tensor-null **inside the restricted `{O_T,O_K,O_D}` representation**. That statement must not be promoted to a full grad-K obstruction.

The missing allowed contraction is `O_X=D_iK D_jK^{ij}`. The corrected TT-safe basis

- `D_iK D^iK -> (9,3,1)`;
- `D_iK^i_j D_kK^{kj} -> (1,1,1)`;
- `D_iK D_jK^{ij} -> (3,2,1)`

has determinant `-4` and spans arbitrary scalar `(U,V,W)` while all three structures are TT-null.

On `r=V/W`, `U=r^2W`, the exact pointwise correction is

`W[((r-1)/2)D_iK+((3-r)/2)D_jK^j_i]^2`.

Corrected CI run `32522247851`, artifact `9460955420`, digest `sha256:b1923d26260050b6992549fc2c03e733efd500b1f382137da040ff9711edfecc`.

Status: GREEN quadratic flat-FLRW tensor-safe representation. **Old broad `R=2` interpretation: SUPERSEDED.**

### F4 Q_cosm restricted diagnostic

Run `32521709199`, artifact `9460770879`, digest `sha256:322b75660ead7eb7420ef6000b94b273bb02d599c96506ea9d24ef24657a5690`.

`Q_cosm=2M_K^2/H^2` changes from `5.1353307766e7` to `8.6792669171e9` over z=0..1, ratio `169.01086404510914`. This excludes maintaining the old restricted-basis `R=2` surface with one constant normalization, but no longer excludes the corrected TT-safe basis.

### F5 zero-H regularity

Run `32522407137`, artifact `9461010370`, digest `sha256:11cfcf0d22834f3c6e23b400d83202568e768ab34a93549a2cd239b6ab547b81`.

Basis-independently within the same minimal EH+clock grad-K scalar form,

`U=(6H^2M_*^2-K_clock)^2/(8K_clock M_K^2 H^2)`.

For finite positive `K_clock/M_K^2`, `U~H^-2`; production gives `lim(H^2U)=M_cosm^2/4`.

Status: BLACK scoped regularity obstruction for the minimal EH+clock+grad-K representation. Auxiliary/modified-constraint/different-branch/cosmology-only-EFT completions remain open.

## Numerical proof chains

### B4 neutrino

Target-v2 base run `32482490823`, artifact `9452581043`: improvement `4.12100232551893e-05`, PD Hessian. Half-scale run `32514077002` is still computing.

### B6 abundances

`research/robustness/RTK_B6_ALTERBBN_RESULT_2026-08-21.md`: GREEN differential robustness only.

### B9 lensing

RTK paired candidate from run `32490152072`, artifact `9456206708`, improved fixed center by `0.017224444894964108`; RTK recenter Hessian run `32518496348` computing.

LCDM job in the same paired run hit the 360-minute limit after 293 exact points. Uploaded partial artifact `9460759915`, digest `sha256:6551f10c5896ef98d042aa578ade61c2922b002941dcc241e13b322d2cdc94c0`. Full-log exact minimum is eval 291: `S_B9=1058.6304210952487`, improvement `0.3906228341422775` from the fixed LCDM B9 center. This is only a frozen interrupted-optimizer recenter seed. Base Hessian run `32522002655` is computing.

### B10 lambda tail

`research/robustness/RTK_B10_FINAL_TAIL_IDENTIFIABILITY_RESULT_2026-08-21.md`: `LAMBDA_NOT_NUMERICALLY_IDENTIFIABLE_AGAINST_PREREGISTERED_DUST_TAIL_AT_0P005` under protocol v1.

## Current theoretical next move

Do not spend more cycles searching linear combinations inside the same minimal grad-K basis. The useful next class is a **regular auxiliary or modified-constraint carrier** that can reproduce the exact scalar pole/residue without singular grad-K Wilson coefficients, then survive same-action DOF/stability, Newton/PPN, GW, compact-object and EFT-cutoff gates.

## Recovery discipline

Every admitted result must retain action/equations, conventions, domain, derivation, symbolic/numerical checks, source commit, workflow/run/artifact provenance, explicit scope/non-claims, and validation status. Workflow success alone is not physics closure.
