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
| B4 | Stationarity/neutrino sector | paired RTK/LCDM analysis | RAY-RECENTER BASE REPLAY LAUNCHED |
| B6 | Primordial abundances | AlterBBN pipeline | RERUN ATTEMPT 2 RUNNING |
| B9 | CMB lensing | matched lensing comparison | FIXED-CENTER ADAPTER PASS; MATCHED REOPTIMIZATION OPEN |
| B10 | Lambda identifiability | fixed-lambda profile + multiscale stationarity | HALF-SCALE RUNNING |
| C8 | Exact UV/IR interpolation | FLRW lapse+shift Schur-complement matching | ALGEBRAIC FILTER ADDED; ACTION MAP OPEN |
| INFRA-HOME3 | Distributed heavy compute | self-hosted Linux/X64 runner + process pool + persistent checkpoint | ENGINE V2 MIGRATED; BOOTSTRAP HANDSHAKE NEXT |

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

### B6 paired AlterBBN abundance gate

- Run 32285359564 attempt 1 was cancelled externally during the long `stand_cosmo.x` abundance-network step.
- Before cancellation, the frozen extended H(T) input lock passed; mapping artifact hashes passed; pinned AlterBBN v2.2 source passed; identical reference/RTK patching passed; all three binary trees built successfully.
- No abundance conclusion may be drawn from the cancelled attempt.
- Exact job rerun requested on 2026-08-21.
- Attempt 2 is currently in progress. Steps 1-7 have passed and step 8, `Run failsafe 1 and 7 for all paired trees`, is executing. No abundance inference is allowed until the artifact is parsed.

### B9 fixed-center Planck lensing diagnostic

- Run 32285180694 completed successfully.
- Contract classification: `B9_FIXED_CENTER_LENSING_ADAPTER_CONTRACT_PASS`.
- LCDM standalone lensing: -2 ln L = 9.054925581629908.
- RTK standalone lensing: -2 ln L = 9.039267332621456.
- Fixed-center lensing delta (RTK-LCDM) = -0.015658249008452, i.e. a very small diagnostic improvement for RTK in this standalone contribution.
- This is not a matched reoptimized objective, local-minimum comparison, significance, AIC/BIC result, or Bayes factor. B9 remains open.

### B4 neutrino negative-mode recenter gate

- Parent negative-mode ray run 32284932113 completed successfully but falsified stationarity of its parent RTK center.
- Objective: `matched-ultra-linstep2+dense-BOSS+nu0p06-additive-v1`; do not compare its absolute scores directly with the massless frozen objective.
- Parent center S_eff = 1050.6979573843187.
- Strongest exact negative-mode ray: mode 0, alpha = +2.0, S_eff = 1050.5880475140204, improvement = 0.10990987029822463 > 0.005 recenter tolerance.
- Frozen recenter winner parameters: As=2.0920212896820786e-9, Ob=0.04722200104991654, Om=0.2528393318824633, h=0.6885660022475836, lambda_D=3043326.1774413693, ns=0.9657332769496741, zre=7.506210209218662.
- Therefore the mandatory next gate is an exact RTK ray-recenter base Hessian at that winner.
- Existing frozen target: `research/robustness/b4_neutrino_rtk_ray_recenter_target_v2.json`, target commit `3b9acfb25a01c6107a4a8427ef2b51ae61017d20`.
- A fresh replay was launched on 2026-08-21 by trigger commit `c71058fe5cb21e033e73b6966baca99686ffd851` because the prior launch result was not represented as a closed result in live state.

### C8 FLRW Schur-complement gate

