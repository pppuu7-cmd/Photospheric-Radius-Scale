#!/usr/bin/env python3
"""C8 exact coefficient-slice gate for one GR-PPN U(1) Hořava family.

Literature conventions
----------------------
The nonprojectable U(1) Hořava IR potential is conventionally written

    L_V = 2 Lambda - beta0 a_i a^i + gamma1 R + ...

inside

    S = zeta^2 int N sqrt(g) [L_K - L_V + ...],
    zeta^2 = 1/(16 pi G) = M_Pl^2/2.

Therefore the action coefficient of a_i a^i is

    + (M_Pl^2/2) beta0.

The exact RTK direct/rolling mixed-kinetic mapping requires

    C_acc = K/(2 M_K^2) = M_Pl^2,

so on this convention the exact RTK slice is beta0=2.

The PPN analysis of arXiv:1310.6666 exhibits an exact-GR family

    sigma2 = 4(1-a1),
    beta0  = -2(gamma1+1).

Canonical IR curvature normalization in the above action requires gamma1=-1
because -L_V contributes -gamma1 R and GR requires +R.  Thus that entire
explicit GR-PPN family has beta0=0, not beta0=2.

Scope
-----
This excludes only that explicit PPN-GR family for the direct rolling RTK
acceleration slice under the stated normalization.  The same PPN work also
contains another exact-GR family (a1=kappa=1, sigma2=0), and more general
nonminimal matter regions remain open.  This theorem is intentionally not a
U(1)-completion no-go.
"""

import json
import sympy as sp

Mpl2,MK2,K = sp.symbols('Mpl2 MK2 K', positive=True, finite=True, real=True)
beta0,gamma1,a1,sigma2 = sp.symbols('beta0 gamma1 a1 sigma2', finite=True, real=True)

zeta2 = Mpl2/2
Kprod = 2*Mpl2*MK2
Cacc = sp.simplify(Kprod/(2*MK2))
assert Cacc == Mpl2

# Match zeta^2 beta0 = Cacc.
beta_rtk = sp.solve(sp.Eq(zeta2*beta0,Cacc),beta0)
assert beta_rtk == [2]

# Canonical IR curvature normalization: -gamma1 R -> +R.
gamma_gr = -1

# Explicit exact-GR PPN family II from arXiv:1310.6666.
beta_family2 = sp.simplify(-2*(gamma1+1))
sigma_family2 = sp.simplify(4*(1-a1))
beta_family2_grnorm = sp.simplify(beta_family2.subs(gamma1,gamma_gr))
assert beta_family2_grnorm == 0

mismatch = sp.simplify(beta_rtk[0]-beta_family2_grnorm)
assert mismatch == 2

out = {
  'classification':'RTK_ROUTE_B_U1_PPN_FAMILY2_RTK_SLICE_GATE_PASS',
  'u1_action_convention':'S=zeta^2 int N sqrt(g)(L_K-L_V+...), L_V=2Lambda-beta0 a^2+gamma1 R+..., zeta^2=M_Pl^2/2',
  'rtk_direct_acceleration':'C_acc=K/(2M_K^2)=M_Pl^2',
  'rtk_beta0_slice':2,
  'canonical_IR_curvature':'gamma1=-1 so -gamma1 R=+R',
  'literature_GR_PPN_family_II':{
    'sigma2':'4(1-a1)',
    'beta0':'-2(gamma1+1)',
    'beta0_at_gamma1_minus1':0
  },
  'mismatch':2,
  'conclusion':'The explicit GR-PPN family II beta0=-2(gamma1+1) does not contain the exact direct rolling RTK beta0=2 slice at canonical IR curvature normalization.',
  'non_claims':[
    'does not exclude the distinct exact-GR family a1=kappa=1, sigma2=0 reported in the same PPN analysis',
    'does not exclude nonminimal/disformal U(1) matter frames',
    'does not solve the full RTK static equations on beta0=2',
    'does not exclude a gauge/auxiliary cancellation that changes the static effective acceleration response while retaining the cosmological mixed kinetic'
  ],
  'next_step':'Evaluate the second explicit GR-PPN family and then solve the U(1) static equations on the exact RTK beta0=2 coefficient slice with one frozen matter-frame choice.'
}

print('RTK_ROUTE_B_U1_PPN_FAMILY2_RTK_SLICE_GATE_PASS',json.dumps(out,sort_keys=True))
