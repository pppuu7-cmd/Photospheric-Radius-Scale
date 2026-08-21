#!/usr/bin/env python3
"""Exact observational incompatibility gate for the direct C8 carrier in the
standard universal low-energy Horava matter frame.

Primary phenomenology source:
A. Emir Gumrukcuoglu, M. Saravani, T. P. Sotiriou,
"Horava gravity after GW170817", Phys. Rev. D 97, 024032 (2018),
arXiv:1711.08845, Eqs. (7)-(12).

In their low-energy parameterization (alpha,beta,gamma):

  G_cosm = 1/[4 pi M_*^2 (2+3 gamma+beta)]
         = 1/[8 pi M_*^2 (1+(3 gamma+beta)/2)],

  G_N    = 1/[8 pi M_*^2 (1-alpha/2)],

and the first translated preferred-frame ppN bound is

  |4(alpha-2 beta)/(1-beta)| <=~ 1e-4.

Their post-GW170817 discussion gives |beta| of order <= 1e-15.  Their BBN
constraint (Eq. 10) is

  |(alpha+3 gamma+beta)/(2+3 gamma+beta)| < 1/8.

The direct RTK FLRW exact-match theorem fixes the coefficient of a_i a^i to
C_required=M_cosm^2 when the production 8piG normalization is identified with
the carrier Friedmann coupling.  Since the standard action coefficient is
M_*^2 alpha/2, exact matching implies

  alpha = 2 + 3 gamma + beta.                         (MATCH)

This immediately gives

  G_cosm/G_N = (2-alpha)/alpha.

Under MATCH, the BBN expression becomes 2(alpha-1)/alpha.  For alpha>0,

  |2(alpha-1)/alpha| < 1/8

is exactly equivalent to

  16/17 < alpha < 16/15.

But with |beta|<=10^-15 the ppN expression has a rigorous lower bound

  |4(alpha-2 beta)/(1-beta)|
   >= 4(alpha_min-2 b)/(1+b),

where alpha_min=16/17 and b=10^-15.  This is >3.76, versus the ppN benchmark
1e-4.  Therefore there is no overlap by more than four orders of magnitude.

The theorem deliberately does NOT claim to exclude nonminimal/disformal matter
frames, companion operators that change Newton/PPN response while preserving
the cosmological scalar kernel, auxiliary-field completions, or theories in
which the production gravitational normalization is not identified with the
standard universal-matter Friedmann coupling used in the cited equations.
"""

from fractions import Fraction
import json

# Exact rational bounds.
BBN = Fraction(1, 8)
PPN = Fraction(1, 10_000)  # 1e-4 first ppN benchmark
BETA_GW = Fraction(1, 10**15)

# From |2(a-1)/a| < 1/8, a>0.
ALPHA_MIN = Fraction(16, 17)
ALPHA_MAX = Fraction(16, 15)

# Verify endpoint algebra exactly.
def bbn_expr_abs(a):
    return abs(Fraction(2) * (a - 1) / a)
assert bbn_expr_abs(ALPHA_MIN) == BBN
assert bbn_expr_abs(ALPHA_MAX) == BBN
assert bbn_expr_abs(Fraction(1)) == 0

# Rigorous triangle-inequality lower bound on the first ppN expression for the
# full BBN-allowed alpha interval and |beta|<=BETA_GW:
# numerator |alpha-2 beta| >= alpha_min-2b;
# denominator |1-beta| <= 1+b.
PPN_LOWER = Fraction(4) * (ALPHA_MIN - 2*BETA_GW) / (1 + BETA_GW)
assert PPN_LOWER > Fraction(3)  # far stronger than needed
assert PPN_LOWER > PPN
EXCLUSION_FACTOR = PPN_LOWER / PPN

# The match itself also fixes the cosmological/Newton ratio independent of
# beta,gamma separately: Gc/GN=(2-alpha)/alpha.  At alpha=1 it is exactly one.
def gc_over_gn(a):
    return (2-a)/a
assert gc_over_gn(Fraction(1)) == 1

out = {
    'classification': 'RTK_ROUTE_B_SPATIAL_COVARIANT_STANDARD_MATTER_NO_GO_PASS',
    'scope': 'direct acceleration-only exact C8 carrier mapped to the standard universal low-energy Horava matter frame of arXiv:1711.08845',
    'source': 'Gumrukcuoglu-Saravani-Sotiriou, PRD97 024032 (2018), arXiv:1711.08845, Eqs. 7-12',
    'source_relations': {
        'G_cosm': '1/[4 pi M_*^2 (2+3 gamma+beta)]',
        'G_N': '1/[8 pi M_*^2 (1-alpha/2)]',
        'BBN': '|(alpha+3 gamma+beta)/(2+3 gamma+beta)| < 1/8',
        'PPN1': '|4(alpha-2 beta)/(1-beta)| <=~ 1e-4',
        'GW_beta_benchmark': '|beta| <=~ 1e-15'
    },
    'direct_match': {
        'coefficient_condition': 'M_*^2 alpha/2 = M_cosm^2',
        'forced_relation': 'alpha=2+3 gamma+beta',
        'G_cosm_over_G_N': '(2-alpha)/alpha',
        'BBN_expression_on_match': '2(alpha-1)/alpha'
    },
    'BBN_allowed_alpha_open_interval': [str(ALPHA_MIN), str(ALPHA_MAX)],
    'BBN_allowed_alpha_decimal': [float(ALPHA_MIN), float(ALPHA_MAX)],
    'PPN_lower_bound_over_BBN_GW_region': str(PPN_LOWER),
    'PPN_lower_bound_decimal': float(PPN_LOWER),
    'PPN_benchmark': float(PPN),
    'minimum_exclusion_factor_vs_PPN_benchmark': float(EXCLUSION_FACTOR),
    'theorem': 'No parameter tuple in the cited standard universal matter frame can satisfy direct exact RTK matching, the cited BBN G_cosm/G_N bound, the post-GW170817 beta bound, and the first ppN bound simultaneously.',
    'non_claims': [
        'not a no-go for nonminimal/disformal matter coupling',
        'not a no-go for fixed companion operators that alter static/Newton/PPN response while retaining the FLRW scalar kinetic factor',
        'not a no-go for auxiliary-field or broader spatially covariant completions',
        'not a statement about global cosmological fit or model evidence',
        'does not invalidate the exact quadratic FLRW scalar carrier theorem'
    ],
    'next_step': 'Construct the minimal companion/nonminimal matter deformation that preserves the exact FLRW kinetic kernel but decouples the cosmological acceleration operator from the standard low-energy preferred-frame PPN coefficient; then redo GW, PPN, Newton and compact-object gates on one fixed tuple.'
}

print('RTK_ROUTE_B_SPATIAL_COVARIANT_STANDARD_MATTER_NO_GO_PASS', json.dumps(out, sort_keys=True))
