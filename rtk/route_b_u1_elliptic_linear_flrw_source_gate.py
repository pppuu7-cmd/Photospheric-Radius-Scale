#!/usr/bin/env python3
"""Exact first-order projected-source theorem for the elliptic U(1) compensator on FLRW.

The operator equation is L Q=H0 with L=1-D^2/M_c^2.  Linearizing,

  delta Q = L0^{-1} delta H0 - L0^{-1}(delta L)L0^{-1} H0_bar.

For spatially homogeneous H0_bar, D_i H0_bar=0 for every spatial metric, so
(delta D^2)H0_bar=0 and therefore (delta L)H0_bar=0.  The metric-resolvent term
vanishes at first order.  A Fourier perturbation mode with
ell=1+k_phys^2/M_c^2 consequently has delta Q=delta H0/ell.
"""
import json
import sympy as sp

ell = sp.symbols('ell', positive=True, finite=True)
Hbar, dH = sp.symbols('Hbar delta_H0', finite=True)
# A two-mode representative: component 0 is the homogeneous background source,
# component 1 is one Fourier perturbation mode.  Homogeneity implies the first
# column of delta L vanishes, i.e. delta L acting on Hbar is exactly zero.
u, v = sp.symbols('u v', finite=True)
L0 = sp.diag(1, ell)
dL = sp.Matrix([[0, u], [0, v]])
H0bar = sp.Matrix([Hbar, 0])
dHvec = sp.Matrix([0, dH])
L0inv = L0.inv()
assert dL * H0bar == sp.zeros(2, 1)

dQ = sp.simplify(L0inv*dHvec - L0inv*dL*L0inv*H0bar)
expected_dQ = sp.Matrix([0, dH/ell])
assert all(sp.simplify(x)==0 for x in (dQ-expected_dQ))

# Fourier dictionary and complementary source transfer.
q, Mc2 = sp.symbols('k_phys_squared M_c_squared', nonnegative=True, finite=True)
Mc2 = sp.symbols('M_c_squared', positive=True, finite=True)
q = sp.symbols('k_phys_squared', nonnegative=True, finite=True)
ell_q = sp.factor(1 + q/Mc2)
qratio = sp.factor(1/ell_q)
aeff = sp.factor(1-qratio)
assert sp.simplify(aeff - q/(Mc2+q)) == 0
assert sp.simplify(qratio - Mc2/(Mc2+q)) == 0
assert sp.simplify(aeff+qratio-1) == 0

dJ = sp.factor((qratio-1)*dH)
dpnu = sp.factor((1-qratio)*dH)
assert sp.simplify(dJ + aeff*dH) == 0
assert sp.simplify(dpnu - aeff*dH) == 0
assert sp.simplify(dJ+dpnu) == 0
assert sp.simplify(aeff.subs(q,0)) == 0
assert sp.simplify(qratio.subs(q,0)-1) == 0
assert sp.simplify(sp.limit(aeff,q,sp.oo)-1) == 0
assert sp.simplify(sp.limit(qratio,q,sp.oo)) == 0

out={
  'classification':'RTK_ROUTE_B_U1_ELLIPTIC_LINEAR_FLRW_SOURCE_PASS',
  'status_scope':'GREEN_EXACT_LINEAR_PROJECTED_SOURCE_TRANSFER_REDUCED_METRIC_CONSTRAINT_MAPPING_PENDING',
  'target':'research/theory_targets/RTK_ROUTE_B_U1_ELLIPTIC_LINEAR_FLRW_SOURCE_TARGET_v1.json',
  'operator_equation':'L Q=H0, L=1-D^2/M_c^2',
  'linearization':'delta Q=L0^{-1}delta H0-L0^{-1}(delta L)L0^{-1}H0_bar',
  'homogeneous_identity':'D_i H0_bar=0 => (delta D^2)H0_bar=0 => (delta L)H0_bar=0',
  'fourier_result':{
    'ell':'1+k_phys^2/M_c^2',
    'delta_Q':'delta H0/ell',
    'Q_transfer':'1/ell=M_c^2/(M_c^2+k_phys^2)',
    'a1_eff':'k_phys^2/(M_c^2+k_phys^2)',
    'delta_J_A_total':'-a1_eff delta H0',
    'delta_p_nu_total':'+a1_eff delta H0',
    'gauge_pair_identity':'delta p_nu_total+delta J_A_total=0'
  },
  'perturbative_order_guard':'The product (delta a_eff)(delta H0) is second order and is not part of the linear source. Metric-resolvent variation re-enters for nonlinear perturbations or inhomogeneous backgrounds.',
  'implementation_consequence':'On homogeneous FLRW, the first-order ordinary+auxiliary projected A/prepotential source can be represented by the scalar transfer a1_eff(k,a), but the final CLASS metric equations still require an explicit reduction/mapping of the U1 constraints; this theorem is not permission to alter only RTK fluid cs2.',
  'non_claims':[
    'does not derive the final reduced Einstein/CLASS metric constraint equations',
    'does not cover nonlinear perturbations or inhomogeneous backgrounds',
    'does not solve massive-neutrino anisotropic stress',
    'does not choose M_c or lambda_HL',
    'does not provide a likelihood result'
  ],
  'next_gate':'extend the standalone completion shadow module with the certified linear source transfer and freeze the reduced metric-constraint mapping required to insert this source into CLASS.'
}
with open('u1_elliptic_linear_flrw_source_result.json','w') as f:
    json.dump(out,f,indent=2,sort_keys=True); f.write('\n')
print(out['classification'], json.dumps(out,sort_keys=True))
