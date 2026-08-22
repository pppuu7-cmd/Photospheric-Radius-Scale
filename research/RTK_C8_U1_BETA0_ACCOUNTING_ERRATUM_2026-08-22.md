# RTK C8 U(1) beta0 bare/effective accounting erratum — 2026-08-22

Status: **CORRECTION / supersedes the v1 full-action beta0 interpretation**

## What was wrong

The earlier U(1) completion notes used the IR gravity convention

`L_V = 2 Lambda - beta0 a_i a^i + gamma1 R + ...`

inside

`S_g = (M_Pl^2/2) int N sqrt(g) [L_K-L_V+...]`,

so the bare gravity action contributes

`+(M_Pl^2/2) beta0_bare a_i a^i`.

They then matched the production RTK direct/rolling lapse-gradient strength `M_Pl^2` to this bare coefficient and wrote `beta0_RTK=2`.

That identification is valid only if the RTK mixed operator is being represented **effectively** by a single `a_i a^i` coefficient and is not also included explicitly.

The explicit U(1) candidate action used in C8 is instead

`S = S_U1-gravity + S_DBI + S_mix`,

with

`S_mix = int N sqrt(g) C D_i Theta_U D^i Theta_U`.

The independently CI-verified rolling-scalar acceleration theorem had already established that, on `q=nabla_perp Sigma_bar != 0`, exact RTK matching fixes

`C q^2 = K_pi/(2 M_K^2) = M_Pl^2`,

and that the **same** product multiplies the induced lapse-gradient term. Therefore `S_mix` itself already supplies the full production target coefficient `M_Pl^2`.

Using `beta0_bare=2` at the same time adds another `M_Pl^2` and double-counts the target strength.

## Correct full-action bookkeeping

For the explicit action `S_g+S_DBI+S_mix`,

`C_total = (M_Pl^2/2) beta0_bare + C q^2`.

With exact RTK matching `C q^2=M_Pl^2` and target `C_total=M_Pl^2`, the unique solution is

**`beta0_bare=0`.**

If the total coefficient is repackaged into a single effective Hořava-style parameter,

`(M_Pl^2/2) beta0_eff = C_total`,

then

**`beta0_eff,total=2`.**

The old simultaneous choice `beta0_bare=2` plus explicit `S_mix` instead gives

`C_total=2 M_Pl^2`,

or `beta0_eff,total=4`.

## Executable provenance

Corrected source commit: `ad101f043df9af55d179fedbbec55c29d5bb5e7b`.

Workflow: `.github/workflows/rtk-route-b-u1-beta0-bare-effective-accounting.yml`, commit `8196c83f6ac3db41b149e9b8efe7248324e0aa4c`.

First run `32566025602` failed for a technical SymPy-domain mistake: `beta_bare` had been declared strictly positive, excluding the physical zero solution. No physical equation was changed.

Corrected rerun `32566078375`: **success**.

Artifact `9474111029`, digest `sha256:f2f323b436a5aa63f59d1fe139766abda14173d160a791b4df46c546fd8d530f`.

Classification: `RTK_ROUTE_B_U1_BETA0_BARE_EFFECTIVE_ACCOUNTING_PASS`.

## Consequence for the frozen U(1) slice

`research/RTK_C8_U1_FAMILY1_FIXED_IR_SLICE_v1.json` is retained as historical provenance but is **withdrawn for full-action use** because its `beta0=2` field was interpreted as a bare gravity coefficient while `S_mix` was also explicit.

The corrected partial action slice is

`rtk-class-build:research/RTK_C8_U1_FAMILY1_FIXED_IR_SLICE_v2.json`,

with

- `a1=1`;
- `a2=0`;
- `kappa=1`;
- `sigma1=sigma2=0`;
- `beta0_bare=0`;
- `gamma1=-1`;
- `lambda_HL` intentionally still symbolic;
- explicit `S_mix` supplying `beta0_eff=2` on the rolling RTK background.

## PPN consequence

There is a narrow algebraic improvement but **not a PPN certification**.

At `a1=1`, `gamma1=-1`, the corrected bare value `beta0_bare=0` satisfies both displayed exact-GR bare-gravity relations in arXiv:1310.6666:

1. family I: `a1=kappa=1`;
2. family II: `sigma2=4(1-a1)=0`, `beta0=-2(gamma1+1)=0`.

However, the published PPN calculation does not contain the separate rolling RTK `S_mix` term whose lapse-gradient source is precisely the effect under study. Therefore those published GR-PPN formulae cannot be promoted to a full-action RTK PPN pass.

A fresh static/Newton/PPN derivation must retain `S_mix` explicitly.

## Consequence for C8 Hamiltonian work

All generic U(1)-invariance, velocity-support, `a2=0` canonical-affinity, primary-identity, Noether and block-reduction statements that do not rely on `beta0_bare=2` remain useful.

Any cross-block/secondary-rank interpretation that treated the old v1 tuple as the complete action must be re-evaluated on v2. In particular, the lapse-stability entry receives the explicit `S_mix` contribution while the bare gravity `beta0` term is absent.

This correction does not close or falsify the U(1) route. It removes a double count and makes the same-action bookkeeping stricter.
