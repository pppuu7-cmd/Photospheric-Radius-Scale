# B9 lensed-C_l interface guard v1

Status: **INTERFACE CONTRACT CONFIRMED; DOES NOT MUTATE B9-v1.**

The selected non-CMB-marginalized Planck R3 lensing product requests `pp,tt,ee,te` (plus unused/zeroed spectra according to its lmax contract). The B9 adapter supplies CLASS `cl_lensed.dat` for the primary CMB spectra and CLASS lensing-potential spectrum for `phiphi`.

This was cross-checked against the official Cobaya interface at public source commit `b76b6fed2a6c8c5594c6f92d5058bef10079746a`:

- `cobaya/likelihoods/base_classes/planck_clik.py` defines ordinary requested spectra through the theory requisite `Cl`; for lensing likelihoods it prepends `pp` to `tt,ee,bb,te,tb,eb`.
- `cobaya/theories/classy/classy.py` handles the ordinary `Cl` requisite by enabling CLASS `lCl`, setting `lensing=yes`, and collecting through CLASS `lensed_cl`.
- The same provider exposes unlensed spectra only through the distinct requisite `unlensed_Cl`, collected via `raw_cl`.

Therefore the project's use of lensed CLASS TT/EE/TE spectra for the ordinary non-marginalized Planck lensing clik matches the official Cobaya+CLASS interface semantics.

This guard does not address calibration-nuisance treatment; that is separately covered by `B9_PLANCK_CALIBRATION_INTERPRETATION_GUARD_v1.md`. It also does not validate nonlinear-lensing accuracy beyond the already frozen CLASS/B9 numerical protocol.

**Conclusion:** `cl_lensed.dat` is the correct CLASS-side CMB spectrum source for the selected B9-v1 clik interface; no B9 restart is required on this interface ground.
