#!/usr/bin/env python3
"""Route-B constructive theorem inside the BPS healthy nonprojectable Horava class.

Primary source: Blas, Pujolas, Sibiryakov, arXiv:0909.3525, Eqs. (12)-(18).
Their scalar quadratic action after integrating nondynamical fields has

  omega^2 = [(lambda-1)/(2(3lambda-1))] * P(-p^2/Mp^2)/Q(-p^2/Mp^2) * p^2,

with
  P(x)=(g2^2-g1*g3)x^4 -(g1*f3+g3*f1-2*g2*f2)x^3
      +(f2^2-4*g2-f1*f3-2*g3-g1*alpha)x^2
      -(2*f3+f1*alpha+4*f2)x +(4-2*alpha),
  Q(x)=g3*x^2+f3*x+alpha.

This script proves an explicit continuous parameter family for which the ratio
is exactly proportional to 1/(1+p^2/Mstar^2), while the source-paper scalar
quadratic stability conditions are satisfied for every p>=0.

Scope: exact Minkowski scalar quadratic embedding in the BPS healthy-extension
class. This is not yet a full RTK cosmological mapping, generic-background DOF
proof, phenomenology fit, strong-coupling calculation, or radiative-stability
result.
"""
import json
import sympy as sp

# Positive unconstrained parameters.  The substitutions below enforce
# 0<alpha<2, f3<0 and lambda>1 without relying on inequality assumptions that
# a symbolic engine may fail to simplify.
z,s,ell,u,x,MP=sp.symbols('z s ell u x MP', positive=True, finite=True, real=True)
alpha=sp.simplify(2*z/(1+z))
f3=-s
lam=1+ell
sqrt_disc=sp.simplify(2/sp.sqrt(1+z))  # sqrt(4-2 alpha)

g1=g2=g3=sp.Integer(0)

# Source-paper polynomials.
def polys(f1,f2):
    P=sp.expand((g2**2-g1*g3)*x**4
                -(g1*f3+g3*f1-2*g2*f2)*x**3
                +(f2**2-4*g2-f1*f3-2*g3-g1*alpha)*x**2
                -(2*f3+f1*alpha+4*f2)*x
                +(4-2*alpha))
    Q=sp.expand(g3*x**2+f3*x+alpha)
    return sp.factor(P),sp.factor(Q)

branches=[]
for sign in (+1,-1):
    ratio=sp.simplify((-2+sign*sqrt_disc)/alpha)  # f2/f3
    f2=sp.simplify(ratio*f3)
    f1=sp.simplify(f2**2/f3)
    P,Q=polys(f1,f2)

    # Exact cancellation of all derivative powers in P.
    P_expected=sp.simplify(4-2*alpha)
    assert sp.simplify(P-P_expected)==0
    assert sp.Poly(P,x).degree()==0
    assert sp.simplify(Q-(alpha+f3*x))==0

    # On physical momentum x=-u, u=p^2/MP^2>=0:
    # Q(-u)=alpha+s*u and P/Q = (P0/alpha)/(1+s*u/alpha).
    P_phys=sp.simplify(P.subs(x,-u))
    Q_phys=sp.simplify(Q.subs(x,-u))
    target_ratio=sp.simplify((P_expected/alpha)/(1+(s/alpha)*u))
    assert sp.simplify(P_phys/Q_phys-target_ratio)==0
    assert sp.simplify(Q_phys-(alpha+s*u))==0

    # Source-paper ghost-free prefactor and resulting exact sound/dispersion.
    kinetic_sign_ratio=sp.simplify((3*lam-1)/(lam-1))
    omega_prefactor=sp.simplify((lam-1)/(2*(3*lam-1)))
    cs2=sp.factor(omega_prefactor*(P_expected/alpha))
    cs2_expected=sp.simplify(ell/(z*(2+3*ell)))
    assert sp.simplify(cs2-cs2_expected)==0

    # Mstar^2 = alpha MP^2/s >0, and denominator is 1+p^2/Mstar^2.
    Mstar2=sp.simplify(alpha*MP**2/s)
    p2=sp.symbols('p2', nonnegative=True, finite=True, real=True)
    u_phys=sp.simplify(p2/MP**2)
    dispersion=sp.simplify(omega_prefactor*(P_phys/Q_phys).subs(u,u_phys)*p2)
    target_dispersion=sp.simplify(cs2*p2/(1+p2/Mstar2))
    assert sp.simplify(dispersion-target_dispersion)==0

    branches.append({
      'sign':sign,
      'f2_over_f3':sp.sstr(ratio),
      'f2':sp.sstr(f2),
      'f1':sp.sstr(f1),
      'P':sp.sstr(P),
      'Q':sp.sstr(Q),
      'kinetic_sign_ratio':sp.sstr(kinetic_sign_ratio),
      'cs2':sp.sstr(cs2),
      'Mstar2':sp.sstr(Mstar2),
    })

