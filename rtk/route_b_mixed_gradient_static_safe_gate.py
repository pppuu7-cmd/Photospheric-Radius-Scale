#!/usr/bin/env python3
"""Exact C8 gate for the smallest mixed-gradient companion basis.

Goal: test whether the direct acceleration coefficient responsible for the
standard-matter PPN/Newton obstruction can be replaced or reduced by operators
that vanish on a strictly static K_ij=0 background while retaining the exact
FLRW RTK scalar kinetic factor.

Use the already-derived flat-FLRW scalar variables

  N=1+n,  N_i=partial_i psi,  gamma_ij=a^2 exp(2 zeta) delta_ij,
  y=p^2=k^2/a^2,
  A=dot(zeta)-H n,
  delta K = 3 A + y psi

(up to the fixed Fourier sign convention used below).

Extend the established EH+clock quadratic scalar Lagrangian by the most direct
quadratic one-spatial-gradient constraint basis

  y [ C n^2 + 2 D n deltaK + B (deltaK)^2 ],

which corresponds to

  C a_i a^i + 2 D a_i D^i K + B D_i K D^i K

at quadratic order.  B and D terms vanish on a strictly static K_ij=0
configuration; C a_i a^i is the dangerous static acceleration term.

After exact elimination of scalar shift and lapse, require the dot(zeta)^2
coefficient to equal the RTK target

  K/(2 H^2) * (1 + y/MK^2)

for all y.

The polynomial matching equations have exactly two branches (for nonzero
positive H,M^2,K,MK^2 and away from 6 H^2 M^2=K):

1. pure acceleration:
   B=D=0,  C=K/(2 MK^2);

2. rank-one mixed branch:
   B = 8 H^2 K M^4 / [MK^2 (6H^2M^2-K)^2],
   D = 2 H K M^2 (6H^2M^2+K) / [MK^2 (6H^2M^2-K)^2],
   C = K(6H^2M^2+K)^2 / [2 MK^2 (6H^2M^2-K)^2].

For positive H^2,M^2,K the mixed branch obeys

  C/C_direct = [(6H^2M^2+K)/(6H^2M^2-K)]^2 > 1.

Therefore this minimal mixed-gradient basis cannot reduce the required static
a_i a^i coefficient below the direct branch.  In particular C=0 has no exact
RTK solution.

Scope: quadratic scalar flat-FLRW theorem for this explicit operator basis.
It does not exclude other extrinsic-curvature tensors, auxiliary fields,
nonminimal matter maps, higher-spatial-gradient operators, or combinations
whose static sector is altered by additional constraints.
"""

import json
import sympy as sp

# Positive physical background symbols.  B,C,D are unrestricted real EFT
# coefficients during solving.
y,H,M2,K,MK2=sp.symbols('y H M2 K MK2', positive=True, finite=True, real=True)
B,C,D=sp.symbols('B C D', finite=True, real=True)
d,z,n=sp.symbols('d z n', real=True)
shift=sp.symbols('shift', real=True)  # shift := y psi

A=d-H*n
deltaK=3*A+shift

# Established EH+clock scalar quadratic L/a^3 before constraint elimination,
# with M2 denoting the bare coefficient M_*^2.  The R3 z terms are retained to
# keep the same constraints, though only the d^2 coefficient is matched here.
L=(
    -3*M2*A**2
    + sp.Rational(1,2)*K*n**2
    + 2*M2*y*n*z
    + M2*y*z**2
    - 2*M2*A*shift
    + y*(C*n**2 + 2*D*n*deltaK + B*deltaK**2)
)

# Eliminate shift and lapse exactly.
eq_shift=sp.diff(L,shift)
eq_n=sp.diff(L,n)
sol=sp.solve([eq_shift,eq_n],[shift,n],dict=True,simplify=False)
assert len(sol)==1
Lred=sp.factor(sp.simplify(L.subs(sol[0])))
kin=sp.factor(sp.diff(Lred,d,2)/2)

target=sp.factor(K/(2*H**2)*(1+y/MK2))
num=sp.factor(sp.together(kin-target).as_numer_denom()[0])
poly=sp.Poly(num,y)
assert poly.degree()==3
coeff=[sp.factor(poly.coeff_monomial(y**i)) for i in range(4)]
assert coeff[0]==0

# Solve exact coefficient matching.  SymPy returns the two analytic branches.
branches=sp.solve(coeff[1:],[B,C,D],dict=True,simplify=False)
assert len(branches)==2

