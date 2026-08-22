# RTK Formula Bible — C8 U(1) low-k rank reduction addendum

Updated: 2026-08-22 22:45 UTC
Status: canonical scoped continuation of the corrected elliptic-compensator Dirac method

## Scope

This note applies only after the exact auxiliary Dirac projection of `(p_Q,C_Lambda)` and only on the controlled special-U(1), flat-FLRW, regular `D_i nu=0` low-k Fourier patch stated below. It must not be generalized silently to curved, anisotropic, inhomogeneous-lapse or nonanalytic-boundary backgrounds.

Use

`q=|k|^2`,

`Jhat=Jg-a_eff H0`,

`a_eff=q/(M_c^2+q)`.

Exact `q=0` is a background/source-cancellation point; physical local rank is tested on `0<q<epsilon^2`.

## 1. Neutral-RTK baseline

The pure-gravity leading block is

`B_g=q[[a2,-b2],[b2,0]]+O(q^2)`,

`b2=2 eta0 P(d-1)/(d lambda-1)`.

Neutral RTK can directly shift only the `(1,1)` entry on the weak momentum-constraint support. Write

`delta a_RTK=r2 q+O(q^2)`.

Therefore

`B_RTK=q[[A,-b2],[b2,0]]+O(q^2)`, `A=a2+r2`,

and

`det B_RTK=b2^2 q^2+O(q^3)`.

The determinant is independent of `r2` at leading order, but `sigma_min` generally is not.

## 2. Filtered matter: source scaling

At low q,

`a_eff=q/M_c^2+O(q^2/M_c^4)`.

On the reduced regular slice,

`Hperp_m=H0`

is lapse-independent, hence the leading filtered correction has no `(1,1)` entry:

`Delta B_m=(q/M_c^2) K+...`,

`K=[[0,k12],[k21,k22]]`.

## 3. Isotropic c21 coefficient

On an isotropic canonical gravity background define

`delta H_g/delta pi^{ij}=V g_ij`,

`tau_H=g_ij delta H0/delta g_ij`.

For `q=g^{ij}k_i k_j`, the metric trace gives `D_g q=-q`. Then

`D_g(-a_eff H0)=M_c^2 q H0/(M_c^2+q)^2-q tau_H/(M_c^2+q)`.

Therefore

`delta c_m=(q/M_c^2) V(H0-tau_H)+O(q^2/M_c^4)`.

Define

`x := k21 = V(H0-tau_H)`.

## 4. Descendant-chain relation

On the homogeneous-lapse leading support, modulo total momentum-constraint terms, use

`phi_hat={Ghat,H_c}`

with the explicitly checked assumptions that the leading filtered `c_m` coefficient is lapse-independent and the remaining descendant terms are weak momentum support. Then

`delta phi_m=N delta c_m`,

and canonical `{pi_N,N}=-1` gives

`delta b_m=-delta c_m`.

Hence

`k12=-k21=-x`.

Do not export this relation to arbitrary inhomogeneous lapse backgrounds without a new gate.

## 5. Flat-constraint suppression of k22

Published special-U(1) gravity contains the sigma source

`(2 Omega-eta0 R+eta1 a^2+eta2 D a) sigma`.

On the scalar-removal branch `eta1=eta2=0`, exactly spatially flat FLRW has `R=0`. Since projected `a_eff(0)=0`, the background `Jhat=0` constraint requires `Omega=0` on this flat branch. Consequently the first local scalar variation of `Jg` begins at `O(q)`.

With

`Jg=O(q)`,

`Jm=O(q/M_c^2)`,

`c_g=O(q)`,

`c_m=O(q/M_c^2)`,

and local analytic Poisson kernels carrying no inverse-q singularity,

`delta d_m=N({Jg,c_m}+{Jm,c_g})+...=O(q^2/M_c^2)`.

Thus the `q/M_c^2` coefficient is

`k22=0`.

The complete leading filtered matrix is therefore

`K=[[0,-x],[x,0]]`.

This is the strongest currently certified leading-symbol statement and is scoped exactly as above.

## 6. Exact leading determinant

Combine

`B_RTK/q=[[A,-b],[b,0]]`, `b=b2`,

with

`Delta B_m/q=(1/M_c^2)[[0,-x],[x,0]]`.

Then

`L=[[A,-(b+x/M_c^2)],[b+x/M_c^2,0]]`

and exactly

`det L=(b+x/M_c^2)^2`.

Therefore:

- `b x >= 0` -> no positive `M_c^2` leading rank-loss root;
- `b x < 0` -> the unique positive root is `M_c^2=-x/b=|x|/|b|`;
- `M_c^2>|x|/|b|` is a sign-independent conservative root-avoidance condition.

The coefficient `A`, including the neutral-RTK leading correction, drops out of the leading determinant exactly.

## 7. Eliminate P and lambda from the rank scale

The published inverse DeWitt metric is

`G_ijkl=1/2(g_ik g_jl+g_il g_jk)-lambda/(d lambda-1) g_ij g_kl`.

For `pi^{ij}=P g^{ij}`,

`G_ijkl pi^{kl}=-P g_ij/(d lambda-1)`.

From the kinetic Hamiltonian,

`V=-4P/[M_Pl^2 sqrt(g)(d lambda-1)]`.

Together with

