#!/usr/bin/env python3
"""Prove that the linear RTK implementation cannot determine a strong-coupling scale.

The implemented CLASS sector fixes a quadratic action/dispersion.  Cubic and
higher operators vanish in the Hessian about the background and therefore are
not identifiable from the linear equations alone.  This script makes that
statement constructive with a family of nonlinear completions sharing exactly
the same quadratic Hessian but arbitrary cubic coefficient.

This is a theorem about information content, not evidence for strong coupling.
"""
import json
import sympy as sp

# One-mode symbolic representative. Spatial structures can be restored without
# changing the order-counting argument.
eps,K,G,A3,Lambda = sp.symbols('eps K G A3 Lambda', positive=True)
q,M,pi,pidot = sp.symbols('q M pi pidot', positive=True)

L2 = sp.Rational(1,2)*K*(1+q**2/M**2)*pidot**2 - sp.Rational(1,2)*G*q**2*pi**2
# Representative cubic interaction with arbitrary scale. Any cubic local
# preferred-frame operator has zero quadratic Hessian at pi=0.
L3 = A3/Lambda * pi*pidot**2
L = L2 + L3

# Scale perturbations pi,pidot -> eps*pi,eps*pidot and extract coefficients.
Leps = sp.expand(L.subs({pi:eps*pi,pidot:eps*pidot}))
c2 = sp.expand(Leps).coeff(eps,2)
c3 = sp.expand(Leps).coeff(eps,3)
quad_independent = sp.simplify(sp.diff(c2,A3))==0 and sp.simplify(sp.diff(c2,Lambda))==0
cubic_depends = sp.simplify(sp.diff(c3,A3))!=0 and sp.simplify(sp.diff(c3,Lambda))!=0

# Quadratic Hessian explicitly independent of cubic parameters.
fields=sp.Matrix([pi,pidot])
H2=sp.hessian(c2,(pi,pidot))
Hfull_at0=sp.hessian(L,(pi,pidot)).subs({pi:0,pidot:0})
hessian_same=sp.simplify(H2-Hfull_at0)==sp.zeros(2)

out={
 'status':'PASS' if (quad_independent and cubic_depends and hessian_same) else 'FAIL',
 'classification':'STRONG_COUPLING_NOT_IDENTIFIABLE_FROM_LINEAR_SECTOR',
 'proof':{
   'quadratic_coefficient_independent_of_cubic_coupling':bool(quad_independent),
   'cubic_coefficient_depends_on_arbitrary_A3_and_Lambda':bool(cubic_depends),
   'quadratic_hessian_unchanged_by_cubic_completion':bool(hessian_same),
   'L2':str(L2),
   'representative_L3':str(L3),
 },
 'consequence':{
   'strong_coupling_scale_from_current_CLASS_linear_equations':'UNDERDETERMINED',
   'M_K_or_k_star_equals_strong_coupling_cutoff':'NOT_DERIVABLE',
   'required_new_input':'EXPLICIT_NONLINEAR_EFT_COMPLETION_AND_CUBIC_COEFFICIENTS',
   'next_calculation':'CANONICALLY_NORMALIZE_CUBIC_OPERATORS_THEN_COMPARE_INTERACTION_AND_QUADRATIC_TERMS',
   'uv_completion':'NOT_CLAIMED'
 }
}
print(json.dumps(out,indent=2,sort_keys=True))
if out['status']!='PASS': raise SystemExit(2)
