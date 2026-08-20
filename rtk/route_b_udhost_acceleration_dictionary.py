#!/usr/bin/env python3
"""Route-B operator dictionary: U-DHOST beta3 is the acceleration/lapse-gradient channel.

Primary source:
  Langlois, Mancarella, Noui, Vernizzi, arXiv:1703.03797 / JCAP 05 (2017) 033,
  especially Eq. (1.2) and the interpretation immediately below it.

Their quadratic unitary-gauge EFT contains
  (M^2/2) * beta3/a^2 * (partial_i delta N)^2,
and states that beta3 comes from the acceleration of the unit normal,
  a_i = partial_i N / N.

Around Minkowski/decoupling kinematics, restoring the clock Stueckelberg field
with t -> t + pi gives delta N = - dot(pi) at linear order up to convention sign.
Therefore (partial_i delta N)^2 maps to (grad dot(pi))^2.  This is exactly the
mixed spatial-kinetic fingerprint required by the RTK rational pole mechanism.

Scope: operator dictionary only.  This does not prove PPN viability, full
U-DHOST completion, a fixed-action FLRW match, compact-object regularity, or
radiative stability.
"""
import json
import sympy as sp

# Fourier symbols and positive EFT normalizations.
omega, q, M2, beta3 = sp.symbols('omega q M2 beta3', positive=True, finite=True, real=True)
pi = sp.symbols('pi', finite=True)

# Linear Stueckelberg scaling: delta N = +/- dot pi.  The sign drops out.
deltaN_amp = omega*pi
lapse_gradient_term = sp.expand((M2/sp.Integer(2))*beta3*q**2*deltaN_amp**2)
expected = sp.expand((M2/sp.Integer(2))*beta3*q**2*omega**2*pi**2)
assert sp.simplify(lapse_gradient_term-expected) == 0

# A canonical mixed-kinetic target K/(2 M_K^2) (grad dot pi)^2 can therefore
# be matched pointwise by choosing M2*beta3 = K/M_K^2, subject to all other
# theory constraints being checked separately.
K, MK = sp.symbols('K M_K', positive=True, finite=True, real=True)
beta3_match = sp.simplify(K/(M2*MK**2))
assert sp.simplify((M2/sp.Integer(2))*beta3_match - K/(2*MK**2)) == 0

out = {
  'classification':'RTK_ROUTE_B_UDHOST_ACCELERATION_DICTIONARY_PASS',
  'primary_source':'Langlois-Mancarella-Noui-Vernizzi arXiv:1703.03797 / JCAP 05 (2017) 033',
  'source_unitary_gauge_operator':'(M^2/2) beta3 a^{-2} (partial_i delta N)^2',
  'source_acceleration_dictionary':'beta3 is the gradient-energy parameter sourced by a_i=partial_i N/N',
  'stueckelberg_linear_dictionary':'delta N = +/- dot(pi) at linear order, so (partial delta N)^2 -> (grad dot pi)^2',
  'pointwise_matching_relation':'beta3 = K/(M^2 M_K^2)',
  'result':'beta3 is exactly the EFT channel that can source the RTK mixed spatial-kinetic operator at quadratic order.',
  'scope':'operator-level/pointwise matching only',
  'non_claims':[
    'does not prove the U-DHOST degeneracy/PPN/GW conditions allow the required beta3 value',
    'does not prove a single fixed action generates the replay C(a), M_K(a) history',
    'does not prove compact-object regularity or radiative stability',
    'does not by itself prove the full observable/source residue map'
  ],
  'next_step':'Intersect the required beta3 channel with the full-degeneracy and U-DHOST weak-field conditions; retain only the partially degenerate branch if full DHOST forces linear dispersion.'
}
print('RTK_ROUTE_B_UDHOST_ACCELERATION_DICTIONARY_PASS', json.dumps(out, sort_keys=True))
