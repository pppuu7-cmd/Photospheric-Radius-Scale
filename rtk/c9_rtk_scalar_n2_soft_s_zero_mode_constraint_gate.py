#!/usr/bin/env python3
"""Exact zero-spatial-momentum admissibility check for the n=2 soft s-channel.

The certified spatial-covariant flat-FLRW scalar reduction integrates out lapse
and scalar shift only for y=k^2/a^2>0.  Its nondynamical constraint block has
  M_npsi = 2 M_Pl^2 H y,
  M_psipsi = 0,
and determinant
  det M = -4 M_Pl^4 H^2 y^2.
Thus the block is invertible on the punctured momentum domain y>0 but singular
at exact y=0.  The momentum/shift equation that yielded n=dot(zeta)/H is
proportional to y and disappears at y=0.

Elastic equal-|k| COM s-channel kinematics has internal spatial momentum
q_s=|k+(-k)|=0.  Therefore the positive-y reduced zeta action/propagator cannot
be evaluated at q_s=0 by naive substitution.  The bare conformal K3_s theorem
is a real interaction statement, but the corresponding exchange line lies in
the homogeneous/background constraint sector and requires an unreduced or
regulated q->0+ calculation.

This gate prevents an overclaim: it does not prove the soft-s contribution
cancels; it proves that the previous fixed-lapse/reduced propagator continuation
at exact q_s=0 is not a valid physical no-go theorem.
"""
import json
import sympy as sp

y,Mpl,H,K=sp.symbols('y M_Pl H K', positive=True, finite=True)
# Keep a generic finite M_nn; the determinant is controlled by the offdiagonal
# shift coupling because M_psipsi=0.
Mnn=sp.symbols('M_nn', real=True, finite=True)
Mnpsi=2*Mpl**2*H*y
M=sp.Matrix([[Mnn,Mnpsi],[Mnpsi,0]])
det=sp.factor(M.det())
assert det==-4*Mpl**4*H**2*y**2
# Inverse exists for positive y.
Minv=sp.simplify(M.inv())
assert sp.simplify(M*Minv-sp.eye(2))==sp.zeros(2)
# Formal determinant at exact zero is zero.
y0=sp.symbols('y0', real=True)
det_general=-4*Mpl**4*H**2*y0**2
assert sp.simplify(det_general.subs(y0,0))==0

# Momentum constraint has the certified form 2 Mpl^2 y(H n-zdot)=0.
n,zdot=sp.symbols('n zdot', real=True, finite=True)
Epsi=2*Mpl**2*y*(H*n-zdot)
# For y>0 it implies n=zdot/H.
assert sp.solve(sp.Eq(Epsi,0),n)==[zdot/H]
# At exact y=0 the equation becomes the identity 0=0 and fixes no n.
assert sp.simplify(Epsi.subs(y,0))==0

# Elastic COM spatial momentum sum.
kx,ky,kz=sp.symbols('kx ky kz', real=True, finite=True)
kin=sp.Matrix([kx,ky,kz])
kin2=-kin
qs=sp.simplify((kin+kin2).dot(kin+kin2))
assert qs==0

# The n=2 intrinsic carrier has no quadratic lapse/shift velocities and hence
# does not repair this zero-mode constraint singularity at quadratic order.
# Encode the certified fact as zero additions to the block.
dM=sp.zeros(2)
assert sp.simplify((M+dM).det()-det)==0

out={
 'classification':'RTK_C9_RTK_SCALAR_N2_SOFT_S_ZERO_MODE_CONSTRAINT_PASS',
 'status_scope':'YELLOW_EXACT_S_CHANNEL_ZERO_MODE_OUTSIDE_PUNCTURED_REDUCED_PROPAGATOR_UNREDUCED_Q_TO_ZERO_TEST_REQUIRED',
 'constraint_block':{
   'M_npsi':'2 M_Pl^2 H y',
   'M_psipsi':'0',
   'determinant':'-4 M_Pl^4 H^2 y^2'
 },
 'punctured_domain':'for y>0 the shift constraint gives n=zdot/H and the lapse/shift block is invertible',
 'exact_zero_mode':'at y=0 the shift equation is 0=0 and the constraint block is singular; the positive-y reduced action is not an exact zero-mode action',
 'elastic_s_channel':'equal-|k| COM has q_s=0 exactly',
 'carrier_effect':'the intrinsic n=2 carrier does not change the quadratic lapse/shift block, so it does not regularize the exact zero-mode reduction',
 'interpretation':'The certified bare K3_s=-96k^6 soft insertion remains an important warning, but using the punctured positive-y reduced zeta propagator at q_s=0 is not justified. The physical s-channel must be computed from the unreduced constrained action or by a controlled q->0+ regulator before n=2 can be rejected or accepted. This zero-mode caveat is the same structural issue already encountered in the classical rank program.',
 'non_claims':[
   'does not prove the s-channel vanishes',
   'does not prove n=2 is unitary',
   'does not invalidate the bare conformal soft theorem',
   'does not identify the correct finite-volume/background treatment of the homogeneous mode'
 ],
 'next_gate':'derive the cubic unreduced lapse+shift+zeta kernel for a regulated internal spatial momentum q>0, solve constraints before taking q->0+, and compare that limit with the naive bare/fixed-lapse s-channel.'
}
open('c9_rtk_scalar_n2_soft_s_zero_mode_constraint_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
