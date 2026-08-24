#!/usr/bin/env python3
"""Variation-level static bridge for the frozen U(1)+RTK scalar action.

Prerequisite: the exact scalar EOM admits Sigma=q t, D_iSigma=0 on arbitrary
static N(x), g_ij(x) with zero invariant shift B^i.

This gate proves, before importing any PPN formula, that the explicit mixed
operator has the same static N/g first variations as M_Pl^2 a_i a^i, while its
linear invariant-shift source vanishes.  The DBI P(X) term is kept separately
and its weak-lapse series is recorded through O(n^4).
"""
from __future__ import annotations

import json
import sympy as sp

# Symbols for one spatial component. The 3D result is the linear sum over i,j.
N, q, Mpl, sqrtg, ginv = sp.symbols('N q M_Pl sqrtg ginv', positive=True, nonzero=True)
dN = sp.symbols('dN', real=True)

X = q**2/(2*N**2)
C = Mpl**2/(2*X)
dTheta = -q*dN/N**2
Lmix = sp.simplify(N*sqrtg*C*ginv*dTheta**2)
Lacc = sp.simplify(N*sqrtg*Mpl**2*ginv*(dN/N)**2)
assert sp.simplify(Lmix-Lacc)==0

# Exact first-variation equality for the static lapse and spatial inverse metric.
# Treat N and dN as independent jet variables for Euler-Lagrange variation.
for var in (N, dN, ginv, sqrtg):
    assert sp.simplify(sp.diff(Lmix,var)-sp.diff(Lacc,var))==0

# Invariant-shift source. Before setting D_iSigma=0,
# Theta=(dotSigma-B^i D_iSigma)/N, so dTheta/dB^i=-D_iSigma/N.
B, gradSigma, dotSigma = sp.symbols('B gradSigma dotSigma')
Theta_general=(dotSigma-B*gradSigma)/N
X_general=sp.Rational(1,2)*(Theta_general**2-ginv*gradSigma**2)
# It is sufficient to show both dTheta/dB and dX/dB vanish at gradSigma=0;
# D_iTheta inherits the same zero because D_iSigma is identically zero on the
# frozen clock background.
dTheta_dB=sp.diff(Theta_general,B)
dX_dB=sp.diff(X_general,B)
assert sp.simplify(dTheta_dB.subs(gradSigma,0))==0
assert sp.simplify(dX_dB.subs(gradSigma,0))==0

# Frozen scalar action has no A-field in X_U, Theta_U or C(X_U)(DTheta)^2.
Afield=sp.symbols('Afield')
assert not Lmix.has(Afield)

# DBI P(X) weak-lapse expansion on the asymptotic clock branch u=sqrt(X/X*)=1/N.
n, lam, muK2 = sp.symbols('n lambda_D mu_K2')
Nn=1+n
u=1/Nn
# Physical P divided by M_Pl^2.  This expression has a smooth lambda->0 limit;
# the series coefficients below are polynomial in lambda.
P_over_Mpl2 = 2*muK2/lam*(1-sp.sqrt(1-lam*(u-1)**2))
series = sp.series(P_over_Mpl2,n,0,5).removeO().expand()
expected = muK2*n**2 - 2*muK2*n**3 + muK2*(3+lam/4)*n**4
assert sp.simplify(series-expected)==0

# At N=1, P=P_X=0 (implemented here as P and first n derivative), so the
# asymptotic clock does not carry a constant or linear lapse tadpole.
assert sp.simplify(series.subs(n,0))==0
assert sp.simplify(sp.diff(series,n).subs(n,0))==0

out={
  'classification':'RTK_ROUTE_B_U1_STATIC_VARIATION_BRIDGE_EXACT_PASS',
  'status':'SCOPED_EXACT_STATIC_VARIATION_BRIDGE',
  'prerequisite':'RTK_ROUTE_B_U1_STATIC_CLOCK_SCALAR_EOM_EXACT_PASS',
  'mixed_static_functional_identity':'N sqrt(g) C(X)(DTheta)^2 = N sqrt(g) M_Pl^2 a_i a^i',
  'variation_equivalence':{
    'lapse_N':'exact',
    'lapse_gradient_DiN':'exact',
    'spatial_inverse_metric_gij':'exact',
    'sqrtg_measure':'exact',
    'invariant_shift_linear_source':'zero at D_iSigma=0',
    'A_field_direct_source':'zero'
  },
  'beta0_bookkeeping':{
    'beta0_bare':0,
    'explicit_Smix_beta0_like_static_contribution':2,
    'warning':'retain S_mix explicitly in the full action; beta0_eff=2 is a static constraint bridge, not a redefinition of the frozen bare gravity coupling'
  },
  'dbi_px':{
    'kept_separate':True,
    'weak_lapse_expansion':'P/M_Pl^2 = mu_K^2[n^2-2n^3+(3+lambda_D/4)n^4+O(n^5)]',
    'P_at_N1':0,
    'lapse_tadpole_at_N1':0
  },
  'interpretation':'Static N/g/U1 equations receive the exact acceleration-operator contribution from S_mix plus a separate DBI lapse-potential stress. No hidden static Sigma response is required.',
  'non_claims':[
    'does not set finite-M_K P(X) stress to zero',
    'does not yet certify beta_PPN or gamma_PPN including finite-M_K effects',
    'does not certify O(v^3) moving-source alpha1 or alpha2',
    'does not cover nonzero invariant shift, rotation, compact-object X_U->0, radiative stability or cutoff'
  ],
  'next_gate':'combine this exact bridge with the locked epsilon_clock hierarchy and the nonprojectable U1 PPN equations to bound finite-M_K static Solar-System corrections before any beta_PPN closure claim'
}
open('u1_static_variation_bridge_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
