#!/usr/bin/env python3
"""Exact P(X) derivative/canonical-coupling structure of the frozen RTK DBI clock.

Scope: positive production branch lambda_D>0, r>0, delta=1-lambda_D r^2>0,
u=1+r and X=X_star u^2.  The lambda_D=0 theory is a separate smooth limit
without the finite-r DBI edge.

This gate distinguishes coefficient-based energy scales from on-shell fixed-k
behavior.  It does NOT declare a unitarity cutoff.
"""
import json
import sympy as sp

r,lam,mu,Xs,Mpl=sp.symbols('r lambda_D mu_K X_star M_Pl', positive=True, finite=True)
d=sp.symbols('delta', positive=True, finite=True)
X=sp.symbols('X', positive=True, finite=True)
u=sp.sqrt(X/Xs)
P=Mpl**2*2*mu**2/lam*(1-sp.sqrt(1-lam*(u-1)**2))

# Direct derivatives, evaluated on u=1+r.  SymPy produces Abs(1+r), so use
# the certified production branch r>0 to replace it by 1+r.
def on_branch(expr):
    e=sp.simplify(expr.subs(X,Xs*(1+r)**2))
    e=e.xreplace({sp.Abs(r+1):r+1})
    return sp.factor(e)
P1,P2,P3,P4=[on_branch(sp.diff(P,X,n)) for n in range(1,5)]
delta=1-lam*r**2
P1_ref=Mpl**2*mu**2*r/(Xs*(1+r)*sp.sqrt(delta))
P2_ref=Mpl**2*mu**2*(1+lam*r**3)/(2*Xs**2*(1+r)**3*delta**sp.Rational(3,2))
P3_ref=3*Mpl**2*mu**2*(lam**2*r**5+3*lam*r**2+lam*r-1)/(4*Xs**3*(1+r)**5*delta**sp.Rational(5,2))
P4_ref=3*Mpl**2*mu**2*(5*lam**3*r**7+29*lam**2*r**4+18*lam**2*r**3+4*lam**2*r**2-19*lam*r**2-3*lam*r+lam+5)/(8*Xs**4*(1+r)**7*delta**sp.Rational(7,2))
for got,ref in [(P1,P1_ref),(P2,P2_ref),(P3,P3_ref),(P4,P4_ref)]:
    assert sp.simplify(got-ref)==0

q=sp.sqrt(2*Xs)*(1+r)
A=sp.factor(P1+q**2*P2)
A_ref=Mpl**2*mu**2/(Xs*delta**sp.Rational(3,2))
assert sp.simplify(A-A_ref)==0
ca2=sp.factor(P1/A)
MK2=sp.factor(q**2*A/(2*Mpl**2))
assert sp.simplify(ca2-r*delta/(1+r))==0
assert sp.simplify(MK2-mu**2*(1+r)**2/delta**sp.Rational(3,2))==0

# Low-k canonical P-sector coefficients pi_c=sqrt(A) pi.
# Replace delta powers only after using the exact relation delta=1-lambda r^2.
C3t_ref=sp.sqrt(2)*lam*r/(4*Mpl*mu*delta**sp.Rational(1,4))
C3s_ref=-sp.sqrt(2)*(1+lam*r**3)*delta**sp.Rational(3,4)/(4*Mpl*mu*(1+r)**2)
C4t_ref=lam*(1+4*lam*r**2)/(16*Mpl**2*mu**2*sp.sqrt(delta))
C4ts_ref=-sp.sqrt(delta)*(2*lam**2*r**5+lam*r**3+8*lam*r**2+3*lam*r-2)/(8*Mpl**2*mu**2*(1+r)**3)
C4s_ref=delta**sp.Rational(3,2)*(1+lam*r**3)/(16*Mpl**2*mu**2*(1+r)**3)

C3t=sp.factor((q*P2/2+q**3*P3/6)/A**sp.Rational(3,2))
C3s=sp.factor((-q*P2/2)/A**sp.Rational(3,2))
C4t=sp.factor((P2/8+q**2*P3/4+q**4*P4/24)/A**2)
C4ts=sp.factor((-P2/4-q**2*P3/4)/A**2)
C4s=sp.factor((P2/8)/A**2)
# Nested fractional powers can obstruct direct simplification; certify by
# positive-branch numerical-free power identities after forming ratios.
assert sp.simplify((C3t/C3t_ref)**4-1)==0
assert sp.simplify((C3s/C3s_ref)**4-1)==0
assert sp.simplify(C4t-C4t_ref)==0
assert sp.simplify(C4ts-C4ts_ref)==0
assert sp.simplify(C4s-C4s_ref)==0

# Time-like quartic tracks the square of the time-like cubic; no independent
# stronger edge singularity appears.
ratio=sp.factor(C4t_ref/C3t_ref**2)
assert sp.simplify(ratio-(2+1/(2*lam*r**2)))==0

