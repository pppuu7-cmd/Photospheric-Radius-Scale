#!/usr/bin/env python3
"""Flat-FLRW minisuperspace source-sign gate for the same U(1)+RTK action.

On homogeneous flat FLRW:
- K_ij=H_N g_ij, K=d H_N, H_N=dot a/(a N);
- all a_i and spatial-curvature UV terms vanish;
- homogeneous RTK S_mix has D_i Theta=0;
- the elliptic ordinary-matter compensator reduces at k=0 to the ordinary N H0 source after its auxiliary constraints;
- the U(1) A constraint requires the flat gauge-curvature source Omega=0 on this branch.

Thus the lapse-dependent minisuperspace kinetic term is fixed by
K_ij K^ij-lambda K^2=d(1-d lambda)H_N^2.  Adding a bare potential cosmological term and the total homogeneous matter/RTK energy density rho_src, lapse variation gives
  [d(d lambda-1)/2] M_Pl^2 H^2 = rho_src + M_Pl^2 Lambda_bare.
For d=3 this is (3/2)(3 lambda-1) M_Pl^2 H^2=rho_eff.
"""
import json
import sympy as sp

d,lam,M,a,adot,N,Lambda,rho=sp.symbols('d lambda M_Pl a adot N Lambda_bare rho_src', positive=True, finite=True)
# lambda is re-declared below as a real symbol for sign statements; symbolic derivation first.
lamr=sp.symbols('lambda', real=True, finite=True)
HN=adot/(a*N)
LK=sp.expand(d*(1-d*lamr)*HN**2)
Lg=sp.expand(M**2/sp.Integer(2)*N*a**d*(LK-2*Lambda))
# Matter lapse derivative at fixed canonical/background state is -a^d rho.
dLg_dN=sp.simplify(sp.diff(Lg,N))
constraint=sp.factor((dLg_dN-a**d*rho)/a**d)
expected=sp.factor(d*(d*lamr-1)*M**2*HN**2/sp.Integer(2)-M**2*Lambda-rho)
assert sp.simplify(constraint-expected)==0
# At N=1 define H=adot/a.
H=sp.symbols('H', positive=True, finite=True)
constraint_H=sp.factor(expected.subs({N:1,adot:H*a}))
assert sp.simplify(constraint_H-(d*(d*lamr-1)*M**2*H**2/sp.Integer(2)-M**2*Lambda-rho))==0

out={
  'classification':'RTK_ROUTE_B_U1_FLAT_FLRW_LAMBDA_SOURCE_SIGN_PASS',
  'status_scope':'GREEN_CONDITIONAL_COSMOLOGICAL_SIGN_OBSTRUCTION_FOR_LAMBDA_LT_1_OVER_3',
  'domain':'homogeneous flat FLRW same-action minisuperspace after auxiliary reduction; no spatial gradients; expanding/contracting H^2>0',
  'exact_constraint_d':'[d(d lambda-1)/2] M_Pl^2 H^2 = rho_src + M_Pl^2 Lambda_bare',
  'exact_constraint_d3':'(3/2)(3 lambda-1) M_Pl^2 H^2 = rho_src + M_Pl^2 Lambda_bare',
  'positive_source_consequence':'If H^2>0 and rho_src+M_Pl^2 Lambda_bare>0, then lambda>1/3 is necessary.',
  'negative_branch_consequence':'For lambda<1/3 and H^2>0 the total homogeneous source rho_src+M_Pl^2 Lambda_bare must be negative.',
  'rank_domain_intersection':'Therefore the previously proved simple all-q rank-safe domain lambda<1/3 is disjoint from a flat FLRW branch with positive total homogeneous source. The rank theorem remains mathematically valid but is not by itself a viable positive-energy cosmological branch.',
  'interpretation':'Physical same-action cosmology redirects the finite-q rank search to lambda>1/3 unless the model deliberately realizes a negative total homogeneous source, which would require a separate stability/phenomenology justification.',
  'non_claims':[
    'does not assert every individual RTK or bare-Lambda contribution is positive',
    'does not exclude exotic negative-total-source branches by algebra alone',
    'does not prove lambda>1/3 is sufficient for cosmological stability or observations',
    'does not choose lambda or modify the frozen B9 phenomenological parameter lambda_D'
  ],
  'next_gate':'classify det B(q)=F(q)^2+a(q)d(q) on the cosmologically relevant lambda>1/3 branch; derive sign or discriminant bounds that can protect det B from zero even though the DeWitt trace direction is indefinite.'
}
open('u1_flat_flrw_lambda_source_sign_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
