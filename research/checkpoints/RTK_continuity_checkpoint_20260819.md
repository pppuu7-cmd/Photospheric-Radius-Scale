# RTK continuity checkpoint — 2026-08-19

**Purpose.** This is a continuity/handoff index, not a new scientific acceptance protocol. The repository, not chat history, is the canonical source of scientific state. Where this note conflicts with `research/state/current.json`, a frozen protocol, a reproducibility lock, or the master closure matrix, those authoritative files win.

## Canonical current numerical result

- Frozen matched objective: `matched-ultra-linstep2+dense-BOSS`.
- Production growth mapping: `eff` (`k01` remains a separate diagnostic mapping).
- Recenter tolerance: `Delta S = 0.005`.
- Interior-minimum certification: passed with adjacent base and half-stencil positive-definite, recenter-clear Hessians.
- Independent fresh-tree paired replay: run `32148894768`, exact replay errors recorded as `0.0` for RTK, LCDM, and their raw delta.
- Accepted RTK score: `1050.249912429787`.
- Accepted LCDM score: `1049.966118347761`.
- Frozen raw local matched delta: `Delta S = +0.2837940820259064` (`S_RTK-S_LCDM`).
- This raw local objective difference is not a significance statement and does not by itself authorize Bayes/Wilks/sigma claims.

## Canonical theoretical frontier

Closed internally at the current declared scope:

- classical background sign/stability scan;
- constructive healthy local quadratic preferred-frame scalar EFT representative at linear level;
- exact finite-k dispersion recovery in that representative;
- positive quadratic Hamiltonian on the tested physical domain;
- Route-A1 symmetry postulate and cubic D<=4 basis audit;
- conditional long-wave P(X) thermodynamic/cubic identities;
- finite-k nonlinear coefficient non-identifiability from the background+linear target alone.

Still open and must not be inferred from the quadratic result:

- unique/full nonlinear RTK completion and coupled constraint/DOF theorem;
- physical strong-coupling scale after choosing a nonlinear completion;
- radiative stability/counterterm closure/naturalness;
- nonlinear/local-gravity/compact-object phenomenology.

## Robustness frontier

### B4 minimal standard-neutrino robustness

Frozen test sector:

- `N_ur = 2.0328`;
- `N_ncdm = 1`;
- `m_ncdm = 0.06 eV`;
- `T_ncdm = 0.71611`;
- `deg_ncdm = 1.0`;
- objective label `matched-ultra-linstep2+dense-BOSS+nu0p06-additive-v1`.

The first paired reoptimization seed, run `32173665110`, was an **infrastructure failure before a scientific likelihood evaluation**. Both RTK and LCDM jobs imported the generated reusable likelihood core with their model name in the worker argv; the core incorrectly interpreted that argv value as a Planck data path, producing `RTK/baseline/...` / `LCDM/baseline/...` lookup failures.

Repairs committed before rerun:

- `7617ce53d658504cc501f48fee10a8bd141c6366` — generated reusable inference core now uses explicit `RTK_PLANCK_DATA` / `planck_data` and never inherits the importing worker's argv for the Planck path;
- `ed6d9e7d1f4e934116edbc904d136419c0d40ecf` — neutrino seed now rejects out-of-bound points explicitly, never clips them silently, counts bound rejections, and records diagnostic-poll provenance;
- main workflow commit `294d1fcdd646c7aad989cd2ec40808ba7b16af1d` — pins `RTK_PLANCK_DATA`, adds an import smoke test reproducing the old `argv=['...','RTK']` failure mode, and requires the hardened bound provenance field.

Paired rerun:

- run `32190997977` (run #2), triggered from main commit `94ecfa01f85ad69b1138719dc9fd78b9e096f7b7`;
- at this checkpoint both RTK and LCDM jobs had passed checkout, frozen-state prerequisites, CLASS build, pinned dependencies, Planck checksum/extraction, and the reusable-likelihood import smoke test;
- both jobs were actively executing the exact neutrino seed reoptimization;
- the seed is only a candidate generator. B4 remains open until model-appropriate stationarity/multiscale checks and an independent paired replay close under the neutrino objective.

## Other robustness/observational status

- Tensor/GW late-time propagation and final-center standard-siren diagnostic are internally closed at their declared scope; no unsupported primordial-tensor claim follows.
- Early-universe final-center background diagnostic reaches very high redshift and is useful evidence, but its persisted artifact explicitly states that it is not a primordial-abundance likelihood or a dedicated BBN calculation. Do not promote it to precision-BBN closure without the missing dedicated gate.
- Survey-level/nonlinear RSD robustness remains open despite the small linear `f sigma8(k)` scale dependence.

## Continuity rule

Older conversations may contain precursor ideas, abandoned search branches, or earlier numerical values. They are not allowed to override the live repository state. Any old-chat item that becomes scientifically relevant again must be reintroduced as an explicit repository task/protocol/checkpoint and revalidated against the current frozen state before it can change a claim.

Primary navigation:

1. `research/state/current.json` — live frozen numerical state and accepted comparison;
2. `research/RTK_MASTER_RESEARCH_CLOSURE_MATRIX.md` — high-level open/closed frontier;
3. `rtk/FINAL_MATCHED_COMPARISON_PROTOCOL.md` and Stage-4D3 protocol files — numerical acceptance semantics;
4. `rtk/reproducibility_lock.json` — runtime/source/data lock;
5. `research/checkpoints/` and `research/robustness/` — theorem/robustness evidence and scoped warnings.
