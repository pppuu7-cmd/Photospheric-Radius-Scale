# RTK cross-chat frontier reconciliation — 2026-08-19

Purpose: preserve scientifically useful items recovered while reconciling parallel/older RTK research chats with the current repository. The repository state and frozen protocols remain authoritative; historical candidates are not revived as current results.

## Recovered items that remain active

1. **B9 — standalone Planck lensing robustness.** Earlier queues explicitly retained Planck lensing as a post-freeze robustness test. The current master matrix now has B9. Interface run `32243756716` passed with pinned Planck R3.00 and `clipy-like==0.15`; the fixed non-CMB-marginalized SMICA product is recorded in `B9_PLANCK_LENSING_ROBUSTNESS_PROTOCOL_v1.md`. No cosmological B9 lensing score existed before that protocol was frozen.

2. **B10 — finite-lambda versus dust-tail identifiability.** Historical broad lambda scans showed weak sensitivity but were not global/profile proofs. A3 remains only a local interior-minimum statement. T1 run `32240381293` now extends the exact fixed-shared tail from `lambda_*/256` to `16384 lambda_*`; protocol mechanically selects `f_tail=64`. T2 targets `64` and `16384` were frozen before profile execution. This is distinct from and cannot retroactively weaken the correctness of A3 as a local result.

3. **B8 — local/nonlinear gravity.** A recovered necessary-condition result says the implemented *linear static* RTK closure provides Newton/Yukawa-type kernels and cannot by itself generate asymptotic `Phi ~ log r` required for flat rotation curves. This is not a nonlinear isolated-system, Solar-System, screening, or compact-object theorem; B8 therefore remains open.

4. **C7 — full coupled DOF/ghost theorem.** Route-B subgates are useful and retained: simple standard potential-only khronometric mappings do not reproduce the target rational dispersion; constant-coefficient acceleration/DHOST-type degeneracy constrains simple completions; a constructive spatially-covariant metric+Khronon benchmark can reproduce the target dispersion with three generic physical DOF. None of these substitutes for the still-open full coupled metric + causal RT + Khronon constraint/DOF theorem.

5. **B6 — early universe / BBN.** Earlier high-z background work found RTK/same-parameter LCDM expansion differences tending rapidly to zero, reaching order `1e-12` by very high redshift. This remains background evidence only. Since then the repository has advanced to pinned AlterBBN v2.2 source/self-test, source-flow audits, and entropy-aware `H(T)` mapping. Run `32243547025` passed with `max |H_RTK/H_LCDM-1| = 2.1702035724047164e-9` over the mapped BBN range and nominal/refined mapping disagreement `1.730393606180769e-12`. Abundance injection and observational comparison remain required.

6. **Massive neutrinos / DESI-full-RSD / evidence.** The old queue items remain represented by current gates: B4 is the separate 0.06-eV paired reoptimization/stationarity branch; B5 carries survey-window/nonlinear-RSD robustness; A6 keeps BIC/Bayes/evidence separate from the frozen raw fit and closed AIC subgate.

## Historical results explicitly superseded

- Old finite-lambda candidate centers near tens/hundreds of thousands are historical search points only. The frozen massless A3/A5 center and score remain authoritative.
- Sparse-BOSS scores are not comparable to the frozen dense objective and must never be mixed into the final matched delta.
- Early high-z `H(z)` convergence is not an abundance-level BBN proof.
- Fixed-shared lambda scans are not profiled identifiability tests.
- Reduced scalar/local EFT ghost checks are not the full causal RT+Khronon coupled DOF theorem.

## Current high-priority active frontier at checkpoint

- **B4:** paired minimal-neutrino base Hessians run `32236524767` active; no duplicate dispatch.
- **B6:** entropy-aware H(T) mapping run `32243547025` passed; next gate is paired AlterBBN R=1 versus RTK R(T) abundance/refinement calculation followed by preregistered observational comparison.
- **B9:** interface run `32243756716` passed; protocol frozen before first cosmological standalone-lensing score; next gate is adapter contract and paired matched reoptimization/stationarity/replay.
- **B10:** T1 run `32240381293` passed; T2 fixed-lambda 6D anchors 64 and 16384 frozen and dispatched; T3 stationarity remains mandatory before classification.

This checkpoint is a reconciliation record, not a new physical claim and not an override of `research/RTK_MASTER_RESEARCH_CLOSURE_MATRIX.md` or `research/state/current.json`.
