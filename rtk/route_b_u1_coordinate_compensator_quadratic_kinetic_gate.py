#!/usr/bin/env python3
"""Quadratic kinetic-rank gate for the degeneracy-preserving coordinate compensator.

Candidate:
    Delta L = -sqrt(g) N sigma F_Sigma(Sigma)
with sigma=(A-Acal)/N and a homogeneous background satisfying sigma_bar=0.

At first order around a zero-gradient homogeneous background,
    delta(N sigma) = delta A + delta dot(nu) + lower-velocity/spatial pieces
(up to the convention-dependent overall sign of nu).  Expanding
    F(Sigma)=F0+F1 deltaSigma+...
shows that the genuinely new quadratic velocity term is only
    -(delta dot(nu)) F1 deltaSigma.
It contains one time derivative but no delta dot(Sigma), so its velocity Hessian
vanishes identically.  The intended scalar kinetic term remains the one already
present in the frozen P(X_U) action.

Thus this compensator preserves the kinetic Hessian rank and the
velocity-independent primary p_nu+J_A+F(Sigma) relation at quadratic order.
This is not yet the full second-class Poisson-rank proof.
"""
import json
import sympy as sp

vnu,vS,q,A1,F0,F1,K,vg,Kg=sp.symbols(
    'v_nu v_Sigma deltaSigma deltaA F0 F1 K_Sigma v_g K_g',
    finite=True, real=True
)
K=sp.symbols('K_Sigma', positive=True, finite=True, real=True)
Kg=sp.symbols('K_g', nonzero=True, finite=True, real=True)

# Minimal quadratic local kinetic representative. vg denotes any already
# regular gravity kinetic direction; vS is the intended RTK scalar velocity.
L_base=sp.Rational(1,2)*Kg*vg**2+sp.Rational(1,2)*K*vS**2
L_comp_quad=-(A1+vnu)*(F0+F1*q)
L_quad=sp.expand(L_base+L_comp_quad)

vel=(vg,vS,vnu)
H_base=sp.hessian(L_base,vel)
H_total=sp.hessian(L_quad,vel)
DeltaH=sp.simplify(H_total-H_base)
assert DeltaH==sp.zeros(3)
assert H_total.rank()==H_base.rank()==2

# p_nu is coordinate-dependent but velocity-independent.
pnu=sp.diff(L_quad,vnu)
assert sp.simplify(pnu+F0+F1*q)==0
assert sp.diff(pnu,vS)==0
assert sp.diff(pnu,vg)==0
assert sp.diff(pnu,vnu)==0

# The compensator changes the constraint/source mixing, not the kinetic rank.
# Its quadratic mixing derivative is F1, which is allowed to be nonzero.
constraint_mix=sp.diff(sp.diff(L_comp_quad,vnu),q)
assert sp.simplify(constraint_mix+F1)==0

out={
  'classification':'RTK_ROUTE_B_U1_COORDINATE_COMPENSATOR_QUADRATIC_KINETIC_PASS',
  'status_scope':'GREEN_SCOPED_QUADRATIC_KINETIC_RANK_PRESERVED_POISSON_RANK_PENDING',
  'candidate':'Delta L=-sigma F_Sigma(Sigma)',
  'background':'homogeneous rolling X_U>0 branch with sigma_bar=0',
  'quadratic_new_velocity_structure':'-delta dot(nu) F_Sigma_prime deltaSigma (plus source/spatial terms)',
  'velocity_hessian_result':{
    'Delta_Hessian':'0 exactly for velocities (gravity_regular_direction, dotSigma, dotnu)',
    'rank_before':2,
    'rank_after':2,
    'p_nu_velocity_dependence':'none'
  },
  'constraint_effect':'The new term mixes the existing U1/A constraint with deltaSigma through F_Sigma_prime but creates no new quadratic kinetic eigenvalue.',
  'interpretation':'Together with the primary-preservation theorem, the coordinate compensator passes the two cheapest classical-degeneracy prefilters. The remaining decisive classical gate is the full second-class Poisson cross-block rank at finite spatial momentum.',
  'non_claims':[
    'not a full nonlinear DOF certificate',
    'not proof that det B is nonzero for every finite k',
    'not a radiative-stability or shift-symmetry protection result',
    'not a PPN or equivalence-principle result'
  ],
  'next_gate':'derive and test the modified four-constraint Poisson block for scalar perturbations on the rolling FLRW branch; require rank 4 for nonzero physical k and track any k=0 gauge/background zero separately.'
}
open('u1_coordinate_compensator_quadratic_kinetic_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
