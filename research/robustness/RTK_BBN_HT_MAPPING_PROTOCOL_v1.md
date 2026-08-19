# RTK BBN H(T) mapping protocol v1

Status: **FROZEN BEFORE FIRST ALTERBBN T-a TRACE / RTK H(T) TABLE EXECUTION**.

This protocol is downstream of `RTK_BBN_ABUNDANCE_PROTOCOL_v1.md`, the pinned AlterBBN v2.2 source lock, the standard-network self-test, and the structural expansion-interface audit. It constructs the RTK expansion-history table only; it does not yet modify the abundance network or compare abundances with observations.

## Fixed cosmological semantics

- use the frozen **massless** A1-A5 RTK accepted-score parameter point;
- radiation baseline: `T_cmb=2.7255 K`, `N_ur=3.046`, `N_ncdm=0`;
- compare RTK model=2 to a model=0 LCDM control at the **same RTK shared parameters** (`h,Omega_b,Omega_nonbaryonic,A_s,n_s,z_reio`), so the table isolates the implemented RTK expansion correction rather than the difference between separately optimized late-time parameter points;
- CLASS upstream and RTK patches remain pinned by the production reproducibility lock.

## Why T=T0(1+z) is not used through the whole BBN epoch

AlterBBN evolves the electromagnetic plasma through the electron/positron annihilation epoch. A naive direct conversion `T_gamma=T0(1+z)` through that interval would ignore the entropy-transfer relation represented by the BBN solver. Therefore the mapping must use AlterBBN's own evolved scale factor.

The structural source audit established that `src/bbn.c` evolves `a` through `da/dt = H*a` and computes the common Hubble rate before the temperature/electron-chemical-potential/scale-factor derivatives. This makes an instrument-only `(T,a,H_reference)` trace the preferred mapping coordinate.

## Instrument-only reference trace

1. Start from the exact pinned AlterBBN v2.2 source bytes.
2. Apply a mechanical instrumentation patch only after the standard Hubble-rate line in `src/bbn.c`. The patch may write `T`, internal `a`, and the unmodified standard `H`; it must not alter any variable used by the network.
3. Build and run the same standard `stand_cosmo.x` central calculation with `failsafe=1`.
4. The printed central abundances must match the already accepted unmodified standard self-test at its printed precision: `Yp=0.2473`, `D/H=2.435e-5`, `He3/H=1.031e-5`, `Li7/H=5.466e-10`. A mismatch is a hard failure of the instrumentation step.
5. Reduce the raw solver-call trace to a monotone thermodynamic path using log-temperature bins; record the reduction rule and retain the raw trace.

## Physical scale-factor calibration

Use a fixed post-electron/positron-annihilation anchor temperature

`T_anchor = 0.01 MeV = 1e-5 GeV`.

Let `a_int(T)` be AlterBBN's internal scale factor and let `a_int,anchor` be the log-interpolated internal scale factor at `T_anchor`. With

`T0 = k_B * 2.7255 K`, `k_B = 8.617333262e-14 GeV/K`,

set

`a_phys,anchor = T0 / T_anchor`

and for every trace temperature

`a_phys(T) = a_phys,anchor * a_int(T)/a_int,anchor`,

`z(T) = 1/a_phys(T) - 1`.

This uses AlterBBN's integrated scale-factor ratio across the e± entropy-transfer epoch rather than assuming `a*T=const` there. The anchor must lie inside the traced network range; no anchor extrapolation is allowed.

## CLASS expansion-ratio table

Run the pinned RTK CLASS background twice:

1. RTK model=2 at the frozen massless RTK accepted-score parameters;
2. model=0 same-parameter control with `Omega_cdm=Omega_khronon` and all shared/radiation parameters identical.

For every retained AlterBBN trace point interpolate the positive CLASS background Hubble rates in `log(1+z)` and define

`R(T) = H_RTK(z(T)) / H_same_params_LCDM(z(T))`.

The CLASS background must cover the full mapped z-range. Any table point outside coverage is a hard failure; no extrapolation is permitted.

## Table reduction and numerical checks

Produce at least two nested log-temperature tables (nominal and refined; target minimum 256 and 512 retained points when the traced path provides enough resolution). Require:

- strictly positive finite `T`, `a_phys`, `H_RTK`, `H_reference`, and `R`;
- monotone T and physical scale factor in the expected opposite directions;
- full BBN traced-temperature coverage without CLASS extrapolation;
- the refined-vs-nominal log-linear interpolation of `R(T)` to agree to absolute `2e-12` or better over the common temperature range, unless the measured RTK effect itself is smaller, in which case retain full double precision and report the absolute interpolation error rather than dividing by a near-zero `R-1`;
- record `max |R-1|` over the network range and at representative temperatures.

## Next gate

Only after this mapping table passes may AlterBBN be patched so that the already-computed standard Hubble rate in `src/bbn.c` is multiplied by the tabulated `R(T)`. The paired reference run must use `R(T)=1` through the identical lookup code path. No `dark_density`, dark-pressure, or dark-entropy hooks are to be repurposed for this first test, because the frozen abundance protocol requests an isolated expansion-history modification.

Before consuming the resulting RTK abundance differences for an observational statement, the Yp/D-H observational constraint set must be separately frozen and cited as required by `RTK_BBN_ABUNDANCE_PROTOCOL_v1.md`.
