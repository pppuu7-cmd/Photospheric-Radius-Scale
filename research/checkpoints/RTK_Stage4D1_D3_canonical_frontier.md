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

## 4. Numerical precision evidence recovered

The v2 -> v3 RTK descent survives CLASS precision tightening:

- Delta S_eff baseline = -0.0718158774705
- Delta S_eff tight = -0.0710021317734
- Delta S_eff provisional-ultra = -0.0709006160891
- tight -> ultra changes the differential by only ~1.0e-4

Focused ultra ell-sampling changes the relative RTK descent by only about 0.00123 across the tested corner; at `l_linstep=2` the tested `l_logstep` values agree.

Absolute production precision is nevertheless not yet fully frozen, so these are differential-convergence controls rather than a final observational comparison.

## 5. BOSS production-systematic caveat

Sparse vs denser redshift-growth evaluation shifts BOSS chi2 by O(0.02-0.03) in the audited points. Dense BOSS evaluation therefore remains a required production-objective upgrade before final model comparison.

## 6. Matched LCDM control recovered and corrected

The original two-start ultra Powell run `31919368067` hit the 120-minute job timeout after finding a lower common LCDM point; this was an infrastructure timeout, not a likelihood failure.

A deterministic replacement run `31935158052` then stopped for a **false regression failure**: the fresh exact matched-ultra center was *lower* than the older harvested expectation by 0.0040896426. Fresh reproduced center:

- S_eff = **1050.2269760031668**
- S_k01 = **1050.2285287876086**

The science script has now been corrected to freeze this fresh center rather than reject the improvement. A v2 matched-ultra LCDM stencil workflow has been launched.

No RTK-vs-LCDM preference may be claimed until both models are locally reoptimized on one final precision/objective definition.

## 7. Active compute allocation after reconciliation

Three complementary streams are maintained, with concurrency chosen to avoid redundant expensive Planck work:

1. **Deep RTK geometry/navigation (primary frontier):** exact symmetric scan along the most-negative v6 7D Hessian eigenvector. Because the v6 gradient is small but Hessian is indefinite, this is more informative than another coordinate poll.
2. **Matched-ultra LCDM control:** corrected two-mapping deterministic stencil refinement, max parallel 2.
3. **Fixed-lambda Stage4D1 acceptance:** existing 8-point profile/certification stream continues independently; it is not duplicated.

Lightweight source-integrity/repeatability audits are already closed and are not rerun unless code/objective changes.

## 8. Acceptance / inference status

✅ Exact Planck runtime, cache-safe production core, component algebra and repeatability are established.

✅ A much deeper RTK navigation basin around lambda_D ~ 2.8-3.0e5 is established by multiple exact runs.

✅ v6 explicit gradient is small enough to pass the configured gradient tolerance.

❌ v6 Hessian is indefinite, so no local-minimum certificate exists.

❌ Final dense-BOSS production objective is not locked.

❌ Absolute CLASS production precision is not fully locked.

❌ RTK and LCDM are not yet both reoptimized on the same final objective.

❌ Finite-lambda interior optimum versus the dust boundary is not established.

❌ No valid final significance, posterior preference, AIC/BIC interpretation, or Bayes factor is claimed.

## 9. Decision rule

Use the deepest directly evaluated point, not the older fixed-lambda frontier, for global navigation. If the negative-curvature exact scan finds a material descent, recenter on that direction and rebuild local 7D geometry. If it does not, characterize the flat lambda direction with a denser lambda/dust profile. In parallel finish the corrected LCDM control and retain fixed-lambda certification for profile shape. Final comparison requires one common precision + dense-BOSS objective and matched local reoptimization of both models.
