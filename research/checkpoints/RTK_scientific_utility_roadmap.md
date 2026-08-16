# RTK / DBI-Khronon scientific-utility roadmap

Purpose: use other cosmological and modified-gravity models as orientation frameworks, not as competitors. The development target is a model that is maximally useful to the scientific community by connecting fundamental theory, robust numerics, observable signatures, cross-framework translation, and reproducible inference.

## Guiding principle

Do not optimize RTK merely to reduce one chi2 relative to LCDM or another model. Every comparison must answer one of four questions:
1. What physical mechanism or limit does RTK clarify?
2. What observable signature can RTK predict that is diagnostic across frameworks?
3. What theoretical/numerical consistency test can RTK make easier for the community?
4. What open-source interface lets other researchers reuse RTK without adopting its full interpretation?

## Capability matrix and open development questions

### A. Fundamental theory and consistency — highest priority

- [ ] Write the complete covariant action and parameter dictionary in one canonical source.
- [ ] Perform explicit degree-of-freedom / constraint count around FLRW and a generic background.
- [ ] Derive scalar, vector and tensor quadratic actions where applicable.
- [ ] Publish no-ghost, no-gradient-instability and hyperbolicity conditions as machine-checkable inequalities.
- [ ] Derive propagation speeds and compare tensor speed to the luminal-GW constraint class used in Einstein-Aether/khronometric and scalar-tensor models.
- [ ] Determine the strong-coupling / EFT cutoff and domain of validity of the cosmological calculation.
- [ ] Map all singular or degenerate parameter surfaces, including lambda_D -> infinity/dust and GR/LCDM-like limits.
- [ ] Clarify whether superluminal characteristic speeds occur and, if so, what causal interpretation/domain is intended.

Deliverable: `rtk/theory_consistency.py` + derivation note + automated stability map.

### B. Cross-framework translation — make RTK reusable by non-RTK researchers

- [ ] Derive an EFT-of-dark-energy / ADM dictionary wherever a single-clock mapping is valid.
- [ ] Export effective alpha-like or equivalent time functions when meaningful; explicitly state where the mapping fails.
- [ ] Derive a PPF-style observable dictionary: effective Poisson response mu(k,a), lensing response Sigma(k,a), gravitational slip eta(k,a), and transition scales.
- [ ] Provide a parameter dictionary to the closest khronometric/Einstein-Aether limits and identify genuinely non-equivalent RTK operators.
- [ ] Provide a compact `RTK -> phenomenology` JSON/table export from CLASS runs.

Deliverable: a translation layer allowing comparison with hi_class/EFT/PPF analyses without forcing the user to use RTK-specific variables.

### C. Observable signature atlas — more important than a single best fit

- [ ] Produce CMB TT/TE/EE/lensing residual templates against a matched background model.
- [ ] Produce matter P(k,z), growth f(k,z), f sigma8, Weyl potential and lensing residual templates.
- [ ] Quantify scale dependence of the two existing RSD mappings instead of treating them only as alternative likelihood conventions.
- [ ] Identify redshift/k ranges where RTK signatures are maximally orthogonal to LCDM, w0-wa, f(R), generic scalar-tensor and khronometric phenomenology.
- [ ] Build a Fisher-information / derivative atlas dO/dtheta showing which experiments constrain which RTK directions.
- [ ] Separate background degeneracy from perturbation-level discriminants.

Deliverable: `research/signature_atlas/` with machine-readable residuals and derivative tables.

### D. Early-universe and thermal-history closure

- [ ] Check BBN-era expansion and radiation domination for the allowed RTK domain.
- [ ] Test recombination and drag-epoch robustness beyond the current late-time fit usage.
- [ ] Determine whether the model has physically meaningful early-time attractors and whether initial conditions are unique/stable.
- [ ] Derive adiabatic/isocurvature initial-condition structure rather than assuming only a late-time implementation.
- [ ] Check whether the model can be consistently extrapolated to inflationary scales; if not, publish the cutoff and explicitly restrict scope.

Deliverable: early-time validity map, not necessarily an inflation model.

### E. Nonlinear structure and astrophysics — major community-value gap

