#!/usr/bin/env python3
"""Complete cubic D=5 basis audit for the frozen preferred-frame Route A1.

Assumptions inherited from PREFERRED_FRAME_EFT_ROUTE_A1.md:
- one scalar pi, constant shift symmetry;
- SO(3), spatial translations and parity;
- three fields at cubic order;
- no more than one time derivative on an individual field;
- reduction modulo spatial integration by parts.

The momentum-space rank calculation is a compact implementation of spatial IBP:
for a local cubic vertex, total spatial derivatives are polynomials in the three
momenta with k1+k2+k3=0.  The dotted leg is labelled 1 for the T=1 sector and
the two undotted legs are symmetrized under 2<->3.
"""
import json
import sympy as sp

# ----- Derivative-count classification -----
# D=5 and parity-even rotational scalars require an even total number S of
# spatial indices.  Since D=T+S and each of three fields carries at most one
# time derivative, T can only be 1 or 3.
D=5
allowed_T=[T for T in range(4) if (D-T)%2==0]
assert allowed_T == [1,3]

# T=3 -> S=2.  Up to identical-field permutations the possible spatial
# partitions are (2,0,0) and (1,1,0).  Spatial IBP relates
# int dot(pi)^2 Delta dot(pi) = -2 int dot(pi)|grad dot(pi)|^2,
# so there is one independent T=3 representative.
T3_basis=['dot(pi)*(grad dot(pi))^2']

# ----- T=1, S=4 exhaustive SO(3) contraction rank -----
# Label the dotted field 1. Shift symmetry requires each undotted field 2,3
# to carry >=1 spatial derivative. Up to 2<->3, the spatial derivative
# partitions are exactly (0,1,3), (0,2,2), (1,1,2), (2,1,1).
partitions=[(0,1,3),(0,2,2),(1,1,2),(2,1,1)]
assert all(sum(p)==4 and p[1]>=1 and p[2]>=1 for p in partitions)

# Momentum invariants. a=k1^2, b=k2^2, c=k3^2. With k1+k2+k3=0:
a,b,c=sp.symbols('a b c', real=True)
d12=(c-a-b)/2
d13=(b-a-c)/2
d23=(a-b-c)/2

# Every parity-even SO(3) contraction for each tensor-rank partition:
# 013: vector x symmetric rank-3 -> one contraction.
# 022: symmetric rank-2 x rank-2 -> trace*trace and full contraction.
# 112: two vectors x rank-2 -> dot*trace and Hessian contraction.
# 211: rank-2 x two vectors -> trace*dot and Hessian contraction.
P={
 '013_grad_third':sp.expand(d23*(b+c)),
 '022_lap_lap':sp.expand(b*c),
 '022_hess_hess':sp.expand(d23**2),
 '112_gradgrad_lap':sp.expand(d12*c+d13*b),
 '112_cross_hess':sp.expand(d13*d23+d12*d23),
 '211_lapdot_gradgrad':sp.expand(a*d23),
 '211_hessdot_gradgrad':sp.expand(d12*d13),
}
assert len(P)==7

# All are symmetric under exchange of the two undotted legs b<->c.
for p in P.values():
    assert sp.simplify(p-p.xreplace({b:c,c:b}))==0

# Coefficient vectors in the complete degree-2 polynomial basis compatible
# with b<->c symmetry: [a^2, a(b+c), b^2+c^2, bc].
def vec(poly):
    q=sp.Poly(sp.expand(poly),a,b,c)
    assert q.coeff_monomial(a*b)==q.coeff_monomial(a*c)
    assert q.coeff_monomial(b**2)==q.coeff_monomial(c**2)
    return sp.Matrix([
        q.coeff_monomial(a**2),
        q.coeff_monomial(a*b),
        q.coeff_monomial(b**2),
        q.coeff_monomial(b*c),
    ])

all_matrix=sp.Matrix.hstack(*[vec(p) for p in P.values()])
assert all_matrix.rank()==3

# Choose three independent real-space representatives:
# B2 = dot(pi) (Delta pi)^2
# B3 = dot(pi) (d_i d_j pi)^2
# B4 = (Delta dot(pi)) (grad pi)^2
chosen=['022_lap_lap','022_hess_hess','211_lapdot_gradgrad']
C=sp.Matrix.hstack(*[vec(P[k]) for k in chosen])
assert C.rank()==3

# Explicit reductions of every exhaustive candidate into [B2,B3,B4].
reductions={}
expected={
 '013_grad_third':(0,-2,1),
 '022_lap_lap':(1,0,0),
 '022_hess_hess':(0,1,0),
 '112_gradgrad_lap':(-2,2,-1),
 '112_cross_hess':(0,0,-1),
 '211_lapdot_gradgrad':(0,0,1),
 '211_hessdot_gradgrad':(1,-1,1),
}
for name,p in P.items():
    sols=list(sp.linsolve((C,vec(p))))
    assert len(sols)==1
    coeff=tuple(sp.simplify(x) for x in sols[0])
    assert coeff==expected[name], (name,coeff)
    reductions[name]=[str(x) for x in coeff]

basis={
 'T3_S2':['dot(pi)*(grad dot(pi))^2'],
 'T1_S4':[
   'dot(pi)*(Laplacian(pi))^2',
   'dot(pi)*(d_i d_j pi)*(d_i d_j pi)',
   'Laplacian(dot(pi))*(grad pi)^2',
 ],
}
assert sum(map(len,basis.values()))==4

result={
 'classification':'RTK_ROUTE_A1_CUBIC_D5_BASIS_PASS',
 'assumptions':'Route A1 + cubic D=5 + spatial IBP',
 'allowed_time_derivative_counts':allowed_T,
 'T1_spatial_partitions':[list(x) for x in partitions],
 'T1_exhaustive_contractions':list(P),
 'T1_contraction_count':len(P),
 'T1_rank_mod_spatial_IBP':all_matrix.rank(),
 'T3_rank_mod_spatial_IBP':1,
 'complete_D5_basis':basis,
 'basis_size':4,
 'reductions_to_T1_basis_B2_B3_B4':reductions,
 'contains_linear_dispersion_nonlinearization':'dot(pi)*(grad dot(pi))^2',
 'no_second_time_derivative_required':True,
 'coefficients_determined_by_linear_target':False,
 'full_finite_k_nonlinear_completion_closed':False,
}
print('RTK_ROUTE_A1_D5_BASIS_PASS',json.dumps(result,sort_keys=True))
