# B10 finite-lambda_D versus dust-tail identifiability protocol v1

Status: **FROZEN BEFORE THE NEW BROAD TAIL RECONNAISSANCE RUN**.

This is a post-A5 robustness/identifiability study. It does not alter the frozen massless matched minimum, does not replace Stage4D3, and does not claim a global minimum.

## Question

Stage4D3 established a local interior RTK minimum at finite `lambda_D≈2.1946e5`. Earlier broad fixed/shared scans showed weak lambda sensitivity. B10 asks the distinct question: after profiling the other six cosmological parameters, is the finite-lambda solution measurably separated from the large-lambda dust-like tail, or is lambda effectively non-identifiable against that boundary on the frozen objective?

## Frozen common objective

- objective: `matched-ultra-linstep2+dense-BOSS`
- production mapping: `eff`; record `k01` separately
- exact-float success-only likelihood
- locked massless neutrino baseline
- same pinned CLASS/Pantheon/Planck/runtime environment as A1-A5
- comparison tolerance for a raw local/tail objective difference: `0.005`; this tolerance is an identifiability/numerical-resolution convention only, not a confidence-level threshold.

## T1: fixed-shared-parameter tail reconnaissance

Hold the six non-lambda parameters at the frozen RTK accepted-score parameter point and evaluate the exact objective at

`lambda_D = lambda_* × f`

for fixed factors

`f = [1/256, 1/64, 1/16, 1/4, 1, 4, 16, 64, 256, 1024, 4096, 16384]`,

where `lambda_*` is the frozen finite accepted value. No factor may be added/removed after inspecting scores in T1.

Record Planck, Pantheon, BOSS-eff, BOSS-k01, total eff/k01, sound horizon, and exact success/failure for every point. No interpolation may turn a failed point into a score.

T1 is diagnostic only. It may establish a numerically flat/asymptotic large-lambda region, but it cannot determine profiled identifiability because the six shared parameters are fixed.

## T2: adaptive-but-preregistered 6D profile anchors

After T1, select tail anchors mechanically:

1. Always include `f=1` (the finite accepted lambda).
2. Among the T1 factors `f>=64`, identify the earliest factor `f_tail` such that it and every larger successful T1 point differ from the largest-factor T1 `S_eff` by at most `0.002`.
3. If such `f_tail` exists, profile the six shared cosmological parameters independently at `f_tail` and at the largest successful factor `16384` (or, if some factors fail, the largest successful preregistered factor). Do not optimize lambda inside either profile.
4. If no such T1 asymptotic onset exists, B10 remains open and a new farther-tail extension must be preregistered before seeing additional results.

Each fixed-lambda 6D profile starts both from the frozen RTK shared parameter point and from the nearest successful T1/previous-profile shared point when available; the better exact converged result is retained. Bounds and optimizer tolerances must be frozen before T2 execution and recorded in its target file.

## T3: local stationarity at tail-profile anchors

Any T2 anchor used for the final finite-vs-tail statement must receive a recenter-clear shared-parameter coordinate poll/Hessian appropriate to the 6D fixed-lambda subspace. A raw optimizer endpoint alone is not sufficient.

## Classification

Let `S_finite` be the already frozen local RTK score and `S_tail` the best stationarity-certified profiled score among the preregistered asymptotic tail anchors.

- if `S_tail - S_finite > 0.005`: classify `FINITE_LAMBDA_LOCALLY_IDENTIFIABLE_AGAINST_PREREGISTERED_DUST_TAIL`;
- if `|S_tail - S_finite| <= 0.005`: classify `LAMBDA_NOT_NUMERICALLY_IDENTIFIABLE_AGAINST_PREREGISTERED_DUST_TAIL_AT_0P005`;
- if `S_tail < S_finite - 0.005`: the frozen finite local solution is not the best point found in the tested tail class; this forces a separate recenter/global-search robustness investigation but does **not** retroactively invalidate the correctness of A3 as a local-minimum statement.

No Bayes factor, confidence interval, sigma/Wilks statement, or global-minimum theorem follows from B10.
