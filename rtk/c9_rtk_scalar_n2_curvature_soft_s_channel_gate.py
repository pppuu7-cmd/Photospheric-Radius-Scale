#!/usr/bin/env python3
"""Exceptional soft-spatial s-channel correction to n=2 curvature UV power counting.

The generic curvature-carrier UV power-count gate assumed all relevant legs
carry the hard spatial momentum.  The exact nonlinear conformal gate instead
found a nonzero elastic s-channel cubic kernel
  K3_s = -96 k^6
while the internal spatial momentum is exactly zero in COM kinematics.
Thus the internal leg does NOT receive the hard-spatial Z(q) normalization.
This gate derives the exact bare-conformal s-channel eigen-amplitude scaling for
  omega^2 = c_a^2 k^2 N/Z,
  N=1+k^4/M_U^4, Z=1+k^2/M_K^2.

Scope: fixed-lapse conformal intrinsic-curvature sector, background alpha6 held
fixed.  Lapse/shift reduction and alpha6 state perturbations may alter/cancel
this channel; therefore this is a warning gate, not a final no-go theorem.
"""
import json
import sympy as sp

k,MU,MK,H,K,ca=sp.symbols('k M_U M_K H K c_a', positive=True, finite=True)
pi=sp.pi
Z=1+k**2/MK**2
N=1+k**4/MU**4
omega2=sp.factor(ca**2*k**2*N/Z)
# d ln omega / d ln k.
D=sp.factor(1 + 2*k**4/(MU**4+k**4) - k**2/(MK**2+k**2))
# Exact phase-space factor g=k^2/(2 omega^2 v_g)=Z^(3/2)/(2 ca^3 N^(3/2) D).
g=sp.factor(Z**sp.Rational(3,2)/(2*ca**3*N**sp.Rational(3,2)*D))

# Use G=ca^2 K. alpha6=-G/(32 H^2 MU^4).  After canonical
# normalization zeta_c=sqrt(K Z)/H zeta, the s cubic vertex is
# g3_s = -[G H/(32 K^(3/2) MU^4)] K3_s/Z, with internal Z(0)=1.
G=ca**2*K
K3s=-96*k**6
C=G*H/(32*K**sp.Rational(3,2)*MU**4)
g3s=sp.factor(-C*K3s/Z)
# Internal spatial momentum is zero and internal energy is 2 omega(k): Ds=4 omega^2.
Ms=sp.factor(-g3s**2/(4*omega2))
# Angle-independent s exchange: a0=Ms/(16 pi) in the adopted convention.
a0s=sp.factor(Ms/(16*pi))
ga0s=sp.factor(g*a0s)
expected_exact=sp.factor(-9*H**2*k**10*sp.sqrt(Z)/(128*pi*K*MU**8*ca*N**sp.Rational(5,2)*D))
assert sp.simplify(ga0s-expected_exact)==0

# Intermediate hierarchy M_U << k << M_K: set Z->1, N->k^4/MU^4, D->3.
intermediate=sp.factor(-3*H**2*MU**2/(128*pi*K*ca))
# Derive with a scaling parameter r -> infinity while MK is taken parametrically harder.
r=sp.symbols('r', positive=True)
# Direct asymptotic dictionary audit.
expr_mid=expected_exact.subs({Z:1}) if False else None
# Algebraic substitution of asymptotic factors is clearer and exact for the leading monomial.
mid_from_factors=sp.factor(-9*H**2*k**10/(128*pi*K*MU**8*ca*(k**10/MU**10)*3))
assert sp.simplify(mid_from_factors-intermediate)==0

# Deep hierarchy k >> M_K,M_U: sqrt(Z)->k/MK, N^(5/2)->k^10/MU^10, D->2.
deep=sp.factor(-9*H**2*MU**2*k/(256*pi*K*ca*MK))
deep_from_factors=sp.factor(-9*H**2*k**10*(k/MK)/(128*pi*K*MU**8*ca*(k**10/MU**10)*2))
assert sp.simplify(deep_from_factors-deep)==0