`b=2 eta0 P(d-1)/(d lambda-1)`,

we obtain

`x/b=-2(H0-tau_H)/[eta0(d-1)M_Pl^2 sqrt(g)]`.

Thus `P` and `d lambda-1` cancel exactly.

Define

`rho_H=H0/sqrt(g)`,

`tau_rho=tau_H/sqrt(g)`.

Then a conservative leading bound is

`M_c^2 > 2|rho_H-tau_rho|/[|eta0|(d-1)M_Pl^2]`.

## 8. Perfect-fluid source dictionary

For a canonical matter Hamiltonian varied at fixed matter canonical variables,

`delta H0/delta g_ij=-sqrt(g) T^{ij}/2`.

For an isotropic perfect fluid, `T^{ij}=p g^{ij}`, hence

`tau_rho=-(d/2)p`.

Therefore

`rho_H-tau_rho=rho+(d/2)p`.

For `p=w rho`,

`M_c^2 > 2 rho |1+d w/2|/[|eta0|(d-1)M_Pl^2]`.

For `d=3, eta0=1`:

- dust: `M_c^2>rho/M_Pl^2`;
- radiation: `M_c^2>(3/2)rho/M_Pl^2`;
- vacuum-like ordinary matter, if it is actually included in filtered `H0`: `M_c^2>(1/2)rho/M_Pl^2` after absolute value.

The homogeneous canonical-scalar Hamiltonian independently reproduces `tau_rho=-(d/2)p_scalar`.

## 9. Which rho belongs here

The frozen elliptic candidate defines

`ordinary_matter_H=[N-(A-Acal)]H0+...`

and separately retains the neutral RTK scalar `P(X_U)+C(X_U)`.

Therefore the density in the formulas above is the ordinary universally coupled matter density represented by the filtered `H0`. Do not include the neutral RTK scalar. Do not automatically include a cosmological term residing in gravity `L_V`; include vacuum energy only if the same completed action explicitly places it in the ordinary matter `H0`.

For independent filtered ordinary species,

`rho_H-tau_rho=sum_s[rho_s+(d/2)p_s]`.

A massive species must use its actual `rho_s(a),p_s(a)` through its relativistic transition.

## 10. From leading rank to a finite epsilon

Write the full reduced block as

`B(q)=q L+q^2 R(q)`.

If

`||R(q)||_2<=C` for `0<=q<=q0`,

then

`sigma_min(L+qR)>=sigma_min(L)-qC`.

Thus

`0<q<min(q0,sigma_min(L)/C)`

is sufficient, or

`0<|k|<sqrt(min(q0,sigma_min(L)/C))`.

This converts the remaining near-zero problem into deriving a uniform action-level remainder bound `C`; no arbitrary dense scan at k->0 is necessary.

## 11. Mandatory next steps

1. Freeze the ordinary-matter species/source composition for the intended completed action.
2. Derive/bound the `O(q^2)` remainder `C`, including the next elliptic-filter term, pure-gravity subleading operators and neutral-RTK subleading support.
3. Intersect the exact leading rank lower bound with the frozen 1% window:
   `M_c^2>=99 k_cos^2`, `M_c^2<=k_local^2/99`.
4. Keep `M_c` symbolic until the existence of the full classical window is established.
5. After low-k closure, inspect intermediate/high-k roots with the full elliptic symbol.
6. Only then proceed to PPN/local gravity, GW, cutoff/strong coupling, compact objects and C9 radiative stability on the same fixed action.

## Provenance highlights

- neutral-RTK leading determinant immunity: run `32601725754`, artifact `9483068985`, digest `sha256:7b517639641a500e42491da4ee1db6f25c42940b3c96d044d35948405c5696f2`;
- filtered scaling/e11 zero: run `32601901874`, artifact `9483114541`, digest `sha256:4a3f171ade1a968ba13703a28f53efa10e36c7aafc466ff8ac9b7934bd39a8e2`;
- c21: run `32602021860`, artifact `9483144714`, digest `sha256:4911ee52705e8f0bb0cce69d720b0a8b8c520468e9e03f62a2651d4f64f81d25`;
- b-c chain: run `32602065308`, artifact `9483155960`, digest `sha256:9c74b61882d805a7e3fa2ca1263603a9cf0b4bbd8acfa09bf7e49a332c2e910e`;
- k22 suppression: run `32602249413`, artifact `9483203753`, digest `sha256:c10628e771613f599455a8a56840b8ffdc70f308adb9d58804b673e5d0ae6130`;
- exact antisymmetric leading determinant: run `32602296960`, artifact `9483217289`, digest `sha256:8ad2519a6c90350e388b50904475165fd9dece9aaa6f664f86bcba08763e1f15`;
- finite-epsilon remainder bridge: run `32602344661`, artifact `9483229696`, digest `sha256:4e4bab4ea8af6756c14070e54047f13e25c9e185e50e982d5ddeffd6f3f4a156`;
- exact P/lambda cancellation: run `32602413662`, artifact `9483248976`, digest `sha256:100a58c082287ad553b15da9c591c384331c7cb64d7686149b512b80c5cab703`;
- perfect-fluid/scalar trace response: run `32602456914`, artifact `9483262275`, digest `sha256:f54beb90cf6f0347289b25d50e85bdf112cbd10feadab174c594a514bb95c6ff`.
