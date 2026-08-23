#!/usr/bin/env python3
"""Exact cubic/quartic conformal-scalar expansion of the preferred n=2 UV carrier.

Scope
-----
Carrier: sqrt(gamma) D_i R3 D^i R3 on the flat rolling patch with
  gamma_ij = a^2 exp(2 zeta) delta_ij,
unit lapse for this bare intrinsic-curvature subproblem, and the background
coefficient alpha6 held fixed while expanding the spatial geometry.

This is deliberately one step before the full reduced amplitude: lapse/shift
perturbations, perturbations of the state-dependent alpha6 coefficient, P(X)
interference, U(1)/auxiliary exchange and loops are not included here.

In d=3,
  R3 = a^-2 exp(-2 zeta) F,
  F  = -4 Delta zeta - 2 (grad zeta)^2.
Therefore exactly
  sqrt(gamma) D_i R3 D^i R3
   = a^-3 exp(-3 zeta) [partial_i F - 2 F partial_i zeta]^2.

Define
  Z_i = partial_i zeta,
  L   = Delta zeta,
  U_i = partial_i Delta zeta,
  V_i = partial_j zeta partial_i partial_j zeta,
  S   = Z_i Z_i.
Then
  A1_i = -4 U_i,
  A2_i = -4 V_i + 8 L Z_i,
  A3_i =  4 S Z_i,
and the exact density through O(zeta^4) is a^-3 (Q2+Q3+Q4):
  Q2 = 16 U^2,
  Q3 = 32 U.V - 64 L U.Z - 48 zeta U^2,
  Q4 = 16 V^2 - 64 L V.Z + 64 L^2 Z^2
       -32 S U.Z -96 zeta U.V +192 zeta L U.Z +72 zeta^2 U^2.

The script also derives momentum-space bare kernels:
* the fully symmetric cubic kernel for k1+k2+k3=0;
* the elastic equal-|k| COM quartic contact kernel;
* the s/t/u cubic channel kernels needed for the next exchange calculation.
"""
import itertools
import json
import sympy as sp

# ---------------------------------------------------------------------------
# 1. Series-combinatorics audit of Q2,Q3,Q4.
# ---------------------------------------------------------------------------
eps, z = sp.symbols('eps zeta', real=True)
L, S = sp.symbols('L S', real=True)
U = sp.Matrix(sp.symbols('U1:4', real=True))
V = sp.Matrix(sp.symbols('V1:4', real=True))
Z = sp.Matrix(sp.symbols('Z1:4', real=True))
A1 = -4*U
A2 = -4*V + 8*L*Z
A3 = 4*S*Z

# Assign perturbative orders with a book-keeping epsilon.
Aeps = eps*A1 + eps**2*A2 + eps**3*A3
exp_series = 1 - 3*eps*z + sp.Rational(9,2)*eps**2*z**2
Iseries = sp.expand(exp_series * Aeps.dot(Aeps))
Q2_from_series = sp.expand(Iseries.coeff(eps,2))
Q3_from_series = sp.expand(Iseries.coeff(eps,3))
Q4_from_series = sp.expand(Iseries.coeff(eps,4))

U2=U.dot(U); UV=U.dot(V); UZ=U.dot(Z)
V2=V.dot(V); VZ=V.dot(Z); Z2=Z.dot(Z)
Q2 = sp.expand(16*U2)
Q3 = sp.expand(32*UV - 64*L*UZ - 48*z*U2)
Q4 = sp.expand(16*V2 - 64*L*VZ + 64*L**2*Z2 - 32*S*UZ
               - 96*z*UV + 192*z*L*UZ + 72*z**2*U2)
assert sp.simplify(Q2_from_series-Q2)==0
assert sp.simplify(Q3_from_series-Q3)==0
assert sp.simplify(Q4_from_series-Q4)==0

# ---------------------------------------------------------------------------
# 2. Fully symmetric cubic Fourier kernel.
# ---------------------------------------------------------------------------
q1,q2,q3 = sp.symbols('q1 q2 q3', positive=True, finite=True)
qs={1:q1,2:q2,3:q3}

