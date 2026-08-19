# RTK BBN H(T) mapping protocol v1.1 — accepted-state trace fix

Status: **FROZEN BEFORE THE SECOND H(T) MAPPING RUN**.

This is a technical addendum to `RTK_BBN_HT_MAPPING_PROTOCOL_v1.md`. It does not change the cosmological model, same-parameter control, fixed post-e± anchor, physical scale-factor calibration, CLASS interpolation, or Hubble-ratio definition. It changes only where the diagnostic AlterBBN `(T,a)` path is observed.

## Reason for the addendum

First mapping run `32238634437` failed closed at the monotonic-path guard. All upstream prerequisites passed, including exact pinned source, unchanged printed standard abundances, and both CLASS backgrounds. The RHS-level trace contained 392086 calls and mixed multiple low/central/high/uncertainty network solves plus trial/rejected stiff-integrator states. A global log-T bin reduction therefore produced 358 non-monotone `a(T)` violations and was correctly rejected.

No abundance or RTK-physics result was consumed from that failed mapping attempt.

## Exact-source evidence

Pinned-source integration-flow audit run `32239397180` established:

1. `stand_cosmo.c` executes
   - `paramrelic.err=2; nucl(...)` (low),
   - `paramrelic.err=0; nucl(...)` (central),
   - `paramrelic.err=1; nucl(...)` (high),
   - then `paramrelic.err=3; nucl_err(...)`.
2. In the `failsafe<20` stiff branch used by `stand_cosmo.x 1`, a step is accepted only in the block
   `if(test==0 && test_precision==0)`
   followed by assignments `T=T2`, `...`, `a=a2`.
3. Rejected steps instead restore `T=T_sav`, `a=a_sav` after reducing the step size.

Thus the accepted-state block is the correct diagnostic observation point.

## Revised trace rule

The instrumentation patch shall:

- assign a monotonically increasing `nucl_single` call serial at entry;
- record only after the `failsafe<20` accepted-step assignments `T=T2` and `a=a2`;
- write columns `call_id`, `paramrelic.err`, `T_internal`, `a_internal`;
- never assign to or otherwise alter `T`, `a`, `dt`, abundances, rates, H, or any solver control variable;
- retain the standard printed-abundance invariance guard from v1.

The mapping builder shall select the **central** standard solve as the unique/first full accepted path with `paramrelic.err==0`, and verify the audited low/central/high call ordering when present. It shall reject any selected path unless:

- `a_internal` is strictly increasing;
- `T_internal` is strictly decreasing;
- the fixed `T_anchor=0.01 MeV` lies within the path;
- enough accepted states exist for stable log interpolation.

No bin-median mixing of independent solves or rejected RHS trials is permitted in v1.1.

## Unchanged downstream rules

The physical scale-factor anchor, `z(T)` construction, RTK / same-shared-parameter LCDM CLASS ratio, no-extrapolation rule, nested 256/512 table test, and later paired `R=1` versus `R(T)` abundance-network gate remain exactly as preregistered in v1.
