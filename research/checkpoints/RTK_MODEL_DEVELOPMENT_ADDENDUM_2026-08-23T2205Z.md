# RTK model development checkpoint — 2026-08-23 22:05 UTC

Status: **CURRENT DURABLE CHECKPOINT — supersedes the 21:55 UTC checkpoint where interpretations conflict**

## New verified results

### 1. Exact nonlinear conformal n=2 carrier

- run `32669082828` — GREEN
- artifact `9500857844`
- digest `sha256:efec6f70955d98f4dffd725038e1818563d70c8273a1b039b4e8237450a39b31`

For `sqrt(gamma) D_iR3 D^iR3` on `gamma_ij=a^2 exp(2zeta)delta_ij`, exact scalar expansion through quartic order is now executable.  The momentum kernels are known explicitly.

Key elastic COM results:

`K4=320 k^6(9-2 cos^2 theta)`;

`K3_s=-96 k^6`;

`K3_t=-32 k^6[4c^3+4c^2-31c+26]`;

`K3_u=32 k^6[4c^3-4c^2-31c-26]`.

All three cubic channel kernels are nonzero on the physical angular interval in the bare conformal sector.

### 2. Mandatory correction to n=2 UV optimism

- run `32669380424` — GREEN
- artifact `9500930355`
- digest `sha256:e3ad2e22dfb28e2d8e8a949b188f25115ab9067104c3caa9000428e3c6cd1f4b`

The exact elastic s-channel has internal spatial momentum `q_s=0` but nonzero `K3_s`.  Therefore the earlier all-hard-leg power count does not control this channel.

For the fixed-lapse bare conformal sector:

`g a0_s = -9 H^2 k^10 sqrt(Z)/[128 pi K M_U^8 c_a N^(5/2) D]`,

with

`N=1+k^4/M_U^4`,

`Z=1+k^2/M_K^2`,

`D=1+2k^4/(M_U^4+k^4)-k^2/(M_K^2+k^2)`.

Limits:

- `M_U<<k<<M_K`: `g a0_s -> -3 H^2 M_U^2/(128 pi K c_a)` — constant/marginal;
- `k>>M_K,M_U`: `g a0_s -> -9 H^2 M_U^2 k/(256 pi K c_a M_K)` — grows linearly.

**Interpretation change:** n=2 is YELLOW / conditional, not promoted or preferred solely from the earlier `k^-1` generic power count.  The decisive next test is whether full lapse/shift plus carrier-coefficient perturbations cancel the soft-s cubic vertex.

### 3. O(4) resolvent source maps to one new generalized potential

- run `32669251516` — GREEN
- artifact `9500899658`
- digest `sha256:1cff1ef2e6d3af26af1640a3dcb31c8f4aa18a0091fd5e2a8f0ce1015a840810`

Using the published projectable O(4) equation, define `S_res` as the additive single-resolvent source.  Then on `a1=1`:

`-2 Delta delta A4=S_res`,

`delta h00=-Delta^-1 S_res`.

Define

`Psi_res=-Delta^-1 S_res`.

The exact kernel is non-separable in output and internal momenta:

`partial_m partial_x log|K_res|=4mx/(m^2+x^2)^2>0`.

Thus for arbitrary extended sources `Psi_res` is generically a new mode-mixing potential, not a constant shift of beta or alpha2.  It vanishes in the local-parent `M_c/k->0` limit.

## Current corrected status table

| Sector | Status |
|---|---|
| Corrected auxiliary Dirac order | ✅ GREEN |
| Flat-FLRW punctured low-k leading rank | ✅ GREEN scoped |
| Static O(2) finite-Mc transfer | ✅ GREEN |
| O(3) alpha1 + preferred-frame combination | ✅ GREEN scoped |
| O(4) single-resolvent structure | ✅ GREEN |
| O(4) source -> Psi_res mapping | ✅ GREEN |
| Source-specific/full O(4) observable solve | 🟡 YELLOW |
| Exact P(X)-only partial-wave cutoff | ✅ GREEN scoped |
| B9 k safety relative to that cutoff | ✅ GREEN |
| Intrinsic-curvature quadratic carrier | ✅ GREEN scoped |
| n=2 bare conformal Q3/Q4 kernels | ✅ GREEN scoped |
| Generic all-hard n=2 UV power count | ✅ algebraically GREEN in scope |
| Full-channel n=2 UV sufficiency | 🟡 YELLOW after soft-s correction |
| Full lapse/shift/state-function n=2 reduction | ❌ open |
| Mixed C(X)+metric/U1/auxiliary unitarity | ❌ open |
| Technical naturalness / RG protection | ❌ open |
| Compact objects / universal horizons | ❌ open |

## Immediate continuation queue

1. **UV decisive gate:** derive cubic lapse/shift constraints with the n=2 carrier and a fully specified nonlinear `alpha6` completion; test directly whether the reduced `q_s=0` cubic vertex cancels.
2. If it survives, quantify its coefficient over the frozen background and compare n=2 with higher-order or symmetry-protected carriers instead of forcing n=2.
3. **O(4) parallel gate:** evaluate `S_res` and `Psi_res` for the already-audited uniform sphere, then solve the modified `A4` equation and derive a source-specific acceleration/redshift observable.
4. Only after these structural gates intersect rank/PPN/UV windows; do not choose `M_c` or `M_U` through a fit.
5. Technical naturalness and strong-field sectors remain mandatory before any claim of a complete theory.

Canonical correction: `research/methods/RTK_FORMULA_BIBLE_C9_N2_SOFT_S_O4_CORRECTION_2026-08-23T2205Z.md`.