def dot3(i,j):
    if i==j:
        return qs[i]
    a,b=sorted((i,j))
    # Momentum conservation k1+k2+k3=0.
    if (a,b)==(1,2): return (q3-q1-q2)/2
    if (a,b)==(1,3): return (q2-q1-q3)/2
    if (a,b)==(2,3): return (q1-q2-q3)/2
    raise AssertionError

# Plane-wave rules:
# U_i(a)=-i q_a k_a_i
# V_i(b,c)=-i (k_b.k_c) k_c_i (ordered b,c)
# Z_i(c)= i k_c_i, L(a)=-q_a.
uv=0; Luz=0; zu2=0
for a,b,c in itertools.permutations([1,2,3]):
    uv += -qs[a]*dot3(a,c)*dot3(b,c)
    Luz += -qs[a]*qs[b]*dot3(b,c)
    zu2 += -qs[b]*qs[c]*dot3(b,c)
K3 = sp.factor(32*uv - 64*Luz - 48*zu2)
s1=q1+q2+q3
s2=q1*q2+q1*q3+q2*q3
s3=q1*q2*q3
K3_expected=16*(s1**3-7*s1*s2+12*s3)
assert sp.simplify(K3-K3_expected)==0

# ---------------------------------------------------------------------------
# 3. Elastic equal-|k| COM quartic contact kernel.
# ---------------------------------------------------------------------------
k, cth = sp.symbols('k cos_theta', positive=True, finite=True, real=True)
labels=[1,2,3,4]
q={i:k**2 for i in labels}

def dot4(i,j):
    if i==j: return k**2
    pair=tuple(sorted((i,j)))
    # all incoming spatial momenta:
    # p1=k n, p2=-k n, p3=-k n', p4=k n', n.n'=cos(theta)
    table={
      (1,2):-k**2,
      (3,4):-k**2,
      (1,3):-cth*k**2,
      (1,4): cth*k**2,
      (2,3): cth*k**2,
      (2,4):-cth*k**2,
    }
    return table[pair]

# Coefficient of one copy of each external plane wave in Q4.
Sv2=SLvz=SL2z2=SSuz=Szuv=SzLuz=Sz2u2=0
for a,b,c,d in itertools.permutations(labels):
    # V(a,b).V(c,d)
    Sv2 += -dot4(a,b)*dot4(c,d)*dot4(b,d)
    # L(a) V(b,c).Z(d)
    SLvz += -q[a]*dot4(b,c)*dot4(c,d)
    # L(a)L(b) Z(c).Z(d)
    SL2z2 += -q[a]*q[b]*dot4(c,d)
    # S(a,b) U(c).Z(d)
    SSuz += -dot4(a,b)*q[c]*dot4(c,d)
    # zeta(a) U(b).V(c,d)
    Szuv += -q[b]*dot4(c,d)*dot4(b,d)
    # zeta(a)L(b)U(c).Z(d)
    SzLuz += -q[b]*q[c]*dot4(c,d)
    # zeta(a)zeta(b)U(c).U(d)
    Sz2u2 += -q[c]*q[d]*dot4(c,d)

K4_com=sp.factor(16*Sv2 - 64*SLvz + 64*SL2z2 - 32*SSuz
                 - 96*Szuv + 192*SzLuz + 72*Sz2u2)
K4_expected=320*k**6*(9-2*cth**2)
assert sp.simplify(K4_com-K4_expected)==0
# For |cos theta|<=1 the polynomial is strictly positive.
assert sp.simplify(K4_expected.subs(cth,1)-2240*k**6)==0
assert sp.simplify(K4_expected.subs(cth,0)-2880*k**6)==0

# ---------------------------------------------------------------------------
# 4. Cubic kernels in elastic s/t/u spatial channels.
# ---------------------------------------------------------------------------
qq=sp.symbols('q', positive=True, finite=True)
x=sp.symbols('x', real=True, finite=True)

def K3q(a,b,c):
    ss1=a+b+c
    ss2=a*b+a*c+b*c
    ss3=a*b*c
    return sp.factor(16*(ss1**3-7*ss1*ss2+12*ss3))

