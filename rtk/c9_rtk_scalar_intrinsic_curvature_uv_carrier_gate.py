#!/usr/bin/env python3
"""Intrinsic-spatial-curvature UV carrier for the spatial-covariant RTK scalar.

Start from the already certified flat-FLRW reduced scalar action

 S2 = 1/2 int a^3/H^2 [ K(1+y/M_K^2) dot(zeta)^2 - G y zeta^2 ],
 y=k^2/a^2, G=rho+p>0 on the rolling branch.

On gamma_ij=a^2 exp(2 zeta) delta_ij in d=3,
  R3^(1) = -4 a^-2 Delta zeta = 4 y zeta in Fourier space.
Therefore
  (R3)^2 -> 16 y^2 zeta^2,
  D_i R3 D^i R3 -> 16 y^3 zeta^2
at quadratic order.

Adding spatial potential operators
  alpha4 (R3)^2
or
  alpha6 D_i R3 D^i R3
with
  alpha4 = -G/(32 H^2 M_U^2),
  alpha6 = -G/(32 H^2 M_U^4)
produces respectively
  omega^2 = c_a^2 y(1+y/M_U^2)/(1+y/M_K^2),
  omega^2 = c_a^2 y(1+y^2/M_U^4)/(1+y/M_K^2).

These operators contain no time derivatives and hence do not alter the quadratic
velocity Hessian.  For a transverse-traceless metric perturbation,
R3^(1)=d_i d_j h_ij-Delta h=0, so these scalar-curvature operators also do not
modify the flat-FLRW tensor quadratic dispersion.  This is a quadratic carrier
theorem, not yet a full nonlinear/U1/radiative completion.
"""
import json
import sympy as sp

y,K,G,H,MK,MU=sp.symbols('y K G H M_K M_U', positive=True, finite=True)
z,zd=sp.symbols('zeta zdot', real=True, finite=True)

# Baseline reduced scalar Lagrangian density divided by a^3.
L0=sp.Rational(1,2)/H**2*(K*(1+y/MK**2)*zd**2-G*y*z**2)
R1sq=16*y**2*z**2
gradR1sq=16*y**3*z**2
alpha4=-G/(32*H**2*MU**2)
alpha6=-G/(32*H**2*MU**4)
L1=sp.expand(L0+alpha4*R1sq)
L2=sp.expand(L0+alpha6*gradR1sq)
L1ref=sp.Rational(1,2)/H**2*(K*(1+y/MK**2)*zd**2-G*y*(1+y/MU**2)*z**2)
L2ref=sp.Rational(1,2)/H**2*(K*(1+y/MK**2)*zd**2-G*y*(1+y**2/MU**4)*z**2)
assert sp.simplify(L1-L1ref)==0
assert sp.simplify(L2-L2ref)==0

ca2=sp.symbols('c_a_squared', positive=True, finite=True)
w1=sp.factor(ca2*y*(1+y/MU**2)/(1+y/MK**2))
w2=sp.factor(ca2*y*(1+y**2/MU**4)/(1+y/MK**2))
assert sp.limit(w1/y,y,sp.oo)==ca2*MK**2/MU**2
assert sp.limit(w2/y**2,y,sp.oo)==ca2*MK**2/MU**4

# Linear scalar curvature of a TT metric perturbation vanishes exactly from TT
# conditions h=0 and k_i h_ij=0. Encode the Fourier contraction algebra.
ktrace,kdiv=sp.symbols('k2_htrace kikhij', real=True, finite=True)
Rtt1=kdiv-y*ktrace
assert sp.simplify(Rtt1.subs({ktrace:0,kdiv:0}))==0

# Neither intrinsic-curvature operator contains any velocity by construction.
# Hence second derivatives wrt zdot vanish, leaving the baseline kinetic Hessian.
assert sp.diff(alpha4*R1sq,zd,2)==0
assert sp.diff(alpha6*gradR1sq,zd,2)==0

