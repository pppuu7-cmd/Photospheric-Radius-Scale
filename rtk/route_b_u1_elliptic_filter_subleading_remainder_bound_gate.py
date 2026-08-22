#!/usr/bin/env python3
"""Exact subleading remainder bounds for the elliptic filter on q>=0.

Let r=q/M_c^2>=0 and
    a_eff=r/(1+r).
Then
    a_eff-r = -r^2/(1+r),
so
    |a_eff-r| <= r^2.

For the isotropic metric-trace derivative used in the c21 theorem,
    D_g J_m = r H0/(1+r)^2 - r tau_H/(1+r).
The leading term is
    r(H0-tau_H).
The exact remainder is
    r^2[-H0(2+r)/(1+r)^2 + tau_H/(1+r)].
Since for r>=0
    (2+r)/(1+r)^2 <= 2,
    1/(1+r) <= 1,
we have
    |R_DJ| <= r^2(2|H0|+|tau_H|).

Multiplying by the isotropic gravity velocity V gives a rigorous filter-only
subleading c-bracket bound
    |R_c,filter| <= |V| q^2/M_c^4 (2|H0|+|tau_H|).

This isolates only the rational-filter remainder. Pure-gravity, neutral-RTK and
other operator subleading terms still require separate bounds before a total C
is claimed.
"""
import json
import sympy as sp

r=sp.symbols('r', nonnegative=True, finite=True)
H,tau,V=sp.symbols('H0 tau_H V', real=True, finite=True)
a=r/(1+r)
a_rem=sp.simplify(a-r)
assert sp.simplify(a_rem + r**2/(1+r))==0

DJ=sp.simplify(r*H/(1+r)**2-r*tau/(1+r))
lead=r*(H-tau)
rem=sp.factor(sp.simplify(DJ-lead))
expected=sp.factor(r**2*(-H*(2+r)/(1+r)**2+tau/(1+r)))
assert sp.simplify(rem-expected)==0

# Algebraic positivity of the coefficient inequalities for r>=0.
coefH=sp.simplify(2-(2+r)/(1+r)**2)
coefTau=sp.simplify(1-1/(1+r))
assert sp.factor(coefH)==r*(3+2*r)/(1+r)**2
assert sp.factor(coefTau)==r/(1+r)

out={
  'classification':'RTK_ROUTE_B_U1_ELLIPTIC_FILTER_SUBLEADING_REMAINDER_BOUND_PASS',
  'status_scope':'GREEN_EXACT_FILTER_REMAINDER_BOUND_NONFILTER_SUBLEADING_C_PENDING',
  'domain':'q>=0, M_c^2>0, same translational/isotropic trace patch used for the filtered-matter c21 theorem',
  'dimensionless_variable':'r=q/M_c^2',
  'source_remainder_exact':'a_eff-r=-r^2/(1+r)',
  'source_remainder_bound':'|a_eff-q/M_c^2|<=q^2/M_c^4',
  'trace_derivative_exact':'D_g J_m=r H0/(1+r)^2-r tau_H/(1+r)',
  'trace_derivative_leading':'r(H0-tau_H)',
  'trace_derivative_remainder_exact':'r^2[-H0(2+r)/(1+r)^2+tau_H/(1+r)]',
  'trace_derivative_remainder_bound':'|R_DJ|<=q^2/M_c^4 (2|H0|+|tau_H|)',
  'c_bracket_filter_remainder_bound':'|R_c,filter|<=|V| q^2/M_c^4 (2|H0|+|tau_H|)',
  'interpretation':'The rational elliptic filter contributes a rigorously bounded O(q^2/M_c^4) remainder. It cannot by itself generate an uncontrolled near-zero singularity on q>=0.',
  'non_claims':['does not bound pure-gravity O(q^2) terms','does not bound neutral-RTK O(q^2) terms','does not bound possible matter-gradient operator coefficients outside the stated trace patch','does not choose M_c or provide the total remainder constant C'],
  'next_gate':'combine this filter-only bound with published pure-gravity q^2 coefficients and a neutral-RTK subleading support bound to construct a total C for the finite-epsilon theorem.'
}
with open('u1_elliptic_filter_subleading_remainder_bound_result.json','w') as f:
    json.dump(out,f,indent=2,sort_keys=True); f.write('\n')
print(out['classification'],json.dumps(out,sort_keys=True))
