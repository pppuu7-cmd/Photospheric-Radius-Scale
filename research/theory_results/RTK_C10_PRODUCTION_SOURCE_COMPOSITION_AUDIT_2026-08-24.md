# C10 production source-composition audit

Date: 2026-08-24
Target: `research/theory_targets/RTK_C10_PRODUCTION_SOURCE_COMPOSITION_TARGET_v1.json`
Classification: **C10_BASELINE_SOURCE_IDENTITY_CONTRACT_PASS_SCOPED**

## Question

Identify the physical ordinary source that may enter the elliptic completion filter in the actual RTK production cosmology, without mistaking a legacy storage slot or the fit key `Om` for physical CDM/total matter.

## Production mapping recovered from source

The production RTK parameter writer uses:

- `Omega_b = p['Ob']`;
- `Omega_khronon = p['Om']`;
- `lambda_D = p['lam']`;
- `Omega_Lambda = 0`, `Omega_fld = 0`, `Omega_scf = 0`, `Omega_k = 0`;
- baseline `N_ur = 3.046`, `N_ncdm = 0`.

The LCDM branch separately maps its fit `Om` to `Omega_cdm`. Therefore the identical Python key name `Om` has different physical meaning in the two model branches. In RTK it is a historical fit/storage name for `Omega_khronon`, not total matter and not dust.

`upgrade_rtk_inputs.py` explicitly implements `Omega_khronon` as a model-2-only alias backed by the legacy CLASS `Omega0_cdm` slot and forbids simultaneous CDM and Khronon input. The alias is storage, not physical CDM.

`upgrade_rtk_matter_sources.py` correspondingly replaces generic dust bookkeeping in model 2 by physical Khronon density/pressure perturbation combinations. This independently rules out interpreting the storage slot as an ordinary CDM fluid.

## Frozen baseline completion-source contract

For the current A5 baseline (`N_ncdm=0`), the ordinary filtered source is restricted to:

1. baryons;
2. photons;
3. massless relativistic species.

The RTK/Khronon completion sector is neutral/unfiltered under this contract. Physical CDM is absent. The legacy `Omega0_cdm` storage alias is never a source species.

For the B4 minimal-neutrino branch, physical massive `ncdm` must be added explicitly and validated separately before a same-action B4 claim.

## What is now closed

The source *identity* ambiguity is closed for the baseline production mapping. Future C10 code must not use fitted RTK `Om` as ordinary matter density.

## What remains open

This audit does **not** prove the same-full-action Friedmann normalization. In particular, the useful inequality

`rho_filtered <= rho_eff`

is not promoted to a theorem merely from the source identity. It must be checked after the completed action's background equations and gravitational normalization are fixed on the same branch. The B4 `ncdm` extension is also still separate.

## Scientific status

**GREEN scoped:** baseline production species identity and no-fake-CDM contract.

**YELLOW:** same-action background normalization, history-wide `rho_filtered <= rho_eff`, and massive-neutrino extension.
