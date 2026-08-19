# B6 AlterBBN H(T) coverage-extension protocol v1

Status: **FROZEN BEFORE THE FIRST EXTENDED T-a TRACE AND BEFORE ANY VALID RTK ABUNDANCE OUTPUT**.

## Why this protocol exists

The preregistered paired abundance gate was executed three times without producing a scientific abundance result:

- run `32251381580` stopped before build/network on a source-text matcher;
- run `32252015488` stopped at compilation after the unique Friedmann site was found but the temperature variable was misidentified;
- run `32252925021` passed all source/artifact hashes, patched all three trees and built all three AlterBBN networks, but the first reference network aborted fail-closed at `T = 8.572921799800281e-7 GeV`, below the old H(T) table minimum `8.614109862550688e-7 GeV`.

No central abundance row was accepted or parsed from any of these runs, so the coverage repair is fixed before seeing an RTK abundance result.

Byte-pinned source audit run `32253452881`, artifact `9365326269`, established for exact pinned `src/bbn.c` SHA256 `528b1416876b0fc9d6ddc1d2a0f6ba8cab43796680cef4a7fd92339e974fb708`:

- the network final-temperature definition is exactly `double Tf=0.01*K_to_eV;`;
- the integration stop test is `T <= Tf`;
- the Friedmann H call is inside `fill_params(double T,...)`, with T directly in GeV.

The small lower-temperature H evaluation is therefore a predictor/corrector coverage effect around the standard final-temperature boundary, not evidence for changing the physical abundance network cutoff.

## Frozen repair

The production abundance networks keep the original pinned AlterBBN final temperature unchanged at `Tf = 0.01*K_to_eV`.

For **trace generation only**, create a byte-separated copy of the same pinned AlterBBN v2.2 source and change exactly the unique final-temperature initialization from

`double Tf=0.01*K_to_eV;`

to

`double Tf=0.009*K_to_eV;`.

No other physics, rates, eta, failsafe setting or integration parameter may change. Apply the existing accepted-state T-a trace instrumentation after this one-line trace-only patch and run the same `stand_cosmo.x 1` central solve. The purpose is only to obtain accepted T-a states that enclose every temperature evaluated by the unmodified abundance network.

The choice `0.009 GK` is fixed before the extended trace result. It is 10% below the standard 0.01-GK termination threshold and comfortably below the already observed failing H-evaluation temperature. It may not be moved again after viewing abundance outputs.

## Extended mapping requirements

Build nominal 256-point and refined 512-point entropy-aware RTK/LCDM H(T) mappings with the existing `build_bbn_rtk_ht_mapping.py` and the unchanged massless accepted RTK point/objective/provenance.

The extended trace/mapping is acceptable only if:

1. the pinned archive SHA/size/version and compiler lock pass;
2. the trace patch changes only instrumentation plus the preregistered trace-only Tf line;
3. the central accepted trace is finite and strictly covers the old lower endpoint;
4. the resulting mapping minimum is **strictly below `8.572921799800281e-7 GeV`** with at least 1% relative lower-temperature margin;
5. the nominal/refined mappings remain nested and their R_H interpolation discrepancy satisfies the existing numerical refinement standard;
6. no abundance network score/yield is evaluated in the mapping workflow.

After a successful mapping run, its run ID, artifact ID and exact file SHA256 values must be frozen into a superseding abundance execution input record **before** rerunning the abundance network. The old run `32243547025` remains valid evidence for the original H(T) mapping but is not silently relabelled as having the required endpoint coverage.

## Claim boundary

This protocol repairs numerical domain coverage only. It does not change B6 observational constraints, eta convention, nuclear rates, standard AlterBBN abundance cutoff, or any A1-A5/B4/B9/B10 objective. No BBN physics conclusion follows from a successful coverage-extension mapping by itself.