# Contact generic n=2 deep scaling is only k^2 after external Z^-2,
# whereas the exceptional s exchange is k^4 before phase space; hence s wins asymptotically.
contact_power=sp.Integer(2)
s_exchange_power=sp.Integer(4)
phase_power=sp.Integer(-3)
assert s_exchange_power+phase_power==1
assert contact_power+phase_power==-1

# Optional production identity K=2 Mpl^2 M_K^2.
Mpl=sp.symbols('M_Pl', positive=True, finite=True)
mid_prod=sp.factor(intermediate.subs(K,2*Mpl**2*MK**2))
deep_prod=sp.factor(deep.subs(K,2*Mpl**2*MK**2))
assert sp.simplify(mid_prod + 3*H**2*MU**2/(256*pi*ca*Mpl**2*MK**2))==0
assert sp.simplify(deep_prod + 9*H**2*MU**2*k/(512*pi*ca*Mpl**2*MK**3))==0

out={
 'classification':'RTK_C9_RTK_SCALAR_N2_CURVATURE_SOFT_S_CHANNEL_WARNING_PASS',
 'status_scope':'YELLOW_BARE_CONFORMAL_SOFT_S_CHANNEL_INVALIDATES_GENERIC_N2_UV_PROMOTION_FULL_CONSTRAINT_CANCELLATION_TEST_PENDING',
 'input_from_exact_nonlinear_gate':'elastic COM s-channel internal spatial momentum q_s=0 but K3_s=-96 k^6 is nonzero',
 'completed_dispersion':'omega^2=c_a^2 k^2(1+k^4/M_U^4)/(1+k^2/M_K^2)',
 'exact_phase_space':'g=Z^(3/2)/[2 c_a^3 N^(3/2) D], D=1+2 k^4/(M_U^4+k^4)-k^2/(M_K^2+k^2)',
 'exact_bare_s_partial_wave':'g a0_s = -9 H^2 k^10 sqrt(Z)/[128 pi K M_U^8 c_a N^(5/2) D]',
 'intermediate_MU_ll_k_ll_MK':'g a0_s -> -3 H^2 M_U^2/[128 pi K c_a] (constant, not k^-1)',
 'deep_k_ll_none':'for k>>M_K,M_U, g a0_s -> -9 H^2 M_U^2 k/[256 pi K c_a M_K], growing linearly',
 'production_dictionary':{
   'K':'2 M_Pl^2 M_K^2',
   'intermediate':'-3 H^2 M_U^2/[256 pi c_a M_Pl^2 M_K^2]',
   'deep':'-9 H^2 M_U^2 k/[512 pi c_a M_Pl^2 M_K^3]'
 },
 'corrected_interpretation':'The previous generic all-hard-leg estimate g a_l~k^-1 for n=2 does not control the elastic s-channel because its internal spatial momentum is soft. Bare conformal n=2 is only marginal in the hierarchy M_U<<k<<M_K and becomes asymptotically worse after k>>M_K. Therefore n=2 must not be promoted until the full lapse/shift and state-function expansion checks whether the K3_s contribution cancels or is constrained away.',
 'non_claims':[
   'not a final no-go for n=2 because nonlinear constraint reduction may cancel/modify K3_s',
   'not a full unitarity amplitude; P(X), C(X), metric/U1/auxiliary channels remain omitted',
   'deep k>>M_K may lie far beyond the physically relevant completion window at some epochs',
   'no M_U chosen and no experimental bound inferred'
 ],
 'next_gate':'derive the full cubic lapse/shift constraints with the n=2 carrier and state-dependent alpha6; test specifically whether the reduced elastic K3_s at q_s=0 vanishes. If it survives, scan its exact coefficient over the frozen background and reconsider n>=3 or a carrier symmetry that forbids the soft-s vertex.'
}
open('c9_rtk_scalar_n2_curvature_soft_s_channel_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
