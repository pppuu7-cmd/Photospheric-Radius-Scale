# RT+DBI-Khronon — Stage 4D1 progress

## Scope

Stage 4D1 profiles the exact objective

`S = -2 ln L_Planck + chi2_Pantheon + chi2_BOSS`

at fixed `lambda_D`, reoptimizing the remaining six cosmological parameters. Two BOSS/RSD mappings are retained: `eff` and `k01`. All results below are local profile candidates, not a global posterior, confidence interval, significance, or Bayesian evidence.

Reference stationarity-checked local LCDM candidates:

- `S_LCDM,eff = 1050.17772999`
- `S_LCDM,k01 = 1050.15993541`

## Completed 14-point raw profile

Workflow `31856275702` completed all seven lambda values for both mappings. The corrected aggregate workflow `31898432252` succeeded after exact artifact-directory validation was fixed.

### eff raw profile

| lambda_D | raw S_eff |
|---:|---:|
| 1e3 | 1054.57485623 |
| 3e3 | 1052.05582877 |
| 1e4 | 1051.79468469 |
| 3e4 | 1051.60923103 |
| 1e5 | 1051.53717674 |
| 1e6 | 1051.55985695 |
| 1e8 | 1051.32449549 |

### k01 raw profile

| lambda_D | raw S_k01 |
|---:|---:|
| 1e3 | 1052.99098948 |
| 3e3 | 1052.01395410 |
| 1e4 | 1051.78242627 |
| 3e4 | 1051.72035633 |
| 1e5 | 1051.60600015 |
| 1e6 | 1051.51907405 |
| 1e8 | 1051.24650973 |

At raw Stage-4D1 optimizer accuracy both mappings look approximately monotonic toward large lambda. This raw conclusion is **not** reliable at the sub-unit level because tighter searches have already found a substantially deeper finite-lambda basin.

## Tight eff refinement

A dedicated five-start tight Powell search with smaller trust boxes and two exact coordinate-poll radii completed for `lambda_D=3e4` and `1e5`.

### lambda_D = 30000

- `S_eff = 1051.0755927897148`
- `S_k01` evaluated at the same point = `1051.0835197820677`
- `h = 0.6905802910391277`
- `Omega_b = 0.04684163640622535`
- `Omega_K0 = 0.2529201285589534`
- `A_s = 2.0630563560740213e-9`
- `n_s = 0.9640474757333444`
- `z_reio = 6.6839724497605335`
- `r_d = 146.965498 Mpc`
- no parameter-box boundary hit
- exact likelihood calls = `626`
- post-optimizer exact poll improvement = `0.0705213`

Relative to the stable local LCDM eff candidate,

`Delta S_eff(3e4) = +0.89786280`.

The sizeable post-optimizer poll improvement means this point is not yet accepted as stationary.

### lambda_D = 100000

- `S_eff = 1051.1778474864889`
- `S_k01` at the same point = `1051.1887989863240`
- `h = 0.6901873895028806`
- `Omega_b = 0.04688758336412194`
- `Omega_K0 = 0.253421603515163`
- `A_s = 2.062306350250812e-9`
- `n_s = 0.9638955372522343`
- `z_reio = 6.647719070471404`
- `r_d = 146.943558 Mpc`
- no parameter-box boundary hit
- exact likelihood calls = `563`
- post-optimizer poll improvement = `0.0006143`

Relative to the stable local LCDM eff candidate,

`Delta S_eff(1e5) = +1.00011750`.

## Consequence for the raw large-lambda interpretation

The raw `lambda_D=1e8` points are

- `S_eff = 1051.32449549`
- `S_k01 = 1051.24650973`.

The tight `lambda_D=3e4` point is already lower than both raw high-lambda objectives, even before a mapping-specific `k01` tight optimization. Therefore it is currently invalid to conclude from the raw 14-point curve that the likelihood prefers the dust boundary. Finite-lambda and asymptotic points must be optimized to the **same numerical depth** before the lambda profile can be classified.

## Validation now running

1. Exact 73-point stationarity/Hessian test at the tight `eff, lambda_D=3e4` center: workflow `31898477269`.
2. Exact 73-point stationarity/Hessian test at the tight `eff, lambda_D=1e5` center: workflow `31898491296`.
3. Symmetric tight refinement workflow `31898624907` for:
   - `eff, lambda_D=1e8`,
   - `k01, lambda_D=1e8`,
   - `k01, lambda_D=3e4`,
   - `k01, lambda_D=1e5`.

These checks are designed to determine whether the finite-lambda dip survives equal-depth optimization and whether it is present in both RSD mappings.

## Large-lambda analytic coordinate

For fixed positive `A=Omega_K0/(6 gamma)` and `delta_D=1/lambda_D`, the exact normalized Khronon density has no `O(lambda_D^-1/2)` correction:

`x(1+t) = A/a^3 - (a^3-1)/a^3 * lambda_D^-1 + O(lambda_D^-3/2)`.

Thus the leading background departure from dust is naturally linear in `delta_D=1/lambda_D`, while `c_a^2 ~ lambda_D^-3/2` and `k_* ~ lambda_D^3/4`.

If the equal-depth numerical profile ultimately minimizes at `delta_D=0`, boundary-aware inference is required. If a stable interior finite-lambda minimum survives, an interior profile/posterior analysis becomes appropriate. In neither case should nominal Delta-S crossings be called confidence limits before numerical stationarity and statistical calibration are established.

## Immediate next decision

Do not launch production MCMC yet. First obtain equal-depth, stationarity-checked fixed-lambda minima for the finite basin and the large-lambda tail. Only then construct the refined profile in `delta_D=1/lambda_D` and decide whether the next stage is an interior finite-lambda posterior or a boundary-aware lower bound on `lambda_D`.
