#!/usr/bin/env python3
"""Leading filtered-matter b=-c chain relation on a homogeneous-lapse patch.

This is deliberately scoped.  After exact auxiliary Dirac projection use

  H_c = N Hperp_hat + A Jhat + H_rest,
  Ghat = p_nu + Jhat,
  phi_hat = {Ghat,H_c}.

On the regular D_i nu=0 flat-FLRW Fourier-symbol patch, modulo the already
existing momentum constraint, assume at the leading filtered-matter order:
  * {Ghat,Jhat}=0;
  * {Ghat,H_rest} is weakly zero / belongs to momentum support;
  * {p_nu,Hperp_hat} is weakly zero in the neutral invariant-shift support;
  * the filtered-matter contribution c_m={Jhat,Hperp_hat}_m has no explicit
    homogeneous lapse dependence at its leading q/M_c^2 coefficient.

Then
  delta phi_m = N delta c_m,
and with canonical orientation {pi_N,N}=-1,
  delta b_m={pi_N,delta phi_m}=-delta c_m.

If
  delta c_m=(q/M_c^2) k21 + O(q^2),
then
  delta b_m=(q/M_c^2) k12 + O(q^2),  k12=-k21.

Combined with the separately proved e11=0, the leading filtered-matter matrix is
  K=[[0,-x],[x,y]], x=k21, y=k22.
Its Frobenius norm is sqrt(2 x^2+y^2), which is a sharper action-aware bound
than treating three entries as unrelated.

This theorem does not derive k22 and does not assert b=-c away from the stated
leading homogeneous-lapse support.
"""
import json
import sympy as sp

N,pN,c0,eps=sp.symbols('N pi_N c0 eps', real=True, finite=True)
# Minimal canonical pair for the multiplier orientation {F,G}=dF/dN dG/dpN-dF/dpN dG/dN.
def PB_N(f,g):
    return sp.simplify(sp.diff(f,N)*sp.diff(g,pN)-sp.diff(f,pN)*sp.diff(g,N))

# pi_N is the momentum coordinate pN.  Let delta phi=N*delta c with c lapse-independent.
delta_c=eps*c0
delta_phi=N*delta_c
delta_b=sp.simplify(PB_N(pN,delta_phi))
assert sp.simplify(delta_b+delta_c)==0
assert sp.diff(delta_c,N)==0

x,y=sp.symbols('x y', real=True, finite=True)
K=sp.Matrix([[0,-x],[x,y]])
frob_sq=sp.expand(sum(z**2 for z in K))
assert sp.simplify(frob_sq-(2*x**2+y**2))==0
# Exact spectral-norm squared from K^T K.
Gram=sp.expand(K.T*K)
tr=sp.expand(sp.trace(Gram)); det=sp.expand(Gram.det())
assert sp.simplify(tr-(2*x**2+y**2))==0
assert sp.simplify(det-x**4)==0

out={
  'classification':'RTK_ROUTE_B_U1_FILTERED_MATTER_BC_CHAIN_RELATION_PASS',
  'status_scope':'GREEN_CONDITIONAL_LEADING_B_MINUS_C_RELATION_K22_PENDING',
  'domain':'regular D_i nu=0 flat-FLRW leading Fourier-symbol patch, homogeneous lapse coefficient, modulo total momentum-constraint support',
  'chain_assumptions':[
    '{Ghat,Jhat}=0 at the stated support order',
    '{Ghat,H_rest} is weak momentum support',
    '{p_nu,Hperp_hat} is weak momentum support',
    'leading filtered-matter c_m coefficient is explicitly lapse-independent on the homogeneous background'
  ],
  'descendant_relation':'delta phi_m=N delta c_m at leading filtered-matter order',
  'bracket_relation':'delta b_m=-delta c_m for {pi_N,N}=-1',
  'coefficient_relation':'k12=-k21',
  'sparse_matrix':'K=[[0,-k21],[k21,k22]]',
  'frobenius_norm':'||K||_F=sqrt(2 k21^2+k22^2)',
  'gram_invariants':['tr(K^T K)=2 k21^2+k22^2','det(K^T K)=k21^4'],
  'interpretation':'Under the explicitly stated homogeneous-lapse leading-chain assumptions, the two off-diagonal filtered-matter coefficients are not independent. Together with the isotropic c21 theorem, k12 is fixed once V(H0-tau_H) is known; only k22 remains structurally undetermined at leading order.',
  'non_claims':[
    'does not prove the relation for arbitrary inhomogeneous lapse backgrounds or boundary conditions',
    'does not derive k22',
    'does not remove the need to use the RTK-shifted sigma_min baseline',
    'does not choose M_c or certify intermediate/high-k rank'
  ],
  'next_gate':'derive k22 from delta d_m={Jhat,phi_hat}_m using the same isotropic FLRW support and then form the exact two-parameter operator-norm bound.'
}
with open('u1_filtered_matter_bc_chain_relation_result.json','w') as f:
    json.dump(out,f,indent=2,sort_keys=True); f.write('\n')
print(out['classification'],json.dumps(out,sort_keys=True))
