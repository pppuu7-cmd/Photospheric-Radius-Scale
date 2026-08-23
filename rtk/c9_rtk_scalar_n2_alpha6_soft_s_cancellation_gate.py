#!/usr/bin/env python3
"""Can local alpha6(X) lapse dressing cancel the n=2 soft-spatial s vertex?

Use the certified cubic carrier structure
  L3/alpha_bar = Q3 + c1 n1 Q2, c1=1-2s1,
and the certified linear lapse solution on the controlled flat rolling patch
  n1 = dot(zeta)/H.
At cubic order no second-order lapse solution is needed: terms proportional to
x2 multiply the linear L2 constraint evaluated on x1 and therefore vanish in
the reduced cubic action.

For elastic COM s-channel kinematics, the internal spatial momentum is zero,
while the internal incoming energy is -2 omega(k).  The certified bare
conformal spatial kernel is
  K3_s(Q3)=-96 k^6.
For Q2=16 U^2, the only nonzero n1 Q2 permutation puts n1 on the soft-spatial
internal leg.  Summing the two U-leg permutations gives magnitude
  |K3_s(nQ2)| = 64 |c1| [omega(k)/H] k^6.
Hence a necessary coefficient-magnitude condition for any cancellation is
  |c1| = 3H/[2 omega(k)].
But c1 is a local background-state response of alpha6, independent of spatial
momentum at a fixed epoch.  Since the completed omega(k) is nonconstant on every
open positive-k interval, a local alpha6(X) completion cannot cancel the soft-s
vertex throughout a finite momentum interval.  It can at most satisfy the
magnitude condition at isolated k (and even there relative phase/sign and the
other channels must be checked).

This is stronger than the sqrt(X) special case but is still scoped to using only
alpha6 state dependence; additional operators or symmetries can change the
conclusion.
"""
import json
import sympy as sp

k,H,s1,ca,MU,MK=sp.symbols('k H s1 c_a M_U M_K', positive=True, finite=True)
c1=1-2*s1
N=1+k**4/MU**4
Z=1+k**2/MK**2
omega=sp.factor(ca*k*sp.sqrt(N/Z))

KQ3=-96*k**6
# Magnitude coefficient; phase convention intentionally factored out.
KnQ2_mag=64*sp.Abs(c1)*omega*k**6/H
ratio=sp.factor(KnQ2_mag/sp.Abs(KQ3))
expected=sp.factor(sp.Rational(2,3)*sp.Abs(c1)*omega/H)
assert sp.simplify(ratio-expected)==0

necessary_c1=sp.factor(3*H/(2*omega))
# Demonstrate omega is not constant: logarithmic derivative is strictly positive.
D=sp.factor(1 + 2*k**4/(MU**4+k**4) - k**2/(MK**2+k**2))
# Rewrite D into a manifestly positive form by combining the first and last term.
Dpos=sp.factor(MK**2/(MK**2+k**2) + 2*k**4/(MU**4+k**4))
assert sp.simplify(D-Dpos)==0
# Both summands in Dpos are strictly positive for positive symbols.
assert (MK**2/(MK**2+k**2)).is_positive
assert (2*k**4/(MU**4+k**4)).is_positive
# Therefore d omega/dk = omega D/k >0 for all positive k.
domega=sp.factor(omega*D/k)
assert sp.simplify(sp.diff(omega,k)-domega)==0
# And the required |c1|(k) is strictly decreasing because
# d(required)/dk = -required*Dpos/k with every factor on the RHS positive.
dreq=sp.factor(sp.diff(necessary_c1,k))
assert sp.simplify(dreq + necessary_c1*Dpos/k)==0

# Special sqrtX completion c1=0 cannot satisfy cancellation at any positive k.
assert sp.simplify(c1.subs(s1,sp.Rational(1,2)))==0

# Useful hierarchy forms for the necessary response.
# k << min(MU,MK): omega~ca k.
req_ir=3*H/(2*ca*k)
# MU << k << MK: omega~ca k^3/MU^2.
req_mid=3*H*MU**2/(2*ca*k**3)
# k >> MU,MK: omega~ca MK k^2/MU^2.
req_uv=3*H*MU**2/(2*ca*MK*k**2)

out={
 'classification':'RTK_C9_RTK_SCALAR_N2_ALPHA6_SOFT_S_CANCELLATION_OBSTRUCTION_PASS',
 'status_scope':'YELLOW_LOCAL_ALPHA6_STATE_DEPENDENCE_CANNOT_CANCEL_SOFT_S_OVER_FINITE_K_INTERVAL_ADDITIONAL_OPERATOR_OR_SYMMETRY_NEEDED',
 'inputs':{
   'cubic_reduced_structure':'Q3+(1-2s1)n1Q2 with n1=dot(zeta)/H',
   'bare_soft_s':'K3_s(Q3)=-96 k^6',
   'completed_dispersion':'omega=c_a k sqrt[(1+k^4/M_U^4)/(1+k^2/M_K^2)]'
 },
 'soft_s_lapse_dressing_magnitude':'|K3_s(n1Q2)|=64 |1-2s1| [omega(k)/H] k^6',
 'ratio':'|K_nQ2|/|K_Q3|=(2/3)|1-2s1| omega(k)/H',
 'necessary_cancellation_magnitude':'|1-2s1|=3H/[2 omega(k)]',
 'monotonicity':'d ln omega/d ln k = M_K^2/(M_K^2+k^2)+2k^4/(M_U^4+k^4)>0, so the required response is strictly k-dependent/decreasing',
 'hierarchy_dictionary':{
   'k_ll_MU_MK':'required |1-2s1| ~ 3H/(2 c_a k)',
   'MU_ll_k_ll_MK':'required |1-2s1| ~ 3H M_U^2/(2 c_a k^3)',
   'k_gg_MU_MK':'required |1-2s1| ~ 3H M_U^2/(2 c_a M_K k^2)'
 },
 'sqrtX':'s1=1/2 gives c1=0 and no lapse-dressing cancellation at any positive k',
 'interpretation':'Quadratic matching plus an arbitrary local alpha6(X) response does not provide a robust soft-s cure. At a fixed background, s1 is momentum independent while the cancellation condition varies strictly with k. A tuning could at most target an isolated momentum and would still need phase/sign and t/u/contact consistency. A viable UV completion therefore needs either an additional operator/symmetry that removes the soft-spatial cubic structure or a more fundamental nonlocal/momentum-dependent mechanism, not merely a choice of local alpha6 state derivative.',
 'non_claims':[
   'does not rule out cancellation from additional independent operators',
   'does not use relative complex/Feynman phase as an assumption; it proves only a necessary magnitude condition',
   'does not claim an isolated-k tuning is physically viable',
   'does not include P(X), C(X), metric/U1/auxiliary interference or loops'
 ],
 'next_gate':'search the six-spatial-derivative intrinsic-curvature operator basis for combinations with the same scalar quadratic p^6 target but vanishing elastic soft-spatial cubic kernel; impose flat-FLRW tensor and velocity-Hessian constraints simultaneously.'
}
open('c9_rtk_scalar_n2_alpha6_soft_s_cancellation_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
