#!/usr/bin/env python3
"""Constructive BPS two-crossover completion of the RTK rational dispersion.

Primary source: Blas, Pujolas, Sibiryakov, arXiv:1007.3503, Eqs. (5.1)-(5.8).
The BPS healthy nonprojectable scalar quadratic action has the exact P/Q
structure in p^2/M_*^2 and requires P/Q>0 for physical x<0. Generic z=3 UV
behavior has omega^2 proportional to p^6.

The exactly rational RTK pole can be obtained by tuning all higher P powers to
zero, but then its all-scale UV dispersion saturates instead of becoming p^6.
This theorem constructs a nearby continuous family that:
  * retains the exact RTK denominator 1+p^2/M_*^2;
  * differs only by a tunably small numerator factor 1+gamma(p^2/M_*^2)^3;
  * is positive/stable for every physical momentum;
  * restores omega^2 ~ p^6 above a separately tunable UV crossover.

Scope: scalar quadratic pole/dispersion construction. It does not by itself
prove the nonlinear strong-coupling inequality M_*<Lambda_p,omega, full DOF
count, radiative stability, or observational equivalence.
"""
import json
import sympy as sp

z,e,u,x=sp.symbols('z e u x', positive=True, finite=True, real=True)
ell=sp.symbols('ell', positive=True, finite=True, real=True)
alpha=sp.simplify(2*z/(1+z))
eta=sp.simplify(e/(1+e))  # exactly in (0,1)
d=sp.simplify(2/sp.sqrt(1+z))  # sqrt(4-2alpha)
rplus=sp.simplify((-2+d)/alpha)
rminus=sp.simplify((-2-d)/alpha)
t=sp.simplify((1-eta)*rplus+eta*rminus)

# Align the first dispersive denominator scale with the BPS higher-derivative
# scale by choosing s=alpha, hence f3=-alpha and Q(-u)=alpha(1+u).
f3=-alpha
f2=sp.simplify(t*f3)
f1=sp.simplify(-(2*f3+4*f2)/alpha)  # kills P_x exactly
g2=g3=sp.Integer(0)
g1=sp.simplify((f2**2-f1*f3)/alpha)  # kills P_x2 exactly

P=sp.expand((g2**2-g1*g3)*x**4
            -(g1*f3+g3*f1-2*g2*f2)*x**3
            +(f2**2-4*g2-f1*f3-2*g3-g1*alpha)*x**2
            -(2*f3+f1*alpha+4*f2)*x
            +(4-2*alpha))
Q=sp.expand(g3*x**2+f3*x+alpha)
P0=sp.simplify(4-2*alpha)
gamma=sp.simplify(4*eta*(1-eta))

# Exact polynomial form: P=P0(1-gamma*x^3), Q=alpha(1-x).
assert sp.simplify(P-P0*(1-gamma*x**3))==0
assert sp.simplify(Q-alpha*(1-x))==0
assert sp.Poly(P,x).degree()==3
assert sp.Poly(Q,x).degree()==1

# Physical x=-u, u=p^2/M_*^2 >=0.
Pphys=sp.simplify(P.subs(x,-u)); Qphys=sp.simplify(Q.subs(x,-u))
assert sp.simplify(Pphys-P0*(1+gamma*u**3))==0
assert sp.simplify(Qphys-alpha*(1+u))==0
ratio=sp.simplify(Pphys/Qphys)
base_ratio=sp.simplify((P0/alpha)/(1+u))
assert sp.simplify(ratio/base_ratio-(1+gamma*u**3))==0

# gamma is manifestly positive and <=1 for eta in (0,1), with arbitrary
# hierarchy gamma->0 as e->0.  The second crossover solves gamma*u^3=1.
assert sp.simplify(gamma-4*e/(1+e)**2)==0
assert sp.limit(gamma,e,0,dir='+')==0
u_uv=sp.simplify(gamma**(-sp.Rational(1,3)))
p_uv_over_Mstar=sp.simplify(gamma**(-sp.Rational(1,6)))
assert sp.limit(p_uv_over_Mstar,e,0,dir='+')==sp.oo

# Source-paper prefactor and UV scaling.
lam=1+ell
pref=sp.simplify((lam-1)/(2*(3*lam-1)))
cs2=sp.simplify(pref*(P0/alpha))
assert sp.simplify(cs2-ell/(z*(2+3*ell)))==0
# Dimensionless omega^2/(M_*^2) = cs2*u*(1+gamma*u^3)/(1+u).
omega2_dimless=sp.simplify(cs2*u*(1+gamma*u**3)/(1+u))
assert sp.limit(omega2_dimless/u**3,u,sp.oo)==sp.simplify(cs2*gamma)

# Stable scalar sign structure on all physical u>=0 is manifest:
# alpha,P0,gamma>0 and both 1+u,1+gamma*u^3 are positive.
# eta in (0,1) also gives gamma<=1 because 4eta(1-eta)=1-(1-2eta)^2.
assert sp.simplify(1-gamma-(1-2*eta)**2)==0

out={
  'classification':'RTK_ROUTE_B_BPS_Z3_TWO_CROSSOVER_PASS',
  'primary_source':'Blas-Pujolas-Sibiryakov arXiv:1007.3503 Eqs. (5.1)-(5.8)',
  'parameterization':{
    'alpha':'2z/(1+z) in (0,2)','lambda':'1+ell >1','eta':'e/(1+e) in (0,1)',
    'f3':'-alpha','f2_over_f3':'linear interpolation between the two exact-rational roots',
    'f1':'-(2f3+4f2)/alpha','g1':'(f2^2-f1 f3)/alpha','g2':0,'g3':0
  },
  'exact_polynomials':{
    'P':'(4-2alpha)[1-gamma x^3]','Q':'alpha(1-x)','gamma':'4eta(1-eta)=4e/(1+e)^2'
  },
  'physical_dispersion':{
    'form':'omega^2=cs^2 p^2 [1+gamma(p^2/M_*^2)^3]/[1+p^2/M_*^2]',
    'cs2':'ell/[z(2+3ell)] >0',
    'first_crossover':'M_disp=M_*',
    'uv_crossover':'p_UV/M_*=gamma^(-1/6)',
    'relative_correction_to_RTK_rational_below_UV':'gamma (p^2/M_*^2)^3',
    'uv_scaling':'omega^2 proportional to p^6'
  },
  'hierarchy':'gamma->0 as e->0, so p_UV/M_*->infinity while the first rational crossover stays at M_*',
  'stability':'For every physical p, P(-p^2/M_*^2)>0 and Q(-p^2/M_*^2)>0; lambda>1 gives positive scalar kinetic coefficient.',
  'theorem':'The BPS healthy scalar quadratic class contains a continuous two-crossover family that approaches the exact RTK rational dispersion arbitrarily closely on any fixed finite momentum range while restoring the z=3 p^6 UV dispersion above a parametrically higher scale.',
  'strong_coupling_guard':'Restoring z=3 scaling makes the BPS strong-coupling-avoidance route available in principle, but the separate inequality M_*<Lambda_p,omega and the selected-family cubic interactions must still be checked explicitly.',
  'non_claims':['not exact RTK rational dispersion at arbitrarily high momentum for gamma>0','not a full nonlinear RTK equivalence','not a completed strong-coupling proof','not radiative stability or a UV-completion proof']
}
print('RTK_ROUTE_B_BPS_Z3_TWO_CROSSOVER_PASS',json.dumps(out,sort_keys=True))
