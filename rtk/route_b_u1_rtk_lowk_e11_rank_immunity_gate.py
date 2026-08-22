#!/usr/bin/env python3
"""Neutral-RTK low-k determinant-immunity theorem on flat FLRW.

Inputs already proved elsewhere in this repository:
  1. The neutral invariant-shift RTK sector can directly modify only
     a={pi_N,H_perp} in the 2x2 cross block B; b,c,d retain pure-gravity
     support weakly on the total momentum constraint.
  2. The RTK correction to a vanishes on the exact homogeneous mode and the
     mixed RTK operator is built from spatial derivatives, so on an analytic
     flat-FLRW Fourier patch its first allowed local symbol is O(k^2).
  3. Pure gravity has
       b=-b2 k^2 + O(k^4), c=+b2 k^2 + O(k^4), d=O(k^4), b2!=0.

Write delta a_RTK=r2 k^2+O(k^4), with r2 arbitrary. Then

  B = [[(a2+r2)k^2+O(k^4), -b2 k^2+O(k^4)],
       [ b2 k^2+O(k^4),       d4 k^4+O(k^6)]].

Therefore det B=b2^2 k^4+O(k^6): the leading punctured-low-k determinant
coefficient is exactly independent of r2. This protects rank in the neutral-RTK
sector alone. It does NOT mean the singular-value margin is independent of r2:
sigma_min of [[a2+r2,-b2],[b2,0]] depends on a2+r2. Any quantitative filtered-
matter perturbation bound must therefore use the RTK-shifted leading matrix.

This is a scoped leading-symbol theorem, not a global all-k rank proof.
"""
import json
import sympy as sp

q=sp.symbols('q', real=True)  # q=|k|^2
b2,a2,r2,d4=sp.symbols('b2 a2 r2 d4', real=True, finite=True)
a4,r4,b4,c4,d6=sp.symbols('a4 r4 b4 c4 d6', real=True, finite=True)

# Keep one subleading order explicitly. q=|k|^2.
a=(a2+r2)*q+(a4+r4)*q**2
b=-b2*q+b4*q**2
c= b2*q+c4*q**2
d=d4*q**2+d6*q**3
B=sp.Matrix([[a,b],[c,d]])
detB=sp.expand(B.det())
lead_q2=sp.expand(detB).coeff(q,2)
assert sp.simplify(lead_q2-b2**2)==0
assert sp.diff(lead_q2,r2)==0
assert sp.diff(lead_q2,a2)==0
assert sp.diff(lead_q2,d4)==0

# Exact support-algebra identity: adding arbitrary delta_a changes det only by
# delta_a*d. If delta_a=O(q), d=O(q^2), the change begins at O(q^3)=O(|k|^6).
ag,bg,cg,dg,da=sp.symbols('a_g b_g c_g d_g delta_a', finite=True)
Bg=sp.Matrix([[ag,bg],[cg,dg]])
Brtk=sp.Matrix([[ag+da,bg],[cg,dg]])
assert sp.simplify(Brtk.det()-Bg.det()-da*dg)==0
rtk_delta_leading=sp.expand((r2*q)*(d4*q**2))
assert sp.expand(rtk_delta_leading).coeff(q,2)==0
assert sp.expand(rtk_delta_leading).coeff(q,3)==r2*d4

# Conditioning caveat: determinant is r2-independent, but singular values are
# not. The Gram trace depends on A=a2+r2 while det(Gram)=b2^4.
A=sp.expand(a2+r2)
B0_rtk=sp.Matrix([[A,-b2],[b2,0]])
Gram=sp.expand(B0_rtk.T*B0_rtk)
gram_trace=sp.expand(sp.trace(Gram))
gram_det=sp.expand(Gram.det())
assert sp.simplify(B0_rtk.det()-b2**2)==0
assert sp.simplify(gram_trace-(A**2+2*b2**2))==0
assert sp.simplify(gram_det-b2**4)==0

out={
  'classification':'RTK_ROUTE_B_U1_RTK_LOWK_E11_RANK_IMMUNITY_PASS',
  'status_scope':'GREEN_NEUTRAL_RTK_LEADING_DETERMINANT_IMMUNITY_FILTERED_MATTER_MARGIN_PENDING',
  'domain':'special eta1=eta2=0 U(1) branch; flat homogeneous background; analytic local Fourier symbols; weakly on total momentum constraint',
  'inputs':[
    'prior neutral-RTK cross-block support: only delta a={pi_N,Hperp} can be nonzero directly',
    'exact homogeneous RTK lapse-affinity: delta a_RTK(k=0)=0',
    'mixed RTK operator contains spatial derivatives, so analytic local correction starts at O(|k|^2)',
    'pure-gravity low-k support b=-b2|k|^2, c=+b2|k|^2, d=O(|k|^4) with b2!=0'
  ],
  'leading_matrix':'B_RTK=|k|^2 [[a2+r2,-b2],[b2,0]] + higher orders, with the (2,2) entry first appearing at O(|k|^4)',
  'leading_determinant':'det B_RTK = b2^2 |k|^4 + O(|k|^6), exactly independent of arbitrary neutral-RTK r2',
  'exact_support_identity':'det(B_gravity+delta_a E11)-det(B_gravity)=delta_a*d_gravity',
  'order_identity':'delta_a_RTK=O(|k|^2) and d_gravity=O(|k|^4) imply delta(det B)_RTK=O(|k|^6)',
  'conditioning_caveat':'Although det([[a2+r2,-b2],[b2,0]])=b2^2 is r2-independent, its Gram trace=(a2+r2)^2+2b2^2, so sigma_min generally depends on r2. Filtered-matter norm bounds must use the RTK-shifted baseline, not the pure-gravity sigma_min blindly.',
  'interpretation':'Neutral RTK alone cannot destroy the pure-gravity punctured-low-k rank at leading |k|^4 order through its only allowed direct cross-block channel. The remaining leading determinant-changing corrections are in the projected filtered-matter sector, while RTK can still alter conditioning through a2+r2.',
  'non_claims':[
    'does not prove all-k or intermediate-k rank',
    'does not bound higher O(|k|^6) RTK terms or provide a numerical epsilon',
    'does not claim sigma_min is invariant under r2',
    'does not cover nonanalytic backgrounds or boundary conditions',
    'does not bound projected filtered-matter metric-resolvent corrections',
    'does not address C9 radiative stability of eta1=eta2=0'
  ],
  'next_gate':'derive/bound filtered-matter E0 using a_eff~|k|^2/M_c^2 and the resolvent variation, and compare it to sigma_min of [[a2+r2,-b2],[b2,0]] while keeping M_c symbolic.'
}
with open('u1_rtk_lowk_e11_rank_immunity_result.json','w') as f:
    json.dump(out,f,indent=2,sort_keys=True); f.write('\n')
print(out['classification'],json.dumps(out,sort_keys=True))
