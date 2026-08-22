# RTK Formula Bible — C8 U(1) completion addendum

Updated: 2026-08-22 22:20 UTC
Status: canonical correction/addition to the older U(1) completion appendix

## Preferred physical Dirac order

The preferred coupled completion sequence is now:

1. audit the actual mixed primary `G=p_nu+J_A,total`;
2. identify the genuine auxiliary second-class pair `(p_Q,C_Lambda)` with `C_Lambda=ell Q-H0`;
3. perform exact Dirac projection/elimination of that pair;
4. work with `Jhat=J_A,total-ell^{-1}C_Lambda=J_A^g-a_eff H0` and `Ghat=p_nu+Jhat`;
5. derive preservation of `pi_N` and `Ghat` to obtain the reduced physical chain `(pi_N,Jhat,Hperp_hat,phi_hat)`;
6. use exact k=0 only for background/source inheritance;
7. test propagating scalar rank on punctured finite-k modes `0<|k|<epsilon`;
8. prove a low-k perturbation margin around the published pure-gravity block;
9. then scan intermediate/high k for rank-loss roots;
10. only after classical rank closure confront PPN/local gravity, GW, cutoff/strong coupling, compact objects and C9 naturalness.

Do not select or fit `M_c` before the classical rank and scale-window conditions are established.

## Conditional 8x8 Schur result — retained but demoted

The earlier old-four plus auxiliary-four matrix theorem

`det M=det E det(O+X E^{-1}X^T)`

with `det E=ell^4` remains an exact algebraic identity for that assumed basis. It is **not** the preferred physical DOF proof because the actual primary `G` contains `Q`, so `{G,p_Q}=1` and the first Dirac consistency equations fix primary multipliers rather than automatically generating the old `phi_A` and `C_Q` as independent first-generation constraints.

The matrix identity may be used as a conditional algebraic lemma only.

## Exact auxiliary projection

For

`ell=1+k_phys^2/M_c^2>0`,

`C_Lambda=ell Q-H0`,

the pair `(p_Q,C_Lambda)` has an invertible bracket operator for every physical Fourier mode and `M_c>0`. Eliminating it gives

`Q=H0/ell`,

`a_eff=1-1/ell=k_phys^2/(M_c^2+k_phys^2)`,

`Jhat=J_A^g-a_eff H0`.

The auxiliary sector contributes zero physical DOF in the reduced support: the second-class pair removes one configuration DOF and the remaining `p_Lambda` multiplier constraint is first class/trivial in the reduced auxiliary sector.

## Exact resolvent variation

For

`L=1-D^2/M_c^2`,

with `-D^2` nonnegative self-adjoint under the chosen boundary conditions,

`||L^{-1}||<=1`,

`delta L^{-1}=-L^{-1}(delta L)L^{-1}`,

`delta a_eff=-(1/M_c^2)L^{-1}[delta(D^2)]L^{-1}`,

and therefore

`||delta a_eff||<=||delta(D^2)||/M_c^2`.

This identity is the route for action-level bounds on the finite-k metric cross-brackets. A Fourier-symbol replacement of `a_eff` by a c-number is allowed only in the explicitly stated translationally invariant patch and cannot replace the functional metric-variation calculation.

## Zero-mode correction

On exactly flat homogeneous FLRW with exactly constant smearing, the local Fourier symbols of the special-U(1) B block can vanish. Therefore:

- exact `k=0` is valid for demonstrating homogeneous source cancellation and inheritance;
- exact `k=0` is **not** a stand-alone local propagating-DOF rank certificate;
- the physical local rank problem is `0<|k|<epsilon`, followed by the `k->0+` limit.

This correction supersedes any earlier inference of rank solely from `B_total(k=0)=B_gravity` plus a generic published nonzero-rank statement.

## Punctured-low-k baseline

On flat homogeneous background with `pi^{ij}=P g^{ij}`,

`B_g(k)=|k|^2 B0+O(|k|^4)`,

`B0=[[a2,-b2],[b2,0]]`,

`b2=2 eta0 P(d-1)/(d lambda-1)`.

For `b2!=0`,

`det B_g=b2^2 |k|^4+O(|k|^6)`,

so analyticity/continuity gives a punctured low-k interval with nonzero pure-gravity rank.

Run `32599000909`, artifact `9482349980`, digest `sha256:ac66d24d4e7a98bd99d6460020c1e4c3d6a8774a75949bd39acd37835e3715a6`.

## Neutral RTK leading support

The neutral invariant-shift RTK theorem permits a direct correction only to the `(1,1)` entry `a={pi_N,Hperp}` weakly; `b,c,d` remain pure gravity. Homogeneous lapse affinity gives `delta a_RTK(k=0)=0`, so in an analytic spatial-derivative expansion write

`delta a_RTK=r2 |k|^2+O(|k|^4)`.

Then

`B_RTK=|k|^2 [[a2+r2,-b2],[b2,0]]+...`

and

`det B_RTK=b2^2 |k|^4+O(|k|^6)`.

Run `32601725754`, artifact `9483068985`, digest `sha256:7b517639641a500e42491da4ee1db6f25c42940b3c96d044d35948405c5696f2`.

Important: determinant immunity does not imply condition-number immunity. `sigma_min` depends on `A=a2+r2`; all filtered-matter norm inequalities must use the RTK-shifted leading matrix.

## General perturbation margin

For a leading correction `E0`, a sufficient condition is

`||E0||_2<sigma_min(B_baseline)`.

For the pure-gravity parameterization,

`sigma_min^2=(a2^2+2b2^2-|a2|sqrt(a2^2+4b2^2))/2`.

After neutral RTK, replace `a2` by `a2+r2` in this expression. If `|e_ij|<=eps0`, then `2 eps0<sigma_min` is sufficient.

Run `32599085426`, artifact `9482371394`, digest `sha256:b229109fa72f89674fbf0f9e364120ee3dbebec623143200f49c6b26b6928d60`.

## Symbolic M_c compatibility strategy

The next action-derived task is to write or bound the leading filtered-matter correction as

`E_m=K/M_c^2`,

with `C_m>=||K||_2`. Then

`M_c^2>C_m/sigma_min(B_RTK)`

is a sufficient low-k rank condition.

Combine this with the already established 1% source-separation window

`M_c^2>=99 k_cos^2`,

`M_c^2<=k_local^2/99`.

The symbolic compatibility test is performed before choosing `M_c`. The action-derived `K` or `C_m` remains pending; no parameter fit may substitute for it.
