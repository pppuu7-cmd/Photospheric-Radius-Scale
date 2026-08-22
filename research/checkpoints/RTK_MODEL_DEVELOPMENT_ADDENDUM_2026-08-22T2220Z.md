# RTK model development addendum — 2026-08-22 22:20 UTC

This append-only checkpoint records the zero-mode correction, the successful punctured-low-k rank gates, the hardened neutral-RTK leading-symbol result, and the mandatory B9 LCDM v7 recenter. It supersedes any earlier wording that could be read as using the exact flat-FLRW k=0 mode itself as a local propagating-rank certificate.

## Correct physical rank target

The exact spatially constant k=0 mode is retained for background/source-cancellation statements only. On spatially flat FLRW the local Fourier symbols of the published special-U(1) B block can vanish at exactly k=0. The physical classical scalar-rank target is therefore a punctured interval 0<|k|<epsilon, followed separately by intermediate/high-k analysis.

## Reduced coupled-Dirac chain already closed

- Reduced constraint-chain recovery: run `32598755378`, SUCCESS. Physical reduced basis `(pi_N,Jhat,Hperp_hat,phi_hat)` with the exact 4x4 Pfaffian reduction.
- Projected ordinary-matter k0 inheritance: run `32598821095`, SUCCESS. On the exact homogeneous source-rescue mode the direct ordinary-matter correction to the published B entries vanishes.
- Homogeneous neutral-RTK lapse affinity: run `32598892522`, SUCCESS; artifact `9482320046`; digest `sha256:aa81af83587bea6c67da37cf951a4362639199bbf8a933ad2ff9df4061d5ae3c`. On the regular homogeneous rolling slice the neutral RTK sector is lapse-affine after Legendre transform and its only previously allowed direct B-block correction vanishes at k=0.

These k=0 results are inheritance/source statements, not a rank certificate for the exact global zero mode.

## Pure-gravity punctured-low-k baseline

Run `32599000909`: SUCCESS.
Artifact `9482349980`.
Digest `sha256:ac66d24d4e7a98bd99d6460020c1e4c3d6a8774a75949bd39acd37835e3715a6`.

On flat homogeneous background with isotropic gravity momentum `pi^{ij}=P g^{ij}` and the special `eta1=eta2=0` U(1) branch,

`b=-B2 |k|^2`, `c=+B2 |k|^2`,

`B2=2 eta0 P(d-1)/(d lambda-1)`.

The other displayed supports give `a=O(|k|^2)`, `d=O(|k|^4)`, so

`det B_g=B2^2 |k|^4+O(|k|^6)`.

For `eta0!=0`, `P!=0`, `d>1`, `d lambda!=1`, continuity supplies a punctured interval `0<|k|<epsilon` with nonzero pure-gravity rank. Exactly k=0 remains separately degenerate as a local symbol.

## General low-k perturbation margin

Run `32599085426`: SUCCESS.
Artifact `9482371394`.
Digest `sha256:b229109fa72f89674fbf0f9e364120ee3dbebec623143200f49c6b26b6928d60`.

For

`B_g=|k|^2 B0+O(|k|^4)`, `B0=[[a2,-b2],[b2,0]]`,

and a coupled leading correction `Delta B=|k|^2 E0+O(|k|^4)`, a sufficient rank condition is

`||E0||_2 < sigma_min(B0)`.

If every entry obeys `|e_ij|<=eps0`, then `2 eps0<sigma_min(B0)` is sufficient. This is a sufficient margin theorem, not a claim that the physical E0 coefficients have already been bounded.

## Hardened neutral-RTK leading-symbol theorem

Run `32601725754`: SUCCESS.
Artifact `9483068985`.
Digest `sha256:7b517639641a500e42491da4ee1db6f25c42940b3c96d044d35948405c5696f2`.

The earlier exact neutral-RTK support theorem allows a direct correction only to

`a={pi_N,Hperp}`,

while `b,c,d` retain pure-gravity support weakly. The exact homogeneous gate gives `delta a_RTK(k=0)=0`; with the spatial-derivative mixed operator, the analytic leading correction can be written

`delta a_RTK=r2 |k|^2+O(|k|^4)`.

Therefore

`B_RTK=|k|^2 [[a2+r2,-b2],[b2,0]]+...`

and

`det B_RTK=b2^2 |k|^4+O(|k|^6)`

independently of arbitrary `r2`. Thus neutral RTK alone cannot destroy the leading punctured-low-k determinant through this direct channel.

Important hardening: this does **not** mean the singular-value margin is r2-independent. The Gram trace is `(a2+r2)^2+2b2^2`, so `sigma_min` generally changes. Any filtered-matter norm bound must use the RTK-shifted baseline matrix.

## Filtered-matter symbolic compatibility window

A new lightweight gate is active to combine the filtered-matter rank bound with the already frozen 1% source-separation window without selecting `M_c`.

If the action-derived leading filtered-matter matrix can be written `E_m=K/M_c^2` and `C_m>=||K||_2`, define

`R_rank=C_m/sigma_min(B_RTK)`.

Then a sufficient low-k rank condition is `M_c^2>R_rank`. Together with the already derived 1% requirements

`M_c^2>=99 k_cos^2`,

`M_c^2<=k_local^2/99`,

a nonempty symbolic window requires

`k_local/k_cos>=99`

and

`R_rank<k_local^2/99`.

The current gate proves this compatibility algebra only. The next physical calculation must derive or bound `C_m` from the frozen projected Hamiltonian and resolvent variation; no value of `M_c` is chosen here.

## B9 LCDM Planck-R3 lensing update

The preregistered v6 half-scale run `32596694426` completed successfully as a computation but failed the stationarity criterion:

- center `S_eff=1058.2447104245823`;
- best exact `S_eff=1058.2173424114785`;
- improvement `0.02736801310379633 > 0.005`;
- best label `cross_3_5_+1_+1`;
- Hessian not positive definite;
- minimum eigenvalue `-0.006081635538921822`.

Artifact `9482901186`, digest `sha256:afa2812d717b7121a0bb1922c34805948e6bdb68fa97b3dfdabeb3823c644fe6`.

This is a scientific/numerical descent result, not a CI failure. The frozen decision tree therefore forbids fresh-tree closure at the v6 center.

New target `research/robustness/B9_LCDM_RECENTER_TARGET_v7.json` is frozen at

- `As=2.099031119902081e-09`;
- `Ob=0.048406958808714234`;
- `Om=0.25869220161756795`;
- `h=0.6803133881531521`;
- `ns=0.9662859140870312`;
- `zre=7.684806125603674`;
- `lam=0`.

The threshold remains `0.005`; the base stencil is restored to scale `1.0`. Heavy base-Hessian run `32601673857` is active. No center/threshold tuning is allowed before it finishes.

## Immediate order

1. Let B9 v7 base-Hessian run to its frozen decision point; do not interfere with its objective or threshold.
2. Complete the lightweight filtered-matter symbolic rank-window gate.
3. Derive action-level leading filtered-matter `K` entries or a rigorous `C_m` bound from `Jhat=Jg-a_eff H0` and the exact resolvent variation.
4. Apply the resulting bound to the RTK-shifted low-k baseline; keep `M_c` symbolic.
5. Only after punctured-low-k coupled rank is certified, proceed to intermediate/high-k root/rank scans and then PPN/GW/cutoff/compact-object gates.
6. C9 technical naturalness remains open: the exceptional `eta1=eta2=0` gravity surface is not promoted to a technically natural completion without a protection/RG/tuning mechanism.