pure={B:sp.Integer(0), C:K/(2*MK2), D:sp.Integer(0)}
mixed={
    B:8*H**2*K*M2**2/(MK2*(6*H**2*M2-K)**2),
    C:K*(6*H**2*M2+K)**2/(2*MK2*(6*H**2*M2-K)**2),
    D:2*H*K*M2*(6*H**2*M2+K)/(MK2*(6*H**2*M2-K)**2),
}

def same_branch(a,b):
    return all(sp.simplify(a[s]-b[s])==0 for s in (B,C,D))
assert any(same_branch(q,pure) for q in branches)
assert any(same_branch(q,mixed) for q in branches)

# Verify each branch reproduces the target identically.
for br in (pure,mixed):
    assert sp.simplify(kin.subs(br)-target)==0

Cdirect=K/(2*MK2)
ratio=sp.factor(mixed[C]/Cdirect)
assert sp.simplify(ratio-((6*H**2*M2+K)/(6*H**2*M2-K))**2)==0
# ratio-1 = 24 H^2 M2 K / (6H^2M2-K)^2 >0 for positive background.
ratio_minus_one=sp.factor(ratio-1)
assert sp.simplify(ratio_minus_one-24*H**2*M2*K/(6*H**2*M2-K)**2)==0

# Rank-one gradient block of the mixed branch: BC-D^2=0.
assert sp.simplify((B*C-D**2).subs(mixed))==0

# Static-safe C=0 cannot solve the matching equations: cubic forces D=0,
# then quadratic forces B=0, while linear coefficient remains nonzero.
coeff_C0=[sp.factor(q.subs(C,0)) for q in coeff[1:]]
# Demonstrate contradiction algebraically under D=0,B=0.
assert sp.factor(coeff_C0[2]) == 2*D**2*K  or sp.factor(coeff_C0[2]) == -2*D**2*K
# independent of sign convention above, C=0 exact matching forces D=0.
assert sp.simplify(coeff_C0[1].subs(D,0)).has(B)
assert sp.simplify(coeff_C0[0].subs({D:0,B:0})) != 0

out={
    'classification':'RTK_ROUTE_B_MIXED_GRADIENT_STATIC_SAFE_GATE_PASS',
    'operator_basis':'C a_i a^i + 2 D a_i D^i K + B D_i K D^i K',
    'target':'K/(2 H^2) [1+p^2/M_K^2] for the reduced dot(zeta)^2 coefficient',
    'branches':{
        'pure_acceleration':{
            'B':'0','D':'0','C':'K/(2 M_K^2)'
        },
        'rank_one_mixed':{
            'B':'8 H^2 K M_*^4/[M_K^2(6H^2 M_*^2-K)^2]',
            'D':'2 H K M_*^2(6H^2 M_*^2+K)/[M_K^2(6H^2 M_*^2-K)^2]',
            'C':'K(6H^2 M_*^2+K)^2/[2M_K^2(6H^2 M_*^2-K)^2]',
            'BC_minus_D2':'0'
        }
    },
    'static_acceleration_floor':{
        'C_direct':'K/(2 M_K^2)',
        'C_mixed_over_C_direct':'[(6H^2 M_*^2+K)/(6H^2 M_*^2-K)]^2',
        'ratio_minus_one':'24 H^2 M_*^2 K/(6H^2 M_*^2-K)^2 > 0'
    },
    'theorem':'Within this minimal mixed-gradient quadratic basis, an exact RTK FLRW kinetic match always requires a nonzero a_i a^i coefficient at least as large as the direct pure-acceleration value. Setting C=0 gives no exact solution.',
    'singular_surface':'6 H^2 M_*^2 = K makes the displayed mixed branch singular and is not an escape solution.',
    'non_claims':[
        'not a no-go for other extrinsic-curvature tensor operators',
        'not a no-go for auxiliary constrained fields',
        'not a no-go for nonminimal/disformal matter frames',
        'not a nonlinear/compact-object theorem',
        'not a radiative-stability or strong-coupling theorem'
    ],
    'next_step':'Move beyond this minimal gradient basis: test operators/auxiliary constraints whose cosmological p^2 dot(zeta)^2 contribution is not tied to a_i a^i, while checking tensor speed, DOF and static PPN simultaneously.'
}
print('RTK_ROUTE_B_MIXED_GRADIENT_STATIC_SAFE_GATE_PASS',json.dumps(out,sort_keys=True))
