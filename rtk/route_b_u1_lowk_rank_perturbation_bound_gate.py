#!/usr/bin/env python3
"""Sufficient low-k rank-stability theorem for the reduced U(1) cross block.

The flat-FLRW pure-gravity special-branch symbol has

    B_g(k)=k^2 B0 + O(k^4),
    B0=[[a2,-b2],[b2,0]],

where b2=2 eta0 P(d-1)/(d lambda-1) is nonzero on the regular expanding branch;
a2 contains the IR lapse-gradient potential coefficient and is arbitrary for
the rank argument.  Coupled filtered-matter/RTK terms can be organized as

    Delta B(k)=k^2 E0 + O(k^4).

A standard singular-value perturbation theorem gives a clean sufficient
condition that does not assume any entry of E0 vanishes:

    ||E0||_2 < sigma_min(B0).

Then B0+E0 is invertible and, by continuity, the full B(k) is invertible on a
punctured interval 0<|k|<epsilon.  If every entry of E0 is bounded by eps0,
||E0||_2 <= ||E0||_F <= 2 eps0, so 2 eps0<sigma_min(B0) is sufficient.

This theorem is the bridge between the exact resolvent bound and the physical
finite-k Pfaffian: the next calculation only has to bound the four scaled
correction coefficients, not solve the full nonlinear determinant globally.
"""
import json
import sympy as sp

a,b=sp.symbols('a2 b2', real=True, finite=True)
# b != 0 is a physical regularity condition recorded in output, not a SymPy
# assumption needed for the algebraic identities.
B0=sp.Matrix([[a,-b],[b,0]])
Gram=sp.simplify(B0.T*B0)
tr=sp.expand(sp.trace(Gram))
det=sp.expand(Gram.det())
assert sp.simplify(tr-(a**2+2*b**2))==0
assert sp.simplify(det-b**4)==0

disc=sp.factor(tr**2-4*det)
assert sp.simplify(disc-a**2*(a**2+4*b**2))==0
# Formal positive expression for the smaller squared singular value.
abs_a=sp.symbols('abs_a', nonnegative=True, finite=True)
smin2=sp.simplify((a**2+2*b**2-abs_a*sp.sqrt(a**2+4*b**2))/2)
# Substitute abs_a^2=a^2 to verify the two eigenvalue roots solve the Gram
# characteristic polynomial.
lam=sp.symbols('s2', finite=True)
char=sp.expand(lam**2-tr*lam+det)
root_minus=(a**2+2*b**2-abs_a*sp.sqrt(a**2+4*b**2))/2
check=sp.expand(char.subs(lam,root_minus)).subs(abs_a**2,a**2)
assert sp.simplify(check)==0

# Exact determinant with a generic leading correction matrix.
e11,e12,e21,e22=sp.symbols('e11 e12 e21 e22', real=True, finite=True)
E=sp.Matrix([[e11,e12],[e21,e22]])
Blead=B0+E
det_lead=sp.expand(Blead.det())
assert sp.simplify(det_lead-((a+e11)*e22-(-b+e12)*(b+e21)))==0

# Neumann/singular-value sufficient condition is recorded analytically.  For an
# entrywise bound eps0, Frobenius norm <=2 eps0 for a 2x2 matrix.
eps0=sp.symbols('eps0', nonnegative=True, finite=True)
frob_upper=2*eps0

out={
  'classification':'RTK_ROUTE_B_U1_LOWK_RANK_PERTURBATION_BOUND_PASS',
  'status_scope':'GREEN_EXACT_SUFFICIENT_LOWK_RANK_BOUND_PHYSICAL_CORRECTION_COEFFICIENTS_PENDING',
  'baseline':'B_g(k)=|k|^2 B0+O(|k|^4), B0=[[a2,-b2],[b2,0]]',
  'baseline_b2':'2 eta0 P(d-1)/(d lambda-1)',
  'baseline_regular_conditions':['b2 != 0','equivalently eta0*P*(d-1)/(d lambda-1) != 0'],
  'sigma_min_squared':'(a2^2+2 b2^2-|a2| sqrt(a2^2+4 b2^2))/2',
  'coupled_expansion':'Delta B(k)=|k|^2 E0+O(|k|^4)',
  'exact_corrected_leading_determinant':'(a2+e11)e22-(-b2+e12)(b2+e21)',
  'sufficient_operator_norm_condition':'||E0||_2 < sigma_min(B0)',
  'entrywise_sufficient_condition':'if |e_ij|<=eps0 for all four entries, then 2 eps0 < sigma_min(B0) is sufficient because ||E0||_2<=||E0||_F<=2 eps0',
  'punctured_interval_consequence':'Under the strict leading-matrix bound and analytic/local higher-spatial-derivative expansion, there exists epsilon>0 with det B(k)!=0 for 0<|k|<epsilon.',
  'resolvent_bridge':'Use ||delta a_eff|| <= ||delta(D^2)||/M_c^2 to convert the filtered-matter pieces of e_ij into explicit 1/M_c^2 bounds; add the inhomogeneous RTK mixed-operator coefficients separately.',
  'interpretation':'Finite-k rank preservation can be certified by a quantitative margin inequality around the published pure-gravity low-k matrix. No assumption that one particular coupled entry vanishes is required.',
  'non_claims':[
    'does not yet supply numerical or action-derived values for e11,e12,e21,e22',
    'does not choose M_c',
    'does not cover intermediate/high k outside the low-k expansion',
    'does not address radiative detuning of eta1=eta2=0'
  ],
  'next_gate':'derive the four E0 coefficients/bounds from the frozen projected matter Hamiltonian and RTK mixed operator, then test 2 eps0<sigma_min(B0) or the sharper exact ||E0||_2 condition symbolically before any M_c fit.'
}
with open('u1_lowk_rank_perturbation_bound_result.json','w') as f:
    json.dump(out,f,indent=2,sort_keys=True); f.write('\n')
print(out['classification'],json.dumps(out,sort_keys=True))
