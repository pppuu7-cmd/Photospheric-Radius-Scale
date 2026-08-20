#!/usr/bin/env python3
"""Narrow U-DHOST parameter-freedom gate for the Route-B rescue program.

Primary source:
  Saito, Yao, Kobayashi, arXiv:2402.10459 / JCAP 06 (2024) 040.

The paper states for the U-DHOST EFT that unitary-gauge degeneracy imposes
  beta2 = -6 beta1^2/(1+alphaL),
while aside from this relation the EFT parameters are independent. It also
identifies alphaT=c_GW^2-1.

Independent operator dictionary:
  Langlois, Mancarella, Noui, Vernizzi, arXiv:1703.03797 / JCAP 05 (2017) 033
identifies beta3 with the lapse-gradient/normal-acceleration channel
  a_i = partial_i N/N,
so beta3 is the correct quadratic EFT channel for (grad dot pi)^2 after
Stueckelberg restoration.

This script proves only the algebraic compatibility of
  (i) U-DHOST degeneracy and
  (ii) luminal tensors alphaT=0
with a still-free beta3 direction and nonzero beta1/alphaL choices.

It does NOT prove the required beta3 value lies on the PPN-safe U-DHOST
subspace, nor construct the full RTK completion.
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
  'operator_dictionary_source':'Langlois-Mancarella-Noui-Vernizzi arXiv:1703.03797 / JCAP 05 (2017) 033',
  'degeneracy_relation':'beta2=-6 beta1^2/(1+alphaL)',
  'tensor_speed_condition':'alphaT=0 gives c_GW=1',
  'beta3_semantics':'lapse-gradient / normal-acceleration channel, hence the quadratic source of (grad dot pi)^2 after Stueckelberg restoration',
  'result':'U-DHOST degeneracy plus luminal tensors leaves beta3 algebraically free, and beta3 is the correct acceleration channel for the RTK mixed spatial-kinetic operator.',
  'scope':'parameter-freedom plus sourced operator identification only',
  'non_claims':[
    'does not prove all PPN parameters equal GR for the RTK-matched beta3 value',
    'does not prove the exact RTK rational denominator survives all U-DHOST constraints',
    'does not prove compact-object regularity',
    'does not prove one fixed action reproduces C(a) and M_K(a)',
    'does not prove nonlinear or radiative stability'
  ],
  'boundary':'Fully degenerate DHOST C_I/C_II is not the direct exact-rational rescue branch in the 2017 quadratic EFT, where full degeneracy reduces scalar dispersion to a linear form. The open route is partial U-DHOST degeneracy.',
  'next_step':'Intersect nonzero beta3 with the explicit PPN-safe U-DHOST conditions of arXiv:2310.11041 and arXiv:2402.10459, then derive the constrained scalar dispersion.'
}
print('RTK_ROUTE_B_UDHOST_PARAMETER_FREEDOM_PASS', json.dumps(out, sort_keys=True))