# Positivity is manifest in the chosen parameterization:
# alpha=2z/(1+z) lies in (0,2), P0=4/(1+z)>0,
# Q(-u)=alpha+s*u>0, kinetic ratio=(2+3ell)/ell>0,
# cs2=ell/[z(2+3ell)]>0 and Mstar^2=alpha MP^2/s>0.
assert sp.simplify(4-2*alpha-4/(1+z))==0
assert sp.simplify((3*lam-1)/(lam-1)-(2+3*ell)/ell)==0

out={
  'classification':'RTK_ROUTE_B_BPS_EXACT_RATIONAL_EMBEDDING_PASS',
  'primary_source':'Blas-Pujolas-Sibiryakov arXiv:0909.3525 Eqs. (12)-(18)',
  'source_polynomial_degree':{'P':4,'Q':2},
  'constructive_family':{
    'free_positive_parameters':['z','s','ell','MP'],
    'alpha':'2 z/(1+z) in (0,2)',
    'lambda':'1+ell > 1',
    'f3':'-s < 0',
    'g1=g2=g3':0,
    'two_f2_over_f3_branches':'(-2 +/- 2/sqrt(1+z))/alpha',
    'f1':'f2^2/f3'
  },
  'exact_reduced_polynomials':{
    'P':'4-2 alpha = 4/(1+z)',
    'Q':'alpha+f3*x',
    'Q_physical':'Q(-p^2/MP^2)=alpha+s p^2/MP^2 > 0'
  },
  'exact_dispersion':{
    'form':'omega^2 = cs^2 p^2/(1+p^2/Mstar^2)',
    'cs2':'ell/[z(2+3ell)] > 0',
    'Mstar2':'alpha MP^2/s > 0'
  },
  'source_paper_stability_conditions':{
    'ghost_ratio':'(3lambda-1)/(lambda-1)=(2+3ell)/ell > 0',
    'gradient_ratio':'P(x)/Q(x)>0 for x<0 because P>0 and Q(-u)>0',
    'alpha_interval':'0<alpha<2 by construction'
  },
  'theorem':'The healthy nonprojectable Horava quadratic scalar sector contains a continuous two-branch coefficient family whose exact dispersion is the RTK target rational mixed-kinetic form, while satisfying the BPS Minkowski scalar ghost/gradient stability conditions.',
  'relation_to_previous_nogo':'This broader higher-spatial-operator BPS class is outside the previously excluded constant-ci c4=2 khronometric subspace, so the earlier narrow no-go does not apply.',
  'next_required_proofs':[
    'map the BPS scalar variable/normalization to the intended RTK Khronon observable sector rather than only the dispersion form',
    'derive/check the full nonlinear constraint and physical DOF count for the selected coefficient family',
    'test FLRW and generic smooth-background scalar/tensor stability beyond the short-wavelength argument',
    'assess the hierarchy/naturalness needed if Mstar is far below MP',
    'derive cubic interactions and the actual strong-coupling scale',
    'assess radiative stability and matter-sector Lorentz-violation constraints'
  ],
  'non_claims':[
    'not yet a full RTK nonlinear completion',
    'not an observational fit',
    'not a generic-background hyperbolicity theorem',
    'not a strong-coupling or loop-stability result',
    'not a UV-completion proof'
  ],
  'branches':branches
}
print('RTK_ROUTE_B_BPS_EXACT_RATIONAL_EMBEDDING_PASS',json.dumps(out,sort_keys=True))
