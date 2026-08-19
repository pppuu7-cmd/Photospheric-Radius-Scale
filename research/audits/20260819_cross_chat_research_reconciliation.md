# Cross-chat RTK research reconciliation audit

Date: 2026-08-19

Purpose: reconcile useful scientific/software work that existed in other RTK/DBI-Khronon research conversations but was not fully represented in the current high-level summary or closure matrix. Repository artifacts/runs, not chat wording, are treated as evidence whenever available.

## Recovered and accepted evidence

### B6: pinned abundance-network infrastructure

The BBN branch had progressed beyond the previously remembered “need a pinned solver” stage.

- published-source pin audit run `32196956939` — success;
- AlterBBN v2.2 published file `alterbbn_v2.2.tar.xz` pinned from DOI `10.17632/k7j3b9zyvf.1`;
- archive SHA256 `2bcb7d2e3f4a74f59cd589e60f0923892bb90296a793f80016897405920c5fae`;
- extracted source-tree content SHA256 `f38f800662ee45cd06c38a83f9862221902a46a9f4d9c5a5f4edf0e3e43e9e3b`;
- unmodified standard-network self-test run `32197663994` — success;
- artifact `9346854614`, digest `sha256:867b28e4a85848337ba010e82aa632c4bce369d7d43604d2a82f950a3ab293f0`;
- self-test classification `ALTERBBN_V2_2_STANDARD_NETWORK_SELFTEST_PASS`.

Recorded standard-network refinement check:

- failsafe1: `Yp=0.2473`, `D/H=2.435e-5`, `He3/H=1.031e-5`, `Li7/H=5.466e-10`;
- failsafe7: `Yp=0.2474`, `D/H=2.466e-5`, `He3/H=1.034e-5`, `Li7/H=5.365e-10`;
- relative refinement differences: D/H `0.012570965125709736`, Yp `0.00040420371867427944`.

Interpretation: the published source pin and standard unmodified network self-test are closed subgates. The RTK H(T) injection, abundance refinement under RTK expansion, and preregistered observational comparison remain open; no BBN consistency claim is inferred from the standard self-test alone.

### Route-B nonlinear-completion exploration

Three repository-backed subgates were recovered.

1. Run `32196811436`, artifact `9346132368`, digest `sha256:6a7fe435676476c7268baf64f03738fb9b317441aee5cd8962449e6f48e00521`:
   `RTK_ROUTE_B_STANDARD_KHRONOMETRIC_POTENTIAL_ONLY_NONMAPPING_PASS`.
   The standard potential-only quadratic khronometric ansatz with constant kinetic coefficient cannot reproduce the target rational dispersion `omega^2=c_a^2 q^2/(1+q^2/M^2)` nontrivially; a momentum-dependent/mixed-derivative kinetic structure can.

2. Run `32197431357`, artifact `9346332881`, digest `sha256:5b5ec1af374710cc17b948bbfc889e6a7bc5147c04d69dc66d4334712fa49135`:
   `RTK_ROUTE_B_KHRONOMETRIC_ACCELERATION_DEGENERACY_AUDIT_PASS`.
   Within the audited constant-c_i khronometric/DHOST subclass, a tunable nonzero acceleration term is strongly constrained by degeneracy and leads to the documented kinetic degeneracy branch; simple pure-c4 completion does not solve the full degeneracy conditions.

3. Run `32198331764`, artifact `9346619409`, digest `sha256:4a1544852547a950c24a7aac19ec2f566890cf2641e3a74fa17d70f028447889`:
   `RTK_ROUTE_B_SPATIAL_COVARIANT_BENCHMARK_PASS`.
   A local preferred-foliation metric+Khronon benchmark of the form
   `N sqrt(gamma)[Mpl^2/2 (R3+KijKij-K^2)+F(N)+C(N)a_i a^i]`
   gives the declared linear mapping, reproduces the target dispersive scalar relation, and has the recorded generic spatially-covariant constraint count of three physical DOF.

Interpretation: these materially narrow viable local nonlinear completions and provide a constructive metric+Khronon benchmark. They do **not** close the full coupled causal RT+Khronon nonlinear DOF/ghost theorem because the causal RT sector is not incorporated into that local benchmark.

### B8: galactic flat-curve necessary-condition falsification

`rtk/galactic_rotation_curve_falsification.py` establishes a deliberately limited negative subgate for the implemented **linear** static/quasistatic closure. The effective kernel is rational/affine in k^2 and gives Newton/Yukawa-like real-space Green functions, not an asymptotic `Phi~log r` potential. Therefore the current linear cosmological closure by itself does not contain a scale-free flat-rotation-curve mechanism around a compact baryonic source.

Interpretation: this rejects a stronger “linear RTK already replaces the galaxy halo” claim. It is not a nonlinear galaxy solution and does not close solar-system, screening, nonlinear structure or compact-object phenomenology.

### Likelihood/software details worth retaining

- The BOSS consensus covariance had an independent positive-definiteness / conditioning audit; the reported correlation-matrix condition number was approximately `13.95`.
- The legacy standalone convergence test that used `A_s_ad` / `n_s_ad` was identified as invalid for this pinned nonlocal CLASS branch. Current hardened signature/inference code explicitly rejects those primordial parameter names and uses `A_s` / `n_s`.
- Earlier fine-search results contaminated by the former rounded/failure cache behavior are historical diagnostics only and must not be revived as accepted minima.

## Recovered open gates that had fallen out of the high-level matrix

### Standalone Planck lensing likelihood robustness

The frozen production objective uses Planck lowT + lowE + Plik-lite TTTEEE, but not the separate Planck lensing likelihood. A dedicated matched robustness comparison including standalone lensing was explicitly left open in earlier work. It is now restored as B9.

### Finite-lambda_D versus dust-boundary / tail identifiability

Stage4D3 proves a local finite-lambda_D RTK interior minimum at the frozen massless objective. That does not answer the different question of whether finite lambda_D is globally/tail-identifiable against the large-lambda (dust-like) boundary. Earlier broad scans showed very weak lambda sensitivity; one recorded factor-64 range changed BOSS chi2 by only about `0.00131`. This global/tail question is restored as B10 and must be handled by a separately preregistered profile/tail scan rather than by reinterpreting the local Hessian.

## Items intentionally not promoted

- No old pre-exact-cache optimum is restored as a scientific minimum.
- No failed/legacy `A_s_ad` / `n_s_ad` convergence result is used as precision evidence.
- No Route-B local benchmark is described as the fundamental RT action or as a proof for the causal nonlocal RT sector.
- No galactic linear-kernel falsification is generalized into a nonlinear local-gravity theorem.
- No neutrino seed optimizer result is called a minimum before multiscale stationarity and fresh replay.

## Integration into authoritative project state

`research/RTK_MASTER_RESEARCH_CLOSURE_MATRIX.md` was updated on 2026-08-19 to include:

- D4 as major closed after model-aware provenance hardening and fresh LCDM locked replay;
- current B4 neutrino stationarity status;
- AlterBBN pin/self-test progress in B6;
- the galactic negative subgate in B8;
- new B9 Planck-lensing robustness row;
- new B10 finite-lambda_D/dust-boundary identifiability row;
- Route-B evidence under C7 while leaving the full causal RT+Khronon theorem open.

This audit is intended to prevent future context loss: future chat-derived claims should be promoted into the matrix only when they are backed by repository artifacts, explicit protocol documents, or clearly labeled open questions.