Ks=sp.factor(K3q(qq,qq,0))
Kt=sp.factor(K3q(qq,qq,2*qq*(1-x)))
Ku=sp.factor(K3q(qq,qq,2*qq*(1+x)))
assert Ks==-96*qq**3
assert sp.simplify(Kt + 32*qq**3*(4*x**3+4*x**2-31*x+26))==0
assert sp.simplify(Ku - 32*qq**3*(4*x**3-4*x**2-31*x-26))==0

# Prove t/u channel cubic kernels have no zero in the physical angular interval.
pt=4*x**3+4*x**2-31*x+26
pu=4*x**3-4*x**2-31*x-26
# Derivative stationary points are outside [-1,1].
crit_t=sp.solve(sp.diff(pt,x),x)
crit_u=sp.solve(sp.diff(pu,x),x)
assert all(bool((r>1) or (r<-1)) for r in crit_t)
assert all(bool((r>1) or (r<-1)) for r in crit_u)
# Both polynomials are strictly decreasing on [-1,1]; endpoint signs fix them.
assert sp.diff(pt,x).subs(x,0)<0 and sp.diff(pu,x).subs(x,0)<0
assert pt.subs(x,1)==3 and pt.subs(x,-1)==57
assert pu.subs(x,1)==-57 and pu.subs(x,-1)==-3

out={
 'classification':'RTK_C9_RTK_SCALAR_N2_CURVATURE_NONLINEAR_CONFORMAL_PASS',
 'status_scope':'GREEN_EXACT_BARE_CONFORMAL_CUBIC_QUARTIC_KERNELS_LAPSE_SHIFT_REDUCTION_AND_FULL_AMPLITUDE_PENDING',
 'exact_density':'sqrt(gamma) D_i R3 D^i R3 = a^-3 exp(-3 zeta)[partial_i F-2 F partial_i zeta]^2, F=-4 Delta zeta-2(grad zeta)^2',
 'definitions':{
   'Z_i':'partial_i zeta','L':'Delta zeta','U_i':'partial_i Delta zeta',
   'V_i':'partial_j zeta partial_i partial_j zeta','S':'(grad zeta)^2'
 },
 'quadratic':'Q2=16 U^2',
 'cubic':'Q3=32 U.V-64 L U.Z-48 zeta U^2',
 'quartic':'Q4=16 V^2-64 L V.Z+64 L^2 Z^2-32 S U.Z-96 zeta U.V+192 zeta L U.Z+72 zeta^2 U^2',
 'cubic_fourier_kernel':{
   'domain':'k1+k2+k3=0, q_i=|k_i|^2',
   'kernel':'K3=16[(q1+q2+q3)^3-7(q1+q2+q3)(q1q2+q1q3+q2q3)+12q1q2q3]'
 },
 'elastic_com_quartic_contact_kernel':'K4=320 k^6(9-2 cos^2 theta), strictly positive polynomial before multiplying the carrier coefficient/sign convention',
 'elastic_channel_cubic_kernels':{
   's':'-96 k^6',
   't':'-32 k^6[4c^3+4c^2-31c+26]',
   'u':'32 k^6[4c^3-4c^2-31c-26]',
   'physical_interval':'all three are nonzero for -1<=c<=1 under this bare-kernel convention'
 },
 'interpretation':'The preferred n=2 intrinsic-curvature carrier has explicit nonvanishing cubic exchange support and a simple positive angular quartic contact polynomial. Power counting alone is therefore insufficient; the next gate can now build the actual curvature exchange/contact amplitude instead of using unknown O(1) vertex coefficients.',
 'non_claims':[
   'not the reduced scalar vertices because lapse and shift perturbations are not yet eliminated at cubic/quartic order',
   'state-function perturbations of alpha6 are not included here',
   'no P(X) or mixed C(X) interference yet',
   'no U1/auxiliary/metric exchange yet',
   'no loop or inelastic unitarity statement'
 ],
 'next_gate':'include lapse/shift and alpha6-state perturbations in the n=2 carrier expansion, solve the nonlinear constraints, then compute the exact reduced curvature contact+exchange contribution and its interference with the certified P(X) amplitude.'
}
open('c9_rtk_scalar_n2_curvature_nonlinear_conformal_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
