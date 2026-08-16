# RTK + DBI-Khronon — canonical Stage4D1 / Stage4D3 frontier

This checkpoint reconciles the previously diverged fixed-lambda Stage4D1 stream and the deeper Stage4D3 As-z_re / precision / matched-LCDM stream. It is the provenance bridge to use before launching new inference work.

## 1. Closed implementation / runtime facts

- Official Planck 2018 baseline R3.00 likelihood is operational through `clipy-like==0.15`; Commander, SimAll and Plik-lite distributed self-tests reproduce.
- Production inference core uses exact IEEE-754 parameter tuple cache keys, modern `A_s/n_s`, and a CLASS timeout. Rounded dimensional cache keys are rejected by workflow grep gates.
- Pantheon full covariance and BOSS DR12 9x9 covariance implementation have independent algebra/convention checks.
- Same-point fresh-CLASS repeatability with cache cleared has zero spread at stored precision in the dedicated Iteration-6 audit.
- Historical rounded-cache optimizer convergence claims are withdrawn; their exact evaluated points remain valid evaluations only.

## 2. Fixed-lambda Stage4D1 stream

The fixed-lambda acceptance program remains useful for profile classification at lambda_D = 3e4, 1e5, 1e6, 1e8, separately for `eff` and `k01`. Its rule remains: positive exact poll gain => recenter; non-improving polls => 73-point Hessian/gradient gate; only then correlated-direction acceptance.

The current fixed-lambda compute stream is intentionally retained, but it is no longer the deepest known RTK navigation frontier.

## 3. Deep Stage4D3 navigation frontier recovered from other chat/research branches

### v4

Commit `2264e11faadbcc2e18b993e9b34f67d313c2bf6a` recorded:

- S_eff = 1050.135699621492
- S_k01 = 1050.149916197271
- lambda_D = 293868.81143246836
- A_s = 2.082203080347647e-9
- z_re = 7.17612905430964

v4 was a boundary navigation record, not a stationary fit.

### v5

Exact 5x5 As-z_re run `31919292115` improved the record to an interior 2D point:

- S_eff = **1050.072580002519**
- S_k01 = **1050.0869167499159**
- lambda_D = 293868.81143246836
- h = 0.6903899123316766
- Omega_b = 0.046851744145772894
- Omega_m = 0.25313821169954864
- A_s = 2.0832030803476467e-9
- n_s = 0.9644164163369503
- z_re = 7.21112905430964

Both v5 2D boundary flags were false. This remained navigation only.

Full 7D v5 Hessians (`eff/k01` x scales 1, 0.5, 0.25; run `31935018530`) were positive definite at the finest scale but failed the explicit gradient gate. Finest-scale exact stencil improvements were small (<0.0004) and Newton proposals worsened.

### v6

Run `31935863103` recentered on a common correlated point:

- lambda_D = 287930.95430552866
- h = 0.6904668858782219
- Omega_b = 0.046835996338062985
- Omega_m = 0.2530185206833107
- A_s = 2.0836316905673827e-9
- n_s = 0.9644013704702473
- z_re = 7.218930610576525
- center S_eff = **1050.0475038880681**
- center S_k01 = **1050.0618892996533**

At the finest 7D scale=0.25:

- best exact S_eff = **1050.0464517618454**
- best exact S_k01 = **1050.0608367436391**
- best design point primarily moves lambda_D to 284354.2185471583
- scaled-gradient gate passes: max |grad_base| ~0.0198 (`eff`) and ~0.0194 (`k01`), below 0.03
- Hessian is **not positive definite** in either mapping
- most-negative eigenvalue in scaled-y coordinates is about -7.646e-4
- the most-negative eigenvector is overwhelmingly the log-lambda direction (~0.9991 component)
- Newton proposals worsen the exact objective

Therefore v6 is a near-stationary but locally indefinite / flat navigation point, **not an accepted minimum**.

### v6 negative-curvature continuation

Exact symmetric scan run `31961816831` followed the most-negative v6 Hessian eigenvector at t = {-16,-12,-8,-6,-4,-2,-1,0,1,2,4,6,8,12,16}. The same CLASS evaluations supplied both BOSS mappings.

The best point for both mappings occurs at **t=-1**, not at the old center:

- lambda_D = **284357.3770256277**
- h = 0.6904692350128682
- Omega_b = 0.04683552900298674
- Omega_m = 0.25301548428566323
- A_s = 2.083631213860309e-9
- n_s = 0.9644009156458047
- z_re = 7.218996521149225
- S_eff = **1050.045724929783**
- S_k01 = **1050.0601104098123**
- chi2_BOSS_eff = 7.559889906650282
- chi2_BOSS_k01 = 7.574275386679554
- chi2_SN = 39.55807432331117
- logL_Planck = -501.4638803499108
- r_d = 146.976511 Mpc

Improvement relative to the v6 center is ~**0.00177896** for both mappings. This proves that the v6 indefinite mode contains a real exact descent, although the gain is shallow. It triggers mandatory recentering rather than any minimum claim.

A new six-job multiscale 73-point Hessian run (`31962435655`; eff/k01 x scales 1,0.5,0.25) is active at this negative-curvature best point.

## 4. Numerical precision evidence recovered

Two independent differential precision audits are now joined to this checkpoint.

### Earlier v2 -> v3 descent

- Delta S_eff baseline = -0.0718158774705
- Delta S_eff tight = -0.0710021317734
- Delta S_eff provisional-ultra = -0.0709006160891
- tight -> ultra changes the differential by only ~1.0e-4

### Exact v4 -> v5 audit, run 31935040222

