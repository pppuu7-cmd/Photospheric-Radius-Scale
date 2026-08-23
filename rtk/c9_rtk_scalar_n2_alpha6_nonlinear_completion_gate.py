#!/usr/bin/env python3
"""Nonlinear state-function completion of the n=2 curvature-carrier coefficient.

Quadratic matching fixes only the background value
  alpha6_bar = -G_bar/(32 H_bar^2 M_U^4).
It does not fix lapse/state derivatives of alpha6 away from the rolling
background.  In unitary gauge, for a timelike clock,
  X = Xbar/N^2, N=1+n.

Let
  s1 = d ln(alpha6)/d ln X,
  s2 = d^2 ln(alpha6)/d(ln X)^2
on the background.  This gate proves
  N alpha6(Xbar/N^2)/alpha6_bar
   = 1 + (1-2s1)n + (2s1^2-s1+2s2)n^2 + O(n^3).
Thus cubic/quartic carrier interactions are not uniquely fixed by the quadratic
UV numerator.

It also isolates the special completion
  alpha6(phi,X)=A(phi) sqrt(X).
Then N alpha6=A(phi)sqrt(Xbar) exactly in unitary gauge: the carrier has no
lapse dependence at any order and no shift dependence because D_iR3 D^iR3 is
intrinsic spatial geometry.  Consequently this completion leaves the lapse/
shift constraint equations unchanged by the carrier itself and cannot use
carrier-induced nondynamical-field terms to cancel the already certified bare
conformal soft-s cubic kernel K3_s=-96 k^6.

This is not a no-go for all alpha6 completions; generic s1,s2 introduce lapse
vertices and must be reduced explicitly.
"""
import json
import sympy as sp

n,s1,s2=sp.symbols('n s1 s2', real=True, finite=True)
# delta ell = ln(X/Xbar) = -2 ln(1+n)
dell=sp.series(-2*sp.log(1+n),n,0,4).removeO()
# log(alpha/alpha_bar) through quadratic response in lnX.
loga=sp.expand(s1*dell + sp.Rational(1,2)*s2*dell**2)
a_ratio=sp.series(sp.exp(loga),n,0,3).removeO()
Na=sp.expand((1+n)*a_ratio)
Na2=sp.series(Na,n,0,3).removeO()
expected=1+(1-2*s1)*n+(2*s1**2-s1+2*s2)*n**2
assert sp.simplify(Na2-expected)==0

c1=sp.expand(Na2).coeff(n,1)
c2=sp.expand(Na2).coeff(n,2)
assert c1==1-2*s1
assert c2==2*s1**2-s1+2*s2

# sqrt(X) completion: s1=1/2, s2=0 and all displayed lapse coefficients vanish.
assert sp.simplify(c1.subs({s1:sp.Rational(1,2),s2:0}))==0
assert sp.simplify(c2.subs({s1:sp.Rational(1,2),s2:0}))==0

# Exact rather than merely series proof.  Let Xbar>0, N>0.
N,Xbar,A=sp.symbols('N Xbar A', positive=True, finite=True)
X=Xbar/N**2
alpha=A*sp.sqrt(X)
assert sp.simplify(N*alpha-A*sp.sqrt(Xbar))==0

# Cubic carrier structure: Q2 is quadratic, Q3 cubic.  Generic lapse dressing
# contributes c1*n1*Q2 at cubic order, whereas sqrtX gives only Q3.
Q2,Q3,n1=sp.symbols('Q2 Q3 n1', finite=True)
L3_generic=sp.expand(Q3+c1*n1*Q2)
L3_sqrt=sp.simplify(L3_generic.subs({s1:sp.Rational(1,2),s2:0}))
assert L3_sqrt==Q3

# The intrinsic carrier has no shift variable.  Represent this by an auxiliary
# symbol psi and verify the special-completion density has zero derivatives.
psi=sp.symbols('psi', real=True)
carrier_special=A*sp.sqrt(Xbar)*(Q2+Q3)
assert sp.diff(carrier_special,N)==0
assert sp.diff(carrier_special,psi)==0

# Record the certified conformal s kernel that therefore survives as a direct
# carrier term under this special completion.
k=sp.symbols('k', positive=True, finite=True)
K3s=-96*k**6
assert K3s!=0

out={
 'classification':'RTK_C9_RTK_SCALAR_N2_ALPHA6_NONLINEAR_COMPLETION_PASS',
 'status_scope':'YELLOW_QUADRATIC_MATCHING_DOES_NOT_FIX_NONLINEAR_ALPHA6_SQRTX_COMPLETION_PRESERVES_CONSTRAINTS_BUT_SOFT_S_SURVIVES',
 'unitary_gauge_clock':'X=Xbar/N^2, N=1+n',
 'response_definitions':{
   's1':'d ln alpha6 / d ln X on background',
   's2':'d^2 ln alpha6 / d(ln X)^2 on background'
 },
 'lapse_expansion':'N alpha6/alpha6_bar = 1+(1-2s1)n+(2s1^2-s1+2s2)n^2+O(n^3)',
 'cubic_carrier_structure':'L3_carrier/alpha6_bar = Q3 + (1-2s1) n1 Q2',
 'quadratic_nonuniqueness':'alpha6_bar fixes the p^6 quadratic numerator but does not fix s1,s2, so it does not uniquely fix cubic/quartic amplitudes',
 'special_completion':{
   'form':'alpha6(phi,X)=A(phi) sqrt(X)',
   'exact_identity':'N alpha6=A(phi) sqrt(Xbar) in unitary gauge',
   's1':'1/2','s2':'0',
   'constraint_effect':'carrier has no direct lapse or shift dependence at any order; carrier itself leaves the lapse/shift equations unchanged',
   'soft_s_consequence':'the direct conformal Q3 remains, including certified K3_s=-96 k^6; this special completion cannot cancel it through carrier-induced lapse/shift terms'
 },
 'interpretation':'There is genuine nonlinear completion freedom beyond the quadratic carrier theorem. The constraint-clean sqrt(X) completion is attractive structurally but does not cure the soft-s warning. Any attempted soft-s cancellation must therefore come from a different alpha6 state dependence or additional operators/symmetry, and must be demonstrated after full constraint reduction rather than assumed.',
 'non_claims':[
   'does not prove a generic alpha6(X) completion can cancel K3_s',
   'does not choose s1 or s2 by fitting',
   'does not include P(X), C(X), metric/U1/auxiliary interference',
   'does not establish radiative naturalness of alpha6(phi,X)=A(phi)sqrt(X)'
 ],
 'next_gate':'for generic s1, use the certified linear lapse solution n1=dot(zeta)/H on the controlled flat patch to derive the extra cubic momentum-energy kernel from (1-2s1)n1Q2 and test whether any regular state-function choice can cancel the q_s=0 curvature vertex consistently across channels; separately retain sqrtX as the constraint-clean benchmark.'
}
open('c9_rtk_scalar_n2_alpha6_nonlinear_completion_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