- [ ] Derive quasistatic and weakly nonlinear limits.
- [ ] Compute spherical collapse / effective force law and identify any screening or recovery mechanism.
- [ ] Determine whether standard halo-model/emulator mappings are valid or fail.
- [ ] Develop or document the ingredients needed for N-body implementation.
- [ ] Derive static spherically symmetric equations for stars/compact objects if the theory permits them.
- [ ] Test Solar-System/PPN-type limits and binary-pulsar consistency where applicable.
- [ ] Investigate black-hole / horizon solutions and extra-mode regularity as a distinct theoretical work package.

Deliverable: even a rigorous statement of where the cosmological theory cannot yet be extended is scientifically useful.

### F. Gravitational-wave and multimessenger sector

- [ ] Derive tensor propagation speed, damping/friction, effective Planck-mass evolution and possible extra polarizations.
- [ ] Determine whether GW luminosity distance differs from electromagnetic luminosity distance.
- [ ] Assess compatibility with GW170817-like tensor-speed bounds in the appropriate low-redshift regime.
- [ ] Identify standard-siren observables and future discriminants.

Deliverable: GW propagation module + standard-siren forecast hooks.

### G. Data and inference modernization

- [ ] Freeze one final objective: exact-float cache + matched CLASS precision + dense BOSS sampling + documented Planck/Pantheon/BOSS conventions.
- [ ] Locally reoptimize RTK and control models on exactly the same objective before any model-comparison statistic.
- [ ] Add modern BAO/RSD/lensing datasets only after the final objective is locked, with dataset-by-dataset validation fixtures.
- [ ] Add posterior sampling after profile/stationarity geometry is numerically stable.
- [ ] Report profile likelihood, posterior, prior sensitivity and parameter-volume effects separately.
- [ ] Use information criteria/Bayes factors only as secondary summaries; never as the development target.

### H. Benchmark-model orientation suite

Use a small set of reference models because they cover distinct mechanisms, not because RTK must beat them:
- LCDM: minimal control and GR limit reference.
- w0-wa / smooth dark energy: background-degeneracy reference.
- f(R) or another scale-dependent scalar-tensor example: modified-growth reference.
- Horndeski/EFT representative: broad single-scalar perturbation reference.
- Einstein-Aether/khronometric representative: preferred-frame/vector-clock reference.
- Interacting/clustered dark-sector toy model: stress test for effective-fluid degeneracy.

For every reference model produce the same observables and derivative basis, then ask: which RTK effect is equivalent, which is degenerate, and which is genuinely distinct?

### I. Reproducibility and community interface

- [ ] Collapse `main` / `rtk-class-build` scientific-source divergence or enforce a single immutable production commit fingerprint.
- [ ] Publish environment lockfiles/container recipe and exact Planck-data provenance instructions.
- [ ] Add a one-command benchmark that reproduces theory limits, three Planck self-tests, one LCDM point and one RTK point.
- [ ] Provide examples for background-only, perturbations-only, likelihood evaluation and parameter scan.
- [ ] Version all scientific outputs by objective fingerprint, source SHA and precision preset.
- [ ] Add failure-mode documentation: invalid gamma roots, stability violations, CLASS timeouts, boundary hits and precision sensitivity.

## Development order

Tier 0 — finish currently active numerical closure:
1. recentered 7D Hessian after negative-curvature descent;
2. matched-ultra LCDM local control;
3. l_linstep=1 vs 2 precision rescue;
4. freeze dense-BOSS + ultra final objective.

Tier 1 — theoretical utility:
5. stability/DOF/propagation-speed package;
6. EFT/PPF/khronometric translation dictionary;
7. observable signature and derivative atlas.

Tier 2 — broaden physical reach:
8. early-universe validity and initial conditions;
9. GW/standard-siren sector;
10. quasistatic/nonlinear/spherical-collapse module;
11. compact-object/local-gravity feasibility program.

Tier 3 — inference and community release:
12. matched modern-data reoptimization;
13. posterior/prior-sensitivity analysis;
14. public reproducibility benchmark and documentation;
15. cross-model capability atlas focused on mechanisms and discriminants rather than ranking.

## Acceptance philosophy

A question is 'closed' only when its result is one of:
- an analytic theorem/derivation with assumptions stated;
- a numerically regression-tested result with precision/domain controls;
- an observational inference made on a frozen common objective;
- a rigorously documented negative result showing why a proposed extension is inconsistent or outside the theory's validity.

A lower chi2 alone closes none of the above.
