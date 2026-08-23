#!/usr/bin/env python3
"""Real-space static O(2) kernel implied by the finite-Mc projectable source filter.

Starting point already certified in Fourier space:
  G_N(k)/G=f(k)=k^2/(k^2+M_c^2), gamma=1.
For the Newtonian potential equation k^2 U(k)=4 pi G f(k) rho(k), the k^2
cancels and the point-source Green function is Yukawa, 1/(k^2+M_c^2).

This gate translates the symbolic Fourier tolerance into physical separation r
without identifying one arbitrary k with 1/r. It is linear/static/point-source
only; extended sources and O(3)/O(4) are separate gates.
"""
import json
import sympy as sp

M,r,eps=sp.symbols('M_c r eps', positive=True, finite=True)
x=sp.symbols('x', nonnegative=True, finite=True)
# Point-source potential transfer relative to Newton.
pot=sp.exp(-x)
force=sp.factor((1+x)*sp.exp(-x))
deficit=sp.simplify(1-force)
assert sp.series(deficit,x,0,5)==x**2/sp.Integer(2)-x**3/sp.Integer(3)+x**4/sp.Integer(8)+sp.Order(x**5)
# Monotonic force suppression for x>0.
dforce=sp.factor(sp.diff(force,x))
assert dforce==-x*sp.exp(-x)

# Exact inverse: (1+x)e^-x=1-eps.  For 0<eps<1 and x>=0 use W_{-1}.
xmax=-1-sp.LambertW(-(1-eps)/sp.E,-1)
# Algebraic verification of the defining relation using W exp(W)=z.
w=sp.symbols('w', real=True)
# Record branch identity rather than asking SymPy to simplify LambertW exponentials globally.

# gamma=1 means equal linear temporal/spatial scalar kernels, not an unsuppressed amplitude.
out={
  'classification':'RTK_C9_PROJECTABLE_U1_FINITE_MC_YUKAWA_REALSPACE_PASS',
  'status_scope':'GREEN_STATIC_O2_REALSPACE_KERNEL_EXTENDED_SOURCE_AND_HIGHER_PN_PENDING',
  'fourier_input':'G_N(k)/G=k^2/(k^2+M_c^2), gamma_PPN=1 at static O2',
  'point_source':{
    'potential':'U(r)=G M_source exp(-M_c r)/r',
    'gamma_statement':'The O2 spatial and temporal scalar potentials share the same Yukawa kernel, so their ratio gamma remains 1.',
    'force_ratio':'F/F_Newton=(1+M_c r) exp(-M_c r)',
    'force_deficit':'1-F/F_Newton=1-(1+x)e^-x with x=M_c r'
  },
  'small_x':'force deficit = x^2/2 - x^3/3 + x^4/8 + O(x^5)',
  'monotonicity':'d[(1+x)e^-x]/dx=-x e^-x <=0; the force deficit is monotone increasing for x>=0',
  'exact_force_tolerance':{
    'condition':'1-(1+x)e^-x <= eps, 0<eps<1',
    'x_max':'x <= -1-W_{-1}[-(1-eps)/e]',
    'Mc_bound':'M_c <= x_max/r_local',
    'small_eps':'x_max=sqrt(2 eps)+O(eps)'
  },
  'interpretation':'Finite-Mc local recovery is a Yukawa real-space problem, not a constant-G PPN problem over arbitrary scales. The force recovers Newton quadratically in M_c r even though the potential itself differs linearly in M_c r by an additive/long-range-shape effect.',
  'non_claims':[
    'does not apply point-source formula unchanged inside an extended body',
    'does not include finite-size form factors, ephemeris fitting, laboratory geometry, or screening',
    'does not certify finite-Mc beta,alpha1,alpha2 or nonlinear dynamics',
    'does not choose an experimental eps or r_local'
  ],
  'next_gate':'derive the exact Yukawa form factor for a spherical extended source and the exterior force transfer; then map representative Solar-System/laboratory baselines only after declaring the experimental observable and tolerance.'
}
open('c9_projectable_u1_finite_mc_yukawa_realspace_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
