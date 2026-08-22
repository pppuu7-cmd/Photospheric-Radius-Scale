# RTK cross-chat reconciliation — 2026-08-22

Status: **authoritative audit checkpoint, but not a replacement for individual frozen result/artifact files**.

Purpose: record which scientifically useful results recovered from neighboring RTK research chats are already durable in the repository, which current live results supersede old summaries, and which chat-only details still require explicit promotion/audit. This prevents future continuation from depending on chat history.

## 1. Neighboring research lineages audited

The reconciliation covered the prior research lineages referred to as:

- `RTK Research Loop` (early and later lineages);
- `RTK Auto-Continue`;
- `RTK Auto-Advance`;
- `Продолжить исследование репозитория`;
- `Продолжить исследование`;
- `Автоматизация итераций исследования` / `Stage 4D1 Completion` lineage.

Policy: repository artifacts, exact workflows, frozen protocols and current source files override chat recollections. A chat-only statement is not upgraded to GREEN merely by being recovered here.

## 2. High-value results confirmed durable

### Numerical / methodology

- Sparse Stage4D3 and dense production scores are explicitly separated; historical sparse `S_eff ~ 1050.0338294787` is navigation only.
- Current production objective is `matched-ultra-linstep2+dense-BOSS`, mapping `eff`, fingerprint `754edb2ff5380eff314867b0ecb1a23a8b861a69f7e46070c4b8251c98573666`.
- Frozen local scores: LCDM `1049.966118347761`, RTK `1050.249912429787`, delta `+0.2837940820259064`; scope remains local raw objective only.
- Full-precision exact-float cache semantics, modern `A_s,n_s`, no rounded-`A_s` optimizer acceptance, exact-poll/recenter/multiscale-Hessian rules and local/global separation are durable in the methodology/recovery files.
- B6 paired AlterBBN differential abundance robustness is closed; `max |R_H-1| = 2.422446243599552e-09`; absolute BBN goodness-of-fit is separate.
- B10 protocol v1 is closed: tail factors 64 and 16384 remain within `0.005`; classification `LAMBDA_NOT_NUMERICALLY_IDENTIFIABLE_AGAINST_PREREGISTERED_DUST_TAIL_AT_0P005`. No missed mandatory B10-v1 gate was found by the earlier chat audit.
- B9 RTK Planck-lensing local stationarity is fresh-tree certified.

### DBI / quadratic EFT

- Broad classical DBI sign/domain scans and exact barotropic identity are represented by the quantum/EFT checkpoint.
- A local preferred-frame quadratic EFT with
  `L2 = K/2 (1+q^2/M_K^2) |pi_dot|^2 - G q^2 |pi|^2/2`
  exactly reproduces the implemented rational scalar dispersion and has a positive quadratic Hamiltonian under the scanned positivity conditions.
- This remains a quadratic existence theorem, not a nonlinear/quantum UV completion.

### C8 carrier / constraint results

- Exact rational finite-positive-pole boundary `alpha = 2h/(3C+h) > 0` for `0<h<1` is durable in Formula Bible/model chronology.
- Scoped two-derivative lapse-only carrier obstruction is durable.
- Exact FLRW Schur-complement algebra, single-linear-pole rank condition and pole/residue discipline are durable.
- Direct spatially-covariant FLRW scalar kernel is constructively reproduced at quadratic order.
- Standard universally coupled low-energy Hořava direct embedding is BLACK scoped by the combined normalization/BBN/PPN/GW theorem; this does not exclude nonminimal matter/constraint architectures.
- Mixed-gradient, rank-one Dirac and aligned mixed-kinetic restrictions are durable; additive independent kinetic directions generally open an extra scalar.

### Current U(1) fixed-action results

- Correct bare/effective bookkeeping: explicit mixed operator supplies the full rolling acceleration contribution, so `beta0_bare=0` while total effective `beta0=2`; old bare `beta0=2 + explicit S_mix` is withdrawn as double counting.
- Fixed scalar action is shift-symmetric `P(X_U)` plus `C(X_U)=M_Pl^2/(2X_U)` on `X_U>0`.
- Fixed-action classical DOF recertification gives exactly three physical DOF in d=3 in the certified region: two tensors + one intended RTK scalar.
- Two-derivative TT sector has positive canonical structure and `c_T^2=1` in scope.
- Static O(v^2) Newton/gamma gate gives GR Newton normalization and `gamma_PPN=1` in scope.
- Static O(v^4) beta gate run `32588268535` succeeded; artifact `9479620022`, digest `sha256:65cc42038f18720017068841594f1ff561dbd9fe25eb76c039bf849ff587805f`. In the regular static-star scope the fixed clock does not shift `beta_PPN=1`.
- Constant-q static DBI branch has a narrow exact real-lapse interval; this is a BLACK scoped branch boundary, not a whole-theory compact-object no-go.
- A regular zero-flux nontrivial scalar profile must satisfy branch-B condition `(rho+p)_8piG = Y/X`; branch existence is algebraically established, global regular stellar/black-hole solutions are not.

## 3. New current obstruction superseding older U(1) optimism

Family-I FLRW A-constraint workflow run `32588741248` succeeded. Artifact `9479738368`, digest `sha256:454fe77a4e99d62a592b7b876aebcd7ff11a127fd31fd8da739894248b491558`.

