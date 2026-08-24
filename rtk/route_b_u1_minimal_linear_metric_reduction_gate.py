#!/usr/bin/env python3
"""C10 exact minimal reduction of nonprojectable U1 scalar metric equations.

Scope: flat FLRW, quasilongitudinal gauge, k>0, lambda_HL>1 algebraic branch.
Primary equations: Zhu-Shu-Wu-Wang arXiv:1110.5106 Eqs.(7.11)-(7.16).
Stress sources are intentionally arbitrary total sources; completed-action source
mapping is a later gate.
"""
import json
from pathlib import Path
import sympy as sp

lam,H,Hp,a,G=sp.symbols('lambda H Hprime a G', positive=True, finite=True, real=True)
ell=sp.symbols('L', nonzero=True, finite=True, real=True)  # Fourier partial^2 eigenvalue; ell=-k^2 for k>0
Eth,Pcal,alpha1,Ahat=sp.symbols('Eth Pcal alpha1 Ahat', finite=True, real=True)
psi,psip,psipp,phi,phip,B,Bp,dA=sp.symbols('psi psip psipp phi phip B Bp deltaA', finite=True, real=True)
dmu,dp,Pi=sp.symbols('delta_mu_total delta_p_total Pi_total', finite=True, real=True)
Mq,Mqp=sp.symbols('Mq Mqprime', finite=True, real=True)  # Mq=8*pi*G*a*q_total
D=3*lam-1
r=lam-1
X=psip+H*phi

# 1. Momentum constraint and algebraic shift solve.
B_expr=sp.factor((Mq-D*X)/(r*ell))
momentum_res=sp.simplify(D*X+r*ell*B_expr-Mq)
assert momentum_res==0

# 2. Hamiltonian constraint and lapse solve.
ham_lhs=D*H*sp.Rational(1,2)*(3*psip+3*H*phi+ell*B)-Pcal*ell*psi+sp.Rational(1,2)*Eth*ell*phi
ham_eq_after_B=sp.expand((ham_lhs+4*sp.pi*G*a**2*dmu).subs(B,B_expr))
# Multiply by 2r and isolate the phi coefficient.
scaled_ham=sp.factor(2*r*ham_eq_after_B)
phi_den=r*Eth*ell-2*D*H**2
phi_rhs=-8*sp.pi*G*a**2*r*dmu-D*H*Mq+2*D*H*psip+2*r*Pcal*ell*psi
assert sp.simplify(scaled_ham-(phi_den*phi-phi_rhs))==0
phi_expr=sp.factor(phi_rhs/phi_den)
assert sp.simplify((phi_den*phi_expr-phi_rhs))==0

# For ell=-k^2, lambda>1 and complete effective Eth>0, denominator is
# -(r Eth k^2+2D H^2), hence cannot vanish for k>0.
k=sp.symbols('k', positive=True, finite=True, real=True)
phi_den_fourier=sp.expand(phi_den.subs(ell,-k**2))
expected_den=-(r*Eth*k**2+2*D*H**2)
assert sp.simplify(phi_den_fourier-expected_den)==0

# 3. Traceless equation algebraically solves delta A.
traceless_lhs=Bp+2*H*B-psi+Pcal*phi-alpha1*ell*psi+(Ahat*psi-dA)/a+8*sp.pi*G*a**2*Pi
dA_expr=sp.factor(Ahat*psi+a*(8*sp.pi*G*a**2*Pi+Bp+2*H*B-psi+Pcal*phi-alpha1*ell*psi))
assert sp.simplify(traceless_lhs.subs(dA,dA_expr))==0

# 4. Insert traceless solve into trace equation; explicit deltaA, alpha1,
# Pcal and Ahat must cancel from the special bracket.
special=psi+alpha1*ell*psi-Pcal*phi-(Ahat*psi-dA)/a
special_reduced=sp.simplify(special.subs(dA,dA_expr))
special_expected=Bp+2*H*B+8*sp.pi*G*a**2*Pi
assert sp.simplify(special_reduced-special_expected)==0
assert not special_reduced.has(dA)
assert not special_reduced.has(alpha1)
assert not special_reduced.has(Pcal)
assert not special_reduced.has(Ahat)