# Express G/H^2 in fixed background quantities: for a P(X) clock G=2 X P_X.
X,PX=sp.symbols('X P_X', positive=True, finite=True)
alpha4_state=sp.factor(alpha4.subs(G,2*X*PX))
alpha6_state=sp.factor(alpha6.subs(G,2*X*PX))
assert sp.simplify(alpha4_state+X*PX/(16*H**2*MU**2))==0
assert sp.simplify(alpha6_state+X*PX/(16*H**2*MU**4))==0

out={
 'classification':'RTK_C9_RTK_SCALAR_INTRINSIC_CURVATURE_UV_CARRIER_PASS',
 'status_scope':'GREEN_EXACT_QUADRATIC_SPATIAL_CURVATURE_CARRIER_NONLINEAR_VERTICES_U1_RANK_AND_RADIATIVE_STABILITY_PENDING',
 'baseline':'S2=1/2 int a^3/H^2 [K(1+y/M_K^2) zdot^2-G y zeta^2], y=k^2/a^2',
 'linearized_curvature':{'scalar_FLRW':'R3^(1)=-4 a^-2 Delta zeta=4 y zeta','TT':'R3^(1)=d_i d_j h_ij-Delta h=0 for transverse traceless h_ij'},
 'n1_carrier':{
   'operator':'alpha4 (R3)^2',
   'alpha4':'-G/[32 H^2 M_U^2]',
   'quadratic_addition':'-G y^2 zeta^2/[2 H^2 M_U^2]',
   'dispersion':'omega^2=c_a^2 y(1+y/M_U^2)/(1+y/M_K^2)',
   'UV':'omega^2~c_a^2 M_K^2 y/M_U^2'
 },
 'n2_carrier':{
   'operator':'alpha6 D_i R3 D^i R3',
   'alpha6':'-G/[32 H^2 M_U^4]',
   'quadratic_addition':'-G y^3 zeta^2/[2 H^2 M_U^4]',
   'dispersion':'omega^2=c_a^2 y(1+y^2/M_U^4)/(1+y/M_K^2)',
   'UV':'omega^2~c_a^2 M_K^2 y^2/M_U^4'
 },
 'clock_state_dictionary':'G=rho+p=2 X P_X, so alpha4=-X P_X/[16 H^2 M_U^2] and alpha6=-X P_X/[16 H^2 M_U^4]; a constant M_U can therefore be represented by a fixed background-state coefficient rather than epoch-by-epoch fitting.',
 'quadratic_constraint_statement':'Both added carriers are intrinsic-spatial potential operators with zero second derivative with respect to zdot. They leave the certified quadratic kinetic factor K(1+y/M_K^2) and lapse/shift velocity Hessian unchanged.',
 'tensor_statement':'Because R3^(1)=0 on a TT perturbation, (R3)^2 and (D R3)^2 start beyond quadratic order in the TT sector on flat FLRW; they do not create a quadratic tensor/GW dispersion correction there.',
 'interpretation':'The previously found symbolic UV numerator deformation has a natural carrier inside the same spatial-covariant architecture: scalar intrinsic-curvature invariants can restore a growing scalar frequency without changing the certified rational kinetic denominator or the flat-FLRW tensor quadratic dispersion.',
 'non_claims':[
   'does not prove the nonlinear U1 constraint algebra or full Dirac rank is unchanged',
   'does not derive cubic/quartic vertices of the curvature carriers',
   'does not prove curved-FLRW, anisotropic or compact-object tensor sectors are unaffected',
   'does not establish radiative stability or technical naturalness',
   'does not choose n or M_U'
 ],
 'next_gate':'expand the n=1 and n=2 intrinsic-curvature carriers to cubic and quartic scalar order on the rolling flat patch, canonically normalize with the exact Z(k), and repeat the partial-wave amplitude/phase-space test before any UV carrier is promoted.'
}
open('c9_rtk_scalar_intrinsic_curvature_uv_carrier_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
