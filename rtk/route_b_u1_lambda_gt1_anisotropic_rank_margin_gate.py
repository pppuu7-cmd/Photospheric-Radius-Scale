#!/usr/bin/env python3
"""Open-neighborhood rank margins around the exact lambda>1 FLRW U(1) block.

Scope: d=3, cosmologically relevant nonprojectable lambda>1 branch, with the
barotropic FLRW response X0=A n n + B g satisfying the previously certified
|T0|<=2A sufficient domain.  This gate does NOT claim a full anisotropic
background solution.  It quantifies how much generic metric-response and full
2x2 reduced-block perturbation can be tolerated without losing positivity/rank.
"""
import json
import sympy as sp

lam,A,r=sp.symbols('lambda A r', positive=True, finite=True)
# DeWitt quadratic form in d=3 after trace/traceless decomposition:
# Q=||S||^2-T^2/[3(3lambda-1)].
S0norm=sp.sqrt(sp.Rational(2,3))*A
T0bound=2*A
crit=sp.factor(S0norm-T0bound/sp.sqrt(3*(3*lam-1)))
# Equivalent compact form.
crit_expected=A/sp.sqrt(3)*(sp.sqrt(2)-2/sp.sqrt(3*lam-1))
assert sp.simplify(crit-crit_expected)==0
# Strict positivity threshold is lambda>1.
assert sp.simplify(crit_expected.subs(lam,1))==0

# For pure traceless fractional anisotropy ||Delta X_TF|| <= r A,
# solve the sufficient inequality r < crit/A for lambda.
lam_min=sp.factor((1+4/(sp.sqrt(2)-sp.sqrt(3)*r)**2)/3)
# Check algebraic saturation without sqrt(square) branch ambiguity.  On the
# stated domain 0<=r<sqrt(2/3), sqrt(2)-sqrt(3)r is strictly positive.
saturation=sp.expand((3*lam_min-1)*(sp.sqrt(2)-sp.sqrt(3)*r)**2-4)
assert sp.simplify(saturation)==0

# Small-r slope of lambda_min-1.
slope=sp.simplify(sp.diff(lam_min,r).subs(r,0))
assert slope==2*sp.sqrt(6)/3

# Full reduced 2x2 block perturbation margin.
a,d,F=sp.symbols('a d F', positive=True, finite=True)
D=sp.factor(F**2+a*d)
frob=sp.sqrt(a**2+d**2+2*F**2)
# Since sigma_max <= ||B||_F and sigma_min=|det B|/sigma_max,
# sigma_min >= D/||B||_F for D>0.
rank_lower=sp.factor(D/frob)
assert rank_lower>0

out={
  'classification':'RTK_ROUTE_B_U1_LAMBDA_GT1_ANISOTROPIC_RANK_MARGIN_PASS',
  'status_scope':'GREEN_EXPLICIT_OPEN_NEIGHBORHOOD_MARGIN_FULL_ANISOTROPIC_SOLUTION_PENDING',
  'domain':'d=3 nonprojectable lambda>1 branch around the certified barotropic FLRW response with |T0|<=2A and exact base block B0=[[a,-F],[F,d]], a>0,d>0',
  'deWitt_decomposition':'XGX=||X_TF||^2-(tr X)^2/[3(3 lambda-1)]',
  'base_traceless_norm':'||X0_TF||=sqrt(2/3) A',
  'response_perturbation_sufficient_condition':'||Delta X_TF|| + |tr Delta X|/sqrt[3(3lambda-1)] < A/sqrt(3) [sqrt(2)-2/sqrt(3lambda-1)]',
  'margin_positive_iff_in_scope':'the displayed conservative margin is zero at lambda=1 and strictly positive for lambda>1',
  'pure_traceless_fractional_bound':{
    'definition':'||Delta X_TF|| <= r A, tr Delta X=0',
    'allowed_r':'0<=r<sqrt(2/3)',
    'lambda_sufficient':'lambda > [1+4/(sqrt(2)-sqrt(3) r)^2]/3',
    'small_r_expansion':'lambda_min-1=(2 sqrt(6)/3) r + O(r^2)'
  },
  'full_block_pointwise_margin':{
    'base_det':'D=F^2+a d>0',
    'frobenius':'||B0||_F=sqrt(a^2+d^2+2F^2)',
    'singular_value_lower_bound':'sigma_min(B0) >= D/||B0||_F',
    'sufficient_condition':'||Delta B||_2 < (F^2+a d)/sqrt(a^2+d^2+2F^2) preserves rank at that q'
  },
  'compact_q_interval_extension':'On any closed q interval [q_min,q_max] with 0<q_min<q_max<infinity and continuous base coefficients, the positive pointwise margin has a positive minimum; a uniform perturbation smaller than that minimum preserves rank on the interval.',
  'interpretation':'The exact FLRW all-q rank theorem has a finite perturbative neighborhood for every lambda>1. However the conservative anisotropy margin collapses linearly as lambda approaches 1 from above, exposing a quantitative near-GR-background versus anisotropic-robustness trade-off.',
  'non_claims':[
    'does not derive Delta X or Delta B from a specific Bianchi, anisotropic-stress, or inhomogeneous solution',
    'does not prove a uniform margin on the noncompact q domain (0,infinity)',
    'does not replace the exact full constraint algebra away from the homogeneous regular slice',
    'does not choose lambda or an anisotropy tolerance'
  ],
  'next_gate':'derive Delta X and the off-diagonal Delta b,Delta c from a weakly anisotropic Bianchi-I/perfect-fluid background; then compare their norm to this certified margin and optimize the allowed lambda interval jointly with the near-GR background bound.'
}
open('u1_lambda_gt1_anisotropic_rank_margin_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
