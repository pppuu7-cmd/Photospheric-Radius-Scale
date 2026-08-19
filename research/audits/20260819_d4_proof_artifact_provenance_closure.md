# D4 proof-artifact identity/provenance closure audit

Date: 2026-08-19

Classification: **D4_PROOF_ARTIFACT_IDENTITY_PROVENANCE_CLOSED**.

This audit concerns reproducibility/control-plane identity only. It does not strengthen the scientific claim beyond the already frozen local matched-comparison scope.

## RTK proof families

The autonomous identity validator now fail-closes completed unparsed RTK proof artifacts on:

- exact objective name;
- exact current accepted center;
- declared Hessian/eigenray scale when applicable;
- canonical objective fingerprint;
- canonical model/center/objective/mapping fingerprint;
- locked CLASS commit;
- locked Pantheon commit;
- locked NumPy version;
- Python / NumPy / SciPy / clipy-like / Planck SHA sidecars when present.

The proof-key set includes base, half, quarter, eighth Hessians and base, half, quarter, eighth exact negative-eigenray artifacts. The terminal `1/8` family is therefore covered by the same locked validation as the earlier proof scales.

## ΛCDM historical-proof replay

The frozen historical ΛCDM Hessian in state remains run `31990397363`. Because that artifact predates the later generalized proof-artifact validator, a fresh audit-only locked replay was executed without changing frozen A1-A5 state.

Fresh audit run: `32195153149`

Artifact: `9347663131`

Artifact digest: `sha256:6889e445c825ea41206d962ddf115676e50fe0e907f17f8879a96c6b6fb7097f`

Classification: `LCDM_LOCKED_STATIONARITY_PROVENANCE_AUDIT_PASS`

Results:

- `best_exact_S = 1049.966118347761`
- frozen accepted score `= 1049.966118347761`
- absolute score error `= 0.0`
- `best_improvement = 0.002496099298923582 <= 0.005`
- Hessian positive definite
- eigenvalues exactly reproduced in the recorded doubles:
  `[0.01076000540446865, 0.05095906682522973, 0.058585744253312616, 0.24761409818154007, 2.9769326338378908, 7.054039686019683]`
- CLASS `36cf283628c4a3330ec9fd3d84239bf775f77317`
- Pantheon `7eb29dc87ba223b4ec8457cd3cccba1216c36fb7`
- NumPy `2.5.2`
- canonical objective and LCDM-center fingerprints matched.

## Model-aware future validation

`rtk/validate_artifact_identity.py` was generalized so future ΛCDM `hessian_run` artifacts receive the same locked provenance treatment as RTK proof artifacts, with model-specific canonical center fingerprints.

A no-network regression verifies:

1. correct RTK proof provenance passes;
2. correct ΛCDM proof provenance passes;
3. a forged ΛCDM center fingerprint is rejected;
4. ΛCDM `hessian_run` remains in the locked proof-key set.

Regression run: `32236809766` — success.

All steps passed: source compilation, global scientific static invariants, and RTK/LCDM locked-provenance unit test.

## Closure statement

D4 is closed at the repository's declared proof-artifact scope: all active local stationarity/eigenray proof families are either directly locked by the validator or, for the frozen historical ΛCDM artifact, independently replayed under the current locked environment with zero score discrepancy. Future RTK and ΛCDM proof artifacts are model-aware and fail-closed on provenance.

This is not an independent external replication and does not imply a global cosmological minimum.
