# RTK B10 prior-chat audit

Iteration start: 2026-08-22 02:46:00 UTC+03:00 / 2026-08-21 23:46:00 UTC
Status: **B10 protocol v1 remains CLOSED; no missing mandatory B10-v1 gate found**

## Why this audit exists

The user explicitly requested a review of the prior research chat titled approximately `B10 gate closed lambda tail not identifiable` to check whether any useful result, caveat, or mandatory follow-up had failed to migrate into the repository.

The recovered chat conclusion was the same classification already stored in the repository:

`LAMBDA_NOT_NUMERICALLY_IDENTIFIABLE_AGAINST_PREREGISTERED_DUST_TAIL_AT_0P005`.

Recovered chat value:

`Delta_tail,best = -0.0008954358222581504`.

## Repository cross-check

Canonical protocol:

- `rtk-class-build:research/robustness/B10_LAMBDA_TAIL_IDENTIFIABILITY_PROTOCOL_v1.md`

Frozen pre-interpretation decision memo:

- `main:research/robustness/RTK_B10_HALF_SCALE_DECISION_MEMO_2026-08-21.md`

Canonical final result:

- `main:research/robustness/RTK_B10_FINAL_TAIL_IDENTIFIABILITY_RESULT_2026-08-21.md`

Current-state summary:

- `main:research/RESEARCH_LEDGER.md`

The repository contains all mandatory B10-v1 stages:

1. T1 preregistered broad fixed-shared tail reconnaissance.
2. T2 fixed-lambda 6D profiling at the mechanically selected asymptotic anchors.
3. Audit showing `profile_improvement=0` means the exact shared start remained better than the successful interior Powell endpoint, not that profiling was skipped.
4. T3 base-stencil local stationarity certification at factors 64 and 16384.
5. Independent half-scale validation at both anchors.
6. Exact finite-versus-tail comparison under the frozen `0.005` numerical-identifiability convention.
7. Scope guard excluding confidence-interval, Wilks/sigma, Bayes-factor, posterior, global-minimum, and mathematical-redundancy interpretations.

## Final numerical closure

Frozen finite point:

`S_finite = 1050.249912429787`.

Stationarity-certified tail anchors:

- factor 64: `S_tail = 1050.249062546245`, `Delta_tail = -0.0008498835418322415`;
- factor 16384: `S_tail = 1050.2490169939647`, `Delta_tail = -0.0008954358222581504`.

Both independent half-scale stencils reproduced their centers exactly, found zero exact improvement, and retained positive-definite Hessians with qualitatively aligned eigenmodes.

Therefore

`|Delta_tail,best| = 0.0008954358222581504 < 0.005`,

so B10-v1 closes mechanically as

`LAMBDA_NOT_NUMERICALLY_IDENTIFIABLE_AGAINST_PREREGISTERED_DUST_TAIL_AT_0P005`.

## Was anything mandatory left in the prior B10 chat?

**No mandatory B10-v1 step was found missing.**

In particular, the protocol does not require a farther-than-16384 tail extension after an asymptotic onset is found and both selected anchors pass T2/T3 certification. A farther-tail run would be a new preregistered study, not unfinished B10-v1 work.

Likewise, posterior sampling, profile-likelihood confidence intervals, BIC/AIC, Bayes evidence, or a global-search theorem are not unfinished B10-v1 tasks. They belong to the separate A6/post-freeze model-selection and inference program and require their own frozen protocol.

## Optional future work, explicitly outside B10-v1

If lambda identifiability becomes important for publication-level inference, a separate protocol may test one or more of:

- a continuous profile likelihood in `log lambda_D` with independently frozen bounds and sampling rule;
- posterior propriety/prior sensitivity of the long lambda tail;
- evidence/Bayes-factor sensitivity to the finite-versus-dust-like boundary;
- global/multistart optimization on an expanded matched objective.

None of these should reopen or reinterpret B10-v1 retroactively.

Classification: `RTK_B10_CHAT_AUDIT_NO_MISSING_MANDATORY_V1_GATE`.
