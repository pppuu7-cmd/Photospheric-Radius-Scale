#!/usr/bin/env python3
"""Exact reduced constraint-chain recovery theorem after auxiliary Dirac projection.

After eliminating the genuine second-class pair

    (p_Q, C_Lambda=L Q-H0),

the projected scalar U(1) sector contains no Q,p_Q variables.  On the regular
D_i nu=0 Fourier-symbol slice the reduced Hamiltonian is affine in A,N and the
projected source

    Jhat = J_A^(g)-a_eff H0,   a_eff=1-L^{-1}

is independent of A and N.  Thus the primary constraints p_A and pi_N generate
Jhat and Hperp_hat, while preservation of

    Ghat=p_nu+Jhat

cannot fix the p_A or pi_N multipliers because {Ghat,p_A}={Ghat,pi_N}=0.  It
therefore generates the reduced descendant phi_hat={Ghat,H_c} (modulo the
already-existing momentum constraints), restoring the structural chain that is
needed before a physical four-constraint rank calculation.

This gate proves the chain structure only.  It deliberately leaves the actual
operators in Hperp_hat and phi_hat abstract; their Poisson matrix is the next
physics gate and must retain metric dependence of L^{-1}.
"""
import json
import sympy as sp

A,pA,N,pN,nu,pnu=sp.symbols('A p_A N pi_N nu p_nu', finite=True)
# Spectator old-sector canonical pair used only to keep J/H nontrivial.
q,p=sp.symbols('q p', finite=True)
a=sp.symbols('a_eff', finite=True)
Jg,H0,Hg,R=sp.symbols('J_g H0 H_g R', finite=True)

coords=[A,N,nu,q]
moms=[pA,pN,pnu,p]
def PB(f,g):
    return sp.simplify(sum(sp.diff(f,x)*sp.diff(g,px)-sp.diff(f,px)*sp.diff(g,x)
                           for x,px in zip(coords,moms)))

# Use nontrivial representatives for old-sector functions while retaining the
# exact support assumptions: Jhat has no A,N dependence and Hperp_hat has no A
# dependence on D_i nu=0.
Jhat=q**2 + p**2 - a*(p**2+q**2)/2
Hperp=(p**2+3*q**2)/2
Ghat=pnu+Jhat
Hrest=q*p  # arbitrary A,N-independent canonical Hamiltonian support
Hc=sp.expand(A*Jhat+N*Hperp+Hrest)

# Canonical affine/lapse support required by the projected a2=0 construction.
assert sp.diff(Jhat,A)==0
assert sp.diff(Jhat,N)==0
assert sp.diff(Hperp,A)==0
assert PB(Ghat,pA)==0
assert PB(Ghat,pN)==0

# First-generation consistency from the two multiplier primaries.
assert sp.simplify(PB(pA,Hc)+Jhat)==0
assert sp.simplify(PB(pN,Hc)+Hperp)==0

# Total Hamiltonian primary multipliers.  Because Ghat is independent of A,N,
# its consistency has no u_A or u_N term.
uA,uN,uG=sp.symbols('u_A u_N u_G', finite=True)
HT=Hc+uA*pA+uN*pN+uG*Ghat
phi=sp.expand(PB(Ghat,Hc))
dotG=sp.expand(PB(Ghat,HT))
assert sp.simplify(dotG-phi)==0
assert sp.diff(dotG,uA)==0
assert sp.diff(dotG,uN)==0
# {Ghat,Ghat}=0 removes its own multiplier identically.
assert sp.diff(dotG,uG)==0

# The recovered scalar-chain candidate is the four-constraint set used by the
# special-branch Hamiltonian theorem.  Its matrix is antisymmetric and its
# determinant is one Pfaffian squared.  We do not assign physical values to the
# six brackets here.
b12,b13,b14,b23,b24,b34=sp.symbols('b12 b13 b14 b23 b24 b34', finite=True)
M=sp.Matrix([
 [0,b12,b13,b14],
 [-b12,0,b23,b24],
 [-b13,-b23,0,b34],
 [-b14,-b24,-b34,0],
])
pf=sp.expand(b12*b34-b13*b24+b14*b23)
assert sp.simplify(M.det()-pf**2)==0
# In the projected regular-slice construction {pi_N,Jhat}=0 exactly.
pf_reduced=sp.simplify(pf.subs(b12,0))
assert sp.simplify(pf_reduced-(-b13*b24+b14*b23))==0

out={
  'classification':'RTK_ROUTE_B_U1_ELLIPTIC_COMPENSATOR_REDUCED_CONSTRAINT_CHAIN_PASS',
  'status_scope':'GREEN_EXACT_CHAIN_RECOVERY_REDUCED_FOUR_BY_FOUR_PHYSICAL_BRACKETS_PENDING',
  'parent_projection':'RTK_ROUTE_B_U1_ELLIPTIC_COMPENSATOR_DIRAC_PROJECTION_PASS',
  'domain':'regular D_i nu=0 Fourier-symbol slice after exact (p_Q,C_Lambda) Dirac elimination',
  'recovered_chain':{
    'p_A':'dot p_A=-Jhat -> Jhat=0',
    'pi_N':'dot pi_N=-Hperp_hat -> Hperp_hat=0',
    'Ghat':'dot Ghat=phi_hat={Ghat,H_c}; no u_A,u_N,u_G dependence -> phi_hat=0 unless it is weakly dependent on existing constraints',
    'projected_primary':'Ghat=p_nu+Jhat'
  },
  'exact_support':{
    '{Ghat,p_A}':'0',
    '{Ghat,pi_N}':'0',
    '{pi_N,Jhat}':'0',
    'reason':'Jhat is A- and N-independent on the projected a2=0 regular slice; Q,p_Q have already been removed by the genuine second-class pair'
  },
  'physical_rank_basis':['pi_N','Jhat','Hperp_hat','phi_hat'],
  'four_by_four_pfaffian':'Pf=-{pi_N,Hperp}{Jhat,phi}+{pi_N,phi}{Jhat,Hperp} because {pi_N,Jhat}=0',
  'rank_four_iff':'the displayed reduced Pfaffian is nonzero on the physical constraint surface',
  'interpretation':'The primary-mixing obstruction does not survive the exact auxiliary Dirac projection: the reduced system recovers the expected U(1) scalar constraint-chain architecture. The remaining question is now genuinely the physical rank of one reduced four-constraint block, not whether C_Q belongs to the chain.',
  'non_claims':[
    'does not prove phi_hat is independent rather than weakly dependent on the other constraints on every background',
    'does not compute the four physical Poisson operators entering the reduced Pfaffian',
    'does not treat the metric dependence of L^{-1} as a c-number in the final field theory',
    'does not choose M_c'
  ],
  'next_gate':'derive the four surviving cross-block operators {pi_N,Hperp_hat}, {pi_N,phi_hat}, {Jhat,Hperp_hat}, {Jhat,phi_hat}, including the resolvent metric variation of L^{-1}; then evaluate the reduced Pfaffian and classify finite-k zero loci.'
}
with open('u1_elliptic_compensator_reduced_constraint_chain_result.json','w') as f:
    json.dump(out,f,indent=2,sort_keys=True); f.write('\n')
print(out['classification'],json.dumps(out,sort_keys=True))
