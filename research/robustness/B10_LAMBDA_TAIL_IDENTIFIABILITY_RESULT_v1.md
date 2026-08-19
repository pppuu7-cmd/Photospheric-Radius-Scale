# B10 lambda-tail identifiability result v1

Status: **CLOSED** under the frozen B10-v1 numerical-identifiability protocol.

## Result

Classification: **`LAMBDA_NOT_NUMERICALLY_IDENTIFIABLE_AGAINST_PREREGISTERED_DUST_TAIL_AT_0P005`**.

The frozen finite RTK A5 reference has `lambda_D = 219457.5727136581` and `S_eff = 1050.249912429787`. T1 preregistered the outer-tail anchors at factors 64 and 16384. T2 profiled the six shared cosmological parameters at both fixed lambda values and found no exact profile improvement from the frozen shared point. T3 run `32252288173` then certified the two profiled tail anchors with recenter-clear base stencils and positive-definite 6D Hessians.

| anchor | lambda_D | S_eff | best improvement | min Hessian eigenvalue | finite-tail delta |
|---|---:|---:|---:|---:|---:|
| factor 64 | 14045284.653674118 | 1050.249062546245 | 0 | 0.046674959619984545 | -0.0008498835418322415 |
| factor 16384 | 3595592871.3405743 | 1050.2490169939647 | 0 | 0.0467070781427316 | -0.0008954358222581504 |

The two outer-tail scores differ by only `-4.5552280425908975e-05`, and both differ from the finite reference by much less than the preregistered `0.005` numerical-identifiability threshold. Therefore B10-v1 cannot numerically distinguish the finite local point from the preregistered asymptotic tail at this score resolution.

## Provenance

- T1 reconnaissance run: `32240381293`.
- T2 paired fixed-lambda profiles: `32244330691`.
- T3 stationarity run: `32252288173`, created `2026-08-19T12:22:06Z`, completed `2026-08-19T14:22:46Z`.
- T3 factor-64 artifact: `9369250983`.
- T3 factor-16384 artifact: `9369257669`.
- Objective remains `matched-ultra-linstep2+dense-BOSS`, production mapping `eff`.

## Scope

This is a local numerical-identifiability result only. It does **not** prove mathematical redundancy of `lambda_D`, an exact dust limit of the complete theory, a global optimum, or model preference/significance/AIC/BIC/Bayes evidence. It does not alter or replace the frozen A1-A5 massless comparison.