On the unchanged published universal matter frame with `a1=1,a2=0`, `sigma1=sigma2=0`, A-neutral fixed RTK scalar and evolving ordinary matter, the homogeneous exact A-constraint becomes

`6 K/a^2 - 2 Lambda_g = 16 pi G rho_H(a)`.

For the flat production cosmology the left side is constant while dust/radiation evolve. Therefore the present universal family-I matter/A-source architecture is

`BLACK_SCOPED_CURRENT_UNIVERSAL_FAMILY1_MATTER_FRAME_FLRW`.

This does **not** invalidate the local DOF/TT/static PPN theorems; it blocks promotion of that unchanged matter architecture to the full production cosmology. A genuinely new A-source/matter/constraint architecture is required.

A broader universal-matter FLRW/PPN/DOF trilemma source exists at commit `c71489f040eca73b0e59b00ef966798f21497b5b`, but at this checkpoint it has not yet received its own workflow/CI certification.

## 4. Live numerical frontier at reconciliation

- B4 minimal-neutrino v4: base was recenter-clear but had one soft negative Hessian mode; exact eigenmode rays found no descent above `0.005`; independent v4 half-resolution run `32587822698` is still in progress.
- B9 LCDM: v4 was positive-definite but exact Newton-trust descent `0.20984894 > 0.005`, so recenter-v5 is mandatory; run `32587768594` is executing/completing the exact v5 base-Hessian workflow.
- B9 RTK: fresh-tree lensing local certification is already closed GREEN.

## 5. Useful adjacent-chat details not yet fully promoted before this audit

Two older theory details were recovered from neighboring chats but were not located as explicit standalone durable statements in the current Formula Bible/search index:

1. **Small-coupling BPS cutoff collapse.** In the recovered exact-rational inversion, as `h -> 0`, both `alpha` and `lambda-1` tend to zero, while the quoted strong-coupling scales
   `Lambda_p = M_P (lambda-1)^(3/4) alpha^(-1/4)` and
   `Lambda_omega = M_P (lambda-1)^(5/4) alpha^(-3/4)`
   scale as `sqrt(h)` (with their ratio tending to a finite constant). Thus taking the low-energy couplings arbitrarily small does not automatically cure strong coupling; it can collapse the cutoff. This recovered statement must retain YELLOW/provenance status until the exact primary-source convention and derivation are independently re-audited.

2. **Slowly-moving compact-object regularity boundary.** A neighboring-chat result stated that the standard two-derivative slowly-moving black-hole sector requires the special low-energy `alpha=beta=0` regularity limit, while the finite-positive-pole exact-rational construction enforces `alpha>0`. This is a scoped warning for that low-energy compact-object architecture, not an RTK no-go; higher-spatial/nonlinear UV completion may change the conclusion. The exact primary-source theorem/convention should be independently pinned before promotion to GREEN.

These two recovered items are now explicitly recorded here so they are not lost.

## 6. Current documentation debt found by the audit

The following files are scientifically useful but stale as current-frontier summaries:

- `research/checkpoints/RTK_CHAT_INDEPENDENT_RECOVERY.md` — last reconciled 2026-08-19;
- `research/checkpoints/RTK_CHAT_INDEPENDENT_STATE.json` — reconciled 2026-08-19;
- `research/RESEARCH_LEDGER.md` — top-level B4/B9/U1 statuses lag the Aug-22 runs;
- parts of `research/methods/RTK_FORMULA_BIBLE.md` still label already-closed B10 or older B9 states as open.

Individual later checkpoints/artifacts are newer and authoritative. A subsequent synchronization pass should update these summary/index files without deleting historical chronology.

## 7. One current CI failure that is infrastructure/algebra-assertion, not a scientific FAIL

Moving-source O(3) clock cancellation run `32588416401` failed at a SymPy structural-equality assertion:

`factor((1-lambda_HL)*(2d-1)) == (1-lambda_HL)*(2d-1)`.

The factored and unfactored expressions are algebraically equivalent, but Python/SymPy structural `==` returned false. Therefore this run is **not evidence against the cancellation theorem**. It must be repaired to use symbolic simplification and rerun before preferred-frame `alpha1,alpha2` can be certified.

## 8. Research priority after reconciliation

1. Finish B4 v4 half-resolution and B9 LCDM v5 according to their frozen decision trees.
2. Repair/rerun moving-source O(3) theorem; do not claim preferred-frame closure before CI success.
3. CI-certify the universal-matter FLRW/PPN/DOF trilemma.
4. Design the smallest new A-source/constraint or non-universal matter architecture that cancels the homogeneous ordinary-matter A-source while preserving the production Friedmann background.
5. Freeze that new action before testing it; require exactly 2 tensor + 1 RTK scalar, Newton/gamma/beta/preferred-frame, GW/tensor, radiative protection, strong-coupling cutoff and compact-object gates on the same action.
6. Separately re-audit the two recovered BPS/compact-object statements above against primary literature and promote them into the Formula Bible only with explicit conventions/provenance.

## Bottom line

No major numerical result from the neighboring RTK chats appears lost. The repository already contains the overwhelming majority of high-value scientific content. The remaining issue is **synchronization and provenance quality**, not reconstruction from scratch: a few summary files are stale, two older theory details needed explicit recovery, one moving-source CI needs a trivial algebraic-assertion repair, and the new U(1) matter architecture must be redesigned after the FLRW A-constraint obstruction.
