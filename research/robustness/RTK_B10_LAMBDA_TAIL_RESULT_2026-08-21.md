# RTK B10 lambda_D tail identifiability result

Date: 2026-08-21 15:43 UTC
Status: **CLOSED under frozen B10 protocol**
Classification: `LAMBDA_NOT_NUMERICALLY_IDENTIFIABLE_AGAINST_PREREGISTERED_DUST_TAIL_AT_0P005`

## Frozen protocol

Protocol: `rtk-class-build:research/robustness/B10_LAMBDA_TAIL_IDENTIFIABILITY_PROTOCOL_v1.md`

Frozen production objective:

`matched-ultra-linstep2+dense-BOSS`

Production mapping: `eff`.

Numerical identifiability tolerance:

`Delta S = 0.005`.

The protocol requires any asymptotic tail anchor entering the finite-vs-tail classification to pass fixed-lambda six-dimensional local stationarity and independent half-scale validation before its score may be used.

## Frozen finite solution

From the independently replay-certified production RTK local minimum:

- `lambda_D = 219457.5727136581`
- `S_finite = 1050.249912429787`.

This is a local certified score, not a global optimum claim.

## Preregistered tail anchors

T2/T3 frozen anchors:

### factor 64

- `lambda_D = 14045284.653674118`
- role: mechanical asymptotic onset
- stationarity-certified center score: `S_eff = 1050.249062546245`.

Base T3 run:

- run `32252288173`
- artifact `9369250983`
- digest `sha256:2169d82f57588d4426c13b7158ddf462da1260f07d8703ef860205c7d21d8487`
- best exact improvement: `0`
- positive definite: yes
- minimum base-scale eigenvalue: `0.046674956...`.

Independent half-scale validation:

- run `32482153752`
- artifact `9450288661`
- digest `sha256:f7f2d67b4770ab611e77f523b2ac2715f1b0c58c1aec685e9f745b454f520ef5`
- stencil scale `0.5`
- center replay exact at `1050.249062546245`
- best exact improvement: `0`
- positive definite: yes
- minimum half-scale eigenvalue: `0.02212379149449256`.

Base/half eigenvector alignment is strong: the absolute diagonal overlaps of corresponding normalized Hessian eigenvectors range from approximately `0.9063` to `0.9870` for the production mapping. All eigenvalue signs remain positive.

### factor 16384

- `lambda_D = 3595592871.3405743`
- role: largest successful preregistered tail factor
- stationarity-certified center score: `S_eff = 1050.2490169939647`.

Base T3 run:

- run `32252288173`
- artifact `9369257669`
- digest `sha256:d6932fbc24786ff4c141fad90312350c4991659a322d14d85281760d339eb63e`
- best exact improvement: `0`
- positive definite: yes
- minimum base-scale eigenvalue: `0.04670708...`.

Independent half-scale validation:

- run `32482153752`
- artifact `9450372881`
- digest `sha256:1f5e57fc7b60d9d6f87535561b1c45403632933ca674e189a5be6ee220517d08`
- stencil scale `0.5`
- center replay exact at `1050.2490169939647`
- best exact improvement: `0`
- positive definite: yes
- minimum half-scale eigenvalue: `0.02218809597516494`.

Base/half eigenvector alignment is again strong: corresponding absolute diagonal overlaps range from approximately `0.9054` to `0.9869` for the production mapping. All eigenvalue signs remain positive.

## Tail score selected by the frozen protocol

The best stationarity-certified score among the preregistered asymptotic anchors is therefore

`S_tail = 1050.2490169939647`

at factor `16384`.

Relative to the frozen finite RTK local score,

`S_tail - S_finite = -0.0008954358222581504`.

Hence

`|S_tail - S_finite| = 0.0008954358222581504 < 0.005`.

The frozen classification rule therefore gives exactly:

`LAMBDA_NOT_NUMERICALLY_IDENTIFIABLE_AGAINST_PREREGISTERED_DUST_TAIL_AT_0P005`.

The tail happens to be lower by about `8.95e-4`, but this is far below the preregistered numerical-identifiability tolerance and does not trigger the protocol's separate `tail better by >0.005` recenter/global-search branch.

The two preregistered tail anchor scores themselves differ by only

`1050.249062546245 - 1050.2490169939647 = 0.0000455522803...`

over a factor `256` change in `lambda_D`, which is consistent with the previously identified asymptotic flat tail. This is supporting diagnostic context; the formal classification comes from the frozen finite-vs-best-certified-tail rule above.

## Scientific interpretation

Within the stated frozen local objective and preregistered dust-tail class, `lambda_D` is not numerically identifiable at the `Delta S=0.005` resolution convention. The data/objective used here do not distinguish the finite local value from the tested large-`lambda_D` tail at that resolution after profiling the six shared cosmological parameters and validating local stationarity at two stencil scales.

This does **not** imply:

- that `lambda_D` is mathematically absent from the theory;
- a confidence interval or posterior statement;
- a Wilks/sigma significance;
- a Bayes factor;
- a global-minimum theorem;
- that the finite local RTK solution is invalid;
- that another dataset or observable cannot identify `lambda_D`.

B10 is closed only in the exact sense defined by its frozen protocol.

## Provenance summary

- frozen T3 target file: `rtk-class-build:research/robustness/b10_t3_fixed_lambda_stationarity_targets.json`
- base run: `32252288173`
- half-scale run: `32482153752`
- factor-64 half artifact: `9450288661`, digest `sha256:f7f2d67b4770ab611e77f523b2ac2715f1b0c58c1aec685e9f745b454f520ef5`
- factor-16384 half artifact: `9450372881`, digest `sha256:1f5e57fc7b60d9d6f87535561b1c45403632933ca674e189a5be6ee220517d08`
- half-scale workflow head SHA: `6dfd19e0a70fcd7d853a9454cc9de6147e3d7322`.
