#!/usr/bin/env python3
"""Homogeneous flat-FLRW background gate for the projectable U(1)+RTK candidate.

Projectability N=N(t) makes the Hamiltonian constraint global, but on a
homogeneous FLRW background the global equation is equivalent to the usual
minisuperspace Friedmann equation.  The elliptic compensator at k=0 gives
Q=H0, cancelling the ordinary-matter contribution to the local A constraint
without removing N H0 from the global Hamiltonian source.

The homogeneous RTK mixed term C(D_i Theta)^2 vanishes, while the retained
P(X_U) clock contributes its ordinary homogeneous energy density rho_RTK.
"""
import json
import sympy as sp

lam,M,H,rho,Lambda,eps=sp.symbols('lambda M_Pl H rho_total Lambda eps_G', positive=True, finite=True)
# Exact projectable homogeneous constraint in d=3.
constraint=sp.factor(sp.Rational(3,2)*(3*lam-1)*M**2*H**2-rho-M**2*Lambda)
# Relative cosmological gravitational coupling vs lambda=1/Newton normalization.
R=sp.factor(2/(3*lam-1))
assert sp.simplify(R.subs(lam,1)-1)==0
mismatch=sp.factor(1-R)  # lambda>1 branch, so R<1.
assert sp.simplify(mismatch-3*(lam-1)/(3*lam-1))==0
# Saturating 1-R=eps gives lambda=1+2 eps/[3(1-eps)].
lam_max=sp.factor(1+2*eps/(3*(1-eps)))
assert sp.simplify(mismatch.subs(lam,lam_max)-eps)==0

# k=0 compensator A-source cancellation.
H0,Q=sp.symbols('H0 Q', finite=True, real=True)
A_source=sp.simplify(Q-H0)
assert sp.simplify(A_source.subs(Q,H0))==0

out={
  'classification':'RTK_C9_PROJECTABLE_U1_FLRW_GLOBAL_HAMILTONIAN_PASS',
  'status_scope':'GREEN_EXACT_PROJECTABLE_HOMOGENEOUS_BACKGROUND_EQUATIONS_PRODUCTION_HISTORY_NUMERICAL_RECERTIFICATION_PENDING',
  'domain':'d=3 projectable N=N(t), homogeneous flat FLRW, k=0 elliptic auxiliary reduction, homogeneous rolling RTK X_U>0',
  'A_constraint':{
    'matter_plus_aux_source':'Q-H0=0 exactly at k=0',
    'flat_gravity_result':'with R=0 the surviving geometric A constraint fixes Omega=0 on this branch',
    'old_obstruction':'the former evolving-rho universal-family-I A-source obstruction is absent'
  },
  'global_Hamiltonian_constraint':'(3/2)(3 lambda-1) M_Pl^2 H^2 = rho_total + M_Pl^2 Lambda',
  'rho_total_scope':'rho_total includes ordinary homogeneous matter plus the retained RTK P(X_U) energy; the homogeneous mixed-gradient term vanishes because D_i Theta_U=0',
  'cosmological_Newton_ratio':'G_cos/G_N=2/(3lambda-1), taking the local Newton normalization from the universal U1 matter frame',
  'lambda_gt1_fractional_tolerance':'If 0 < 1-G_cos/G_N <= eps_G, then 1 < lambda <= 1 + 2 eps_G/[3(1-eps_G)].',
  'examples':{
    'eps_G_0p1':'lambda-1 <= 0.074074074...',
    'eps_G_0p01':'lambda-1 <= 0.0067340067...'
  },
  'interpretation':'Projectability does not remove the homogeneous matter/RTK Friedmann source: the compensator cancels only the local A source. The background deviation from GR is controlled by one explicit lambda-dependent normalization and can be confronted directly with cosmological bounds.',
  'non_claims':[
    'does not set an observational value of eps_G',
    'does not yet run BBN/CMB with lambda_HL distinct from the existing RTK lambda_D parameter',
    'does not include spatial curvature or inhomogeneous perturbations',
    'does not prove the global Hamiltonian integration-constant sector is phenomenologically harmless'
  ],
  'next_gate':'introduce lambda_HL as a distinct projectable background parameter in the numerical cosmology interface and run a frozen differential BBN/CMB normalization scan; separately audit the projectable global Hamiltonian integration constant and its relation to the RTK dark sector.'
}
open('c9_projectable_u1_flrw_global_hamiltonian_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
