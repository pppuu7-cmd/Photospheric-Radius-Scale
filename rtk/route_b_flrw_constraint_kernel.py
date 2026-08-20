#!/usr/bin/env python3
"""Structural FLRW escape theorem for a fixed healthy-Horava action.

Primary source: Kobayashi, Urakawa, Yamaguchi, arXiv:1002.3101v2,
Eqs. (19)-(20) of the paper (linearized Hamiltonian constraint and delta-H
higher-spatial-derivative operator on flat FLRW).

With physical momentum p=k/a, the coefficient multiplying the lapse scalar
phi in the Hamiltonian constraint contains
  D_phi(p,H) = 3(3 lambda-1) H^2
               - eta p^2 - eta2 p^4/M_Pl^2 + eta4 p^6/M_Pl^4.
Thus one fixed set of Wilson coefficients can have background-dependent
constraint-pole roots because H=H(a) changes. This is exactly the structural
mechanism missing from the already-proved fixed-Minkowski rational map.

Scope: structural linear-FLRW theorem only. It does not prove that the selected
Route-B coefficient family reproduces the RTK C(a), M_K(a), nor that all
stability/DOF/source conditions pass.
"""
import json
import sympy as sp

lam,H,y,M,eta,eta2,eta4=sp.symbols('lambda H y M eta eta2 eta4', finite=True, real=True)
# y=p^2. Keep generic M for the symbolic source form.
D=sp.expand(3*(3*lam-1)*H**2-eta*y-eta2*y**2/M**2+eta4*y**3/M**4)
# Use algebraic equality rather than structural SymPy expression identity.
assert sp.simplify(sp.diff(D,H,2)-6*(3*lam-1))==0  # nonzero H^2 coefficient generically
assert sp.simplify(D.subs(H,0)-(-eta*y-eta2*y**2/M**2+eta4*y**3/M**4))==0

# Implicit pole motion for a simple root y_*(H): D(y_*,H)=0.
Dy=sp.diff(D,y)
dydH2=sp.factor(-3*(3*lam-1)/Dy)
assert sp.simplify(dydH2 + 3*(3*lam-1)/(-eta-2*eta2*y/M**2+3*eta4*y**2/M**4))==0

# In the two-derivative truncation eta2=eta4=0, the nonzero constraint root is
# exactly proportional to H^2 when eta and 3lambda-1 have the same sign.
y_ir=sp.factor(3*(3*lam-1)*H**2/eta)
assert sp.simplify(D.subs({eta2:0,eta4:0,y:y_ir}))==0

# A fixed-coefficient action therefore does NOT imply a fixed effective pole on
# FLRW. The Minkowski globalization no-go applies only to using the H=0 reduced
# formulas unchanged at every epoch.
out={
  'classification':'RTK_ROUTE_B_FLRW_CONSTRAINT_KERNEL_PASS',
  'primary_source':'Kobayashi-Urakawa-Yamaguchi arXiv:1002.3101v2 Eqs. (19)-(20)',
  'fourier_dictionary':'nabla^2/a^2 -> -p^2, nabla^4/a^4 -> p^4',
  'lapse_kernel':'D_phi=3(3lambda-1)H^2-eta p^2-eta2 p^4/M_Pl^2+eta4 p^6/M_Pl^4',
  'minkowski_limit':'H->0 removes the constant H^2 term and recovers a pure momentum polynomial.',
  'generic_simple_root_motion':'d(pole p^2)/d(H^2) = -3(3lambda-1)/(dD_phi/d(p^2)); generically nonzero.',
  'ir_example':'with eta2=eta4=0, p_pole^2=3(3lambda-1)H^2/eta when the ratio is positive.',
  'theorem':'A fixed healthy-Horava action can generate a background-dependent linear-FLRW constraint pole without time-dependent Wilson coefficients. Therefore the fixed-Minkowski globalization no-go does not extend to fixed-action FLRW by itself.',
  'guards':['constraint-kernel root is not yet the fully integrated propagating scalar pole','matter/source mixing and shift constraint must be integrated before matching RTK observables','the selected BPS Route-B higher-derivative coefficients must be mapped into the FLRW eta_i,g_i basis','no stability, PPN, nonlinear-DOF, radiative or compact-object closure claim'],
  'next_step':'Derive/integrate the full scalar FLRW constraint matrix for the selected Route-B coefficient family and fit its effective pole/residue functions to the replay-certified C(a),M_K(a) rows using one fixed coefficient tuple.'
}
print('RTK_ROUTE_B_FLRW_CONSTRAINT_KERNEL_PASS',json.dumps(out,sort_keys=True))
