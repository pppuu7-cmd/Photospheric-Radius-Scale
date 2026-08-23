#!/usr/bin/env python3
"""Symbolic higher-spatial quadratic UV-completion window for the RTK scalar.

The certified production quadratic dispersion is
  omega_0^2 = c_a^2 k^2/[1+k^2/M_K^2].
Its frequency saturation drives v_g->0 and the two-particle phase-space factor
g~k^5.  Consider a deliberately minimal spatial-only numerator deformation

  omega_n^2 = c_a^2 k^2 [1+(k/M_U)^(2n)]/[1+k^2/M_K^2],  n>=1.

This can arise from additional higher-spatial quadratic operators without
introducing higher time derivatives at quadratic order.  This gate does NOT
select such an operator as the final UV completion; it derives the scale window
needed for it to be invisible below an observed momentum k_obs while turning on
no later than a certified momentum cutoff k_unit.

For n=1 the asymptotic dispersion becomes linear and the phase-space factor
approaches a constant.  For n=2 the asymptotic dispersion is Lifshitz-like
omega~k^2 and phase space falls as k^-3.  Interaction vertices and all-sector
constraint/loop consistency must be rederived before either case is accepted.
"""
import json
import sympy as sp

k,ca,MK,MU,kobs,kunit,eps=sp.symbols('k c_a M_K M_U k_obs k_unit epsilon_obs', positive=True, finite=True)
Z=1+k**2/MK**2
w0sq=ca**2*k**2/Z

# n=1 and n=2 exact deformations.
w1sq=sp.factor(w0sq*(1+k**2/MU**2))
w2sq=sp.factor(w0sq*(1+k**4/MU**4))
assert sp.simplify(w1sq/w0sq-1-k**2/MU**2)==0
assert sp.simplify(w2sq/w0sq-1-k**4/MU**4)==0

w1=ca*k*sp.sqrt(1+k**2/MU**2)/sp.sqrt(Z)
w2=ca*k*sp.sqrt(1+k**4/MU**4)/sp.sqrt(Z)
vg1=sp.diff(w1,k); vg2=sp.diff(w2,k)
g1=sp.factor(k**2/(2*w1**2*vg1))
g2=sp.factor(k**2/(2*w2**2*vg2))

# UV phase-space limits.
g1inf=sp.simplify(sp.limit(g1,k,sp.oo))
g1ref=MU**3/(2*ca**3*MK**3)
assert sp.simplify(g1inf-g1ref)==0
kg2inf=sp.simplify(sp.limit(k**3*g2,k,sp.oo))
g2ref=MU**6/(4*ca**3*MK**3)
assert sp.simplify(kg2inf-g2ref)==0

# High-k dispersions.
w1_over_k=sp.simplify(sp.limit(w1/k,k,sp.oo))
w2_over_k2=sp.simplify(sp.limit(w2/k**2,k,sp.oo))
assert sp.simplify(w1_over_k-ca*MK/MU)==0
assert sp.simplify(w2_over_k2-ca*MK/MU**2)==0

# Exact symbolic observational/onset windows.
# n=1: (kobs/MU)^2<=eps and (kunit/MU)^2>=1.
low1=kobs/sp.sqrt(eps); high=kunit
# n=2: (kobs/MU)^4<=eps.
low2=kobs/eps**sp.Rational(1,4)
ratio1=sp.simplify(low1/kobs)
ratio2=sp.simplify(low2/kobs)
assert ratio1==1/sp.sqrt(eps)
assert ratio2==eps**(-sp.Rational(1,4))

