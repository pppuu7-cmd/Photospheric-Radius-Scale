# RTK live research state — recovery entry point

This directory is the first stop after chat loss. Do **not** assume that `current.json` alone contains every newly reopened robustness/basin question: the autonomous baseline orchestrator and manually advanced frozen subprotocols can move on different cadences.

## Read in this order

1. `current.json` — canonical autonomous baseline/control-plane state and the historical frozen A1-A5 local pair.
2. `A5_cross_basin_current.json` — authoritative override for the **best-known A5 basin status** whenever present. It does not erase the historical pair; it records whether stronger cross-basin evidence has reopened the reference-minimum question.
3. `B9_current.json` — authoritative live state for the standalone Planck-lensing robustness branch.
4. `../RTK_MASTER_RESEARCH_CLOSURE_MATRIX.md` — current high-level closure/reopening matrix.
5. Relevant frozen target/result files in `../robustness/` and methodology documents before executing a next gate.

## Current precedence correction — 2026-08-24

`current.json` still records the historical fresh-tree replay-certified local pair

- LCDM `1049.966118347761`;
- RTK `1050.249912429787`;
- historical local `Delta S = +0.2837940820259064`.

Those numbers remain correct for those exact certified points. However, an independent fresh-tree four-point audit has now exactly reproduced a lower LCDM point of the **same unchanged objective**:

- new LCDM cross-basin seed `1049.400976604194`;
- improvement over historical LCDM point `0.5651417435669828`;
- all four target score replay errors `0.0`;
- classification `A5_B9_CROSS_BASIN_REPLAY_PASS_NEW_LCDM_SEED_CONFIRMED`.

Therefore, until the new LCDM seed completes its own baseline stationarity and fresh-tree replay chain:

- treat the historical A5 pair as a valid **historical local-basin certificate**;
- do **not** describe `+0.2837940820259064` as the current best-known final pair;
- do **not** update `current.json` accepted centers merely from the seed replay;
- follow `A5_cross_basin_current.json` for the active replacement-candidate gate;
- statistics derived from the historical pair are historical/conditional until A5 is re-frozen.

## B9

Read `B9_current.json` plus

- `../methodology/B9_LIVE_RECOVERY_METHOD.md`;
- `../methodology/RTK_B9_A5_CROSS_BASIN_ADDENDUM_2026-08-24.md`.

The current provisional B9 local difference must not be frozen until the RTK independent fresh-tree certification and the preregistered final paired exact replay pass.

## Safety rule

A launch commit, workflow green check, optimizer endpoint, or lower raw score alone is never a replacement certificate. Advance only through the frozen decision tree, preserving objective fingerprints, exact centers, tolerances, and provenance boundaries.
