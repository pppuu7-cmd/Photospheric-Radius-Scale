# RTK minimal-neutrino matched reoptimization protocol v1

Status: **FROZEN ROBUSTNESS PROTOCOL BEFORE REOPTIMIZATION**.

This protocol is a robustness layer. It does **not** alter or replace the already frozen massless matched comparison `matched-ultra-linstep2+dense-BOSS` or its A1–A5 certifications.

## Scientific question

Does the local RTK-vs-ΛCDM matched comparison remain qualitatively stable when the legacy massless-neutrino baseline is replaced by one standard minimal-mass neutrino species and **both models are reoptimized under the same new robustness objective**?

The existing six-point fixed-center diagnostic is not sufficient because the 0.06 eV change shifts the objective by many score units at the old minima.

## Frozen primary neutrino convention

Use one massive species with the pinned legacy CLASS convention:

- `N_ncdm = 1`
- `m_ncdm = 0.06` eV
- `T_ncdm = 0.71611`
- `deg_ncdm = 1.0`
- `N_ur = 2.0328`

`Ob` remains baryonic matter. `Om` remains the fitted CDM coordinate in ΛCDM and fitted Khronon non-baryonic dark-sector coordinate in RTK. The massive neutrino density is added by CLASS as a separate species. **Do not pre-subtract Omega_nu from Om in the primary reoptimization.** Because `Om` is itself refitted, the optimizer is free to compensate the added neutrino density if the likelihood prefers it.

The earlier `mnu006_fixed_total_nonbaryonic` fixed-center mode remains a secondary sensitivity convention only; it is not the primary B4 matched robustness objective.

## Objective

Robustness objective name:

`matched-ultra-linstep2+dense-BOSS+nu0p06-additive-v1`

Keep exactly the same observational and numerical structure as the frozen massless objective:

- Planck 2018 Commander lowT + SimAll lowE + Plik-lite TTTEEE;
- Pantheon binned full covariance with the common offset analytically profiled;
- BOSS DR12 full 9x9 consensus covariance;
- production growth mapping `eff`; keep `k01` recorded separately;
- exact dense `z_pk` grid from `research/state/current.json`;
- exact ultra CLASS precision block from `research/state/current.json`;
- Newtonian gauge;
- RECFAST;
- exact-float successful-evaluation cache only;
- failed CLASS/post-processing evaluations must never be memoized;
- same pinned CLASS/Pantheon/Planck/NumPy/SciPy provenance as the frozen comparison.

Only the neutrino block above changes.

## Models and fitted coordinates

ΛCDM robustness fit: six fitted coordinates

`As, Ob, Om(cdm), h, ns, zre`.

RTK robustness fit: seven fitted coordinates

`As, Ob, Om(Khronon), h, log(lambda_D), ns, zre`.

Start from the independently replayed massless local minima in `research/state/current.json`. These are starts only, not accepted minima for the neutrino objective.

## Search and acceptance sequence

1. Reproduce each starting point once with the neutrino objective and record all likelihood components.
2. Perform a deterministic local reoptimization in normalized coordinates with explicit physical bounds and exact likelihood evaluations.
3. Run an exact coordinate poll around the optimizer candidate. Any exact downhill improvement larger than `0.005` requires recentering and another local optimization/poll cycle.
4. Once coordinate-recenter-clear, run the same model-appropriate stationarity proof logic used by the frozen comparison: Hessian/negative-eigenray/multiscale checks as needed. Do not call a candidate an interior local minimum merely because a Powell optimizer stopped.
5. Independently fresh-tree replay both final neutrino robustness minima before freezing the robustness `Delta S_nu`.

## Robustness outputs

Freeze and report separately from the massless result:

- `S_RTK_nu0p06`
- `S_LCDM_nu0p06`
- `Delta S_nu0p06 = S_RTK_nu0p06 - S_LCDM_nu0p06`
- shift of each model score relative to its massless local minimum;
- shifts in fitted parameters;
- Planck / Pantheon / BOSS component decomposition;
- `eff` and `k01` separately;
- stationarity and replay provenance.

## Interpretation gate

B4 may receive 🚀 only if **both models have matched, reoptimized, stationarity-certified neutrino robustness minima and an independent paired replay passes**.

Fixed-center comparisons, a single optimizer stop, or one-model-only reoptimization cannot close B4.

No replacement of the massless baseline, no Bayes/significance claim, and no global-minimum claim follows from this robustness exercise.
