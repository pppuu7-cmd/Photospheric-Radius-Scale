# Published RT growth phenomenology cross-check

Status: **external qualitative sanity check; not an exact code-to-code validation**.

Primary reference: Y. Dirian, S. Foffa, M. Kunz, M. Maggiore, V. Pettorino, *Non-local gravity and comparison with observational datasets. II. Updated results and Bayesian model comparison with LambdaCDM*, arXiv:1602.03558.

## Published RT behavior

The published modified-CLASS analysis reports that the RT and other studied nonlocal models generically predict somewhat larger growth than LambdaCDM. For the RT model, at redshifts relevant to structure formation, roughly z >= 0.5, the deviations in structure-formation diagnostics were at most about 1% in that analysis. The authors connect the enhanced clustering to the modified-gravity sector and also note that, for the same cosmological parameters, RT can have a lower expansion rate than LambdaCDM, which further favors growth.

The same paper explicitly warns that growth conclusions depend on the assumed neutrino masses; their baseline used a normal hierarchy with sum m_nu = 0.06 eV.

## Relation to current RTK results

Our validated cross-anchor RTK diagnostic, holding the six shared cosmological parameters fixed, finds:

- f sigma8 enhancement about +2.17--2.23% over z=0.38--0.61;
- H(z) about 1% lower than LCDM at the same shared parameters;
- linear P(k) enhancement about +1.3--2.4% over the currently safer k range;
- the current Khronon itself is extremely deep in its dust limit, with w_K ~1e-6--1e-5 and c_a^2 ~1e-10--1e-8.

Thus the **sign and qualitative structure** of the present RTK growth signature are consistent with known RT phenomenology: lower expansion / modified gravity accompanies stronger growth.

## Why the numerical amplitude is not expected to match exactly

This is not a pure-RT reproduction. Differences include:

1. RTK replaces physical CDM with DBI-Khronon, even though the current Khronon is very dust-like.
2. The current RTK/LCDM parameter centers and data objective differ from the 2016 analysis.
3. The current production baseline uses `N_ncdm=0`, while the published RT analysis used a 0.06 eV massive-neutrino baseline and explicitly noted growth sensitivity to neutrino masses.
4. The current growth mapping and BOSS compressed likelihood are project-specific matched diagnostics.

Therefore +2.2% versus the historical <=~1% pure-RT scale should be treated as a **quantitative difference to investigate**, not as a contradiction or exact validation.

## Scientific consequence

The literature cross-check strengthens the interpretation that the current percent-level growth excess is primarily associated with the RT/nonlocal gravitational dynamics rather than the tiny finite DBI pressure at lambda_D ~2.2e5. A future controlled test should compare:

- pure RT + CDM,
- RT + dust-limit Khronon,
- finite-lambda RTK,
- matched LCDM,

all at identical shared parameters and with a common realistic massive-neutrino baseline. That factorial comparison would isolate the RT, Khronon-replacement and finite-DBI contributions separately.
