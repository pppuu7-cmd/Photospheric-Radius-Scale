#!/usr/bin/env python3
"""Exact beta=0 normalization gate for the direct spatial-covariant C8 carrier.

The previous FLRW exact-match theorem showed, in production units,

    K_8piG = 2 M_K^2,

and therefore the local acceleration operator must have physical coefficient

    C_acc,required = K_phys/(2 M_K^2).

A subtlety is which gravitational normalization converts the production
`rho_8piG,p_8piG` quantities to physical units.  For a minimally/universally
coupled healthy-Horava/khronometric interpretation of the *same cosmological
background*, the relevant conversion is the Friedmann coupling G_cosm, not the
bare Planck coefficient by assumption.

For the beta=0 matter-frame branch of Blas-Pujolas-Sibiryakov (arXiv:1007.3503,
Eqs. 5.30-5.32), with bare reduced Planck coefficient M_b^2 and lambda'=ell,

    M_N^2    := 1/(8 pi G_N)    = M_b^2 (1-alpha/2),
    M_cosm^2 := 1/(8 pi G_cosm) = M_b^2 (1+3 ell/2).

The covariant acceleration term carries coefficient

    C_acc,BPS = M_b^2 alpha/2.

Identifying the production background normalization with G_cosm gives

    C_acc,required = M_cosm^2.

Exact RTK matching therefore forces

    alpha = 2 + 3 ell.

The beta=0 low-energy scalar has c_chi^2 = ell/alpha.  For a healthy positive
kinetic/gradient branch one needs alpha>0 and ell/alpha>0.  Positive finite
Newton gravity also requires 1-alpha/2>0 (equivalently 0<alpha<2).
The exact matching relation makes these requirements mutually incompatible:

* ell>0  -> alpha>2 -> negative Newton reduced mass squared;
* ell=0  -> alpha=2 -> singular G_N and c_chi^2=0;
* -2/3<ell<0 -> 0<alpha<2 but c_chi^2<0;
* ell<=-2/3 -> alpha<=0.

Thus the direct acceleration-only C8 exact-match carrier has no healthy,
positive-Newton realization in the minimal beta=0 universally coupled branch
once the cosmological-vs-bare normalization is treated correctly.

Scope is intentionally narrow.  This is not a no-go for beta!=0, xi!=1,
nonminimal/disformal matter frames, companion operators, auxiliary-field
realizations, or the spatially-covariant quadratic EFT viewed without this
specific covariant/matter identification.
"""

from __future__ import annotations
import json
import sympy as sp

Mb2, alpha, ell = sp.symbols('Mb2 alpha ell', positive=True, finite=True, real=True)

MN2 = sp.simplify(Mb2 * (1 - alpha/2))
Mcosm2 = sp.simplify(Mb2 * (1 + 3*ell/2))
C_bps = sp.simplify(Mb2 * alpha/2)
C_required = Mcosm2

# Exact-match equation.
alpha_match = sp.solve(sp.Eq(C_bps, C_required), alpha)
assert alpha_match == [2 + 3*ell]
alpha_exact = alpha_match[0]

MN2_on_match = sp.factor(MN2.subs(alpha, alpha_exact))
assert sp.simplify(MN2_on_match + sp.Rational(3,2)*Mb2*ell) == 0

cchi2_on_match = sp.factor(ell/alpha_exact)
assert sp.simplify(cchi2_on_match - ell/(2+3*ell)) == 0

# Friedmann/Newton ratio under the exact-match relation.
# G_cosm/G_N = MN2/Mcosm2 because G = 1/(8 pi M_reduced^2).
ratio_Gcosm_GN = sp.factor(MN2_on_match / Mcosm2.subs(alpha, alpha_exact))
assert sp.simplify(ratio_Gcosm_GN + 3*ell/(2+3*ell)) == 0

# Boundary cases encoded exactly.
assert sp.simplify(alpha_exact.subs(ell, 0) - 2) == 0
assert sp.simplify(MN2_on_match.subs(ell, 0)) == 0
assert sp.simplify(cchi2_on_match.subs(ell, 0)) == 0
assert sp.simplify(alpha_exact.subs(ell, -sp.Rational(2,3))) == 0

# A generic numerical sanity point from each relevant interval.
for e, expected in [
    (sp.Rational(1,10), 'alpha_gt_2'),
    (-sp.Rational(1,10), 'gradient_negative'),
    (-sp.Rational(3,4), 'alpha_nonpositive'),
]:
    a = sp.N(alpha_exact.subs(ell, e))
    mn = sp.N(MN2_on_match.subs({ell:e, Mb2:1}))
    cs = sp.N(cchi2_on_match.subs(ell, e))
    if expected == 'alpha_gt_2':
        assert a > 2 and mn < 0 and cs > 0
    elif expected == 'gradient_negative':
        assert 0 < a < 2 and mn > 0 and cs < 0
    else:
        assert a <= 0

out = {
    'classification': 'RTK_ROUTE_B_SPATIAL_COVARIANT_COSMOLOGICAL_NEWTON_GATE_PASS',
    'scope': 'minimal/universal beta=0 matter-frame identification with production 8piG interpreted as the carrier Friedmann coupling G_cosm',
    'source_relations': {
        'M_N_squared': 'M_bare^2 (1-alpha/2)',
        'M_cosm_squared': 'M_bare^2 (1+3 lambda_prime/2)',
        'C_acc_BPS': 'M_bare^2 alpha/2',
        'c_chi_squared_beta0': 'lambda_prime/alpha'
    },
    'production_exact_match': {
        'K_8piG': '2 M_K^2',
        'C_acc_required': 'M_cosm^2',
        'forced_relation': 'alpha = 2 + 3 lambda_prime'
    },
    'on_match': {
        'M_N_squared': '-(3/2) M_bare^2 lambda_prime',
        'G_cosm_over_G_N': '-3 lambda_prime/(2+3 lambda_prime)',
        'c_chi_squared': 'lambda_prime/(2+3 lambda_prime)'
    },
    'no_solution_partition': [
        'lambda_prime>0: scalar gradient sign is positive but alpha>2 and M_N^2<0',
        'lambda_prime=0: alpha=2, M_N^2=0, G_N singular and scalar speed vanishes',
        '-2/3<lambda_prime<0: 0<alpha<2 and M_N^2>0 but c_chi^2<0',
        'lambda_prime<=-2/3: alpha<=0, outside the healthy acceleration branch'
    ],
    'theorem': 'No healthy positive-finite-Newton exact RTK realization exists in this beta=0 direct acceleration-only universal matter branch after distinguishing bare, Newton and cosmological gravitational normalizations.',
    'non_claims': [
        'not a no-go for beta!=0 or xi!=1',
        'not a no-go for nonminimal/disformal matter coupling',
        'not a no-go for companion operators that change static/Newton normalization while preserving the FLRW kinetic kernel',
        'not a no-go for auxiliary-field or broader spatially-covariant/covariant completions',
        'does not invalidate the exact quadratic scalar FLRW match as an EFT benchmark'
    ],
    'next_step': 'Test the smallest beta!=0/companion-operator or nonminimal matter-frame deformation against the exact FLRW kernel, GW speed, PPN, G_cosm/G_N and compact-object constraints with one fixed coefficient tuple.'
}

print('RTK_ROUTE_B_SPATIAL_COVARIANT_COSMOLOGICAL_NEWTON_GATE_PASS', json.dumps(out, sort_keys=True))
