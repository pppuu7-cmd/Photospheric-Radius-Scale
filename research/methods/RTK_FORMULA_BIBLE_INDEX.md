# RTK Formula Bible Index

Updated: 2026-08-21 19:48 UTC
Status: canonical derivation/provenance map

## Purpose

This file is the recovery index for RTK mathematics. The main Formula Bible stores project-level formulas/status; detailed derivations live in named appendices. A future research session must be able to reconstruct the current frontier without any chat transcript.

Status markers:

- GREEN — exact/validated within stated assumptions;
- YELLOW — promising or algebraically derived, but a required CI/action/phenomenology gate remains;
- RED — open;
- BLACK — scoped excluded construction only.

## Core Formula Bible

Canonical file:

`research/methods/RTK_FORMULA_BIBLE.md`.

Core subjects include:

1. action/carrier requirements;
2. frozen production objective;
3. Khronon/DBI implementation invariants;
4. perturbation/stability requirements;
5. weak-field transition-radius formulas;
6. rational/alpha scoped boundaries;
7. lapse-only and U-DHOST scoped no-go results;
8. PPN/acceleration mappings;
9. observational robustness gates;
10. FLRW Schur algebra;
11. B6 differential abundance closure;
12. derivation/provenance discipline.

## Appendix A — C8 FLRW Schur/rank/q-residue algebra

File:

`research/methods/RTK_FORMULA_BIBLE_C8_SCHUR_APPENDIX.md`.

Supporting sources on `rtk-class-build`:

- `rtk/route_b_flrw_schur_kernel.py`;
- `rtk/route_b_flrw_schur_rank_residue.py`;
- `rtk/route_b_pole_residue_distinction.py`.

CI result:

- run `32490690248`;
- artifact `9449602889`;
- digest `sha256:1f2bfda3959e8b6c57866bd35e7279e7cb398460c1a6cd296d4b2d146e092dce`;
- result document `research/RTK_C8_SCHUR_CI_RESULT_2026-08-21.md`.

For `M(q)=M0+qM1`, a real symmetric nonzero 2x2 mechanism claiming a strict nonconstant linear constraint denominator requires `det M1=0`, hence `rank M1=1`. q-plane Schur residues are normalized by `D1`; they are not automatically physical `omega^2` propagator residues.

Status: GREEN scoped algebra.

## Appendix B — C8 residue/source redefinition locality

File:

`research/methods/RTK_FORMULA_BIBLE_C8_SOURCE_REDEFINITION_APPENDIX.md`.

Executable theorem:

`rtk-class-build:rtk/route_b_residue_source_redefinition_gate.py`, refined commit `7f5fda897938e24170b8a0228ce8a392e4110e8a`.

CI:

- run `32491666126`;
- artifact `9449986685`;
- digest `sha256:006d396c0bd686a76c1b76da2aaf3dd2c462b5ef696227b9ce5bf456134661d9`.

For `K_RTK=(1+r q^2)K_BPS`, exact scalar normalization requires `T=sqrt(1+r q^2)` and the source transforms by the same factor. `J^2/K` is invariant under a consistent field+source change. The scoped locality result is that the square root is not a finite polynomial in `q^2`, so the exact scalar-only finite-derivative shortcut cannot leave the original q-independent source unchanged.

Status: GREEN scoped theorem.

## Appendix C — direct spatial-covariant FLRW exact scalar match

File:

`research/methods/RTK_FORMULA_BIBLE_C8_SPATIAL_COVARIANT_FLRW_APPENDIX.md`.

Executable theorem:

- `rtk-class-build:rtk/route_b_spatial_covariant_flrw_exact_match.py`;
- source commit `36c30a9b94ad120bfe461d93057daf57db8d14dc`.

CI:

- run `32514697064`;
- artifact `9458330218`;
- digest `sha256:72fe15a918873ee0d7bf6af27f6eab51ef47dea48d4a4c3d7db9d65de9aeeb74`.

Production identity:

`K_8piG=(rho_8piG+p_8piG)/c_a^2=2 M_K^2`.

Controlled flat-FLRW lapse/shift elimination gives

`S2 = 1/2 int a^3/H^2 [K_phys(1+p^2/M_K^2) dot(zeta)^2-G_phys p^2 zeta^2]`,

hence exactly

`omega^2=c_a^2 p^2/(1+p^2/M_K^2)`.

This mechanism does not claim a strict linear pole in the constraint determinant; the Appendix-A `D2=0` filter addresses a different mechanism.

Status: GREEN exact quadratic scalar FLRW theorem; physical completion remains YELLOW/RED.

## Appendix D — gravity normalization and standard matter frame

File:

`research/methods/RTK_FORMULA_BIBLE_C8_GRAVITY_NORMALIZATION_APPENDIX.md`.

This appendix is mandatory whenever the direct scalar EFT is mapped to a physical matter frame. It distinguishes:

- bare action coefficient `M_*^2`;
- `M_cosm^2=(8 pi G_cosm)^-1`;
- `M_N^2=(8 pi G_N)^-1`.

Do not revert to an unspecified single `Mpl` in physical carrier arguments.

### D1 — beta=0 normalization theorem

Exact standard-matter match gives

`alpha=2+3 lambda_prime`.

CI:

- source `rtk/route_b_spatial_covariant_cosmological_newton_gate.py`, commit `2670aa4c5a53d55a5816abe03be3e8db856ffdc0`;
- run `32518243787`;
- artifact `9459582368`;
- digest `sha256:1250056abd3426d1b78a32d4c97272dd6fa7d609f954adcd2cdb2e8cb14235d9`.

No healthy positive-finite-Newton exact solution exists in the standard beta=0 direct acceleration-only universal matter branch.

Status: BLACK scoped no-go.

### D2 — general standard universal matter frame

Using the modern `(alpha,beta,gamma)` low-energy relations,

`alpha=2+3 gamma+beta`,

and on the exact-match hypersurface

`G_cosm/G_N=(2-alpha)/alpha`.

The cited BBN bound becomes

`16/17 < alpha < 16/15`.

With the post-GW170817 `|beta|<=~1e-15` benchmark, the first PPN expression is bounded below by `3.7647058823529296`, versus the `1e-4` benchmark.

CI:

- source `rtk/route_b_spatial_covariant_standard_matter_no_go.py`, commit `303e1922cc0950ece6cf77f24525ed3e564ccd07`;
- run `32518936616`;
- artifact `9459822043`;
- digest `sha256:07f9e3bb7e64139a5f35df9e7aa2d77a7bfe2b06b4578a545e14354c046aca02`;
- canonical result `research/RTK_C8_STANDARD_MATTER_NO_GO_RESULT_2026-08-21.md`.

Therefore the direct exact acceleration-only carrier cannot be embedded in the cited standard universal low-energy Hořava matter frame. This is not a no-go for nonminimal/disformal matter, companion operators, auxiliary fields or broader completions.

Status: BLACK scoped no-go.

## Appendix-E candidate — minimal static-safe mixed-gradient basis

Executable theorem under CI:

- `rtk-class-build:rtk/route_b_mixed_gradient_static_safe_gate.py`;
- source commit `7aa3f26e3896baf69deb2c45d915f7b38ec50ba0`.

Tested operator basis:

`C a_i a^i + 2D a_i D^i K + B D_iK D^iK`.

The committed exact polynomial matching gives two branches. The nontrivial mixed branch has

`C/C_direct=[(6H^2M_*^2+K)/(6H^2M_*^2-K)]^2`,

and therefore

`C/C_direct - 1 = 24 H^2 M_*^2 K/(6H^2M_*^2-K)^2 > 0`.

Thus the minimal mixed-gradient branch cannot reduce the static acceleration coefficient below the pure direct value; `C=0` has no exact solution in this basis. Promote to GREEN/BLACK only after CI artifact inspection.

Status: YELLOW pending CI.

## Numerical proof chains

### B4 neutrino

Canonical chain:

`research/robustness/RTK_B4_NEUTRINO_STATIONARITY_CHAIN_2026-08-21.md`.

Target-v2 base run `32482490823`, artifact `9452581043`, passed the base gate with improvement `4.12100232551893e-05` and a positive-definite Hessian. Required half-scale run `32514077002` was still computing at the latest direct check.

### B6 abundances

Canonical result:

`research/robustness/RTK_B6_ALTERBBN_RESULT_2026-08-21.md`.

Status: GREEN differential robustness only.

### B10 lambda-tail identifiability

Canonical result:

`research/robustness/RTK_B10_FINAL_TAIL_IDENTIFIABILITY_RESULT_2026-08-21.md`.

Classification:

`LAMBDA_NOT_NUMERICALLY_IDENTIFIABLE_AGAINST_PREREGISTERED_DUST_TAIL_AT_0P005`.

Status: GREEN protocol-v1 closure.

## Recovery discipline

Every admitted formula/result must record or link to:

- starting action/equations;
- conventions and dimensions;
- derivation steps;
- assumptions/domain;
- symbolic/numerical checks;
- implementation file;
- commit/workflow/run/artifact provenance;
- explicit scope and non-claims;
- validation status.

Never promote workflow success alone to a physics closure. Inspect the artifact and apply the frozen scientific decision rule.
