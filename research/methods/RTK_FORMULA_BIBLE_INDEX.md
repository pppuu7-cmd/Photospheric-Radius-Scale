# RTK Formula Bible Index

Updated: 2026-08-21 18:56 UTC
Status: canonical derivation/provenance index

## Purpose

The main Formula Bible stores project-level equations and status. Long derivations are kept in named appendices. This index is the recovery map: a future session must be able to reconstruct the current theory frontier without any chat transcript.

Status markers:

- GREEN — exact/validated within the stated assumptions;
- YELLOW — mathematically/structurally promising but a required action-level/CI/phenomenology gate remains;
- RED — open;
- BLACK — scoped excluded construction only.

## Core Formula Bible

Canonical file:

`research/methods/RTK_FORMULA_BIBLE.md`.

Its major subjects are:

1. fundamental action/candidate-carrier requirements;
2. frozen production background and objective;
3. Khronon/DBI implementation invariants;
4. perturbation/stability requirements;
5. weak-field transition-radius formulas;
6. exact-rational alpha boundary;
7. scoped lapse-only two-derivative no-go;
8. Route-B U-DHOST/PPN algebra;
9. acceleration-sector mapping;
10. observational robustness gates;
11. FLRW Schur-complement algebra;
12. B6 differential abundance closure;
13. derivation/provenance discipline.

## C8 Appendix A — FLRW Schur/rank/q-residue algebra

File:

`research/methods/RTK_FORMULA_BIBLE_C8_SCHUR_APPENDIX.md`.

Executable sources on `rtk-class-build`:

- `rtk/route_b_flrw_schur_kernel.py`;
- `rtk/route_b_flrw_schur_rank_residue.py`;
- `rtk/route_b_pole_residue_distinction.py`.

Canonical protocol:

`research/RTK_C8_FLRW_SCHUR_MATCHING_PROTOCOL_2026-08-21.md` on `rtk-class-build`.

Strengthened CI result:

- workflow run `32490690248`;
- artifact `9449602889`;
- digest `sha256:1f2bfda3959e8b6c57866bd35e7279e7cb398460c1a6cd296d4b2d146e092dce`;
- result document `research/RTK_C8_SCHUR_CI_RESULT_2026-08-21.md`.

Exact theorem for `M(q)=M0+q M1`, real symmetric 2x2:

- a strict nonconstant linear constraint denominator requires `det(M1)=0` and `M1!=0`;
- hence `rank(M1)=1`;
- `q_p=-D0/D1`;
- `Res_q[N/D]=N(q_p)/D1`;
- the Schur contribution to `K_eff=K0-N/D` has residue `-N(q_p)/D1`.

Conditional rank-one form `M1=sigma v v^T`, with invertible `M0`:

`q_p=-1/(sigma a)`, `a=v^T M0^-1 v`,

`Res_q[Schur]=-b(q_p)^2/(sigma a^2)`,

`b(q)=v^T M0^-1 J(q)`.

Scope: q-plane reduced-coefficient theorem, not automatically an `omega^2` propagator residue, ghost criterion, DHOST degeneracy condition or UV completion.

Status: GREEN algebra / YELLOW action application.

## C8 Appendix B — residue/source redefinition locality gate

File:

`research/methods/RTK_FORMULA_BIBLE_C8_SOURCE_REDEFINITION_APPENDIX.md`.

Executable theorem:

`rtk-class-build:rtk/route_b_residue_source_redefinition_gate.py`, refined commit `7f5fda897938e24170b8a0228ce8a392e4110e8a`.

CI:

- run `32491666126` — success;
- artifact `9449986685`;
- digest `sha256:006d396c0bd686a76c1b76da2aaf3dd2c462b5ef696227b9ce5bf456134661d9`.

Starting exact relation:

`K_RTK=(1+r q^2)K_BPS`.

A scalar-only multiplicative map that exactly converts the kernels requires

`T(q)=sqrt(1+r q^2)`

and therefore

`J_RTK=T(q) J_BPS`.

Crucial invariant:

`J_RTK^2/K_RTK = J_BPS^2/K_BPS`.

Therefore a fixed-source residue mismatch is not by itself a physical inequivalence theorem. The scoped locality result is instead that `sqrt(1+r q^2)` is not a finite polynomial in `q^2` for `r>0`. A scalar-only finite-derivative local normalization cannot realize the exact map while leaving the original q-independent source unchanged.

Multi-field constraint elimination, auxiliary fields, derived/disformal matter maps and different local carriers remain open.

Status: GREEN scoped theorem.

## C8 Appendix C — direct spatial-covariant FLRW exact match

File:

`research/methods/RTK_FORMULA_BIBLE_C8_SPATIAL_COVARIANT_FLRW_APPENDIX.md`.

Parent local benchmark:

`rtk-class-build:rtk/route_b_spatial_covariant_benchmark.py`.

New executable theorem:

- `rtk-class-build:rtk/route_b_spatial_covariant_flrw_exact_match.py`;
- source commit `36c30a9b94ad120bfe461d93057daf57db8d14dc`.

CI:

- workflow run `32514697064` — success;
- artifact `9458330218`;
- digest `sha256:72fe15a918873ee0d7bf6af27f6eab51ef47dea48d4a4c3d7db9d65de9aeeb74`;
- artifact provenance confirms research source commit `36c30a9b94ad120bfe461d93057daf57db8d14dc`, Python 3.12.3.

Candidate unitary-gauge action:

`S = int N sqrt(gamma) [ Mpl^2/2 (R3+KijKij-K^2) + F(t,N) + C_acc a_i a^i ]`.

Production DBI-Khronon identities:

`G_8piG = rho_8piG+p_8piG = 2 mu_K^2 x Q`,

`K_8piG = G_8piG/c_a^2 = 2 mu_K^2 Q^2 s^3 = 2 M_K^2`.

Hence

`K_phys=2 Mpl^2 M_K^2`

and the exact direct acceleration match requires the **constant** coefficient

`C_acc = K_phys/(2 M_K^2) = Mpl^2`.

For finite physical `p^2=k^2/a^2`, the shift constraint gives

`delta N = dot(zeta)/H`.

The reduced scalar action is

`S2 = 1/2 int a^3/H^2 [ K_phys(1+p^2/M_K^2) dot(zeta)^2 - G_phys p^2 zeta^2 ]`,

therefore

`omega^2 = c_a^2 p^2/(1+p^2/M_K^2)`

exactly, with no epoch-by-epoch tuning of `C_acc`.

The constraint determinant is proportional to `p^4`; this mechanism does not claim a strict linear constraint-determinant pole. Therefore the Schur `D2=0` filter applies to a different mechanism and is not violated here.

Status: GREEN exact quadratic scalar FLRW kernel; YELLOW as a physical/covariant completion.

## C8 Appendix D — minimal Newton-normalization boundary

Executable theorem under CI:

`rtk-class-build:rtk/route_b_spatial_covariant_newton_boundary.py`, source commit `c9579ef48d508f0864b11914f399d9d517ed72de`.

In the standard healthy non-projectable Hořava/BPS low-energy normalization

`S ⊃ (M_P^2/2) alpha a_i a^i`.

The direct exact match above has coefficient `C_acc=M_P^2`, so its direct identification requires

`alpha = 2 C_acc/M_P^2 = 2`.

For the minimal/universal `xi=1, beta=0` matter branch,

`G_N = 1/[8 pi M_P^2(1-alpha/2)]`.

Thus the direct exact match lands at the singular Newton-normalization boundary `alpha=2` for finite bare `M_P`.

A regularization `alpha=2(1-epsilon)` restores the Newton denominator but changes the exact kinetic factor to

`1+(1-epsilon)p^2/M_K^2`,

or equivalently `Mdisp=M_K/sqrt(1-epsilon)`, so it no longer matches the frozen production `M_K` without another operator/normalization change.

Scope: this is a negative result only for the **direct acceleration-only identification with minimal xi=1,beta=0 universal matter normalization**. It does not exclude nonminimal/disformal matter coupling, `xi!=1`, fixed companion operators, auxiliary fields or the spatially covariant scalar EFT itself.

Status: YELLOW pending CI artifact at this index update; core algebra exact.

## B4 numerical proof chain

Canonical file:

`research/robustness/RTK_B4_NEUTRINO_STATIONARITY_CHAIN_2026-08-21.md`.

Target-v2 base replay:

- run `32482490823` — success;
- artifact `9452581043`;
- digest `sha256:c5bb88ef4d182104d8e5b5ed578b749dd4e0f9b5b4857f047633782540d7223d`;
- center `S_eff=1050.5880475140204`;
- best exact improvement `4.12100232551893e-05 < 0.005`;
- Hessian positive definite;
- smallest eigenvalue `1.1738932605478353e-05`.

Frozen base decision on `rtk-class-build`:

`research/robustness/b4_neutrino_rtk_ray_recenter_base_decision_v2.json`.

Required half-scale run:

`32514077002` — running at the last live check.

B4 remains open until half-scale and then fresh-tree replay pass; paired robustness also requires the LCDM side under the same frozen protocol.

## B6 abundance result

Canonical file:

`research/robustness/RTK_B6_ALTERBBN_RESULT_2026-08-21.md`.

Status: GREEN differential robustness only. Do not reinterpret it as an absolute BBN likelihood.

## B10 lambda-tail identifiability — CLOSED

Canonical final result:

`research/robustness/RTK_B10_FINAL_TAIL_IDENTIFIABILITY_RESULT_2026-08-21.md`.

Classification:

`LAMBDA_NOT_NUMERICALLY_IDENTIFIABLE_AGAINST_PREREGISTERED_DUST_TAIL_AT_0P005`.

The base and independent half-scale stationarity gates pass at factors 64 and 16384. Best stationarity-certified preregistered tail difference from the finite local point is

`Delta S = -0.0008954358222581504`,

whose absolute magnitude is below the frozen `0.005` numerical-identifiability convention.

This is not a posterior, confidence interval, Bayes factor or global-minimum statement.

Status: GREEN protocol-v1 closure.

## Recovery discipline

Every formula/result admitted to the project must record or link to:

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
