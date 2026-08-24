# RTK live research state — recovery entry point

This directory is the first stop after chat loss. Do **not** assume that `current.json` alone contains every newly reopened robustness/basin/theory question: the autonomous baseline orchestrator and manually advanced frozen subprotocols can move on different cadences.

## Read in this order

1. `current.json` — canonical autonomous baseline/control-plane state and the historical frozen A1-A5 local pair.
2. `A5_cross_basin_current.json` — authoritative override for the **best-known A5 basin status** whenever present. It does not erase the historical pair; it records whether stronger cross-basin evidence has reopened the reference-minimum question.
3. `B9_current.json` — authoritative live state for the standalone Planck-lensing robustness branch.
4. `C10_current.json` — detailed completed-U(1) cosmology-bridge closure ledger.
5. `C10_physical_history_current.json` — authoritative override for the **latest C10 active frontier** whenever it is newer than the active-gate paragraph in `C10_current.json`.
6. `../RTK_MASTER_RESEARCH_CLOSURE_MATRIX.md` — high-level closure/reopening matrix; check its timestamp against the live state files before relying on it.
7. Relevant frozen target/result files and methodology documents before executing a next gate.

## A5 precedence correction — 2026-08-24

`current.json` still records the historical fresh-tree replay-certified local pair

- LCDM `1049.966118347761`;
- RTK `1050.249912429787`;
- historical local `Delta S = +0.2837940820259064`.

Those numbers remain correct for those exact certified points. However, an independent fresh-tree four-point audit exactly reproduced a lower LCDM point of the **same unchanged objective**:

- new LCDM cross-basin seed `1049.400976604194`;
- improvement over historical LCDM point `0.5651417435669828`;
- all four target score replay errors `0.0`;
- classification `A5_B9_CROSS_BASIN_REPLAY_PASS_NEW_LCDM_SEED_CONFIRMED`.

Therefore, until the new LCDM seed completes its own baseline stationarity and fresh-tree replay chain:

- treat the historical A5 pair as a valid **historical local-basin certificate**;
- do **not** describe `+0.2837940820259064` as the current best-known final pair;
- do **not** update `current.json` accepted centers merely from the seed replay;
- follow `A5_cross_basin_current.json` and `A5_LCDM_cross_basin_stationarity_current.json` for the active replacement-candidate chain;
- statistics derived from the historical pair are historical/conditional until A5 is re-frozen.

## B9 — closed local robustness branch

Read `B9_current.json` plus

- `../methodology/B9_LIVE_RECOVERY_METHOD.md`;
- `../methodology/RTK_B9_A5_CROSS_BASIN_ADDENDUM_2026-08-24.md`.

B9 itself is now closed under its frozen local protocol:

- classification `B9_FINAL_PAIRED_EXACT_REPLAY_PASS`;
- `S_LCDM = 1058.2173424114785`;
- `S_RTK = 1059.2719553175134`;
- local paired `Delta S = +1.0546129060348903` (RTK minus LCDM);
- RTK independent fresh-tree certification passed.

This is a **local frozen robustness** result only. It is not global optimality, significance, AIC/BIC, posterior preference, Bayes factor, nonlinear-lensing completeness, or fixed-action completion evidence. Continue the separate A5 cross-basin chain independently; do not retroactively modify B9 closure from A5 recentering.

## C10 — completed-U(1) cosmology bridge

Read

- `C10_current.json` for detailed closed subgates;
- `C10_physical_history_current.json` for the newest active frontier;
- `../methodology/C10_LIVE_RECOVERY_METHOD.md` for formulas and derivations;
- the frozen target/result files under `../theory_targets/` and `../theory_results/`.

Latest C10 advance as of 2026-08-25:

- the ordinary-only A-source versus total metric/Ward momentum split is frozen;
- the Newtonian/Stueckelberg source transformation is frozen;
- the transformed finite-k determinant has no new pole on the certified branch;
- a standalone shadow metric reference (`../shadow/rtk_c10_completed_metric_shadow_v1.py`) is green algebraically and does not touch production CLASS;
- a reordered solver (`../shadow/rtk_c10_completed_metric_shadow_v2.py`) uses the exact identity `r E_th L phi = R_H + 2 H R_M`, removing avoidable direct-2x2 cancellation;
- arbitrary synthetic k-independent sources correctly expose a required physical small-k regularity condition rather than proving it: `R_H + 2 H R_M = O(k^2)` is required for finite super-horizon `phi`.

The active C10 gate is therefore **read-only replay of real RT-CLASS source histories** through shadow-v2. Do not feed completed-U1 potentials back into the Boltzmann hierarchy until that replay demonstrates source conventions, constraint residuals and small-k regularity.

## Safety rule

A launch commit, workflow green check, optimizer endpoint, lower raw score, synthetic algebra test, or isolated source replay alone is never a replacement certificate. Advance only through the frozen decision tree, preserving objective fingerprints, exact centers, tolerances, action/source conventions and provenance boundaries.
