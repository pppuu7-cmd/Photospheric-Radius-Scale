# RTK dense dust-boundary screening checkpoint v1

This checkpoint records the completed matched-ultra (`l_linstep=2`) + dense-BOSS fixed-lambda nuisance screening. It is a screening result, not a proof of a global minimum or a model-comparison statistic.

## Provenance

- Workflow: `RTK dense-objective dust-boundary nuisance poll`
- Run: `31981673256` — **PASS**
- Objective: matched-ultra `l_linstep=2` + dense BOSS
- Cache: exact-float normalized parameter keys
- Physical boundary coordinate: `u = 1/lambda_D`; dust boundary is `u=0`
- Nuisance center at every lambda:
  - h = 0.6904831253428524
  - Ob = 0.046836300417955265
  - Om = 0.25300743080221694
  - As = 2.0837288833768707e-9
  - ns = 0.9643603115669437
  - zre = 7.21843542110055

## Screening results

At each fixed lambda_D, 13 exact points were evaluated: the nuisance center and symmetric one-axis offsets in the six nuisance coordinates. The center remained the best tested nuisance point for both `eff` and `k01` at every lambda listed below.

| lambda_D | u=1/lambda_D | best S_eff | best S_k01 | Delta S_eff vs lambda=217225.016 |
|---:|---:|---:|---:|---:|
| 217225.01601516694 | 4.603520e-6 | 1050.4252325721458 | 1050.4396142594750 | 0 |
| 300000 | 3.333333e-6 | 1050.4255666105184 | 1050.4257901460376 | +0.0003340383726 |
| 1000000 | 1.000000e-6 | 1050.4246836819493 | 1050.4248934274240 | -0.0005488901965 |
| 10000000 | 1.000000e-7 | 1050.4245708650 | not copied into this checkpoint | approximately -0.0006617071 |
| 100000000 | 1.000000e-8 | 1050.4246128170641 | 1050.4248211658548 | -0.0006197550817 |
| 1000000000 | 1.000000e-9 | 1050.4246650299430 | 1050.4248733776976 | -0.0005675422028 |

The shallow best sampled `S_eff` is near lambda_D ~ 1e7, but its advantage over the finite Round5 lambda is only about 6.6e-4. This is far below the established recenter/improvement gate 0.005 and is comparable to the scale on which numerical precision systematics must still be controlled.

## Interpretation

1. No tested fixed-lambda nuisance axis point improves on its corresponding nuisance center.
2. The matched dense objective becomes very flat in lambda_D for lambda_D >= O(1e6).
3. The screening does **not** establish a finite-lambda interior minimum.
4. The screening does **not** establish the dust boundary u=0 as the minimum.
5. A simple statement that "larger lambda is better" is false for the sampled points: S_eff decreases toward ~1e7 and then rises slightly by 1e8 and 1e9, but the total excursion is < 0.001.
6. Because the excursion is much smaller than the 0.005 scientific gate, the next valid step is a refined log-lambda/u profile plus a numerical-floor/precision audit at representative points before spending compute on a full new 7D Hessian.

## Decision rule

- Do **not** recenter from this screening.
- Do **not** claim finite-lambda preference or dust-boundary preference.
- Refine lambda_D around the broad plateau and measure reproducibility / precision dependence of Delta S.
- Only if a robust improvement exceeding the numerical floor and the scientific gate appears should a new dense 7D stationarity calculation be centered there.
