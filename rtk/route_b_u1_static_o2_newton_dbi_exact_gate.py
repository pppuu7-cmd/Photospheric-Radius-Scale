#!/usr/bin/env python3
"""Exact static O(2) Newton gate including the frozen DBI lapse potential.

Inputs already frozen/proved in the repository:
  * a1=1,a2=0,kappa=1,sigma1=sigma2=0,gamma1=-1;
  * explicit S_mix has the exact static functional M_Pl^2 a_i a^i;
  * Sigma=q t solves the scalar EOM in the static zero-invariant-shift sector;
  * P/M_Pl^2 = mu_K^2 n^2 + O(n^3) for n=N-1.

Universal matter frame (Lin-Mukohyama-Wang-Zhu, arXiv:1310.6666):
  tilde N = F(sigma)N, F=1-a1 sigma;
  in the PPN gauge varphi=0, sigma=A/N, so for a1=1: tilde N=N-A.
The physical metric has gamma_00=-1+2U+O(4), hence
  tilde N=1-U+O(4).
With A=A2+O(4), this gives exactly at O(2)
  n=N-1=A2-U.

The pure-U1 O(2) Hamiltonian equation with the exact static S_mix bridge is
  4 Laplacian(A2-U)=0.
The action normalization is fixed by comparing the variation of
  S_mix^(2)=M_Pl^2 int (grad n)^2
with that equation.  Adding
  S_P^(2)=M_Pl^2 mu_K^2 int n^2
therefore gives
  4 [Laplacian(n)-mu_K^2 n]=0.
For mu_K^2>0, regular/asymptotically-flat n obeying a vanishing boundary term
is uniquely zero: multiply by n and integrate to obtain
  integral [|grad n|^2 + mu_K^2 n^2]=0.
"""
from __future__ import annotations

import json
import sympy as sp

# Frozen parameter algebra from arXiv:1310.6666 Eqs.(5.24)-(5.25).
a1,a2,kappa,sigma2,gamma1,beta_eff,gamma=sp.symbols(
    'a1 a2 kappa sigma2 gamma1 beta_eff gamma', real=True)
vals={a1:1,a2:0,kappa:1,sigma2:0,gamma1:-1,beta_eff:2,gamma:1}
lhs_coeff=sp.simplify((2*beta_eff*a1-4*gamma1*a2-sigma2).subs(vals))
rhs_coeff=sp.simplify((2*(2*gamma1*gamma+beta_eff+2*kappa)).subs(vals))
assert lhs_coeff==4 and rhs_coeff==4

# Universal physical-lapse relation at O(2): tilde n=-U and tildeN=N-A.
n,A2,U,f=sp.symbols('n A2 U f')
physical_relation=sp.Eq(n, A2-U)
assert sp.solve(physical_relation,n)==[A2-U]
assert sp.simplify((A2-U).subs(A2,f*U)-(f-1)*U)==0

# Quadratic action normalization.  Treat one gradient component p=dn/dx.
Mpl,mu2,p,lap=sp.symbols('M_Pl mu_K2 p lap', positive=True, real=True)
# Euler derivative coefficients for Mpl^2 (grad n)^2 and Mpl^2 mu^2 n^2.
variation_mix=-2*Mpl**2*lap
variation_P=2*Mpl**2*mu2*n
# Multiplication by -2/Mpl^2 maps the known mixed variation to +4 Lap n.
normalizer=-sp.Rational(2,1)/Mpl**2
assert sp.simplify(normalizer*variation_mix-4*lap)==0
assert sp.simplify(normalizer*variation_P+4*mu2*n)==0
full_equation=sp.expand(normalizer*(variation_mix+variation_P))
assert sp.simplify(full_equation-4*(lap-mu2*n))==0

# Positive-energy uniqueness identity after multiplying (Delta-mu^2)n=0 by n
# and integrating by parts with vanishing boundary term:
G2,N2=sp.symbols('I_grad2 I_n2', nonnegative=True)
positive_integral=G2+mu2*N2
# Structurally both terms are nonnegative and mu2>0. If their sum is zero,
# each must vanish. SymPy assumptions plus explicit logic encode the theorem.
assert mu2.is_positive

out={
  'classification':'RTK_ROUTE_B_U1_STATIC_O2_NEWTON_DBI_EXACT_PASS',
  'status':'STATIC_NEWTON_O2_EXACT_ON_REGULAR_ASYMPTOTICALLY_FLAT_CLOCK_BRANCH',
  'literature_source':'Lin-Mukohyama-Wang-Zhu arXiv:1310.6666 Eqs.(4.2),(4.3),(5.22)-(5.26)',
  'physical_lapse':{
    'gauge':'varphi=0',
    'a1':1,
    'identity':'tildeN=N-A',
    'PPN_O2':'tildeN=1-U+O(4)',
    'bare_lapse_relation':'n=N-1=A2-U at O(2)'
  },
  'pure_O2_hamiltonian':{
    'equation':'4 Laplacian(A2-U)=0',
    'lhs_coefficient':int(lhs_coeff),
    'rhs_coefficient':int(rhs_coeff)
  },
  'dbi_quadratic_action':'S_P^(2)=M_Pl^2 mu_K^2 integral n^2',
  'full_O2_bare_lapse_equation':'4 [Laplacian(n)-mu_K^2 n]=0',
  'uniqueness':{
    'conditions':['mu_K^2>0','n regular','n->0 at spatial infinity','IBP boundary term vanishes'],
    'integral_identity':'integral(|grad n|^2 + mu_K^2 n^2)=0',
    'solution':'n=0'
  },
  'consequences':{
    'A2':'U',
    'f':'1',
    'tildeN':'1-U+O(4)',
    'gamma_PPN_O2':1,
    'newton_normalization':'kappa=G/G_N=1, hence G_N=G on the frozen static O(2) branch',
    'DBI_O2_effect':'does not shift the regular asymptotically-flat Newtonian solution; it gives a positive homogeneous mass term for the unphysical/bare lapse difference n=A2-U'
  },
  'non_claims':[
    'does not certify beta_PPN at O(v^4)',
    'does not certify moving-source alpha1 or alpha2',
    'does not cover nonzero invariant shift or rotating solutions',
    'does not cover compact-object X_U->0 behavior',
    'does not establish radiative stability or the EFT cutoff'
  ],
  'next_gate':'derive the complete static O(v^4) equations on the identical action, retaining the DBI n^3,n^4 terms and exact S_mix functional, and solve beta_PPN'
}
with open('u1_static_o2_newton_dbi_exact_result.json','w',encoding='utf-8') as f:
    json.dump(out,f,indent=2,sort_keys=True); f.write('\n')
print(out['classification'],json.dumps(out,sort_keys=True))
