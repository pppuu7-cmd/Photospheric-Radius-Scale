#!/usr/bin/env python3
"""Exact leading low-k rank margin for the corrected current full action.

Repository inputs already certified in their stated common flat-FLRW scope:
  * corrected partial IR slice v2 has beta0_bare=0, so the bare two-spatial-
    derivative lapse-gradient a_i a^i coefficient is absent;
  * neutral RTK sector gives no direct canonical {pi_N,H_perp} lapse Hessian on
    the homogeneous canonical rolling background, even for spatial N(x);
  * projected filtered ordinary matter has leading e11=0;
  * filtered matter has k12=-k21=-x and k22=0 at leading order, where
      x=V(H0-tau_H),
    and the pure-gravity off diagonal is +/-b2.

Therefore the entire q=|k|^2 leading matrix is antisymmetric:
  B(q)=q [[0,-t],[t,0]] + O(q^2),  t=b2+x/Mc^2.
Its two singular values are both |t| and det=t^2. Rank loss at leading order is
an isolated root, not a half-line inequality. The older Mc^2>|x/b2| condition
remains a conservative sufficient choice when the root is positive, but is not
necessary.
"""
import json
import sympy as sp

b,x,m2=sp.symbols('b2 x M_c_squared', real=True, finite=True, nonzero=True)
t=sp.simplify(b+x/m2)
L=sp.Matrix([[0,-t],[t,0]])
assert sp.simplify(L.det()-t**2)==0
Gram=sp.simplify(L.T*L)
assert sp.simplify(Gram-t**2*sp.eye(2))==sp.zeros(2)
root=sp.simplify(-x/b)
assert sp.simplify(t.subs(m2,root))==0
# Distance-to-root factorization.
fac=sp.factor(t-b*(m2-root)/m2)
assert sp.simplify(fac)==0

# For a subleading B=q L+q^2 R with ||R||<=C, Weyl gives the exact sufficient
# local condition q C < sigma_min(L)=|t|.
q,C=sp.symbols('q C', positive=True, finite=True)

out={
  'classification':'RTK_ROUTE_B_U1_CURRENT_FULL_ACTION_LEADING_RANK_MARGIN_PASS',
  'status_scope':'GREEN_EXACT_CURRENT_ACTION_LEADING_MATRIX_SUBLEADING_TOTAL_C_PENDING',
  'domain':'common flat-FLRW homogeneous-canonical background scope of the beta0-bare correction, RTK canonical lapse-immunity, and projected filtered-matter low-k gates',
  'leading_matrix':'B(q)=q [[0,-t],[t,0]]+O(q^2), t=b2+x/M_c^2',
  'exact_leading_determinant':'det L=(b2+x/M_c^2)^2',
  'exact_singular_values':'sigma_1(L)=sigma_2(L)=|b2+x/M_c^2|',
  'leading_rank_loss_root':'M_c^2=-x/b2, only if this value is positive',
  'distance_factorization':'t=b2*(M_c^2-(-x/b2))/M_c^2',
  'correction_to_old_bound':'M_c^2>|x/b2| is conservative when -x/b2>0 but is not necessary; leading rank is full on both sides of the isolated root.',
  'finite_q_margin':'if B=qL+q^2R and ||R||_2<=C, q C < |b2+x/M_c^2| is sufficient for rank two at that q',
  'interpretation':'The corrected full-action bookkeeping plus canonical ensemble removes the leading diagonal uncertainty. Future M_c compatibility tests should exclude/buffer the isolated root rather than impose an artificial one-sided rank floor.',
  'non_claims':[
    'does not yet provide the total subleading C including all UV gravity Wilson coefficients',
    'does not certify intermediate/high k',
    'does not extend the canonical RTK lapse-immunity theorem to inhomogeneous scalar canonical backgrounds',
    'does not choose M_c or resolve C9 naturalness'
  ],
  'next_gate':'combine the exact root with the 1% scale window and a bound on total subleading C to derive an explicit root-exclusion buffer inside the allowed M_c interval.'
}
open('u1_current_full_action_leading_rank_margin_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
