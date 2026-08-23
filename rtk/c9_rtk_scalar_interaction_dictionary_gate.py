#!/usr/bin/env python3
"""Cubic/quartic interaction dictionary for the frozen intended RTK scalar.

Background: projectable or locally unit-lapse flat rolling slice
  Sigma=q t+pi, N=1, N^i=0, g_ij=delta_ij, q>0.
Define
  X=1/2[(q+dot pi)^2-(grad pi)^2],
  C(X)=M_Pl^2/(2X).
The action is P(X)+C(X)(grad dot pi)^2 on this slice.

The gate expands through O(pi^4), records the exact P-derivative and mixed
interaction coefficients, canonically normalizes in the low-k regime, and
checks the high-k powers induced by the exact quadratic Z(k)=Akin(1+k^2/M_K^2).
It intentionally does NOT declare a unitarity/strong-coupling cutoff.
"""
import json
import sympy as sp

e,q,u,s2,h2,Mpl,MK=sp.symbols('eps q u s2 h2 M_Pl M_K', positive=True, finite=True)
P1,P2,P3,P4=sp.symbols('P1 P2 P3 P4', real=True, finite=True)
X0=q**2/sp.Integer(2)
dX=e*q*u+e**2*(u**2-s2)/2
Pseries=P1*dX+P2*dX**2/2+P3*dX**3/6+P4*dX**4/24
Pseries=sp.expand(Pseries)
P2ord=sp.factor(Pseries.coeff(e,2))
P3ord=sp.factor(Pseries.coeff(e,3))
P4ord=sp.factor(Pseries.coeff(e,4))
assert sp.simplify(P2ord-(sp.Rational(1,2)*(P1+q**2*P2)*u**2-sp.Rational(1,2)*P1*s2))==0
assert sp.simplify(P3ord-(q*P2*u*(u**2-s2)/2+q**3*P3*u**3/6))==0
assert sp.simplify(P4ord-(P2*(u**2-s2)**2/8+q**2*P3*u**2*(u**2-s2)/4+q**4*P4*u**4/24))==0

Cexact=Mpl**2/(2*(X0+dX))
Cseries=sp.series(Cexact,e,0,3).removeO()
Lmix=sp.expand(Cseries*e**2*h2)
Lmix2=sp.factor(Lmix.coeff(e,2))
Lmix3=sp.factor(Lmix.coeff(e,3))
Lmix4=sp.factor(Lmix.coeff(e,4))
assert Lmix2==Mpl**2*h2/q**2
assert Lmix3==-2*Mpl**2*h2*u/q**3
assert sp.simplify(Lmix4-Mpl**2*h2*(s2+3*u**2)/q**4)==0

A=sp.symbols('Akin', positive=True, finite=True)
# Frozen production identity q^2 Akin=2 M_Pl^2 M_K^2.
Asol=2*Mpl**2*MK**2/q**2
g3=sp.factor((-2*Mpl**2/q**3)/Asol**sp.Rational(3,2))
g4=sp.factor((Mpl**2/q**4)/Asol**2)
assert sp.simplify(g3+1/(sp.sqrt(2)*Mpl*MK**3))==0
assert sp.simplify(g4-1/(4*Mpl**2*MK**4))==0

# Dimensional low-k scales associated with these coefficients only.
Lam3=sp.factor((sp.sqrt(2)*Mpl*MK**3)**sp.Rational(1,4))
Lam4=sp.factor((4*Mpl**2*MK**4)**sp.Rational(1,6))
# Both are parametrically above MK for M_Pl >> MK; ratios retained symbolically.
ratio3=sp.factor(Lam3/MK)
ratio4=sp.factor(Lam4/MK)

