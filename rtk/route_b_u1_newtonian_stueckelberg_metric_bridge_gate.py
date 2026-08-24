#!/usr/bin/env python3
"""C10 physical-metric Newtonian-coordinate/Stueckelberg bridge theorem.

This is a kinematic coordinate representation plus substitution of the already
certified quasilongitudinal traceless deltaA solve.  The preferred-foliation
Stueckelberg chi is deliberately distinct from the RTK/DBI scalar Sigma and from
U1 prepotential varphi.
"""
import json
from pathlib import Path
import sympy as sp

H,a,G,L=sp.symbols('H a G L', nonzero=True, finite=True, real=True)
Phi,Psi,B,E,Ep,T,Lg,Lgp=sp.symbols('Phi Psi B E Eprime T Lg Lgprime', finite=True, real=True)
phi,psi,dA,Bp,Pi,Pcal,alpha1,Ahat=sp.symbols('phi psi deltaA Bprime Pi Pcal alpha1 Ahat', finite=True, real=True)
chi=sp.symbols('chi', finite=True, real=True)

# General scalar coordinate transformation convention frozen in target.
Phi_t=sp.expand(Phi-H*T-sp.Symbol('Tprime'))
Psi_t=sp.expand(Psi+H*T)
B_t=sp.expand(B+T-Lgp)
E_t=sp.expand(E-Lg)
# sigma=B-E'; under the same transform E'->E'-L'.
sigma=sp.expand(B-Ep)
sigma_t=sp.expand(B_t-(Ep-Lgp))
assert sp.simplify(sigma_t-(sigma+T))==0

# Newtonian-coordinate choice L=E, T=-sigma.
Phi_N_general=sp.expand(Phi+H*sigma+sp.Symbol('sigmaprime'))
Psi_N_general=sp.expand(Psi-H*sigma)
assert sp.simplify(B-sigma-Ep)==0  # B_N with L'=E' and T=-sigma
assert sp.simplify(E-E)==0

# Preferred/unitary coordinates have chi=0; scalar T_fol perturb transforms chi->chi-T.
chi_N=sp.simplify(0-(-sigma))
assert sp.simplify(chi_N-sigma)==0

# Frozen quasilongitudinal physical matter metric: E=0, sigma=B,
# Phi_matter=phi-deltaA/a, Psi_matter=psi, Ahat=0.
Phi_m=phi-dA/a
Psi_m=psi
Phi_N=sp.expand(Phi_m+H*B+Bp)
Psi_N=sp.expand(Psi_m-H*B)

# Existing exact traceless solution from C10 minimal reduction.  Apply the
# frozen Ahat=0 branch to the replacement expression before inserting it;
# SymPy does not recursively reapply a same-call dict substitution inside a
# newly inserted replacement in all cases.
dA_expr=Ahat*psi+a*(8*sp.pi*G*a**2*Pi+Bp+2*H*B-psi+Pcal*phi-alpha1*L*psi)
dA_expr_Ahat0=sp.expand(dA_expr.subs(Ahat,0))
Phi_N_reduced=sp.factor(Phi_N.subs(dA,dA_expr_Ahat0))
Phi_N_expected=sp.expand((1-Pcal)*phi+psi+alpha1*L*psi-H*B-8*sp.pi*G*a**2*Pi)
assert sp.simplify(Phi_N_reduced-Phi_N_expected)==0
assert not Phi_N_reduced.has(Bp)
assert not Phi_N_reduced.has(Ahat)

Psi_N_expected=sp.expand(psi-H*B)
assert sp.simplify(Psi_N-Psi_N_expected)==0
slip=sp.factor(Phi_N_expected-Psi_N_expected)
slip_expected=sp.expand((1-Pcal)*phi+alpha1*L*psi-8*sp.pi*G*a**2*Pi)
assert sp.simplify(slip-slip_expected)==0
assert not slip.has(B) and not slip.has(Bp)

out={
  'classification':'C10_U1_NEWTONIAN_STUECKELBERG_METRIC_BRIDGE_PASS_SCOPED',
  'status_scope':'GREEN_KINEMATIC_NEWTONIAN_COORDINATE_REPRESENTATION_SOURCE_TRANSFORM_AND_POLE_AUDIT_NEXT',
  'general_newtonian_metric_map':{
    'sigma_phys':'B_phys-E_prime',
    'Phi_N':'Phi_matter+H sigma_phys+sigma_phys_prime',
    'Psi_N':'Psi_matter-H sigma_phys'
  },
  'preferred_foliation_stueckelberg':{
    'unitary_preferred_coordinates':'chi=0',
    'after_T_minus_sigma_coordinate_change':'chi_N=sigma_phys',
    'non_identification':'chi is neither RTK/DBI Sigma nor U1 Newtonian prepotential varphi'
  },
  'frozen_quasilongitudinal_branch':{
    'sigma_phys':'B',
    'Phi_matter':'phi-deltaA/a',
    'Psi_matter':'psi',
    'Ahat':0
  },
  'reduced_newtonian_potentials':{
    'Phi_N':'(1-Pcal)phi+psi+alpha1 L psi-H B-8 pi G a^2 Pi_total',
    'Psi_N':'psi-H B',
    'Phi_N_minus_Psi_N':'(1-Pcal)phi+alpha1 L psi-8 pi G a^2 Pi_total'
  },
  'Bprime_cancellation':'exact after substituting the already-certified traceless deltaA solve on the frozen Ahat=0 branch',
  'interpretation':'A standard Newtonian-coordinate matter metric can be constructed without discarding preferred-foliation information: the latter is carried by chi_N=B internally. The physical Newtonian potentials require no B-prime variable after the exact traceless constraint is used. This is a constructive route to a CLASS interface, not a direct unitary-gauge identification.',
  'next_gate':'transform total density/momentum/pressure sources between preferred/quasilongitudinal and Newtonian coordinates and audit the transformed algebraic constraints for poles over the certified finite-k rank domain',
  'non_claims':[
    'not a completed transformed gravity solver',
    'not a proof that chi vanishes',
    'not a new degree-of-freedom theorem',
    'not a CLASS implementation',
    'not a likelihood result',
    'not an identification of chi with RTK/DBI Sigma'
  ],
  'target':'research/theory_targets/RTK_C10_U1_NEWTONIAN_STUECKELBERG_METRIC_BRIDGE_TARGET_v1.json'
}
Path('u1_newtonian_stueckelberg_metric_bridge_result.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