The baseline points reproduce to the configured 1e-9 regression gate. The same v4 -> v5 move gives:

- baseline: Delta S_eff = **-0.063119618973**, Delta S_k01 = **-0.062999447355**
- tight: Delta S_eff = **-0.072806814371**, Delta S_k01 = **-0.072686704908**
- ultra: Delta S_eff = **-0.072544614566**, Delta S_k01 = **-0.072424487505**
- tight -> ultra differential change = **+2.621998e-4** (`eff`) and **+2.622174e-4** (`k01`)

For reference, absolute v5 scores are 1050.072580002519 / 1050.086916749916 at baseline, 1050.398153378145 / 1050.412424594242 at tight, and 1050.392110639593 / 1050.406389087194 at ultra. Thus absolute scores are precision-level dependent, while the deep local descent is much more stable.

Focused ultra ell-sampling changes the relative RTK descent by only about 0.00123 across the tested corner; at `l_linstep=2` the tested `l_logstep` values agree.

Absolute production precision is nevertheless not yet fully frozen, so these are differential-convergence controls rather than a final observational comparison.

## 5. BOSS production-systematic caveat

Sparse vs denser redshift-growth evaluation shifts BOSS chi2 by O(0.02-0.03) in the audited points. Dense BOSS evaluation therefore remains a required production-objective upgrade before final model comparison.

A candidate final-objective builder already exists on the production branch. It combines exact-float cache semantics, matched-ultra CLASS settings with `l_linstep=2`, and dense BOSS `z_pk` growth sampling. Its smoke workflow `31935950335` completed successfully. This is a **candidate** objective, not yet the frozen final inference target.

## 6. Matched LCDM control and production code-state distinction

The original two-start ultra Powell run `31919368067` hit the 120-minute job timeout after finding a lower common LCDM point; this was an infrastructure timeout, not a likelihood failure.

A later investigation revealed that `main` and `rtk-class-build` are substantially diverged code histories. Most production likelihood workflows explicitly check out `rtk-class-build`. Therefore absolute objective values produced from different branch/code states must not be mixed.

For the current `rtk-class-build` production state, matched-ultra center run `31961828138` reproduced:

- S_eff = **1050.2310656457898**
- S_k01 = **1050.2326184302317**
- chi2_BOSS_eff = 6.901163589356042
- chi2_BOSS_k01 = 6.9027163737979205
- chi2_SN = 39.80582793778543
- logL_Planck = -501.7620370593242
- r_d = 146.974624 Mpc

The production-branch stencil script has been updated to freeze these values, and failed jobs in run `31961828138` were rerun as attempt 2. They are active.

The previously quoted lower fresh center 1050.2269760031668 / 1050.2285287876086 belongs to a different code/objective state and is retained only as provenance evidence, not as the current production baseline.

No RTK-vs-LCDM preference may be claimed until both models are locally reoptimized on one final branch, one final CLASS precision, and one final dense-BOSS objective.

## 7. Production provenance rule

Until the branch histories are collapsed for publication freeze:

1. `rtk-class-build` is the numerical source of truth for workflows that explicitly check it out.
2. Every absolute S value must carry branch/code-state and precision provenance.
3. Cross-branch absolute score differences are **not physics**.
4. Differential precision tests within a fixed code state remain valid numerical-convergence evidence.
5. Before final model selection, canonical source and production source must be collapsed or cryptographically fingerprinted as one frozen objective.

## 8. Active compute allocation after reconciliation

Three complementary streams are maintained, with concurrency chosen to avoid redundant expensive Planck work:

1. **Deep RTK geometry/navigation (primary frontier):** six active 73-point stationarity jobs centered on the negative-curvature best `S_eff=1050.045724929783`, `S_k01=1050.0601104098123`.
2. **Matched-ultra LCDM control:** corrected production-branch deterministic stencil refinement, two mappings in parallel, attempt 2 of run `31961828138`.
3. **Fixed-lambda Stage4D1 acceptance:** existing 8-point profile/certification stream continues independently; it is not duplicated.

Lightweight source-integrity/repeatability audits are already closed and are not rerun unless code/objective changes.

## 9. Acceptance / inference status

✅ Exact Planck runtime, cache-safe production core, component algebra and repeatability are established.

✅ A much deeper RTK navigation basin around lambda_D ~ 2.8-3.0e5 is established by multiple exact runs.

✅ v6 explicit gradient was small enough to pass the configured gradient tolerance.

✅ Exact negative-curvature continuation found a further shallow descent and supplied a new recenter target.

❌ A positive-definite recentered Hessian certificate has not yet been obtained.

🟡 Matched-ultra LCDM production-branch refinement is active.

🟡 Candidate final dense-BOSS + matched-ultra objective builder exists and its smoke test passes.

❌ Final dense-BOSS production objective is not yet frozen for both-model reoptimization.

❌ RTK and LCDM are not yet both reoptimized on the same frozen final objective.

❌ Finite-lambda interior optimum versus the dust boundary is not established.

❌ No valid final significance, posterior preference, AIC/BIC interpretation, or Bayes factor is claimed.

## 10. Decision rule

Use the deepest directly evaluated point with matching code-state provenance, not the older fixed-lambda frontier, for global navigation. If the recentered 73-point Hessian becomes positive definite while the scaled gradient and exact-improvement gates pass, launch the independent correlated-direction ray. If it remains indefinite or finds a new exact descent, recenter/trace the corresponding mode again. In parallel finish the production-branch LCDM control. Final comparison requires one common production branch, final precision + dense-BOSS objective, and matched local reoptimization of both models.
