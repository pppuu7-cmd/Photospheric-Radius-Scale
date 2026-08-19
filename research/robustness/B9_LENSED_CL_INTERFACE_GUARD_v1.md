# B9 lensed-C_l interface guard v1

Status: **INTERFACE CONTRACT CONFIRMED; DOES NOT MUTATE B9-v1.**

The selected non-CMB-marginalized Planck R3 lensing product requests `pp,tt,ee,te` (plus unused/zeroed spectra according to its lmax contract). The B9 adapter supplies CLASS `cl_lensed.dat` for the primary CMB spectra and CLASS lensing-potential spectrum for `phiphi`.

## Lensed versus unlensed CMB spectra

This was cross-checked against the official Cobaya interface at public source commit `b76b6fed2a6c8c5594c6f92d5058bef10079746a`:

- `cobaya/likelihoods/base_classes/planck_clik.py` defines ordinary requested spectra through the theory requisite `Cl`; for lensing likelihoods it prepends `pp` to `tt,ee,bb,te,tb,eb`.
- `cobaya/theories/classy/classy.py` handles the ordinary `Cl` requisite by enabling CLASS `lCl`, setting `lensing=yes`, and collecting through CLASS `lensed_cl`.
- The same provider exposes unlensed spectra only through the distinct requisite `unlensed_Cl`, collected via `raw_cl`.

Therefore the project's use of lensed CLASS TT/EE/TE spectra for the ordinary non-marginalized Planck lensing clik matches the official Cobaya+CLASS interface semantics.

## Pinned CLASS `phiphi` output units

The production CLASS source is pinned to `dirian/class_public` commit `36cf283628c4a3330ec9fd3d84239bf775f77317`. In that source, `output_open_cl_file()` declares the class-format spectral column `phiphi`, and `output_one_line_of_cl()` defines

`factor = l(l+1)/(2 pi)`

and writes `factor * cl[index_ct]` for **every** class-format spectral column. Thus class-format `phiphi` is exactly `l(l+1) C_l^{phiphi}/(2 pi)`, not the CAMB-style deflection-power normalization with additional powers of `l(l+1)`.

The B9 adapter's operation `C_l^{phiphi} = printed_phiphi / factor` is therefore the exact inverse of the pinned CLASS class-format output. For TT/EE/TE it applies the same inverse factor and then the project FIRAS-temperature conversion to micro-Kelvin squared, matching the clik/Cobaya raw-C_l convention.

This guard does not address calibration-nuisance treatment; that is separately covered by `B9_PLANCK_CALIBRATION_INTERPRETATION_GUARD_v1.md`. It also does not validate nonlinear-lensing accuracy beyond the already frozen CLASS/B9 numerical protocol.

**Conclusion:** `cl_lensed.dat` is the correct CLASS-side CMB spectrum source and the project's `phiphi` D_l-to-C_l conversion is correct for the pinned CLASS source; no B9 restart is required on these interface grounds.
