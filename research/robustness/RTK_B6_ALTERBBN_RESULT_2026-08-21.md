# RTK B6 paired AlterBBN result

Date: 2026-08-21
Status: **B6 DIFFERENTIAL ABUNDANCE ROBUSTNESS CLOSED**

## Provenance

- GitHub Actions run: `32285359564`, attempt 2
- Workflow: `.github/workflows/rtk-b6-alterbbn-paired-abundances.yml`
- Artifact: `rtk-b6-paired-alterbbn-abundances`, artifact id `9447623417`
- Artifact digest: `sha256:d8cae8fbd36b886219b611603ef90852dff18251f93e020b0ab87c393e012287`
- Source head recorded by artifact: `86ef96187cecf7b0b03d8ad1416d8ae758b8f6ec`
- AlterBBN v2.2 archive SHA256: `2bcb7d2e3f4a74f59cd589e60f0923892bb90296a793f80016897405920c5fae`
- Frozen eta: `6.122532926262666e-10`
- Paired scientific difference: only the injected `R_H(T)` table differs between reference and RTK trees.

The execution classification in the artifact is `RTK_B6_ALTERBBN_PAIRED_ABUNDANCE_EXECUTION_PASS`. All source/artifact locks, three builds, six network runs and full-precision parsing passed.

## Expansion-history perturbation

Across the injected BBN temperature range the RTK mapping has

`max |R_H - 1| = 2.422446243599552e-09`.

The refined table has 512 points and the nominal table has 256 points. The mapping refinement and source-lock requirements passed before abundance interpretation.

## Paired abundance shifts

Primary shifts below are refined-table, failsafe=1, `RTK-reference`.

| Observable | primary shift | numerical classification | conservative absolute bound |
|---|---:|---|---:|
| `Yp` | `+1.4314660568004456e-12` | resolved | `1.5052958879380185e-12` |
| `D/H` | `+1.6226982865047423e-15` | below numerical resolution | `4.560750648668899e-15` |
| `He3/H` | `+1.8563065852256894e-16` | below numerical resolution | `9.671794886246393e-16` |
| `Li7/H` | `-3.1757428269865546e-20` | below numerical resolution | `7.745760614977179e-20` |
| `Li6/H` | `+7.1749581456928775e-25` | below numerical resolution | `1.9053783428691917e-24` |
| `Be7/H` | `-3.3431331636943167e-20` | below numerical resolution | `7.433024304886193e-20` |

The protocol defines a shift as resolved only when its magnitude exceeds five times the larger of table-refinement and solver-mode sensitivity. Therefore unresolved shifts are not called exact zero; their conservative bounds above are retained.

## Frozen observational diagnostic

Frozen observations used before output:

- `Yp = 0.2458 +/- 0.0013`;
- `D/H = (2.533 +/- 0.024)e-5`.

Failsafe=1 values:

Reference:

- `Yp = 0.2473246530992457` -> `z = +1.1728100763428537`;
- `D/H = 2.4200608021640088e-05` -> `z = -4.705799909832967`.

RTK refined:

- `Yp = 0.24732465310067717` -> `z = +1.1728100774439814`;
- `D/H = 2.4200608023262786e-05` -> `z = -4.705799903071724`.

Thus the RTK-induced change in the standardized residual is only about

- `+1.10e-9 sigma` for `Yp`;
- `+6.76e-9 sigma` for `D/H`.

The conservative paired-shift bounds correspond to only about

- `1.16e-9` of the frozen `Yp` observational sigma;
- `1.90e-8` of the frozen `D/H` observational sigma.

## Scientific interpretation

**B6 differential robustness closes positively:** at the preregistered massless A1-A5 RTK point, the RTK modification of `H(T)` changes AlterBBN abundances by an observationally negligible amount under the frozen paired protocol.

This means the tiny RTK-vs-reference expansion-history difference does not generate a new BBN abundance tension at this gate.

It does **not** mean that the absolute BBN fit is certified. In particular, the frozen reference calculation itself lies about `-4.706 sigma` from the selected D/H central value when only the quoted observational sigma is used. The paired B6 gate was designed to isolate the RTK differential effect; it does not absorb nuclear-rate theory uncertainty or refit eta.

No claim is made about solving the lithium problem, global model selection, or a full BBN likelihood.

## Closure rule

The preregistered scientific-closure requirements are satisfied:

1. source/artifact provenance is pinned;
2. paired network execution is complete;
3. table and solver sensitivity are quantified;
4. every abundance has either a stable resolved shift or a conservative upper bound;
5. the frozen Yp and D/H observational residuals are explicitly reported.

Classification: `RTK_B6_DIFFERENTIAL_ABUNDANCE_ROBUSTNESS_CLOSED`.