# Generic n formula retained symbolically as text; executable checks use n=1,2.
# Numerical illustration uses only the already configured B9 envelope at z=1e9
# and the certified early single-channel P(X) tree cutoff. It does not choose M_U.
h=0.691103719964454
MPC_M=3.0856775814913673e22
HBARC_EV_M=1.973269804e-7
INV_MPC_EV=HBARC_EV_M/MPC_M
kobs_eV=5.0*h*(1.0+1.0e9)*INV_MPC_EV
kunit_eV=1.9807199478328038e-4
ratio=kunit_eV/kobs_eV
illustrative={}
for e in [1e-2,1e-4,1e-6,1e-8]:
    n1_req=e**-0.5
    n2_req=e**-0.25
    illustrative[f'{e:.0e}']={
      'n1_required_kunit_over_kobs':n1_req,
      'n2_required_kunit_over_kobs':n2_req,
      'n1_window_exists_for_conservative_B9_envelope':ratio>=n1_req,
      'n2_window_exists_for_conservative_B9_envelope':ratio>=n2_req,
    }
    assert ratio>=n1_req and ratio>=n2_req

out={
 'classification':'RTK_C9_RTK_SCALAR_HIGHER_SPATIAL_UV_WINDOW_PASS',
 'status_scope':'GREEN_KINEMATIC_UV_COMPLETION_SCALE_WINDOW_OPERATOR_INTERACTIONS_AND_FULL_CONSTRAINTS_PENDING',
 'baseline':'omega_0^2=c_a^2 k^2/[1+k^2/M_K^2]',
 'candidate_family':'omega_n^2=omega_0^2[1+(k/M_U)^(2n)], spatial-only quadratic numerator deformation',
 'generic_asymptotics':{
   'omega':'~ c_a M_K k^n/M_U^n',
   'v_group':'~ n c_a M_K k^(n-1)/M_U^n',
   'phase_space':'g~M_U^(3n) k^(3-3n)/[2 n c_a^3 M_K^3]'
 },
 'n1':{
   'relative_omega_squared_correction':'(k/M_U)^2',
   'uv_omega':'~(c_a M_K/M_U) k',
   'uv_phase_space':'g -> M_U^3/(2 c_a^3 M_K^3), finite rather than k^5 divergent',
   'scale_window':'k_obs/sqrt(epsilon_obs) <= M_U <= k_unit',
   'existence_iff':'k_unit/k_obs >= epsilon_obs^(-1/2)'
 },
 'n2':{
   'relative_omega_squared_correction':'(k/M_U)^4',
   'uv_omega':'~(c_a M_K/M_U^2) k^2',
   'uv_phase_space':'g~M_U^6/[4 c_a^3 M_K^3 k^3] ->0',
   'scale_window':'k_obs/epsilon_obs^(1/4) <= M_U <= k_unit',
   'existence_iff':'k_unit/k_obs >= epsilon_obs^(-1/4)'
 },
 'generic_window':'k_obs epsilon_obs^(-1/(2n)) <= M_U <= k_unit; exists iff k_unit/k_obs >= epsilon_obs^(-1/(2n))',
 'conservative_B9_illustration':{
   'k_obs_definition':'configured 5 h/Mpc envelope redshifted all the way to z=1e9',
   'k_obs_eV':kobs_eV,
   'early_single_channel_k_unit_eV':kunit_eV,
   'k_unit_over_k_obs':ratio,
   'tolerance_examples_not_adopted_constraints':illustrative
 },
 'interpretation':'A very large symbolic scale window exists in which an additional spatial-only quadratic operator can be negligible throughout the conservatively extended B9 momentum range yet turn on before the P(X)-only phase-space cutoff. n=1 removes the k^5 density-of-states divergence kinematically; n>=2 makes the high-k phase space decrease. This establishes room for a UV completion but does not identify a complete one.',
 'non_claims':[
   'does not choose n or M_U',
   'does not compute interaction vertices induced by the new spatial operator',
   'does not recertify the U1/auxiliary Dirac constraint rank after embedding the operator in the complete action',
   'does not prove loop stability, causality, positivity, compact-object consistency or renormalizability',
   'does not claim the production rational dispersion is valid above the turnover scale'
 ],
 'next_gate':'construct explicit n=1 and n=2 spatial operators in the frozen RTK action, derive their cubic/quartic vertices and repeat the exact partial-wave calculation; reject any completion that spoils the certified low-k dispersion, constraint rank or cosmological transfer functions.'
}
open('c9_rtk_scalar_higher_spatial_uv_window_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps({'conservative_B9_illustration':out['conservative_B9_illustration']},sort_keys=True))
