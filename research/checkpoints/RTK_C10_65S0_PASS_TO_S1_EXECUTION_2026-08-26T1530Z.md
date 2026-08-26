# RTK recovery checkpoint — C10.65s0 PASS → C10.65s1 execution

UTC: 2026-08-26T15:30Z
Branch: `rtk-class-build`
Repository: `pppuu7-cmd/Photospheric-Radius-Scale`

## Confirmed inherited frontier

- C10.65r2: `PASS_SCOPED` for diagnostic in-CLASS first-RHS parity; no production `dy`/metric feedback is implied.
- C10.65s0: `C10_65S0_DIRECT_ONSET_INITIALIZATION_ARCHITECTURE_PASS_LEGACY_AUX_EXCLUSION_REQUIRED_SCOPED`.
- C10.65s0 establishes direct opt-in start at certified `a_on`, ordinary `pa_old=NULL -> perturb_vector_init -> perturb_initial_conditions`, and requires legacy model=2 `dU/dV/dZ` perturbations to be excluded from the completed forward state.
- C10.65s1 target was frozen before implementation in commit `532266d30f4eb4fa6ef1c9509fc5b0c5691d9a8d`.

## C10.65s1 frozen purpose

Inventory the complete scalar perturbation state actually integrated by pinned CLASS at the four certified low-k onset anchors, source-lock TCA/RSA/UFA and active `l_max_ur`, determine the finite-k higher-UR hierarchy control, and construct all 9x4 completed onset states without consuming historical metric potentials or legacy nlde auxiliaries.

## Implementation added in this iteration

1. `rtk/apply_rtk_c10_65s1_readonly_state_observer_patch.py`
   - adds a separate `rtk_c10_65s1_observer.c` translation unit to a disposable CLASS tree;
   - observer body is `noinline,noclone` on GCC;
   - dormant unless `RTK_C10_65S1_OBSERVER_FILE` is set;
   - writes only a sidecar CSV;
   - does not assign `dy` or `pvecmetric` and does not add production perturbation columns;
   - exports `a`, `k`, TCA/RSA/UFA flags, `l_max_ur`, integrated Newtonian `phi`, baryon/photon/UR/CDM-slot state, all six historical nlde auxiliary coordinates, and `F_l/k^l` for active UR `3<=l<=30`.

2. `research/shadow/rtk_c10_65s1_finite_state_completion_at_onset.py`
   - selects the observer row nearest the frozen `a_on` for each of the four exact anchors and requires relative `a` error <= `1e-12`;
   - requires TCA ON on all anchors and common RSA/UFA/l_max state;
   - if the full UR hierarchy is active, checks regular low-k slopes for `l=3,4,5` against the frozen `<=0.35` slope tolerance, with explicit resolution-limited classification when values are below `1e-280`;
   - constructs 36 completed state records from C10.65n/o using
     `phi_CLASS=Psi_N`,
     `delta_b=Db+3 Psi_N`,
     `delta_g=Dg+4 Psi_N`,
     `delta_ur=Dur+4 Psi_N`,
     `theta_b=theta_g=theta_ur=k^2 V_N`,
     `delta_cdm=(1+w_khr)(J_khr+3 Psi_N)`,
     `theta_cdm=k^2 V_N`,
     `shear_ur=k^2 S_ur0`;
   - appends active historical `F_l` values only as `HIGHER_ORDER_HISTORICAL_CONTROL`;
   - explicitly excludes all six legacy nlde auxiliary coordinates from the completed state.

3. `.github/workflows/rtk-c10-65s1-finite-state-completion-at-onset.yml`
   - builds an r1 control tree and an s1 disposable observer tree from pinned CLASS SHA `36cf283628c4a3330ec9fd3d84239bf775f77317`;
   - first requires exact SHA identity of all four ordinary perturbation numeric-row streams with the observer dormant;
   - then runs the read-only observer with one thread and the four exact low-k anchors;
   - executes the unchanged frozen s1 analyzer and persists result/provenance only if the gate passes or receives the target's explicitly allowed resolution-limited scoped classification.

## GitHub Actions

Run launched: `32985185447` — **RTK C10.65s1 finite-state completion at onset**.
At checkpoint creation the run is queued, so **C10.65s1 is not classified as PASS**.

## Required interpretation

Until the Action completes, status is:

- C10.65s0: PASS_SCOPED.
- C10.65s1: EXECUTION_PENDING / OPEN.
- Production completed-U1 feedback, direct state initialization, and forward `dy` evolution remain forbidden.
- C9 radiative naturalness and same-full-action primordial/background closure remain open fundamental gates.

## Next action after run completion

- If s1 passes: freeze C10.65s2 before implementation, exactly as named in the s1 target: direct-at-`a_on` opt-in initialization plus first one/short-step completed-U1 production-feedback canary on one completion point x four anchors, with legacy nlde perturbation allocation suppressed and exact OFF rollback plus preferred A/H/M constraint-drift measurement.
- If s1 fails: diagnose the failing frozen check (OFF identity, onset alignment, approximation-state consistency, l-hierarchy scaling, or state finiteness) and repair implementation without weakening the target unless a separate scientific justification is first frozen.
