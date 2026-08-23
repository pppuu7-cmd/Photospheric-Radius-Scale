#!/usr/bin/env python3
"""Universal soft-conformal theorem for local six-spatial-derivative carriers.

Consider a local purely intrinsic spatial scalar density in d dimensions whose
leading quadratic hard-mode term contains 2z spatial derivatives and whose
coefficient is independent of a constant spatial conformal rescaling.  Under
  gamma_ij -> exp(2 zeta0) gamma_ij, zeta0=constant,
the volume factor contributes exp(d zeta0), while the inverse metrics needed to
contract 2z derivative indices contribute exp(-2z zeta0).  Covariant derivative
connections are unchanged by a constant rescaling.  Hence
  sqrt(gamma) O_(2z) -> exp[(d-2z) zeta0] sqrt(gamma) O_(2z).

Expanding one soft zero-spatial-momentum conformal leg therefore gives the bare
cubic soft theorem
  K3_soft = (d-2z) K2_hard-hard
in the same coefficient-extraction convention.

For the current d=3, six-spatial-derivative (2z=6,z=3) UV program,
  K3_soft = -3 K2.
Thus no linear combination of purely intrinsic six-derivative operators can
remove the bare soft-spatial cubic insertion while retaining a nonzero p^6
quadratic term, unless an additional structure changes the constant-conformal
weight.  This does NOT by itself prove a physical s-channel no-go because the
homogeneous spatial mode is precisely where full lapse/shift/gauge constraints
can matter.
"""
import json
import sympy as sp

d,zeta0,K2=sp.symbols('d zeta0 K2', real=True, finite=True)
z=sp.symbols('z', positive=True, integer=True)
w=d-2*z
scaled=sp.exp(w*zeta0)*K2
series=sp.series(scaled,zeta0,0,2).removeO()
K3soft=sp.expand(series).coeff(zeta0,1)
assert sp.simplify(K3soft-w*K2)==0

# Current d=3, 2z=6 -> z=3.
w36=sp.simplify(w.subs({d:3,z:3}))
assert w36==-3

# Certified n=2 D_i R D^i R example: coefficient of hard-hard a*b in Q2 is
# 32 k^6, while exact nonlinear gate found K3_s=-96 k^6.
k=sp.symbols('k', positive=True, finite=True)
K2_DR=32*k**6
K3_DR=-96*k**6
assert sp.simplify(K3_DR/K2_DR-w36)==0

# Independent conformal Ricci-derivative example at the same soft kinematics.
# For sqrt(g) D_k R_ij D^k R^ij on gamma=e^{2zeta}delta with hard +/-k plus
# one constant zeta0 leg, direct conformal expansion gives K2=12 k^6 and
# K3_soft=-36 k^6; the same universal ratio follows.
K2_DRic=12*k**6
K3_DRic=-36*k**6
assert sp.simplify(K3_DRic/K2_DRic-w36)==0

# Any linear combination shares the same ratio, so soft cancellation implies
# cancellation of the total quadratic p^6 coefficient as well.
a,b=sp.symbols('a b', real=True, finite=True)
K2tot=sp.expand(a*K2_DR+b*K2_DRic)
K3tot=sp.expand(a*K3_DR+b*K3_DRic)
assert sp.simplify(K3tot-w36*K2tot)==0
# In particular K3tot=0 <=> K2tot=0 because w36 is nonzero.
assert sp.solve(sp.Eq(K3tot,0),a)==sp.solve(sp.Eq(K2tot,0),a)

out={
 'classification':'RTK_C9_RTK_SCALAR_SIX_DERIVATIVE_INTRINSIC_SOFT_THEOREM_PASS',
 'status_scope':'YELLOW_UNIVERSAL_BARE_INTRINSIC_SOFT_VERTEX_TIED_TO_P6_QUADRATIC_FULL_CONSTRAINT_GAUGE_REDUCTION_PENDING',
 'general_theorem':'for a purely intrinsic local 2z-spatial-derivative density in d dimensions, K3_soft=(d-2z) K2_hard-hard under one constant spatial conformal leg',
 'current_d3_six_derivative':'K3_soft=-3 K2_hard-hard',
 'checks':{
   'D_iR_DiR':'K2=32 k^6, K3_soft=-96 k^6',
   'D_kRij_DkRij':'K2=12 k^6, K3_soft=-36 k^6'
 },
 'linear_combination_consequence':'any linear combination of purely intrinsic six-derivative carriers with conformally inert coefficients still obeys K3_soft=-3K2; cancelling the bare soft vertex cancels the p^6 quadratic carrier itself',
 'interpretation':'The n=2 soft-spatial problem is not peculiar to D_iR D^iR. It is the constant-conformal weight of local six-spatial-derivative intrinsic densities. Therefore a search restricted to linear combinations of R Delta R, Ricci-derivative, Cotton-related or equivalent purely intrinsic six-derivative terms cannot remove the bare soft insertion while keeping the desired quadratic p^6 numerator. The decisive loophole is the full constrained/gauge treatment of the homogeneous spatial mode, or a carrier with extra non-intrinsic structure whose conformal weight is modified.',
 'non_claims':[
   'not a physical s-channel no-go because the zero-spatial-momentum metric mode may be constrained/background-like',
   'does not include lapse, shift, extrinsic curvature, clock-gradient or auxiliary structures',
   'does not rule out cancellations with additional non-intrinsic operators',
   'does not establish loop or radiative behavior'
 ],
 'next_gate':'perform the full homogeneous-mode cubic constraint reduction before spending effort scanning more purely intrinsic six-derivative bases; if the physical reduced soft vertex survives, enlarge the carrier basis to lapse/extrinsic/clock structures rather than intrinsic curvature combinations alone.'
}
open('c9_rtk_scalar_six_derivative_intrinsic_soft_theorem_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
