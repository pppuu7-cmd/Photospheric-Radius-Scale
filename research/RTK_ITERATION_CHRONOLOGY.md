# RTK Research Iteration Chronology

Status: canonical append-only iteration timing log
Created: 2026-08-21

Purpose: record the wall-clock start of each assistant-driven research iteration separately from the scientific model chronology. This prevents ambiguity about when a reasoning/repository cycle began. Scientific conclusions remain in `research/RESEARCH_LEDGER.md`, formula derivations in the Formula Bible, and major model evolution in `research/RTK_MODEL_CHRONOLOGY.md`.

Rules:

1. Record the start time as stated at the beginning of the user-facing research iteration.
2. Store both user-local time with UTC offset and UTC.
3. Record the main frontier entered at iteration start.
4. Add commit/run/artifact IDs produced during the iteration when available.
5. This timing log is provenance only; its timestamps do not imply scientific completion.

---

## Iteration started 2026-08-21 23:32:00 UTC+03:00 / 2026-08-21 20:32:00 UTC

User instruction: continue research and explicitly record the time at which the response/research iteration began.

Frontier at start:

- B4 target-v2 half-scale Hessian run `32514077002` still in exact Hessian step.
- B9 RTK recenter base Hessian run `32518496348` still in exact Hessian step.
- B9 LCDM interrupted-recenter base Hessian run `32522002655` still in exact Hessian step.
- C8 corrected TT-safe grad-K basis already CI-verified.
- C8 minimal EH+clock grad-K zero-H regularity obstruction already CI-verified.
- C8 algebraic auxiliary-rank and pure K^2 deformation gates had been launched and awaited direct artifact inspection.

New action in this iteration:

- added `rtk-class-build:rtk/route_b_gradK_dynamic_auxiliary_pole_gate.py`, commit `66b0c726e0acdff52ef7accb48d870c4dd9fb2a7`;
- added workflow `.github/workflows/rtk-route-b-gradk-dynamic-auxiliary-pole.yml`, commit `ed472cf61e81c59908aaec001c884f36881d78fe`;
- launched the gate with trigger commit `453f2e38d0be543abb88f11fb1a4b85b63c2550a`.

The theorem tests the minimal genuinely dynamical auxiliary. For

`L = 1/2 K0 X^2 + b X y + 1/2(A-Z omega^2)y^2`,

exact elimination gives

`K_eff = K0 - b^2/(A-Z omega^2)`.

For finite nonzero `b,Z`, this introduces an extra pole `omega_aux^2=A/Z`. If one tries to obtain the required `H^-2` enhancement with regular finite `b,Z` through `A~H^2`, then `omega_aux^2~H^2 -> 0`: the auxiliary mode becomes light at the static boundary. The result is scoped to the minimal single dynamical auxiliary; explicitly degenerate/gauge multi-field systems and action-derived exact cancellations remain open pending CI and further DOF analysis.