trace_lhs=psipp+2*H*psip+H*phip+(2*Hp+H**2)*phi+(r/D)*ell*special_reduced
trace_rhs=8*sp.pi*G*a**2/D*(dp+D*sp.Rational(1,3)*ell*Pi)
trace_res=sp.expand(trace_lhs-trace_rhs)

# 5. Differentiate momentum constraint (lambda and comoving ell fixed):
# D(psipp+Hp phi+H phip)+r ell Bp=Mqprime.
Bp_expr=(Mqp-D*(psipp+Hp*phi+H*phip))/(r*ell)
# Use original momentum to eliminate B as well.
trace_after=sp.factor(trace_res.subs({Bp:Bp_expr,B:B_expr})*D)
compat=D*(Hp-H**2)*phi+Mqp+2*H*Mq-8*sp.pi*G*a**2*dp-sp.Rational(16,3)*sp.pi*G*a**2*ell*Pi
assert sp.simplify(trace_after-compat)==0
# Guard that the reduced relation has no metric second derivative or shift derivative.
assert not compat.has(psipp)
assert not compat.has(phip)
assert not compat.has(Bp)
assert not compat.has(psip)

out={
  'classification':'C10_U1_MINIMAL_LINEAR_METRIC_REDUCTION_PASS_K_GT_0_SCOPED',
  'status_scope':'GREEN_EXACT_ALGEBRAIC_METRIC_REDUCTION_COMPLETED_ACTION_STRESS_MAPPING_OPEN',
  'definitions':'D=3 lambda-1; r=lambda-1; L=partial^2 Fourier eigenvalue; Mq=8 pi G a q_total',
  'momentum_shift_solve':'L B=[Mq-D(psi_prime+H phi)]/r',
  'hamiltonian_lapse_equation':'[r Eth L-2D H^2] phi=-8 pi G a^2 r delta_mu_total-D H Mq+2D H psi_prime+2r Pcal L psi',
  'lapse_denominator_fourier':'for L=-k^2: -(r Eth k^2+2D H^2); if the complete effective Eth>0, lambda>1, k>0 then no lapse-solve pole exists',
  'traceless_deltaA_solve':'deltaA=Ahat psi+a[8 pi G a^2 Pi_total+B_prime+2H B-psi+Pcal phi-alpha1 L psi]',
  'trace_after_traceless_special_bracket':'B_prime+2H B+8 pi G a^2 Pi_total; explicit deltaA, alpha1, Pcal and Ahat cancel exactly',
  'final_compatibility':'D(Hprime-H^2) phi+Mqprime+2H Mq=8 pi G a^2 delta_p_total+(16 pi G a^2/3)L Pi_total',
  'propagation_statement':'After the independent A constraint fixes psi, momentum fixes B, Hamiltonian fixes phi and traceless fixes deltaA. The remaining trace relation contains no psi_double_prime, phi_prime or B_prime after momentum differentiation. This is consistent with absence of an extra propagating gravitational scalar in this scoped linear system.',
  'critical_boundary':'The final compatibility relation is not yet declared redundant: it must be compared with the completed-action matter/Khronon conservation equations. Likewise Eth and total stress sources must be derived with explicit S_mix retained before CLASS implementation.',
  'non_claims':[
    'not a completed-action stress-source theorem',
    'not a proof that pure-gravity Eth equals the complete effective lapse kernel',
    'not a proof that the final compatibility equation follows from completed matter conservation',
    'not an exact k=0 or lambda=1 theorem',
    'not a CLASS or likelihood result'
  ],
  'target':'research/theory_targets/RTK_C10_U1_MINIMAL_LINEAR_METRIC_REDUCTION_TARGET_v1.json'
}
Path('u1_minimal_linear_metric_reduction_result.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
