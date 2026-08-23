#!/usr/bin/env python3
"""Map the finite-Mc single-resolvent O(4) source into the projectable PPN A4 equation.

Published parent structure: Lin, Mukohyama, Wang, Zhu, arXiv:1310.6666v4,
Sec. VI.  Their Eq.(6.12) gives on the projectable branch
  h00 = 2 U - U^2 + 2 a1 A4 + O(6),
and Eq.(6.17) contains the fourth-order gauge-field term only through
  -2 Delta A4
inside the combined A-constraint + trace-dynamical equation.

Our already-certified finite-Mc source theorem says the genuinely new O(4)
metric/source nonlocality is controlled by one resolvent derivative
  delta f = -(1/Mc^2) L^-1 delta(D^2) L^-1.
Define S_res^(4) as the corresponding additive source on the RHS of the
published Eq.(6.17), with all parent/local O(4) terms held fixed.
Then exactly
  -2 Delta delta A4 = S_res,
so on the current a1=1 branch
  delta h00 = - Delta^-1 S_res.
This defines one new generalized nonlocal potential Psi_res.

The companion exact d=3 conformal kernel is
  K_res/gamma = -m^2(3x^2-x c)/[(m^2+1)(m^2+x^2)],
  m=Mc/k, x=q/k.
This script proves it is genuinely non-separable in output and internal
momenta.  Therefore for arbitrary extended sources the new potential cannot in
general be represented by a constant shift of a standard local PPN coefficient.
The standard constant-PPN description is recovered only in controlled limits
(e.g. local-parent m->0 or source-specific reductions where the convolution
collapses onto the usual potential basis).
"""
import json
import sympy as sp

lap,a1,Sres=sp.symbols('Delta a1 S_res', nonzero=True, finite=True)
dA4,dh00=sp.symbols('delta_A4 delta_h00', finite=True)
# Difference between modified and parent Eq.(6.17).
dA4_sol=sp.factor(-Sres/(2*lap))
dh00_sol=sp.factor(2*a1*dA4_sol)
assert sp.simplify(dh00_sol + a1*Sres/lap)==0
# Current physical metric branch a1=1.
dh00_a1=sp.factor(dh00_sol.subs(a1,1))
assert dh00_a1==-Sres/lap

# Fourier dictionary Delta -> -k^2.
k=sp.symbols('k', positive=True, finite=True)
dh00_fourier=sp.simplify(dh00_a1.subs(lap,-k**2))
assert dh00_fourier==Sres/k**2

# Exact companion resolvent-variation kernel and non-separability proof.
m,x,c=sp.symbols('m x c', positive=True, finite=True)
K=sp.factor(-m**2*(3*x**2-x*c)/((m**2+1)*(m**2+x**2)))
# The m-x entanglement is entirely visible through (m^2+x^2).  For a
# separable nonzero function F(m)G(x,c), the mixed derivative of log|K|
# would vanish.  Work on a sign-fixed open patch; the mixed derivative is
# independent of the angular numerator and is strictly positive for m,x>0.
mixed=sp.factor(sp.diff(sp.diff(sp.log(m**2/((m**2+1)*(m**2+x**2))),m),x))
expected=4*m*x/(m**2+x**2)**2
assert sp.simplify(mixed-expected)==0
assert expected.is_positive

# A cross-product identity provides an algebraic separability test without logs.
m1,m2,x1,x2=sp.symbols('m1 m2 x1 x2', positive=True, finite=True)
base=lambda mm,xx: mm**2/((mm**2+1)*(mm**2+xx**2))
cross=sp.factor(base(m1,x1)*base(m2,x2)-base(m1,x2)*base(m2,x1))
# It must not vanish identically; its numerator contains (m1^2-m2^2)(x1^2-x2^2).
num=sp.factor(sp.together(cross).as_numer_denom()[0])
assert sp.simplify(num - m1**2*m2**2*(m1**2-m2**2)*(x1**2-x2**2))==0

# Local-parent limit: at fixed k,q, m=Mc/k ->0 kills the new kernel.
assert sp.limit(K,m,0,dir='+')==0

out={
 'classification':'RTK_C9_PROJECTABLE_U1_FINITE_MC_O4_RESOLVENT_POTENTIAL_MAP_PASS',
 'status_scope':'GREEN_EXACT_O4_SOURCE_TO_H00_MAP_AND_NONSEPARABILITY_FULL_SOURCE_SPECIFIC_PPN_SOLVE_PENDING',
 'published_parent':{
   'reference':'Lin-Mukohyama-Wang-Zhu arXiv:1310.6666v4 Sec.VI Eqs.(6.12),(6.17)',
   'h00_relation':'h00=2U-U^2+2 a1 A4+O(6)',
   'A4_coefficient_in_combined_O4_equation':'-2 Delta A4'
 },
 'definition':'S_res is the additive finite-Mc single-resolvent O(4) source on the RHS of the parent combined A-constraint + trace-dynamical equation',
 'exact_map':{
   'delta_A4':'-(1/2) Delta^-1 S_res',
   'delta_h00_general':'-a1 Delta^-1 S_res',
   'delta_h00_a1_1':'-Delta^-1 S_res',
   'fourier_a1_1':'delta h00(k)=S_res(k)/k^2'
 },
 'new_potential':'Psi_res := -Delta^-1 S_res; on a1=1, delta h00=Psi_res',
 'resolvent_kernel':'K_res/gamma=-m^2(3x^2-x cosTheta)/[(m^2+1)(m^2+x^2)], m=Mc/k, x=q/k',
 'nonseparability_proof':{
   'mixed_log_derivative':'4 m x/(m^2+x^2)^2 > 0 for m,x>0',
   'cross_product_numerator':'m1^2 m2^2 (m1^2-m2^2)(x1^2-x2^2)',
   'consequence':'the generic extended-source resolvent contribution is true mode mixing, not a diagonal multiplicative f(k) and not generically a constant PPN coefficient shift'
 },
 'local_parent_limit':'K_res -> 0 as Mc/k ->0 at fixed q/k, so Psi_res disappears in the local-parent limit',
 'interpretation':'The full finite-Mc O4 problem should be formulated as generalized/nonlocal PPN: solve the parent local potential coefficients plus one additional source-dependent Psi_res. Only after evaluating Psi_res for a concrete source/support can one test whether it is approximated by a constant beta/alpha2 shift over that experiment.',
 'non_claims':[
   'does not yet compute S_res for the complete Solar-System matter distribution',
   'does not assign an experimental bound to Psi_res',
   'does not claim standard constant PPN is invalid in the high-k local-recovery regime',
   'does not include compact-object self-gravity or nonlinear screening',
   'does not alter the already-certified O2/O3 finite-Mc results'
 ],
 'next_gate':'construct S_res explicitly in the parent Eq.(6.17) potential basis for a controlled source (uniform sphere first), solve A4 and h00 including Psi_res, and compare acceleration/redshift observables to the local-parent result rather than forcing a premature constant-beta fit.'
}
open('c9_projectable_u1_finite_mc_o4_resolvent_potential_map_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
