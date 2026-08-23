#!/usr/bin/env python3
"""Generic matter-Poisson extension to d={Jhat,phi_hat} on flat FLRW.

Let Jm=-a(g) H0(g,z) with matter canonical variables z and let K_g(g,pi) be
the gravity kinetic Hamiltonian. On the reduced flat support where
{Jm,H0}_matter=0, the descendant from the kinetic channel is
  phi = (D_g J) . K_pi.
Then
  {J,phi} = (D_gJ) K_pipi (D_gJ)
            + {Jm,D_gJm}_matter . K_pi.
Because
  D_gJm=-(D_g a)H0-a D_gH0,
bilinearity and {H0,H0}=0 give exactly
  {Jm,D_gJm}_m = a^2 {H0,D_gH0}_m.
For isotropic K_pi^{ij}=V g^{ij}, the extra term is
  d_extra=a_eff^2 V {H0,tau_H}_m,
where tau_H=g_ij delta H0/delta g_ij.
Thus the barotropic/commuting-response DeWitt-square theorem is recovered when
{H0,tau_H}_m=0, while the generic leading q^2 correction is explicitly known.
"""
import json
import sympy as sp

# A concrete canonical representative verifies the structural PB identity for
# arbitrary independent quadratic coefficients; the identity itself follows
# from PB bilinearity and metric-only a,Da.
q,p=sp.symbols('q_m p_m', real=True, finite=True)
a,Da=sp.symbols('a_eff Dg_a_eff', real=True, finite=True)
u1,u2,t1,t2=sp.symbols('u1 u2 t1 t2', real=True, finite=True)
H=sp.expand(u1*p**2/2+u2*q**2/2)
T=sp.expand(t1*p**2/2+t2*q**2/2)  # representative D_g H0 component/trace response

def PB(f,g):
    return sp.simplify(sp.diff(f,q)*sp.diff(g,p)-sp.diff(f,p)*sp.diff(g,q))
Jm=-a*H
DgJm=-Da*H-a*T
lhs=sp.expand(PB(Jm,DgJm))
rhs=sp.expand(a**2*PB(H,T))
assert sp.simplify(lhs-rhs)==0

# Low-q expansion of a_eff^2.
Q,M2=sp.symbols('Q M_c_squared', positive=True, finite=True)
aeff=Q/(M2+Q)
lead=sp.simplify(sp.limit(aeff**2/Q**2,Q,0,dir='+'))
assert sp.simplify(lead-1/M2**2)==0

out={
  'classification':'RTK_ROUTE_B_U1_FILTERED_MATTER_GENERIC_D_POISSON_EXTENSION_PASS',
  'status_scope':'GREEN_EXACT_GENERIC_MATTER_POISSON_STRUCTURE_BACKGROUND_BRACKET_VALUE_PENDING',
  'domain':'Dirac-projected flat homogeneous support with Jm=-a_eff H0, gravity kinetic channel K_g, and isotropic K_pi^{ij}=V g^{ij} for the scalar trace reduction',
  'exact_identity':'{Jm,D_gJm}_matter=a_eff^2 {H0,D_gH0}_matter',
  'isotropic_extra_d':'d_extra=a_eff^2 V {H0,tau_H}_matter',
  'lowk_extra_d':'d_extra=(q^2/M_c^4) V {H0,tau_H}_matter+O(q^3/M_c^6)',
  'barotropic_limit':'If {H0,tau_H}_matter=0, the extra term vanishes and the total d4 is exhausted by the DeWitt-square gate.',
  'interpretation':'Generic matter does not introduce an arbitrary new d4 function: beyond the DeWitt square there is one explicit matter-Poisson response scalar V{H0,tau_H}/M_c^4 at q^2.',
  'non_claims':[
    'does not assert {H0,tau_H}=0 for generic canonical matter',
    'does not evaluate the bracket for massive neutrinos or interacting species',
    'does not include anisotropic-stress tensor responses',
    'does not choose M_c'
  ],
  'next_gate':'evaluate {H0,tau_H} for canonical scalar and barotropic fluid representatives, then include this explicit scalar in the generic q^2 remainder norm.'
}
open('u1_filtered_matter_generic_d_poisson_extension_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