- Existing FLRW constraint-kernel work shows that a fixed-Minkowski obstruction cannot automatically be promoted to FLRW because background quantities such as H can enter the constraint kernel and move a pole with epoch even for fixed Wilson coefficients.
- The next exact algebraic object is the full nondynamical lapse+shift matrix M=[[A,C],[C,B]] with mixing J=(P,R).
- Eliminating the constraints gives K_eff = K0 - (B P^2 - 2 C P R + A R^2)/(A B - C^2).
- For A=a0+a1 q, B=b0+b1 q, C=c0+c1 q, the determinant has D2=a1 b1-c1^2 as the q^2 coefficient. A strict one-linear-pole target therefore requires the necessary algebraic condition D2=0.
- This is not, by itself, a DHOST degeneracy theorem and not a UV completion claim. Pole matching must be followed by residue matching, stability, DOF, cutoff, PPN and GW gates for the same fixed action.
- Added exact-rational diagnostic module on `rtk-class-build`: `rtk/route_b_flrw_schur_kernel.py`, commit `175adcc14bdfcdfc83218055dcbe4b0096545980`.
- Added protocol: `research/RTK_C8_FLRW_SCHUR_MATCHING_PROTOCOL_2026-08-21.md`, commit `b6b9b4f0c2829b7732a4a658d37bbbe7dcd1a1a4`.
- Added GitHub Actions self-test workflow commit `0a21da3359e211b113f58aa0945d5b06b1b21796`; launched by trigger commit `5d2417ed179f63fc25c9e6cbdbb0e47deef9b841`.

### Home compute architecture migration

- Recovered configured node contract: runner `RTK-HOME-PC`, Linux/X64, custom label `rtk-home3`, current node 10 logical CPUs.
- Legacy home workflows used `rtk-home`; routes were migrated to `rtk-home3`.
- Home benchmark was changed from automatic `push` execution to deliberate manual dispatch.
- Heavy home workflows now share `concurrency: rtk-home3-exclusive`; only one heavyweight job occupies the PC while that job may use the full process pool internally.
- Engine v2 supports `RTK_WORKERS=auto` and `RTK_RESERVE_CPUS`; maximum-throughput mode uses all available logical CPUs, while an 8-worker/2-reserved mode remains available.
- Process-parallel workflows set OMP/OpenBLAS/MKL/NumExpr inner threads to 1 to prevent nested oversubscription.
- Checkpoint state moved out of checkout to `$HOME/.rtk-runner-state/<run_key>/checkpoint.json` with atomic writes, schema/fingerprint checks and `next_index` resume semantics.
- Engine now handles SIGINT/SIGTERM by committing the last contiguous completed prefix and exposes percent/rate/ETA/status via persistent `progress.json` and `live.log`.
- Added Ubuntu console wrapper `scripts/rtk_home_runner_console.sh`; bootstrap will install it as `$HOME/.local/bin/rtk-runner-start`.
- Canonical architecture: `docs/RTK_COMPUTE_ARCHITECTURE.md`.
- Canonical chronology created: `research/RTK_MODEL_CHRONOLOGY.md`.
- Formula Bible expanded with C8 Schur derivation and mandatory formula-provenance rules.
- Scientific result status is unchanged by the infrastructure migration; placeholder engine workloads are infrastructure tests only.

## Next Research Cycle

1. Inspect B10 half-scale artifacts; if both pass, quantify tail flatness and decide the next lambda-identifiability claim conservatively.
2. Inspect B6 rerun abundance outputs; only then discuss Y_p, D/H, Li or observational compatibility.
3. Inspect the fresh B4 ray-recenter base artifact; if improvement >0.005 recenter again, if Hessian is indefinite run exact negative-mode rays, otherwise run half-scale validation.
4. Validate the C8 Schur self-test artifact, then map A,B,C,P,R,K0 from one explicit candidate fixed action; do not fit these coefficients independently by epoch.
5. Freeze a matched B9 lensing reoptimization protocol before using lensing in any model-comparison statement.
6. Continue the 2026-08-20 Route-B / PPN / compact-object / FLRW audit and merge only scoped, validated conclusions into the recovery manual and Formula Bible.
7. Run the `rtk-home3` bootstrap handshake, record actual node/worker/progress/checkpoint behavior, then route the next suitable frozen heavy scientific workload to the home node without duplicating an already-running GitHub-hosted calculation.
