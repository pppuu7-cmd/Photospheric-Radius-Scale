# RTK model development addendum — 2026-08-22 22:45 UTC

This append-only checkpoint records the reduction of the projected filtered-matter punctured-low-k rank problem from a generic 2x2 perturbation to one leading coefficient on the controlled flat-FLRW/homogeneous-lapse branch. It also records the exact matter-density rank scale and keeps all scope restrictions explicit.

## Heavy B9 branch

The frozen LCDM v7 base-Hessian run `32601673857` remains active at the time of this checkpoint. Pinned CLASS build, likelihood stack and Planck download/verification completed successfully; the exact Hessian step is still running. No threshold, center or stencil retuning is allowed while it runs.

The v7 target was forced by the v6 half-scale result: run `32596694426`, artifact `9482901186`, digest `sha256:afa2812d717b7121a0bb1922c34805948e6bdb68fa97b3dfdabeb3823c644fe6`, with exact improvement `0.02736801310379633 > 0.005` and non-PD Hessian.

## Low-k starting point already certified

Pure-gravity flat-FLRW punctured-rank baseline:
- run `32599000909`, artifact `9482349980`;
- digest `sha256:ac66d24d4e7a98bd99d6460020c1e4c3d6a8774a75949bd39acd37835e3715a6`;
- `b=-b2 q`, `c=+b2 q`, `d=O(q^2)`, `q=|k|^2`;
- `b2=2 eta0 P(d-1)/(d lambda-1)`;
- `det B_g=b2^2 q^2+O(q^3)`.

Neutral-RTK leading determinant immunity:
- run `32601725754`, artifact `9483068985`;
- digest `sha256:7b517639641a500e42491da4ee1db6f25c42940b3c96d044d35948405c5696f2`;
- neutral RTK can shift only `a={pi_N,Hperp}` directly at leading order;
- `B_RTK=q[[a2+r2,-b2],[b2,0]]+...`;
- leading determinant remains `b2^2 q^2` although `sigma_min` may change.

## Filtered-matter reduction

### 1. Symbolic rank/scale window

Run `32601855966`: SUCCESS after a purely symbolic-equality CI hardening.
Artifact `9483102433`, digest `sha256:ee42cf7f57a8a806266301da0fc625686f2b3bcce2f6adbe481a2523a8133b69`.

For a generic leading filtered matrix `E_m=K/M_c^2`, a sufficient low-k condition is `M_c^2>C_m/sigma_min(B_RTK)` with `C_m>=||K||_2`. Combined with the frozen 1% source-separation requirements, a conservative symbolic window is possible only if the rank lower edge lies below `k_local^2/99`. No `M_c` was selected.

### 2. Explicit one-over-Mc-squared scaling and e11=0

Run `32601901874`: SUCCESS.
Artifact `9483114541`, digest `sha256:4a3f171ade1a968ba13703a28f53efa10e36c7aafc466ff8ac9b7934bd39a8e2`.

On the regular `D_i nu=0` Fourier patch,

`a_eff=q/(M_c^2+q)=q/M_c^2+O(q^2/M_c^4)`.

Because the reduced ordinary-matter `Hperp_m=H0` is lapse-independent, the leading filtered correction has

`K=[[0,k12],[k21,k22]]`.

### 3. Action-level c21 coefficient

Hardened run `32602021860`: SUCCESS.
Artifact `9483144714`, digest `sha256:4911ee52705e8f0bb0cce69d720b0a8b8c520468e9e03f62a2651d4f64f81d25`.

On an isotropic gravity canonical background define

`delta H_g/delta pi^{ij}=V g_ij`,

`tau_H=g_ij delta H0/delta g_ij`.

Then

`delta c_m=(q/M_c^2) V(H0-tau_H)+O(q^2/M_c^4)`,

so

`k21=x=V(H0-tau_H)`.

### 4. Leading b-c chain relation

Run `32602065308`: SUCCESS.
Artifact `9483155960`, digest `sha256:9c74b61882d805a7e3fa2ca1263603a9cf0b4bbd8acfa09bf7e49a332c2e910e`.

On the explicitly stated homogeneous-lapse leading-chain support, modulo total momentum-constraint support,

`delta phi_m=N delta c_m`,

hence for `{pi_N,N}=-1`,

`delta b_m=-delta c_m`,

and therefore

`k12=-k21`.

This relation is not promoted to arbitrary inhomogeneous lapse backgrounds.

### 5. Flat-constraint k22 suppression

Run `32602249413`: SUCCESS.
Artifact `9483203753`, digest `sha256:c10628e771613f599455a8a56840b8ffdc70f308adb9d58804b673e5d0ae6130`.

Published exceptional-U(1) gravity has the sigma source proportional to

`2 Omega-eta0 R`

when `eta1=eta2=0`. On exactly spatially flat FLRW, `R=0`; after projection `a_eff(0)=0`, so `Jhat_background=0` requires `Omega=0` on this branch. Thus the first local scalar variation of `Jg` starts at `O(q)`.

Together with `Jm=O(q/M_c^2)`, `c_g=O(q)` and `c_m=O(q/M_c^2)`, and assuming local analytic Poisson kernels without inverse-q boundary singularities,

