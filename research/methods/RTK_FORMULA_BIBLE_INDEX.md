# RTK Formula Bible Index

Updated: 2026-08-21 23:59 UTC
Status: canonical derivation/provenance map

## Purpose

Recovery index for RTK mathematics. Main formulas live in `research/methods/RTK_FORMULA_BIBLE.md`; detailed derivations/corrections live in appendices and dated result notes. No chat transcript is required to reconstruct the current mathematical frontier.

Markers: GREEN = validated in stated scope; YELLOW = active/pending; RED = open; BLACK = scoped excluded construction; SUPERSEDED = broader interpretation corrected while narrower algebra may remain true.

## Core invariants

- exact-float `A_s` cache semantics;
- physical RTK `Omega_cdm=0`;
- positive bracketed Khronon normalization root;
- `eff` and `k01` are separate mappings;
- sparse and dense objectives are not interchangeable;
- local Hessian/stationarity does not imply a global optimum;
- q-plane Schur residues are not automatically physical `omega^2` propagator residues;
- a field redefinition must transform the source consistently before physical response is compared.

## Appendix A — FLRW Schur/rank/q-residue

File: `research/methods/RTK_FORMULA_BIBLE_C8_SCHUR_APPENDIX.md`.

CI run `32490690248`, artifact `9449602889`, digest `sha256:1f2bfda3959e8b6c57866bd35e7279e7cb398460c1a6cd296d4b2d146e092dce`.

For `M(q)=M0+qM1`, a strict nonconstant linear determinant requires `det M1=0`; for real symmetric nonzero 2x2 `M1` this implies rank one. Normalized q-plane residue must include the denominator derivative.

Status: GREEN scoped algebra.

## Appendix B — source/redefinition locality

File: `research/methods/RTK_FORMULA_BIBLE_C8_SOURCE_REDEFINITION_APPENDIX.md`.

CI run `32491666126`, artifact `9449986685`, digest `sha256:006d396c0bd686a76c1b76da2aaf3dd2c462b5ef696227b9ce5bf456134661d9`.

For `K_RTK=(1+r q^2)K_BPS`, exact scalar normalization needs `T=sqrt(1+r q^2)` and the source transforms by the same factor. Then `J^2/K` is invariant. The obstruction is only to a scalar-only finite-polynomial local shortcut that keeps the original q-independent source unchanged.

Status: GREEN scoped theorem.

## Appendix C — direct spatially-covariant FLRW scalar match

File: `research/methods/RTK_FORMULA_BIBLE_C8_SPATIAL_COVARIANT_FLRW_APPENDIX.md`.

CI run `32514697064`, artifact `9458330218`, digest `sha256:72fe15a918873ee0d7bf6af27f6eab51ef47dea48d4a4c3d7db9d65de9aeeb74`.

Production identity:

`K_8piG=(rho_8piG+p_8piG)/c_a^2=2M_K^2`.

Controlled scalar reduction gives

`omega^2=c_a^2 p^2/(1+p^2/M_K^2)`.

Status: GREEN exact quadratic scalar theorem; full physical completion open.

## Appendix D — gravity normalization / standard universal matter

File: `research/methods/RTK_FORMULA_BIBLE_C8_GRAVITY_NORMALIZATION_APPENDIX.md`.

Always distinguish bare `M_*`, cosmological/Friedmann `G_cosm`, and local `G_N`.

- beta=0 run `32518243787`, artifact `9459582368`: BLACK scoped no-solution branch.
- general-beta run `32518936616`, artifact `9459822043`: exact direct standard universal low-energy matter frame excluded by combined BBN/Newton, PPN and GW requirements on the same direct slice.

Canonical result: `research/RTK_C8_STANDARD_MATTER_NO_GO_RESULT_2026-08-21.md`.

Status: BLACK scoped. Nonminimal/disformal/gauge/constraint completions remain open.

## Appendix E — grad-K and ordinary auxiliary ladder

The narrow `{a_i,D_iK}` basis cannot eliminate the direct static acceleration coefficient: run `32519335082`, artifact `9459962141`.

The corrected full TT-safe grad-K basis *can* span arbitrary pointwise scalar `(U,V,W)`; old broad `R=2` interpretation is SUPERSEDED. Corrected run `32522247851`, artifact `9460955420`.