# High-k canonical prefactor powers using Z(k)=A(1+k^2/MK^2).
k=sp.symbols('k', positive=True, finite=True)
Z=1+k**2/MK**2
# Mixed cubic carries k^2 before field normalization: k^2/Z^(3/2) ~ k^-1.
uv3=sp.simplify(sp.limit((k**2/Z**sp.Rational(3,2))*k, k, sp.oo))
assert uv3==MK**3
# Highest-spatial quartic carries k^4/Z^2 -> constant MK^4.
uv4=sp.simplify(sp.limit(k**4/Z**2,k,sp.oo))
assert uv4==MK**4

out={
  'classification':'RTK_C9_RTK_SCALAR_INTERACTION_DICTIONARY_PASS',
  'status_scope':'GREEN_EXACT_CUBIC_QUARTIC_DICTIONARY_STRONG_COUPLING_AMPLITUDE_ANALYSIS_PENDING',
  'background':'flat rolling Sigma=q t+pi, q>0, unit projectable/local lapse and zero shift; X0=q^2/2',
  'quadratic':{
    'P_sector':'1/2(P1+q^2 P2) dotpi^2 - 1/2 P1 (grad pi)^2',
    'mixed_sector':'(M_Pl^2/q^2)(grad dotpi)^2',
    'Akin':'P1+q^2 P2',
    'production_identity':'q^2 Akin=2 M_Pl^2 M_K^2'
  },
  'P_cubic':'(q P2/2) dotpi[dotpi^2-(grad pi)^2] + (q^3 P3/6) dotpi^3',
  'P_quartic':'(P2/8)[dotpi^2-(grad pi)^2]^2 + (q^2 P3/4)dotpi^2[dotpi^2-(grad pi)^2] + (q^4 P4/24)dotpi^4',
  'mixed_cubic':'-(2 M_Pl^2/q^3) dotpi (grad dotpi)^2',
  'mixed_quartic':'(M_Pl^2/q^4)[(grad pi)^2+3 dotpi^2](grad dotpi)^2',
  'lowk_canonical_mixed':{
    'pi_c':'sqrt(Akin) pi',
    'cubic_coefficient':'-1/(sqrt(2) M_Pl M_K^3)',
    'quartic_coefficient':'1/(4 M_Pl^2 M_K^4)',
    'background_q_cancellation':'exact'
  },
  'dimensional_scales_not_cutoffs':{
    'Lambda3_coeff':'(sqrt(2) M_Pl M_K^3)^(1/4)',
    'Lambda4_coeff':'(4 M_Pl^2 M_K^4)^(1/6)',
    'warning':'These are dimensional scales inferred from low-k canonical coefficients, not certified strong-coupling cutoffs because for M_Pl>>M_K they lie parametrically above the kinetic crossover M_K.'
  },
  'highk_quadratic_normalization':'Z(k)=Akin[1+k^2/M_K^2]',
  'highk_mixed_vertex_scaling':{
    'cubic_spatial_prefactor':'k^2/Z^(3/2) ~ M_K^3/k',
    'highest_spatial_quartic_prefactor':'k^4/Z^2 -> M_K^4'
  },
  'interpretation':'The higher-spatial kinetic term softens the canonically normalized mixed cubic vertex at k>>M_K and prevents the highest-spatial mixed quartic prefactor from growing with k. Therefore a low-k dimensional coefficient alone cannot be used to claim cutoff collapse; a proper anisotropic-dispersion scattering/power-counting analysis is required around k~M_K and above.',
  'non_claims':[
    'does not compute a 2-to-2 amplitude or partial-wave unitarity bound',
    'does not include metric/U1/auxiliary exchange diagrams',
    'does not yet substitute the reconstructed DBI P3,P4 along the full cosmological trajectory',
    'does not prove asymptotic freedom or UV completeness',
    'does not cover X_U approaching zero'
  ],
  'next_gate':'substitute exact reconstructed P(X) derivatives P1..P4 along the frozen background and form dimensionless canonically normalized cubic/quartic couplings as functions of redshift; then perform anisotropic Lifshitz power counting/scattering estimates across k/M_K rather than using the low-k coefficient scales as cutoffs.'
}
open('c9_rtk_scalar_interaction_dictionary_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
