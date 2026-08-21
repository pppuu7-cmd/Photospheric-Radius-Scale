# RTK Research Ledger

Version: 2026-08-21

Purpose: preserve research state independently from chat history.

## Rules

Every iteration records:

- Date/time UTC
- Research question
- Method
- Evidence
- Result
- Status
- Next action

## Current Frontier

| ID | Question | Method | Status |
|---|---|---|---|
| B4 | Stationarity/neutrino sector | paired RTK/LCDM analysis | OPEN |
| B6 | Primordial abundances | AlterBBN pipeline | OPEN; latest run 32285359564 cancelled |
| B9 | CMB lensing | matched lensing comparison | OPEN |
| B10 | Lambda identifiability | fixed-lambda profile + multiscale stationarity | HALF-SCALE RUNNING |

## Closed / established results

- Direct minimal U-DHOST branch ruled out.
- Several fixed-action constructions ruled out.
- Dense objective replay infrastructure established.
- B10 T3 base stationarity run 32252288173 completed successfully at preregistered factors 64 and 16384.
- B10 factor 64: lambda_D = 14045284.653674118; S_eff(center) = 1050.249062546245; exact stencil improvement = 0; Hessian positive definite; minimum eigenvalue ~= 0.046675.
- B10 factor 16384: lambda_D = 3595592871.3405743; S_eff(center) = 1050.2490169939647; exact stencil improvement = 0; Hessian positive definite; minimum eigenvalue ~= 0.046707.
- These base-stencil results do not close B10. The worker itself requires half-scale validation.

## 2026-08-21 continuation

### B10 half-scale gate

- New workflow: `.github/workflows/rtk-b10-t3-half-scale-stationarity.yml`.
- Workflow commit: `4909b91c898a64d29f4920da8c737d8593249740`.
- Trigger commit: `6dfd19e0a70fcd7d853a9454cc9de6147e3d7322`.
- Stencil scale: 0.5.
- Factors: 64 and 16384, run in parallel on GitHub-hosted Ubuntu.
- Acceptance rule: center replay within 2e-6 of frozen T2 score; no exact improvement > 0.005; Hessian remains positive definite and qualitatively consistent.
- Scientific interpretation is deferred until both artifacts are complete and inspected.

## Next Research Cycle

1. Inspect B10 half-scale artifacts; recenter or negative-mode follow-up only if required by the artifact.
2. Restart/repair B6 paired AlterBBN abundance run; do not infer BBN abundance agreement from H(T) alone.
3. Inspect/complete B9 matched lensing score.
4. Complete B4 paired neutrino robustness package.
5. Continue Formula Bible and preserve all negative results with assumptions explicit.