One constant `(U,V,W)` tuple cannot follow production `M_K(a)`: run `32521251025`, artifact `9460618747`.

Within the minimal EH+clock+grad-K representation the required `U~H^-2`: run `32522407137`, artifact `9461010370`. This is a representation/regularity obstruction, not automatically a physical strong-coupling theorem.

Regular algebraic auxiliary Schur blocks cannot generate that divergence without singular unreduced coefficients or loss of auxiliary Hessian rank: run `32523115561`, artifact `9461246849`.

A pure `K^2`/Hořava-lambda deformation does not solve the exact-match problem: corrected run `32524954554`, artifact `9461843454`; exact identity forces `eta=0`.

A single ordinary dynamical auxiliary adds an extra finite frequency pole: corrected run `32524978316`, artifact `9461850988`. Two ordinary positive auxiliaries cannot cancel all frequency dependence: run `32524715584`, artifact `9461764440`.

Status: mixed GREEN algebra / BLACK scoped constructions. Genuine Dirac/gauge degeneracy remains the constructive route.

## Appendix F — Dirac-degenerate one-scalar mechanism

Detailed derivation: `research/methods/RTK_FORMULA_BIBLE_C8_DEGENERATE_AUXILIARY_APPENDIX.md`.

For

`L_kin = k/2 (dot X + a dot y)^2`,

the velocity Hessian has rank one. The primary constraint `p_y-a p_X=0` and a nondegenerate secondary constraint remove one configuration-space DOF, leaving one physical scalar.

For source direction `v=(1,a)` and positive potential matrix `V`,

`v^T(V-k omega^2 vv^T)^-1 v = Q/(1-kQ omega^2)`, `Q=v^T V^-1 v`.

Corrected CI run `32525622115`, artifact `9462068516`, digest `sha256:c9f42d3b8917cdaa083972edd9bc1ad4961a082ca62ce5c1cc2d45a08f8a4800`.

An invertible nondynamical lapse/shift Schur block leaves the rank-one velocity Hessian intact and replaces `V` by `V_eff=V-C A_z^-1 C^T`. Bridge run `32525916760`, artifact `9462166939`, digest `sha256:1b23375d2dbd6af5076c3bb9b1404bc4cd84cec5702fc0831ff93e3d3a35dc77`.

Status: GREEN quadratic/constraint toy mechanism; full nonlinear gravitational embedding open.

## Appendix G — fixed-state mixed-kinetic scalar EFT

Corrected CI run `32528572862`, artifact `9463080405`, digest `sha256:30af13757eb4b78553f97d1b887c11f6eb690a7f7bb02550bb03c11096211113`.

Fixed production state-functions give

`L2 = K(r)/2 [dot S^2 + (D_i dot S)^2/M_K(r)^2] - G(r)/2 (D_i S)^2`,

hence exactly

`omega^2 = c_a^2(r) p^2/[1+p^2/M_K(r)^2]`.

The production identity makes the mixed coefficient

`K/(2M_K^2)=M_Pl^2`,

a constant in the stated normalization.

Important embedding restrictions:

- kinetic-alignment theorem, run `32528978511`, artifact `9463185301`: for rank-one ordinary/mixed directions `v,w`, one-scalar rank for all p requires `w || v`;
- additive companion rank theorem, run `32529167558`, artifact `9463249160`: simply appending an independent healthy companion to an already propagating DBI scalar opens a second kinetic direction;
- alignment/background-silence obstruction, run `32529238991`, artifact `9463273507`: the same aligned rolling DBI combination cannot also be background silent;
- rolling normalization invariant, run `32529333288`, artifact `9463302781`: exact rolling mixed coefficient fixes `C q^2=M_Pl^2`, so a field rescaling/small background speed cannot weaken the direct acceleration strength;
- FDiff companion Dirac action theorem, run `32529105315`, artifact `9463228552`: an isolated aligned companion action can retain the primary rank-one constraint.

Status: GREEN for the isolated quadratic EFT and exact algebraic restrictions; full production-clock embedding remains open.

## Appendix H — local-U(1) gauge/constraint completion

File: `research/methods/RTK_FORMULA_BIBLE_C8_U1_COMPLETION_APPENDIX.md`.

U(1)-invariant mixed-scalar gate:

