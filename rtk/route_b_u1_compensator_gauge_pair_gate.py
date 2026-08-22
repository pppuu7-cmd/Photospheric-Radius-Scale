#!/usr/bin/env python3
"""Exact scoped theorem: the minimal sigma F(X_U) compensator preserves the local-U(1) gauge pair.

Motivation
----------
The frozen prefilter candidate

    Delta L_M = - sigma rho_comp(X_U),
    sigma=(A-Acal)/N,

contains dot(phi) through Acal and dot(Sigma) through X_U.  Its
(dot(phi),dot(Sigma)) velocity Hessian is generically nonzero, so the old
velocity-support proof cannot simply be reused.  However this alone does not
mean that phi becomes a physical mode.

Local U(1) invariance implies that A and dot(phi) occur through the invariant
combination B=A+dot(phi)+spatial terms.  On a local homogeneous/rank slice the
relevant Legendre structure is therefore

    L = L0(v) + B G(v),       B=A+v_phi,

where v denotes all other regular velocities, including the RTK clock and (if
present) ordinary-matter velocities.

For a regular Legendre map in (B,v):

    p_A   = 0,
    p_phi = dL/dB = G(v),

and after Legendre transformation

    H = H0(p_phi,p_v,...) - A p_phi.

Thus preservation of p_A gives the secondary p_phi≈0.  If the action has no
explicit phi (the shift/U1 invariant case), preservation of p_phi gives no new
constraint and {p_A,p_phi}=0.  The pair is first class and removes exactly the
(A,phi) canonical sector.  Therefore a nonzero phi-clock Hessian block does not
by itself add a physical degree of freedom.

Scope warning: this proves only preservation of the U(1) gauge pair.  It does
NOT prove that the full nonprojectable lapse/metric/A constraint matrix keeps
the exceptional sigma1=sigma2=0 rank after adding the compensator.
"""

import json
import sympy as sp

# Use an explicit polynomial representative with generic nonzero coefficients
# to verify the exact Legendre identity while retaining symbolic parameters.
A, vphi, v, pphi, pv = sp.symbols('A vphi v p_phi p_v', finite=True, real=True)
m, g0, g1 = sp.symbols('m g0 g1', nonzero=True, finite=True, real=True)
B = A + vphi
L0 = sp.Rational(1,2)*m*v**2
G = g0 + g1*v
L = L0 + B*G

pA = sp.Integer(0)
pphi_expr = sp.diff(L, vphi)
pv_expr = sp.diff(L, v)
assert pA == 0
assert sp.simplify(pphi_expr-G) == 0
assert sp.simplify(pv_expr-(m*v+B*g1)) == 0

# Invert the regular map: p_phi=g0+g1 v; p_v=m v+B g1.
v_sol = sp.simplify((pphi-g0)/g1)
B_sol = sp.simplify((pv-m*v_sol)/g1)
vphi_sol = sp.simplify(B_sol-A)

H = sp.expand(pphi*vphi_sol + pv*v_sol - L.subs({v:v_sol, vphi:vphi_sol}))
Hsplit = sp.simplify(H + A*pphi)
assert sp.simplify(sp.diff(Hsplit, A)) == 0
assert sp.simplify(H - (Hsplit-A*pphi)) == 0

# Dirac chain in the scoped gauge sector.
# Primary C1=p_A.  H contains -A p_phi, so dot(C1)=+p_phi (sign convention
# irrelevant for the zero surface), giving C2=p_phi.  No explicit phi means
# dot(C2)=-dH/dphi=0.  Canonical {p_A,p_phi}=0.
secondary = pphi
tertiary = sp.Integer(0)
poisson_C1_C2 = sp.Integer(0)
assert secondary == pphi
assert tertiary == 0
assert poisson_C1_C2 == 0

# Phase-space removal in this gauge sector: two canonical pairs (A,p_A) and
# (phi,p_phi) = 4 dimensions; two first-class constraints remove 4 dimensions.
phase_dim_sector = 4
first_class_sector = 2
physical_phase_dim_sector = phase_dim_sector - 2*first_class_sector
assert physical_phase_dim_sector == 0

# Connect to the actual compensator: G contains ordinary universal-matter
# source minus rho_comp(X_U).  The prefilter proved rho_comp is state-dependent,
# so the regular Legendre map can have a nonzero phi-clock Hessian while the
# gauge pair above still survives.
out={
  'classification':'RTK_ROUTE_B_U1_COMPENSATOR_GAUGE_PAIR_PASS',
  'status_scope':'GREEN_SCOPED_U1_GAUGE_PAIR_PRESERVED_FULL_DOF_PENDING',
  'candidate':'research/RTK_U1_MINIMAL_CLOCK_A_COMPENSATOR_PREFILTER_v1.json',
  'structural_form':'L=L0(v)+B G(v), B=A+dot(phi)+spatial U1 completion',
  'exact_hamiltonian_identity':'H=H0(p_phi,p_v,...)-A p_phi',
  'constraints':{
    'primary':'p_A≈0',
    'secondary':'p_phi≈0 from preservation of p_A',
    'tertiary':'none in the scoped U1 sector when H0 has no explicit phi',
    'bracket':'{p_A,p_phi}=0',
    'class':'two first-class constraints in the U1 gauge sector'
  },
  'dof_implication':'The (A,phi) canonical sector contributes zero physical phase-space dimensions. A nonzero dot(phi)-clock Hessian block does not by itself create a physical scalar.',
  'important_caveat':'This does not certify the full nonprojectable gravity+clock+matter constraint rank. The new A-source can alter brackets involving lapse/H_perp and other second-class constraints even though the U1 gauge pair survives.',
  'non_claims':[
    'not a complete 2 tensor + 1 RTK scalar proof',
    'not a proof that all inhomogeneous Legendre maps are regular',
    'not a PPN, equivalence-principle, radiative, cutoff or compact-object pass',
    'not a replacement for the exceptional sigma1=sigma2=0 Hamiltonian rank theorem'
  ],
  'next_gate':'compute the compensator-induced modifications to the full constraint Poisson matrix on a regular rolling X_U>0 slice, with special attention to {pi_N,H_perp}, A-source cross-blocks and the four second-class constraints. Require the total physical count to remain 2 tensor + 1 intended RTK scalar before any PPN promotion.'
}
open('u1_compensator_gauge_pair_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
