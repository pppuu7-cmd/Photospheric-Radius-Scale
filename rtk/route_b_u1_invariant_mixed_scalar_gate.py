#!/usr/bin/env python3
"""C8 exact U(1)-invariant building-block gate for the RTK mixed scalar.

Conventions follow the nonprojectable U(1) Hořava Hamiltonian literature
(arXiv:1504.07357):

    delta N^i = N D^i alpha,
    delta nu  = alpha,
    delta N = delta g_ij = 0,
    delta A = N partial_perp alpha
            = dot alpha - N^i D_i alpha.

The invariant shift is

    Ntilde^i = N^i - N D^i nu.

A second standard invariant is

    sigma = A/N - partial_perp nu - 1/2 D_i nu D^i nu.

For a U(1)-neutral scalar Sigma, define

    Theta_U = [dot Sigma - Ntilde^i D_i Sigma]/N.

Since Ntilde^i and N are invariant, Theta_U is invariant. Therefore a
mixed-derivative operator

    C(X,...) D_i Theta_U D^i Theta_U

is compatible with the local U(1) symmetry. This is a symmetry feasibility
theorem only. It does not establish that the full coupled RTK candidate has the
special Hamiltonian constraint structure required to eliminate the gravity
scalar, nor that its PPN/radiative gates pass.
"""

import json
import sympy as sp

# Work in one spatial direction; all formulas are tensorially componentwise.
N,Ni,nui,ai = sp.symbols('N Ni nui ai', nonzero=True, finite=True, real=True)
Adotalpha, nudot, A = sp.symbols('Adotalpha nudot A', finite=True, real=True)
sdot, si = sp.symbols('sdot si', finite=True, real=True)

# Infinitesimal U(1) variations. ai = D_i alpha, Adotalpha = dot(alpha).
dNi = N*ai
dnui = ai
dA = Adotalpha-Ni*ai

Ntilde = Ni-N*nui
dNtilde = sp.simplify(dNi-N*dnui)
assert dNtilde == 0

# partial_perp nu=(nudot-Ni*nui)/N.
# Its infinitesimal variation includes the shift variation:
# delta(partial_perp nu)=[dot alpha - deltaNi*nui - Ni*ai]/N.
dperpnu = sp.simplify((Adotalpha-dNi*nui-Ni*ai)/N)
perpalpha = sp.simplify((Adotalpha-Ni*ai)/N)
assert sp.simplify(dperpnu-(perpalpha-ai*nui)) == 0

# delta[1/2 (D nu)^2]=nui*ai in one Cartesian component.
dgradnu2half = nui*ai
# delta(A/N)=partial_perp alpha.
dAoverN = perpalpha
dsigma = sp.simplify(dAoverN-dperpnu-dgradnu2half)
assert dsigma == 0

# Neutral Sigma: delta Sigma=0. Theta_U uses only invariant shift and lapse.
Theta = sp.simplify((sdot-Ntilde*si)/N)
# Since dNtilde=dN=dsdot=dsi=0 under U(1), its variation is exactly zero.
dTheta = sp.simplify(-dNtilde*si/N)
assert dTheta == 0

out = {
  'classification':'RTK_ROUTE_B_U1_INVARIANT_MIXED_SCALAR_GATE_PASS',
  'u1_transformations':{
    'delta_Ni':'N D_i alpha',
    'delta_nu':'alpha',
    'delta_A':'dot alpha-N^i D_i alpha',
    'delta_N':'0'
  },
  'invariant_shift':'Ntilde^i=N^i-N D^i nu',
  'invariant_sigma':'A/N-partial_perp nu-(D nu)^2/2',
  'neutral_scalar_normal_derivative':'Theta_U=(dot Sigma-Ntilde^i D_i Sigma)/N',
  'allowed_mixed_operator':'C D_i Theta_U D^i Theta_U is U(1)-invariant for U(1)-neutral C/state invariants',
  'interpretation':'The RTK q^2 omega^2 mixed kinetic fingerprint can be embedded in the standard local-U(1) preferred-foliation gauge algebra without breaking the U(1) by the operator itself.',
  'non_claims':[
    'not a proof that the coupled gravity+Sigma system has only one scalar DOF',
    'not a proof that the special eta1=eta2=0 gravity surface is radiatively stable',
    'not a PPN/Newton or matter-frame calculation',
    'not a proof of the full production DBI coefficient map'
  ],
  'next_step':'Combine the U(1)-special gravity constraint surface with one rolling DBI/RTK scalar using Theta_U, then audit: total nonlinear DOF, exact production mixed coefficient, static PPN response in the universal matter metric, and radiative regeneration of the scalar-graviton couplings.'
}
print('RTK_ROUTE_B_U1_INVARIANT_MIXED_SCALAR_GATE_PASS',json.dumps(out,sort_keys=True))