- run `32529835219`;
- artifact `9463470436`;
- digest `sha256:de07dea62ab61573a0395271d4f5c22edad2b5257a1760641b54412104e10f66`.

With `delta N_i=N D_i alpha`, `delta nu=alpha`, the combination

`Ntilde^i=N^i-N D^i nu`

is invariant. For U(1)-neutral `Sigma`,

`Theta_U=[dot Sigma-Ntilde^i D_i Sigma]/N`

is invariant, so `D_i Theta_U D^i Theta_U` is allowed by the local U(1) symmetry.

Direct rolling RTK coefficient maps to `beta0_RTK=2` in the convention `zeta^2=M_Pl^2/2`.

Published explicit GR-PPN families include:

- family I: `a1=kappa=1`, `sigma2=0`; these displayed equalities do not fix beta0, so beta0=2 is algebraically open but NOT PPN-certified;
- family II: `sigma2=4(1-a1)`, `beta0=-2(gamma1+1)`; canonical `gamma1=-1` gives beta0=0, excluding the direct beta0=2 slice in this family only.

Executable family-II source commit `bb04a706a7742005569dfa5feeb27bc59e42ef8c`; CI trigger `1ad8f32ce6d857016cc1717d135ac06081df4164`.

Executable family-I source commit `21fff2f9911350bd4fe4d701559acaf71821705d`; CI trigger `4247ed53d5d9f4d7850318c6ea34a03c6a467fd9`.

Status: YELLOW overall pending the two CI artifacts and then a same-tuple static/constraint calculation.

## Numerical proof chains

### B4 neutrino

Target-v2 base run `32482490823` was recenter-clear and PD at base scale. Independent half-scale run `32514077002`, artifact `9463331303`, has zero exact stencil improvement but a non-PD Hessian with `lambda_min=-0.007154172940511002`.

Frozen negative/soft-mode ray target: `rtk-class-build:research/robustness/b4_neutrino_rtk_target_v2_half_eigenmode_rays_target_v1.json`, commit `b0f17ffddb943c73c48f769de1407456e4aefd82`. Ray run launched by trigger `69f07b8956ead1611f0add45ad8474ab859018a7`.

### B6 abundances

`research/robustness/RTK_B6_ALTERBBN_RESULT_2026-08-21.md`: GREEN differential robustness only.

### B9 lensing

RTK recenter base run `32518496348`, artifact `9464480301`: exact improvement 0, PD Hessian, minimum eigenvalue `0.0005825694006286208`; independent half-scale launched, trigger `3f8f9fe18530bec31e7a9bfc69c03b780b4df721`.

LCDM run `32522002655`, artifact `9463358870`: parent center improved by `0.03518806934675922 > 0.005`; recenter-v2 target frozen and fresh base launched by trigger `5f034d51b0b71ed335819ff11c03126f137adb52`.

### B10 lambda tail

Canonical result `research/robustness/RTK_B10_FINAL_TAIL_IDENTIFIABILITY_RESULT_2026-08-21.md`:

`LAMBDA_NOT_NUMERICALLY_IDENTIFIABLE_AGAINST_PREREGISTERED_DUST_TAIL_AT_0P005`.

Cross-chat audit `research/robustness/RTK_B10_CHAT_AUDIT_2026-08-22.md`, commit `22515a46f6f908e022026ea2156ca547fabd4723`: **no missing mandatory B10-v1 gate**. Posterior/global/evidence work is separate A6, not unfinished B10.

## Current theoretical next move

Do not return to arbitrary pole fitting or simple additive companions. The useful frontier is one **complete fixed local-U(1)/Dirac-constrained action** that simultaneously:

1. keeps exactly the intended RTK scalar direction;
2. produces the exact mixed kinetic coefficient;
3. solves the static/PPN/Newton equations on the same beta0=2 tuple;
4. preserves the tensor/GW sector;
5. has a stable nonlinear constraint count;
6. survives radiative-stability and C9 cutoff checks.

Family-I algebraic openness is only a candidate starting surface, not viability.

## Recovery discipline

Every admitted result must retain action/equations, conventions, domain, derivation, exact symbolic/numerical checks, source commit, workflow/run/artifact provenance, scope/non-claims and validation status. Workflow success alone is not a physical closure.
