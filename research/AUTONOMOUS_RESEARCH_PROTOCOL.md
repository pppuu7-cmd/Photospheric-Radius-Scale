# RTK autonomous research protocol

## Goal

Run one repository-synchronized research-control iteration every 10 minutes using GitHub Actions. All durable state lives in the repository, not in chat context.

## Important capability boundary

The 10-minute loop is a repository-side state machine and compute orchestrator. It can inspect GitHub Actions, parse exact scientific artifacts, apply predeclared scientific decision rules, update accepted centers, launch the next allowed workflow, and journal every decision. It is not itself a free-form ChatGPT session. A future LLM hook may be attached separately if a model endpoint and secret are deliberately configured.

## Durable state

- `research/state/current.json` — authoritative scientific frontier and accepted centers.
- `research/state/lock.json` — human-readable lease mirror.
- `research/iterations/` — one immutable JSON journal file per orchestrator iteration.
- `research/checkpoints/` — milestone snapshots.

## Synchronization

The scheduled orchestrator uses GitHub Actions `concurrency` so only one control iteration executes at a time. Each iteration checks out `rtk-class-build`, reads the latest committed state, queries current run status through the GitHub API, parses completed artifacts, updates state, commits it, then dispatches at most one new heavy workflow.

## Scientific guardrails

1. Never compare old sparse scores directly to the matched-ultra+dense production objective.
2. Keep `eff` and `k01` as separate objective variants. The production mapping is currently `eff`.
3. Recenter only when an exact improvement on the same mapping exceeds `0.005`.
4. A successful GitHub job is not automatically a scientific PASS; parse `summary.json`.
5. Local Hessians are not global posterior/evidence proofs.
6. Do not produce AIC/BIC/Bayes/significance claims until both matched RTK and LCDM minima are frozen.

## State machine

### `await_dense_axis_and_lcdm_hessian`

Watch current RTK dense axis run and LCDM dense Hessian run.

RTK axis completion:
- parse `best_improvement_eff`, `best_eff.params`, and gate;
- if `best_improvement_eff > 0.005`, update RTK accepted center to the exact `best_eff` point and dispatch a new dynamic dense RTK axis gate around that center;
- otherwise dispatch the dynamic full dense RTK 7D Hessian at the accepted center.

LCDM Hessian completion:
- record center score, best exact score, best improvement, Hessian eigenvalues/PD flag, and Newton result;
- if improvement is small and local geometry acceptable, mark local certification complete;
- if a meaningful exact descent is found, preserve the result and request/relaunch a recentered LCDM certification rather than pretending the old center is final.

### `rtk_axis_recenter`

Repeat dynamic axis gates until `best_improvement_eff <= 0.005`, then launch RTK full dense Hessian.

### `rtk_hessian_running`

Watch the RTK full dense Hessian. If its exact stencil/Newton point improves by more than `0.005`, recenter and return to the axis gate. Otherwise freeze the RTK local dense candidate.

### `matched_dense_ready`

When RTK and LCDM matched local certifications are both frozen, calculate

`Delta S = S_RTK,min - S_LCDM,min`

for the same production mapping and same objective. Store the result and advance the research queue; do not silently turn raw Delta-S into model evidence.

## Recovery

A new chat/session should begin by reading `research/state/current.json`, this protocol, and the latest files in `research/iterations/`. GitHub state takes precedence over remembered chat text.
