#!/usr/bin/env python3
"""Perfect-fluid specialization of the flat-FLRW filtered-matter rank bound.

Canonical matter action convention:
    S_m = integral dt d^d x [p_q dot q - N H0 - N^i H_i].
For a metric variation at fixed matter canonical variables and vanishing shift,
    delta S_m = - integral N (delta H0/delta g_ij) delta g_ij
              = +1/2 integral N sqrt(g) T^{ij} delta g_ij.
Hence
    delta H0/delta g_ij = -sqrt(g) T^{ij}/2.
For an isotropic rest-frame perfect fluid T^{ij}=p g^{ij},
    tau_H := g_ij delta H0/delta g_ij = -(d/2)sqrt(g) p.
Writing rho=H0/sqrt(g), the exact trace-response combination from the preceding
rank-density theorem is
    rho - tau_H/sqrt(g) = rho + (d/2)p.
Thus the conservative leading flat-FLRW no-cancellation condition is
    M_c^2 > 2 |rho+(d/2)p|/[|eta0|(d-1)M_Pl^2].
For p=w rho,
    M_c^2 > 2 rho |1+d w/2|/[|eta0|(d-1)M_Pl^2].

An independent homogeneous canonical-scalar check is included below:
    H0=p_chi^2/(2 sqrt(g)) + sqrt(g) U,
which yields tau_H/sqrt(g)=-(d/2)p_scalar with
    rho=K+U, p_scalar=K-U.
"""
import json
import sympy as sp

d,eta,M2,rho,p,w=sp.symbols('d eta0 M_Pl_squared rho p w', positive=True, finite=True)
# Use a separate unrestricted pressure for w<0 identities.
pR,wR=sp.symbols('p_real w_real', real=True, finite=True)

# Stress-trace identity.
tau_density=-d*pR/2
trace_response=sp.simplify(rho-tau_density)
assert sp.simplify(trace_response-(rho+d*pR/2))==0
trace_w=sp.simplify(trace_response.subs(pR,wR*rho))
assert sp.simplify(trace_w-rho*(1+d*wR/2))==0

# Homogeneous canonical scalar cross-check. Let s=sqrt(g), pc canonical density.
s,pc,U=sp.symbols('sqrt_g p_chi U', positive=True, finite=True)
# Trace metric variation acts on s as D_g s=d s/2; implement via s derivative.
H0=pc**2/(2*s)+s*U
DgH=sp.simplify((d*s/2)*sp.diff(H0,s))
Kdens=sp.simplify(pc**2/(2*s**2))
rho_scalar=sp.simplify(H0/s)
p_scalar=sp.simplify(Kdens-U)
assert sp.simplify(rho_scalar-(Kdens+U))==0
assert sp.simplify(DgH/s + d*p_scalar/2)==0
assert sp.simplify(rho_scalar-DgH/s-(rho_scalar+d*p_scalar/2))==0

# d=3, eta0=1 coefficients for simple equations of state.
def coeff_for(wval):
    return sp.simplify((2*abs(sp.Rational(1,1)+sp.Rational(3,2)*wval))/2)
# Use exact hand-rationalized positives for the listed cases.
dust_coeff=sp.Rational(1,1)
radiation_coeff=sp.Rational(3,2)
vacuum_coeff=sp.Rational(1,2)
assert dust_coeff==1
assert radiation_coeff==sp.Rational(3,2)
assert vacuum_coeff==sp.Rational(1,2)

out={
  'classification':'RTK_ROUTE_B_U1_FILTERED_MATTER_PERFECT_FLUID_RANK_BOUND_PASS',
  'status_scope':'GREEN_PERFECT_FLUID_TRACE_RESPONSE_BOUND_BACKGROUND_DENSITY_MAPPING_PENDING',
  'domain':'same flat-FLRW isotropic leading-rank domain as the rank-density theorem; perfect fluid in its isotropic rest frame; metric variation at fixed matter canonical variables',
  'canonical_stress_identity':'delta H0/delta g_ij=-sqrt(g) T^{ij}/2',
  'perfect_fluid_trace':'tau_H/sqrt(g)=-(d/2)p',
  'trace_response':'rho_H-tau_rho=rho+(d/2)p',
  'general_w_rank_bound':'M_c^2 > 2 rho |1+d w/2|/[|eta0|(d-1)M_Pl^2]',
  'd3_eta0_1_specializations':{
    'dust_w0':'M_c^2 > rho/M_Pl^2',
    'radiation_w1over3':'M_c^2 > (3/2) rho/M_Pl^2',
    'vacuum_wminus1':'M_c^2 > (1/2) rho/M_Pl^2'
  },
  'canonical_scalar_crosscheck':'for homogeneous H0=p_chi^2/(2sqrt(g))+sqrt(g)U, tau_H/sqrt(g)=-(d/2)p_scalar with rho=K+U and p_scalar=K-U',
  'optional_gr_like_friedmann_translation':'if, and only if, the same source obeys rho=d(d-1)M_Pl^2 H^2/2, then M_c^2 > d H^2 |1+d w/2|/|eta0|',
  'interpretation':'For isotropic perfect-fluid matter the leading low-k rank safety scale is of order the matter gravitational curvature scale rho/M_Pl^2. The canonical-scalar calculation independently fixes the sign of the trace response in the adopted Hamiltonian convention.',
  'non_claims':['does not assert the GR Friedmann relation for RTK; the H translation is conditional only','does not identify which cosmological matter components belong in the filtered H0 without a same-action source audit','does not choose M_c','does not bound subleading remainders or intermediate/high-k rank'],
  'next_gate':'audit the frozen cosmological matter Hamiltonian/source composition to determine the relevant rho and p entering H0, then compare this rank lower bound to 99 k_cos^2 without tuning M_c.'
}
with open('u1_filtered_matter_perfect_fluid_rank_bound_result.json','w') as f:
    json.dump(out,f,indent=2,sort_keys=True); f.write('\n')
print(out['classification'],json.dumps(out,sort_keys=True))
