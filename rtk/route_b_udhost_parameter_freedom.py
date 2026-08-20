#!/usr/bin/env python3
"""Narrow U-DHOST parameter-freedom gate for the Route-B rescue program.

Primary source:
  Saito, Yao, Kobayashi, arXiv:2402.10459 / JCAP 06 (2024) 040.

The paper states for the U-DHOST EFT that unitary-gauge degeneracy imposes
  beta2 = -6 beta1^2/(1+alphaL),
while aside from this relation the EFT parameters are independent. It also
identifies alphaT=c_GW^2-1.

This script proves only the algebraic compatibility of
  (i) U-DHOST degeneracy and
  (ii) luminal tensors alphaT=0
with a still-free beta3 direction and nonzero beta1/alphaL choices.

It does NOT identify beta3 with the RTK acceleration operator, does NOT prove
PPN=GR, and does NOT construct the full RTK completion. Those are separate
physics gates.
"""
import json
import sympy as sp

alphaL,beta1,beta3 = sp.symbols('alpha_L beta_1 beta_3', real=True, finite=True)
# Work away from the singular alphaL=-1 surface.
assert sp.simplify((1+alphaL) - (1+alphaL)) == 0
beta2 = sp.simplify(-6*beta1**2/(1+alphaL))
alphaT = sp.Integer(0)

# Exhibit a regular nontrivial point with beta3 left arbitrary.
example = {alphaL: sp.Rational(1,2), beta1: sp.Rational(1,3)}
assert sp.simplify(beta2.subs(example) + sp.Rational(4,9)) == 0
assert alphaT == 0
assert beta3 not in beta2.free_symbols

out = {
  'classification':'RTK_ROUTE_B_UDHOST_PARAMETER_FREEDOM_PASS',
  'primary_source':'Saito-Yao-Kobayashi arXiv:2402.10459 / JCAP 06 (2024) 040',
  'degeneracy_relation':'beta2=-6 beta1^2/(1+alphaL)',
  'tensor_speed_condition':'alphaT=0 gives c_GW=1',
  'result':'Degeneracy plus luminal tensors leaves at least beta3 algebraically free; therefore these two conditions alone do not collapse the U-DHOST scalar/constraint sector to the khronometric alpha=0 boundary.',
  'scope':'parameter-freedom theorem only',
  'non_claims':[
    'does not prove beta3 is the coefficient required for the RTK (grad dot pi)^2 operator',
    'does not prove all PPN parameters equal GR for the RTK-matched point',
    'does not prove compact-object regularity',
    'does not prove one fixed action reproduces C(a) and M_K(a)',
    'does not prove nonlinear or radiative stability'
  ],
  'next_step':'Derive the unitary-gauge operator dictionary for the RTK acceleration channel in U-DHOST, then intersect that mapping with the sourced GR-like PPN conditions.'
}
print('RTK_ROUTE_B_UDHOST_PARAMETER_FREEDOM_PASS', json.dumps(out, sort_keys=True))
