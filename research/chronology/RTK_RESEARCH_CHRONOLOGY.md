# RTK / DBI-Khronon — recovered research chronology

This is the human-readable chronology. It combines recoverable chat timestamps with repository-verified GitHub timestamps. UTC is canonical; Europe/Helsinki is shown for operator convenience. When an exact time could not be recovered, no synthetic time is invented.

For every future autonomous iteration, the machine-readable append-only source is `RTK_RESEARCH_CHRONOLOGY.jsonl`.

| UTC | Europe/Helsinki | Source | Step / result | Status |
|---|---|---|---|---|
| 2026-08-14 03:30:29Z | 2026-08-14 06:30:29 +03 | early `RTK Research Loop` | Accepted next scan: `lambda_D=8000,10000,12500,15000,20000`; compute multi-z `P(k,z)`, `f sigma8(z)`, then coarse likelihood. | ✅ historical decision |
| 2026-08-14 04:57:09Z | 2026-08-14 07:57:09 +03 | early `RTK Research Loop` | Accepted extension to `lambda_D=1000,2000,3000`, full SN/BAO/RSD covariance, and official Planck likelihood. | ✅ historical decision |
| 2026-08-15 02:02:12Z | 2026-08-15 05:02:12 +03 | early `RTK Research Loop` | Requested a self-contained recovery methodology so the project could survive chat loss. | ✅ process requirement |
| 2026-08-15 21:14:07Z | 2026-08-16 00:14:07 +03 | early `RTK Research Loop` | Full RT+Khronon CLASS plus Planck/Pantheon/BOSS likelihood in use; DBI stability tested on 263,424 states with residuals ~`1e-16`; finite-lambda candidate around `lambda_D~4.04e4`, `S_eff~1050.77247`; local/global proof still open. | 🟡 milestone, not final minimum |
| 2026-08-15 21:26:26Z | 2026-08-16 00:26:26 +03 | early `RTK Research Loop` | Priority order fixed: close finite-lambda proof gates first; then massive neutrinos, Planck lensing, DESI/full-RSD, production MCMC/evidence. | ✅ roadmap decision |
| 2026-08-16 08:23:09Z | 2026-08-16 11:23:09 +03 | `RTK Auto-Continue` lineage | Shifted from sparse/baseline to candidate final `matched-ultra+dense-BOSS`; exact-float cache and modern `A_s/n_s` reproducible; dense BOSS changed RTK candidate more than LCDM control, proving sparse/dense scores must not be mixed. | ✅ provenance boundary |
| 2026-08-16 22:17:52Z | 2026-08-17 01:17:52 +03 | earlier `RTK Research Loop`/parallel theory branch | User accepted a separate RTK quantum-theory branch to run in parallel with cosmology. | ✅ branch decision |
| 2026-08-16 22:23:13Z | 2026-08-17 01:23:13 +03 | quantum branch | Quantum baseline run `31975991159` succeeded: `1225/1225` points, `0` algebraic violations. Round5 sparse best recorded `S_eff=1050.0338294787382`, `S_k01=1050.0482111660676`, `lambda_D=217225.01601516694`. Strong-coupling/loops/UV and full nonlinear/constraint issues remained open. | ✅ baseline / ❌ full quantum closure |
| 2026-08-17 00:02:45Z | 2026-08-17 03:02:45 +03 | `RTK Auto-Advance` | Strict checklist fixed: no recenter without exact improvement; verify both `eff` and `k01`; preserve exact Planck runtime/self-tests, full-precision cache, component audits, deterministic starts, two-level poll, 73-point Hessian, strict 7D `log(lambda_D)` geometry, lambda-boundary/precision/dense-BOSS gates; no premature preference claims. | ✅ methodological contract |
| 2026-08-17 00:14:01Z | 2026-08-17 03:14:01 +03 | `RTK Auto-Continue` / Auto-Advance | Round5 sparse center `S_eff=1050.0338294787`, `S_k01=1050.0482111661`; correlated-ray exact improvement `0.000000` for both => `NO_RECENTER`. Partial commit identifiers recovered from chat: `45a175c...`, `08d364d...`; these are provenance hints only until full SHA is repository-verified. | ✅ sparse local navigation only |
| 2026-08-17 16:43:04Z | 2026-08-17 19:43:04 +03 | `RTK Auto-Continue` | Production objective fixed as `matched-ultra-linstep2+dense-BOSS`; corrected accepted LCDM best-exact score later reconciled to `1049.966118347761`; RTK axis gate improvement `0`; RTK center at that stage `1050.332707865856`; no model-selection claim. | ✅ objective / 🟡 RTK stationarity then open |
| 2026-08-17 16:47:05Z | 2026-08-17 19:47:05 +03 | `RTK Auto-Continue` | RTK run `31998282437` classified as compute failure with zero artifacts, not a scientific failure. Worker hardened with up to 3 transient retries, incremental diagnostics, `always()` artifact upload; replacement run `32047204215` launched from commit `f1542e4...`. | ✅ infrastructure correction |
| 2026-08-18 12:39:15Z | 2026-08-18 15:39:15 +03 | later `RTK Research Loop` | User required continuous research progress and separation of internally closable items from external blockers. | ✅ process rule |
| 2026-08-18 13:30:40Z | 2026-08-18 16:30:40 +03 | later `RTK Research Loop` | While user is present they steer; if absent, automated mode continues; code/logic audit should continue in parallel. | ✅ process rule |
| 2026-08-18 19:31:25Z | 2026-08-18 22:31:25 +03 | separate later `RTK Research Loop` | Reports required to be self-contained and explicitly mark `✅ closed` / `❌ open`. | ✅ reporting rule |
| 2026-08-18 22:03:20Z | 2026-08-19 01:03:20 +03 | GitHub commit `7617ce53...` | `Make reusable inference core Planck path module-safe`: reusable core no longer inherits worker argv as Planck path; explicit `RTK_PLANCK_DATA`. | ✅ bug fixed |
| 2026-08-18 22:04:01Z | 2026-08-19 01:04:01 +03 | GitHub commit `ed6d9e7d...` | Hardened neutrino seed physical bounds and poll provenance: OOB proposals rejected/logged rather than clipped. | ✅ bug/guardrail fixed |
| 2026-08-18 22:04:30Z | 2026-08-19 01:04:30 +03 | GitHub commit `294d1fcd...` | Hardened B4 workflow Planck path and added import smoke test reproducing the earlier argv failure mode. | ✅ regression gate added |
| 2026-08-18 22:07:54Z | 2026-08-19 01:07:54 +03 | GitHub commit `455156cf...` | Added cross-chat continuity checkpoint. Frozen matched local scores recorded: RTK `1050.249912429787`, LCDM `1049.966118347761`, raw `Delta S=+0.2837940820259064`; replay run `32148894768` error `0.0`. | ✅ continuity checkpoint |
| 2026-08-19 09:13:41Z | 2026-08-19 12:13:41 +03 | GitHub Actions run `32236524767` | B4 paired minimal-neutrino **base stationarity** started for RTK and LCDM. | 🟡 in progress at 11:06Z check |
| 2026-08-19 09:29:50Z | 2026-08-19 12:29:50 +03 | run `32237897006` | Pinned AlterBBN expansion-interface audit started and completed successfully. | ✅ interface audit |
| 2026-08-19 09:47:22Z | 2026-08-19 12:47:22 +03 | run `32239397180` | Pinned AlterBBN integration-flow audit started and completed successfully. | ✅ integration-flow audit |
| 2026-08-19 09:58:58Z | 2026-08-19 12:58:58 +03 | run `32240381293` | B10 fixed-shared lambda-tail reconnaissance launched; completed at `10:19:14Z`. Preregistered asymptotic onset factor `64`; fixed-shared flatness does not establish profiled identifiability. | ✅ T1 / ❌ profile conclusion |
| 2026-08-19 10:37:00Z | 2026-08-19 13:37:00 +03 | run `32243547025` | B6 entropy-aware `H(T)` mapping launched; completed successfully at `10:37:58Z`. `max |R_H-1| ~2.17e-9`; nominal/refined mismatch ~`1.73e-12`. | ✅ expansion mapping / ❌ abundance closure |
| 2026-08-19 10:39:39Z | 2026-08-19 13:39:39 +03 | run `32243756716` | B9 pinned Planck standalone-lensing interface audit launched; completed successfully at `10:40:21Z`. | ✅ interface / ❌ paired cosmological lensing closure |
| 2026-08-19 10:46:39Z | 2026-08-19 13:46:39 +03 | run `32244330691` | B10 paired fixed-lambda T2 profiled jobs launched at factors `64` and `16384`. | 🟡 in progress at 11:06Z check |
| 2026-08-19 11:06:00Z | 2026-08-19 14:06:00 +03 | current cross-chat reconciliation | Recovered both `RTK Research Loop` lineages plus `RTK Auto-Continue` and `RTK Auto-Advance`; promoted their durable rules/results into the canonical repository methodology and chronology. | ✅ this reconciliation |

## Historical items with incomplete exact timestamps

Foundational covariant/DBI/MOND/lensing derivations and some early CLASS integration steps predate the exact timestamps recoverable from the named chats. They are preserved in the canonical methodology and prior derivation/checkpoint files, but this chronology deliberately does **not** invent clock times for them.

## Correction policy

If a later audit changes any row above, append a dated correction row. Do not edit historical claims into appearing as if they were always known.