`delta d_m=O(q^2/M_c^2)`.

Therefore the leading `q/M_c^2` coefficient is

`k22=0`.

On this controlled branch the complete leading filtered matrix is therefore

`K=[[0,-x],[x,0]]`, `x=V(H0-tau_H)`.

## Exact leading determinant collapse

Run `32602296960`: SUCCESS.
Artifact `9483217289`, digest `sha256:8ad2519a6c90350e388b50904475165fd9dece9aaa6f664f86bcba08763e1f15`.

Combining the physical leading matrix above with the neutral-RTK baseline gives

`L=[[A,-(b+x/M_c^2)],[b+x/M_c^2,0]]`,

where `A=a2+r2` and `b=b2`.

Exactly,

`det L=(b+x/M_c^2)^2`.

Consequences:
- if `b*x>=0`, no positive `M_c^2` leading rank-loss root exists;
- if `b*x<0`, the unique positive root is `M_c^2=-x/b=|x|/|b|`;
- `M_c^2>|x|/|b|` is a conservative sign-independent root-avoidance bound.

The neutral-RTK conditioning coefficient `A` cancels from this leading determinant exactly.

## Exact cancellation of P and lambda in the rank scale

Run `32602413662`: SUCCESS.
Artifact `9483248976`, digest `sha256:100a58c082287ad553b15da9c591c384331c7cb64d7686149b512b80c5cab703`.

From the published Hamiltonian inverse-DeWitt metric,

`V=-4P/[M_Pl^2 sqrt(g)(d lambda-1)]`

for `pi^{ij}=P g^{ij}`. With

`b2=2 eta0 P(d-1)/(d lambda-1)`,

one obtains the exact ratio

`x/b2=-2(H0-tau_H)/[eta0(d-1)M_Pl^2 sqrt(g)]`.

Thus both `P` and `d lambda-1` cancel. Define

`rho_H=H0/sqrt(g)`, `tau_rho=tau_H/sqrt(g)`.

A conservative leading rank bound is

`M_c^2 > 2|rho_H-tau_rho|/[|eta0|(d-1)M_Pl^2]`.

This is independent of `P` and `lambda` within the stated branch.

## Perfect-fluid specialization and scalar sign cross-check

Run `32602456914`: SUCCESS.
Artifact `9483262275`, digest `sha256:f54beb90cf6f0347289b25d50e85bdf112cbd10feadab174c594a514bb95c6ff`.

For canonical isotropic perfect-fluid matter at fixed canonical variables,

`delta H0/delta g_ij=-sqrt(g) T^{ij}/2`,

so

`tau_H/sqrt(g)=-(d/2)p`.

Therefore

`M_c^2 > 2 rho |1+d w/2|/[|eta0|(d-1)M_Pl^2]`

for `p=w rho`.

For `d=3`, `eta0=1`:
- dust: `M_c^2>rho/M_Pl^2`;
- radiation: `M_c^2>(3/2)rho/M_Pl^2`;
- a vacuum-like ordinary matter component, if explicitly included in H0: `M_c^2>(1/2)rho/M_Pl^2` after absolute value.

An independent homogeneous canonical-scalar Hamiltonian calculation reproduces `tau_H/sqrt(g)=-(d/2)p_scalar`, fixing the sign convention.

## Finite punctured interval bridge

Run `32602344661`: SUCCESS.
Artifact `9483229696`, digest `sha256:4e4bab4ea8af6756c14070e54047f13e25c9e185e50e982d5ddeffd6f3f4a156`.

If the full reduced block is

`B(q)=q L+q^2 R(q)`, `||R(q)||_2<=C` for `0<=q<=q0`,

then

`sigma_min(L+qR)>=sigma_min(L)-qC`.

Hence a certified finite punctured interval is

`0<|k|<sqrt(min(q0,sigma_min(L)/C))`.

The next technical task is therefore to derive an action-level bound `C` for the subleading remainder; no arbitrarily dense numerical scan near zero is required if such a bound is available.

## Frozen H0 source scope

The frozen candidate explicitly separates

`ordinary_matter_H=[N-(A-Acal)]H0+...`

from the neutral RTK `P(X_U)+C(X_U)` sector. Therefore the `H0` entering the elliptic constraint is the ordinary universally coupled matter source. The neutral RTK scalar must not be double-counted into the density rank bound. A gravity-potential cosmological term is likewise not automatically an ordinary-matter `H0` contribution.

A dedicated multifluid source-scope gate has been launched to encode the linear sum over ordinary species and retain massive-neutrino `rho(a),p(a)` symbolically.

## Current frontier

The controlled flat-FLRW leading low-k rank problem is now reduced to a single ordinary-matter trace-response coefficient. Remaining classical tasks are:

1. certify the ordinary-matter species/source dictionary for the intended completed cosmology;
2. derive a uniform subleading remainder bound `C` and thus an explicit `epsilon`;
3. move to intermediate/high-k rank-loss analysis with the full elliptic symbol retained;
4. only after classical rank closure apply PPN, GW, cutoff/strong-coupling, compact-object and C9 naturalness gates to the same fixed action.

Exact `k=0` remains a background/source-cancellation mode, not a propagating-rank certificate.
