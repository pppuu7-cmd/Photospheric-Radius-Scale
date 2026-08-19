# B6 paired AlterBBN abundance robustness result v1

**Classification: `B6_ALTERBBN_ABUNDANCE_ROBUSTNESS_PASS`.**

This closes the B6 abundance robustness gate for the accepted massless A1–A5 RTK point under the frozen `RTK_BBN_ABUNDANCE_EXECUTION_PROTOCOL_v1.md`. It does not mutate the production likelihood and is not a global model-selection statement.

## Reproducibility chain

- Extended entropy-aware H(T) coverage: run `32284769820`, artifact `9377196879`, `B6_EXTENDED_HT_MAPPING_COVERAGE_PASS`, max `|R_H-1| = 2.422446243599552e-9`.
- Initial abundance run `32285359564` was stopped only by its 45-minute workflow timeout after five of six valid networks.
- Exact continuation run `32290608424` reused those five preserved networks, reproduced the missing refined build from the identical source/mapping/manifest/compiler semantics, matched the prior refined binary SHA256 `4470fa1cdd36dd03b1f319a9b7482eebfa9106277b6848388c2fc33fbbe24b45`, ran only the missing refined failsafe-7 network, then aggregated all six.
- Final artifact: `9380003379`, digest `sha256:3961ff52803574d3389111dc93fc5dcf843c463a54968f4d75c7e0c909ac6dca`.

## Paired result

The primary comparison is refined-table failsafe=1, `delta = RTK - reference`.

| Abundance | Primary delta | Frozen numerical classification |
|---|---:|---|
| `Yp` | `+1.4314660568004456e-12` | `ABUNDANCE_SHIFT_RESOLVED` |
| `D/H` | `+1.6226982865047423e-15` | `ABUNDANCE_SHIFT_BELOW_NUMERICAL_RESOLUTION` |
| `He3/H` | `+1.8563065852256894e-16` | `ABUNDANCE_SHIFT_BELOW_NUMERICAL_RESOLUTION` |
| `Li7/H` | `-3.1757428269865546e-20` | `ABUNDANCE_SHIFT_BELOW_NUMERICAL_RESOLUTION` |
| `Li6/H` | `+7.1749581456928775e-25` | `ABUNDANCE_SHIFT_BELOW_NUMERICAL_RESOLUTION` |
| `Be7/H` | `-3.3431331636943167e-20` | `ABUNDANCE_SHIFT_BELOW_NUMERICAL_RESOLUTION` |

The resolved helium shift is nevertheless physically tiny: about `1.10e-9` of the frozen observational sigma `0.0013`. The conservative D/H shift bound is `4.560750648668899e-15`, about `1.90e-8` of the frozen observational sigma `2.4e-7`.

## Frozen observational diagnostic

For `Yp = 0.2458 +/- 0.0013`, reference and RTK-refined failsafe=1 give standardized residuals `+1.1728100763` and `+1.1728100774` respectively.

For `(D/H)_p = (2.533 +/- 0.024)e-5`, reference and RTK-refined give `-4.7057999098` and `-4.7057999031`. The large observational-only D/H residual is therefore already present in the reference AlterBBN-v2.2 network; RTK changes it only at the eighth decimal place in sigma units. Per the frozen protocol this diagnostic does **not** silently include nuclear-rate theory uncertainty, so it must not be promoted into a full BBN exclusion claim.

## Scientific conclusion

At the tested accepted massless RTK point, the entropy-aware RTK modification of the BBN expansion history is abundance-negligible. B6 is therefore closed as a pointwise BBN robustness test. This is not a lithium-problem statement, not a modern nuclear-rate uncertainty analysis, and not a proof for parameter space away from the tested RTK point.