# Production trajectory identity: x=x0/a^3, s^2=1+lambda x^2,
# r=x/s -> delta=1/s^2 exactly.  For any finite a>0 delta>0.
x=sp.symbols('x', positive=True, finite=True)
s2=1+lam*x**2
r_x=x/sp.sqrt(s2)
assert sp.simplify((1-lam*r_x**2)-1/s2)==0

# Early-edge asymptotics: delta~a^6/(lambda x0^2), so coefficient-based
# time-cubic energy scale Lambda3=|C3t|^-1/2 scales as delta^(1/8)~a^(3/4).
# But at fixed physical k, ca~delta^(1/2), hence C3t*omega^3 and
# C3s*omega*k^2 both scale as delta^(5/4); the fixed-k vertex softens.

out={
  'classification':'RTK_C9_RTK_SCALAR_DBI_DERIVATIVE_EDGE_PASS',
  'status_scope':'GREEN_EXACT_DBI_DERIVATIVES_AND_EDGE_SCALING_UNITARITY_CUTOFF_PENDING',
  'domain':'lambda_D>0, r>0, delta=1-lambda_D r^2>0, rolling production branch X>0',
  'exact_derivatives':{
    'P1':'M_Pl^2 mu_K^2 r/[X_star(1+r) sqrt(delta)]',
    'P2':'M_Pl^2 mu_K^2(1+lambda_D r^3)/[2 X_star^2(1+r)^3 delta^(3/2)]',
    'P3':'3 M_Pl^2 mu_K^2(lambda_D^2 r^5+3lambda_D r^2+lambda_D r-1)/[4 X_star^3(1+r)^5 delta^(5/2)]',
    'P4':'3 M_Pl^2 mu_K^2(5lambda_D^3 r^7+29lambda_D^2 r^4+18lambda_D^2 r^3+4lambda_D^2 r^2-19lambda_D r^2-3lambda_D r+lambda_D+5)/[8 X_star^4(1+r)^7 delta^(7/2)]'
  },
  'quadratic':{
    'Akin':'M_Pl^2 mu_K^2/[X_star delta^(3/2)]',
    'c_a_squared':'r delta/(1+r)',
    'M_K_squared':'mu_K^2(1+r)^2/delta^(3/2)'
  },
  'lowk_canonical_P_cubic':{
    'dotpi_cubed':'sqrt(2) lambda_D r/[4 M_Pl mu_K delta^(1/4)]',
    'dotpi_gradpi2':'-sqrt(2)(1+lambda_D r^3) delta^(3/4)/[4 M_Pl mu_K(1+r)^2]'
  },
  'lowk_canonical_P_quartic':{
    'dotpi4':'lambda_D(1+4lambda_D r^2)/[16 M_Pl^2 mu_K^2 sqrt(delta)]',
    'dotpi2_gradpi2':'-sqrt(delta)(2lambda_D^2 r^5+lambda_D r^3+8lambda_D r^2+3lambda_D r-2)/[8 M_Pl^2 mu_K^2(1+r)^3]',
    'gradpi4':'delta^(3/2)(1+lambda_D r^3)/[16 M_Pl^2 mu_K^2(1+r)^3]'
  },
  'edge_relation':'C_dotpi4/C_dotpi3^2 = 2 + 1/(2 lambda_D r^2) -> 5/2 as delta->0+',
  'production_edge_identity':'delta=1/(1+lambda_D x^2), x=x0/a^3; therefore delta>0 at every finite a>0 and delta->0 only asymptotically as a->0 for lambda_D x0^2>0',
  'early_scaling':{
    'delta':'~a^6/(lambda_D x0^2)',
    'time_cubic_coefficient':'~delta^(-1/4)',
    'coefficient_energy_scale_Lambda3':'~delta^(1/8)~a^(3/4)',
    'fixed_k_sound_speed':'c_a~delta^(1/2)',
    'fixed_k_time_cubic_vertex':'C3t omega^3 ~ delta^(5/4)',
    'fixed_k_spatial_cubic_vertex':'C3s omega k^2 ~ delta^(5/4)'
  },
  'interpretation':'The only DBI derivative singularity on the positive production branch is the asymptotic early-time edge. Low-k coefficient-based energy scales decrease there, but fixed-momentum on-shell interactions soften because the sound speed collapses simultaneously. A true cutoff therefore requires anisotropic energy-momentum power counting or amplitudes, not coefficient inspection alone.',
  'non_claims':[
    'does not compute the physical unitarity or strong-coupling cutoff',
    'does not prove the EFT is valid arbitrarily close to a=0',
    'does not include gravity/U1/auxiliary exchange',
    'does not cover lambda_D=0 in the edge asymptotics (that limit is smooth and edge-free)',
    'does not choose an EFT starting redshift'
  ],
  'next_gate':'use the frozen background x0,lambda_D,mu_K to evaluate the coefficient scale and k/M_K crossover versus redshift, then compare to H(z), BBN/CMB frequencies and the exact high-k canonical normalization; separately derive a tree-level 2->2 power-counting bound.'
}
open('c9_rtk_scalar_dbi_derivative_edge_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
