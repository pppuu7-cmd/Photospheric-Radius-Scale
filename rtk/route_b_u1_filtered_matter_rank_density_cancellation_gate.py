#!/usr/bin/env python3
"""Exact cancellation of P and lambda in the flat-FLRW leading rank ratio.

Published special-U(1) Hamiltonian input (Mukohyama et al., arXiv:1504.07357):
  G_ijkl = 1/2(g_ik g_jl+g_il g_jk) - lambda/(d lambda-1) g_ij g_kl,
  H_g,kin = 2/(M_Pl^2 sqrt(g)) pi^{ij} G_ijkl pi^{kl}.

For the isotropic canonical background pi^{ij}=P g^{ij},
  G_ijkl pi^{kl} = -P/(d lambda-1) g_ij,
so
  delta H_g/delta pi^{ij} = V g_ij,
  V = -4P/[M_Pl^2 sqrt(g)(d lambda-1)].

The already verified flat-FLRW pure-gravity cross-block coefficient from the
published Eqs. (56)-(57) is
  b2 = 2 eta0 P(d-1)/(d lambda-1).

The filtered-matter c21 theorem gives
  x=k21=V(H0-tau_H).
Therefore
  x/b2 = -2(H0-tau_H)/[eta0(d-1)M_Pl^2 sqrt(g)],
with exact cancellation of P and d lambda-1.

The conservative leading no-cancellation condition M_c^2>|x|/|b2| becomes
  M_c^2 > 2 |rho_H-tau_rho|/[|eta0|(d-1)M_Pl^2],
where rho_H=H0/sqrt(g), tau_rho=tau_H/sqrt(g).

No value of M_c is selected here.
"""
import json
import sympy as sp

P,lam,d,eta0,Mpl2,sqrtg,H0,tau=sp.symbols(
    'P lambda d eta0 M_Pl_squared sqrt_g H0 tau_H',
    real=True, finite=True, nonzero=True
)

# Isotropic inverse-DeWitt contraction coefficient.
Giso=sp.simplify(P*(1-d*lam/(d*lam-1)))
assert sp.simplify(Giso + P/(d*lam-1))==0
V=sp.simplify(4*Giso/(Mpl2*sqrtg))
Vexpected=-4*P/(Mpl2*sqrtg*(d*lam-1))
assert sp.simplify(V-Vexpected)==0

b2=sp.simplify(2*eta0*P*(d-1)/(d*lam-1))
x=sp.simplify(V*(H0-tau))
ratio=sp.simplify(x/b2)
expected_ratio=-2*(H0-tau)/(eta0*(d-1)*Mpl2*sqrtg)
assert sp.simplify(ratio-expected_ratio)==0
assert sp.diff(ratio,P)==0
assert sp.diff(ratio,lam)==0

# Density variables merely remove the common sqrt(g) from H0 and tau_H.
rhoH,tauR=sp.symbols('rho_H tau_rho', real=True, finite=True)
ratio_density=sp.simplify(expected_ratio.subs({H0:rhoH*sqrtg,tau:tauR*sqrtg}))
assert sp.simplify(ratio_density + 2*(rhoH-tauR)/(eta0*(d-1)*Mpl2))==0

out={
  'classification':'RTK_ROUTE_B_U1_FILTERED_MATTER_RANK_DENSITY_CANCELLATION_PASS',
  'status_scope':'GREEN_FLAT_FLRW_EXACT_P_LAMBDA_CANCELLATION_MATTER_TRACE_RESPONSE_PENDING',
  'domain':'exceptional eta1=eta2=0 U(1) branch; flat FLRW; pi^{ij}=P g^{ij}; P!=0; d lambda!=1; eta0!=0; same canonical normalization as published Hamiltonian and verified pure-gravity low-k gate',
  'published_hamiltonian_input':'H_g,kin=2 pi^{ij}G_ijkl pi^{kl}/(M_Pl^2 sqrt(g)), G_ijkl isotropic contraction=-P g_ij/(d lambda-1)',
  'isotropic_velocity':'V=-4P/[M_Pl^2 sqrt(g)(d lambda-1)]',
  'pure_gravity_offdiagonal':'b2=2 eta0 P(d-1)/(d lambda-1)',
  'filtered_coefficient':'x=V(H0-tau_H)',
  'exact_ratio':'x/b2=-2(H0-tau_H)/[eta0(d-1)M_Pl^2 sqrt(g)]',
  'density_ratio':'x/b2=-2(rho_H-tau_rho)/[eta0(d-1)M_Pl^2], rho_H=H0/sqrt(g), tau_rho=tau_H/sqrt(g)',
  'conservative_rank_bound':'M_c^2 > 2|rho_H-tau_rho|/[|eta0|(d-1)M_Pl^2]',
  'cancellations':['P cancels exactly','d lambda-1 cancels exactly; leading rank bound is lambda-independent within this scoped branch'],
  'interpretation':'On the controlled flat-FLRW isotropic branch, the leading filtered-matter rank safety scale is set by a matter Hamiltonian trace-response divided by M_Pl^2, not by the background gravitational momentum P or the Hořava lambda parameter.',
  'non_claims':['does not yet evaluate tau_rho for a specific matter species','does not choose M_c','does not bound O(k^4) remainders','does not certify curved/anisotropic backgrounds or intermediate/high-k rank'],
  'next_gate':'evaluate rho_H-tau_rho for canonical perfect-fluid/dust/radiation/scalar matter sectors at fixed canonical variables; determine whether the bound reduces to a simple rho,p combination and compare symbolically with the 1% scale window.'
}
with open('u1_filtered_matter_rank_density_cancellation_result.json','w') as f:
    json.dump(out,f,indent=2,sort_keys=True); f.write('\n')
print(out['classification'],json.dumps(out,sort_keys=True))
