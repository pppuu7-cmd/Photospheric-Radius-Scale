# RTK C8 strengthened FLRW Schur CI result

Date: 2026-08-21
Status: GREEN for the encoded reduced-kernel algebra only

## GitHub provenance

- workflow run: `32490690248`
- workflow: `RTK C8 FLRW Schur diagnostic self-test`
- head SHA: `b6fb32f79b1bc951ea7ae50b8bdda5947c526229`
- artifact id: `9449602889`
- artifact name: `rtk-c8-flrw-schur-selftest`
- artifact digest: `sha256:1f2bfda3959e8b6c57866bd35e7279e7cb398460c1a6cd296d4b2d146e092dce`
- research source commit recorded by artifact: `0276df24ef7dc3146cc0528d61fff6b924b53e06`
- Python: `3.12.3`

## Artifact checks

The artifact contains both markers:

- `C8_FLRW_SCHUR_SELFTEST_PASS`
- `C8_FLRW_SCHUR_RANK_RESIDUE_SELFTEST_PASS`

The exact diagnostic report records:

- `D0 = 2`
- `D1 = 6`
- `D2 = 0`
- strict linear denominator gate: PASS
- gradient block rank: `1`
- rank-one necessary gate: PASS
- q-plane coefficient pole: `q_pole = -1/3`
- `Res_q[N/D] = +1/9`
- `Res_q[Schur term in K_eff] = -1/9`
- unique nonzero gradient-eigenvalue sign: positive
- conditional rank-one residue-sign gate: PASS

This explicitly validates the sign theorem for the encoded exact-arithmetic example: positive rank-one gradient-block sign gives a negative nonzero q-plane Schur residue.

## Scope

This CI result promotes the encoded two-constraint reduced-matrix algebra and its rank/residue self-tests to reproducibly verified status.

It does **not** establish:

- a DHOST degeneracy condition;
- the physical propagator residue in `omega^2`;
- a ghost/no-ghost result;
- a fixed-action RTK source map;
- nonlinear DOF closure;
- an EFT cutoff;
- a UV completion.

The artifact itself labels the residue variable as spatial `q`, not `omega^2`, and carries the same warning.

## Next C8 bridge

The next nonredundant gate is to derive `M0,M1,J,K0` from one explicit fixed FLRW carrier action and test pole, normalized q-residue, polynomial remainder and physical source response with the same Wilson coefficients across epochs.
