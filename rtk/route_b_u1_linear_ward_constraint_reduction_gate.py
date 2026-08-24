#!/usr/bin/env python3
"""C10 exact linear U1 Ward-constraint reduction on flat FLRW, k>0.

Preregistered target:
  research/theory_targets/RTK_C10_U1_LINEAR_WARD_CONSTRAINT_REDUCTION_TARGET_v1.json

Primary scalar equations are Zhu-Shu-Wu-Wang arXiv:1110.5106
Eqs.(7.10)-(7.12),(7.16), with the source-side Ward normalization already
certified in RTK_C10_U1_PREPOTENTIAL_WARD_NORMALIZATION_RESULT_v1.json.
"""
import json
import sympy as sp

H, lam, G, a = sp.symbols('H lambda G a', finite=True, real=True, nonzero=True)
psi, phi, psip, lapB, q = sp.symbols('psi phi psi_prime lapB q', finite=True, real=True)
lap_psip, lap_psi = sp.symbols('lap_psi_prime lap_psi', finite=True, real=True)
dP, dPp, lapq = sp.symbols('delta_P delta_P_prime lap_q', finite=True, real=True)

# Frozen linear Ward source in conformal flat-FLRW variables:
# delta J_varphi = a^-1 [deltaP' + 3 H deltaP - a^-1 partial^2 q].
ward_rhs = sp.expand(8*sp.pi*G*a**3 * (dPp + 3*H*dP - lapq/a)/a)
ward_rhs_expected = sp.expand(8*sp.pi*G*a**2*(dPp+3*H*dP) - 8*sp.pi*G*a*lapq)
assert sp.simplify(ward_rhs-ward_rhs_expected) == 0

# A constraint with literature delta J_A=2 deltaP:
# partial^2 psi = 4 pi G a^2 deltaP.
# Differentiate in conformal time, using (a^-2)'=-2H a^-2:
# deltaP' = [lap psi' - 2 H lap psi]/(4 pi G a^2).
dP_from_A = lap_psi/(4*sp.pi*G*a**2)
dPp_from_A = (lap_psip-2*H*lap_psi)/(4*sp.pi*G*a**2)
density_piece = sp.simplify(8*sp.pi*G*a**2*(dPp_from_A+3*H*dP_from_A))
density_expected = 2*(lap_psip+H*lap_psi)
assert sp.simplify(density_piece-density_expected) == 0

# Therefore the full prepotential-source RHS is a Laplacian of a bracket.
# partial^2 q is represented by lapq and linearity gives
# RHS = partial^2[2(psi'+H psi)-8 pi G a q].
source_bracket = sp.expand(2*(psip+H*psi)-8*sp.pi*G*a*q)

# Momentum constraint Eq.(7.12).
momentum_q = sp.expand((3*lam-1)*(psip+H*phi)+(lam-1)*lapB)
source_after_momentum = sp.expand(source_bracket.subs(8*sp.pi*G*a*q, momentum_q))

# Eq.(7.10) prepotential gravitational bracket.
prepotential_bracket = sp.expand(2*H*(psi-phi)+(1-lam)*(lapB+3*psip+3*H*phi))
residual = sp.simplify(source_after_momentum-prepotential_bracket)
assert residual == 0

# Independent coefficient audit, guarding against an accidental simplification.
vars_basis=[psip,H*psi,H*phi,lapB]
coeff_a={str(v):sp.expand(source_after_momentum).coeff(v) for v in vars_basis}
coeff_b={str(v):sp.expand(prepotential_bracket).coeff(v) for v in vars_basis}
assert coeff_a==coeff_b

out={
  'classification':'C10_U1_LINEAR_PREPOTENTIAL_REDUNDANCY_PASS_K_GT_0_SCOPED',
  'status_scope':'GREEN_EXACT_LINEAR_WARD_CONSISTENCY_K_GT_0_HAMILTONIAN_AND_DYNAMICAL_SECTOR_OPEN',
  'primary_equations':'Zhu-Shu-Wu-Wang arXiv:1110.5106 Eqs.(7.10)-(7.12),(7.16)',
  'current_convention':'Eq.(3.16) defines J^i=-N delta L_M/delta N_i; Eq.(7.16) uses delta J^i=a^-2 partial^i q.',
  'linear_Ward_source':'delta J_varphi=a^-1[(delta P)\u0027+3H delta P-a^-1 partial^2 q], with delta J_A=2 delta P',
  'A_constraint':'partial^2 psi=4 pi G a^2 delta P',
  'differentiated_A_constraint':'delta P\u0027=[partial^2 psi\u0027-2H partial^2 psi]/(4 pi G a^2)',
  'density_source_identity':'8 pi G a^2[(delta P)\u0027+3H delta P]=2 partial^2(psi\u0027+H psi)',
  'prepotential_RHS_after_Ward_and_A':'partial^2[2(psi\u0027+H psi)-8 pi G a q]',
  'momentum_constraint':'8 pi G a q=(3lambda-1)(psi\u0027+H phi)+(lambda-1)partial^2 B',
  'exact_reduced_bracket':'2H(psi-phi)+(1-lambda)(partial^2 B+3psi\u0027+3H phi)',
  'symbolic_residual':'0',
  'interpretation':'For every nonzero scalar Fourier mode, Eq.(7.10) is exactly the Ward-consistency consequence of the A constraint Eq.(7.11), momentum constraint Eq.(7.12), and the locally U1-consistent source definitions. It is not an additional independent linear source constraint in this scoped flat-FLRW gauge sector.',
  'important_remaining_constraint':'Eq.(7.11) remains an independent extra A constraint relative to GR; this result does not remove the U1 scalar restriction that eliminates the unwanted gravitational scalar mode.',
  'k0_guard':'The common partial^2 operator may be cancelled only for k>0. Exact k=0 remains governed by the separately certified homogeneous bridge and is outside this theorem.',
  'next_gate':'Reduce Eqs.(7.13)-(7.15) on the same source/action conventions, determine a minimal independent metric system after eliminating the derived Eq.(7.10), and only then define a CLASS implementation interface.',
  'non_claims':[
    'not a nonlinear Ward/redundancy theorem',
    'not an exact k=0 theorem',
    'does not close Eq.(7.13) Hamiltonian constraint',
    'does not close Eqs.(7.14)-(7.15) trace/traceless dynamics',
    'does not implement CLASS or change any likelihood result',
    'does not include the separate B4 massive-neutrino extension'
  ],
  'target':'research/theory_targets/RTK_C10_U1_LINEAR_WARD_CONSTRAINT_REDUCTION_TARGET_v1.json'
}
open('u1_linear_ward_constraint_reduction_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
