# RTK C10.65r2 — rerun-2 numeric parity passes, OFF-path identity remains blocker

Date: 2026-08-26 UTC
Branch: `rtk-class-build`
Frozen target: `research/theory_targets/RTK_C10_65R2_IN_CLASS_FIRST_RHS_DIAGNOSTIC_PARITY_TARGET_v1.json`

## Confirmed state

The first genuine C10.65r2 execution failed because r1 shear quantities are stored as `sigma/k^2` while the first C port inserted them as physical `sigma`. This was an implementation-unit bug, not a reason to change any frozen threshold.

The correction `rtk/fix_rtk_c10_65r2_shear_units.py` restores the missing factor of `k^2` in photon and UR Euler terms. The frozen workflow now applies that correction before rebuilding the r2 diagnostic CLASS binary.

## Frozen rerun-2 result

The unchanged frozen analyzer still classifies the gate as `C10_65R2_IN_CLASS_FIRST_RHS_DIAGNOSTIC_PARITY_FAIL_SCOPED`, but the scientific/numerical RHS checks now pass:

- max C vs independent-local RHS relative error: `2.0678011024437408e-10` (bound `5e-9`)
- max C vs detached-parent RHS relative error: `2.0678011024437408e-10` (bound `1e-6`)
- max r1 projector regression relative: `0.0` (bound `5e-11`)
- max Bprime actual-slip invariance relative: `0.0` (bound `5e-9`)
- max normalized photon-baryon slip cancellation residual: `2.051302863246e-16` (bound `5e-13`)
- exact onset: true
- all four anchors TCA-on: true
- all outputs finite: true
- no `dy` write: true
- no production metric/RHS write: true

Therefore the only current blocker is the frozen OFF-path exact numeric-text identity check.

## OFF-path diagnostic

A separate diagnostic workflow was added without changing the frozen target or analyzer. It compares r1-control and dormant-r2 perturbation files token by token.

All four files have identical row counts and token shapes, but are not text-identical. The first mismatches are tiny floating differences in existing columns, and the largest relative difference over all numeric tokens is `3.730940864022068e-09`.

Per-file maximum relative differences:

- k0: `2.9979324459093542e-09`
- k1: `1.5543967693442416e-09`
- k2: `2.3211117923084208e-09`
- k3: `3.730940864022068e-09`

This is consistent with the r2 diagnostic block perturbing compiler register/code-layout behavior for pre-existing r1 diagnostic computations even when the runtime r2 flag is OFF. It is not evidence of a changed physical RHS, but the frozen criterion is exact identity, so C10.65r2 remains FAIL until this is removed rather than waived.

## Next implementation step

Do not weaken the frozen OFF-path criterion. Refactor the r2 diagnostic implementation so the dormant branch cannot perturb pre-existing r1 calculations/stores. The preferred implementation is to move the r2 computation after all r1 diagnostic values have been stored and/or isolate it in a `noinline` helper called only when `c10_65r2_diag > 0.5`. Then rerun the exact same OFF-path hash test and the unchanged 36-point frozen analyzer.

Production `dy`, metric-source feedback, state handoff, and real completed-U1 evolution remain forbidden until C10.65r2 passes.

Fundamental physical gates remain open independently: C9 radiative naturalness and same-full-action primordial/background closure.
