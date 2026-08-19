# RTK BBN H(T) mapping protocol v1.2 — failsafe=1 accepted-state trace fix

Status: **FROZEN BEFORE THE THIRD H(T) MAPPING RUN**.

This addendum supersedes only the diagnostic observation location from v1.1. It does not change the cosmological parameters, radiation baseline, same-shared-parameter LCDM control, fixed `T_anchor=0.01 MeV`, physical scale-factor calibration, CLASS ratio definition, no-extrapolation rule, nested table test, or downstream abundance gate.

## Why run 2 failed closed

Run `32239927888` passed all source/runtime/build guards and again reproduced the accepted standard printed abundances exactly at the self-test precision:

- `Yp=0.2473`
- `D/H=2.435e-5`
- `He3/H=1.031e-5`
- `Li7/H=5.466e-10`

The accepted-state trace file existed but contained zero data rows. The v1.1 patch had instrumented the accepted block of the `failsafe<10` adaptive stiff method. However `stand_cosmo.x 1` sets `failsafe=1`, and pinned AlterBBN v2.2 dispatches this case through the earlier branch

`if(paramrelic->failsafe<5) /* Original order 2 method for stiff equations */`.

Therefore the zero-row result is an instrumentation-location failure, not a network or cosmological failure.

## Exact v2.2 source rule for failsafe=1

Within the `failsafe<5` branch, each integration step runs `loop=1` predictor followed by `loop=2` corrector. The corrected accepted state is assigned in

`else /* if(loop==2) */`

through

- `T=T0+(dT_dt+dT0_dt)*0.5*dt`,
- `h_eta=...`, `phie=...`,
- `a=a0+(da_dt+da_dt0)*0.5*dt`,
- `Tnu=...`,
- `Y[i]=Y0[i]+(dY_dt[i]+dY_dt0[i])*0.5*dt`.

The branch has no separate adaptive reject/retry test analogous to `failsafe<10`; invalid-temperature protection occurs in the predictor and returns failure rather than accepting a bad corrected state. Thus the end of the `loop==2` corrector is the appropriate observation point for the standard `failsafe=1` run.

## Revised trace rule

The third-run instrumentation shall:

1. assign a monotonically increasing `nucl_single` call serial at function entry;
2. for `failsafe<5`, write one diagnostic row only at the end of the corrected `loop==2` state, after `T`, `a`, `Tnu`, and all `Y[i]` have been updated;
3. write columns `call_id`, `paramrelic.err`, `T_internal`, `a_internal`;
4. never assign to `T`, `a`, `dt`, rates, abundances, H, timestep controls, or any other network state;
5. leave the standard printed-abundance invariance guard mandatory.

The mapper keeps the v1.1 call-serial selection logic: choose the first complete `err=0` central solve immediately preceded by the direct `err=2` low solve and followed by the direct `err=1` high solve, then require strict `T↓` and `a↑` along the selected path.

## Evidence provenance

The source-branch correction follows the pinned AlterBBN v2.2 source structure independently re-audited in run `32239397180`. Run `32239927888` is retained as a fail-closed diagnostic artifact and is not consumed as an H(T) result.
