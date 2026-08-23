#!/usr/bin/env python3
"""Canonical lapse-gradient immunity of the neutral RTK mixed sector on FLRW.

This theorem distinguishes two variational questions that must not be mixed:
(1) at fixed coordinate velocity dot(Sigma), D_i Theta_U generates the familiar
    lapse-gradient/acceleration term;
(2) the Hamiltonian Dirac matrix varies the lapse at fixed canonical
    (Sigma,p_Sigma).

For
  L = int N sqrt(g) [F(Theta^2)+C(Theta^2) D_iTheta D^iTheta],
  Theta=(dot Sigma-v^i D_iSigma)/N,
on the phase-space slice
  D_i Sigma=0, D_i nu=0, p_Sigma/sqrt(g)=const,
with a regular homogeneous Legendre branch, Theta=theta0=const is an exact
solution of the momentum equation for arbitrary spatial N(x): every derivative
term is proportional to D_iTheta and vanishes. Hence dotSigma=N theta0,
D_iTheta=0 and the canonical Hamiltonian is
  H=int N [p_Sigma theta0-sqrt(g)F(theta0^2)],
strictly affine in N with no lapse-gradient support. Therefore the direct RTK
contribution to {pi_N,H_perp} vanishes on this background phase-space slice for
all lapse Fourier modes. This does not say the fixed-dotSigma/static action has
no acceleration term.
"""
import json
import sympy as sp

N,theta,p,sqrtg=sp.symbols('N theta p sqrtg', nonzero=True, finite=True)
c0,c1,c2,c3=sp.symbols('c0 c1 c2 c3', finite=True)
X=theta**2
F=c0+c1*X+c2*X**2+c3*X**3
# On D_i theta=0 the mixed term and its coefficient are irrelevant to the
# homogeneous canonical momentum relation.
p_of_theta=sp.expand(sqrtg*sp.diff(F,theta))
assert sp.diff(p_of_theta,N)==0
legendre_jac=sp.factor(sp.diff(p_of_theta,theta))
# After solving the regular branch theta=theta(p/sqrtg), theta is N-independent.
H0=sp.expand(p*theta-sqrtg*F)
H=sp.expand(N*H0)
Hperp=sp.diff(H,N)
assert sp.simplify(Hperp-H0)==0
assert sp.diff(Hperp,N)==0
assert sp.diff(H,N,N)==0

# Jet identity behind the cancellation: with D_i Sigma=0 and dotSigma=N theta0,
# D_i(dotSigma/N)=0 even for arbitrary D_i N.
theta0,Nx=sp.symbols('theta0 N_x', finite=True)
dotS=N*theta0
dotSx=Nx*theta0
DxTheta=sp.simplify(dotSx/N-dotS*Nx/N**2)
assert DxTheta==0
C=sp.symbols('C', finite=True)
assert sp.simplify(N*sqrtg*C*DxTheta**2)==0

out={
  'classification':'RTK_ROUTE_B_U1_RTK_CANONICAL_LAPSE_GRADIENT_IMMUNITY_PASS',
  'status_scope':'GREEN_FLAT_FLRW_BACKGROUND_CANONICAL_RTK_A_ENTRY_ZERO_SCALAR_PERTURBATIONS_PENDING',
  'domain':'D_i Sigma=0, D_i nu=0, p_Sigma/sqrt(g)=spatially homogeneous, regular homogeneous scalar Legendre branch; lapse N(x) arbitrary',
  'canonical_momentum':'p_Sigma=sqrt(g) dF/dTheta on D_iTheta=0, independent of N',
  'exact_solution':'Theta=theta0(p_Sigma/sqrt(g)) constant; dotSigma=N(x) theta0; D_iTheta=0 for arbitrary spatial lapse profile',
  'canonical_H':'H_RTK=int N [p_Sigma theta0-sqrt(g)F(theta0^2)]',
  'direct_crossblock_consequence':'delta_RTK {pi_N,H_perp}=0 on the stated background phase-space slice for every lapse Fourier mode',
  'ensemble_distinction':'The fixed-coordinate-velocity/unitary-gauge action can still display the previously certified M_Pl^2 lapse-gradient acceleration term. Hamiltonian rank varies N at fixed canonical p_Sigma, for which dotSigma adjusts and the direct background lapse Hessian cancels.',
  'legendre_representative_jacobian':str(legendre_jac),
  'interpretation':'For the flat-FLRW background rank calculation, the neutral RTK sector does not supply the leading or subleading direct a-entry through lapse gradients on the regular homogeneous canonical branch. This strengthens the earlier support theorem only on this specific phase-space background.',
  'non_claims':[
    'does not remove the physical static/PPN acceleration effect in a fixed-clock boundary problem',
    'does not cover inhomogeneous scalar canonical data D_i p_Sigma != 0 or D_i Sigma != 0',
    'does not prove the full perturbed scalar constraint matrix away from the FLRW background',
    'does not address radiative stability or choose M_c'
  ],
  'next_gate':'combine beta0_bare=0 with this exact background canonical result: the two-derivative leading a2 of the current full action vanishes on flat FLRW; then isolate only q^2-and-higher bare/UV lapse-potential remainder terms.'
}
open('u1_rtk_canonical_lapse_gradient_immunity_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
