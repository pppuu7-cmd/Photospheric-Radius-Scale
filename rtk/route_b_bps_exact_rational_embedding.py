#!/usr/bin/env python3
"""Route-B constructive theorem inside the BPS healthy nonprojectable Horava class.

Primary source: Blas, Pujolas, Sibiryakov, arXiv:1007.3503, Eqs. (5.1)-(5.8).
Their scalar quadratic action after integrating nondynamical fields has

  omega^2 = [(lambda-1)/(2(3lambda-1))] * P(-p^2/Muv^2)/Q(-p^2/Muv^2) * p^2,

where Muv denotes the independent higher-spatial-derivative scale M_* of the
source paper, not the Planck mass.  The polynomials are
  P(x)=(g2^2-g1*g3)x^4 -(g1*f3+g3*f1-2*g2*f2)x^3
      +(f2^2-4*g2-f1*f3-2*g3-g1*alpha)x^2
      -(2*f3+f1*alpha+4*f2)x +(4-2*alpha),
  Q(x)=g3*x^2+f3*x+alpha.

This script proves an explicit continuous parameter family for which the ratio
is exactly proportional to 1/(1+p^2/Mdisp^2), while the source-paper scalar
quadratic stability conditions are satisfied for every p>=0.

Scope: exact Minkowski scalar pole/dispersion embedding in the BPS healthy
extension.  This is not yet a full RTK cosmological mapping, off-shell
propagator/source mapping, generic-background DOF proof, phenomenology fit,
strong-coupling calculation, or radiative-stability result.
"""
import json
import sympy as sp

# Positive unconstrained parameters. The substitutions enforce 0<alpha<2,
# f3<0 and lambda>1 algebraically.
z,s,ell,u,x,Muv=sp.symbols('z s ell u x Muv', positive=True, finite=True, real=True)
alpha=sp.simplify(2*z/(1+z))
f3=-s
lam=1+ell
sqrt_disc=sp.simplify(2/sp.sqrt(1+z))
g1=g2=g3=sp.Integer(0)

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
    ratio=sp.simplify((-2+sign*sqrt_disc)/alpha)
    f2=sp.simplify(ratio*f3)
    f1=sp.simplify(f2**2/f3)
    P,Q=polys(f1,f2)
    P_expected=sp.simplify(4-2*alpha)
    assert sp.simplify(P-P_expected)==0
    assert sp.Poly(P,x).degree()==0
    assert sp.simplify(Q-(alpha+f3*x))==0

    P_phys=sp.simplify(P.subs(x,-u))
    Q_phys=sp.simplify(Q.subs(x,-u))
    target_ratio=sp.simplify((P_expected/alpha)/(1+(s/alpha)*u))
    assert sp.simplify(P_phys/Q_phys-target_ratio)==0
    assert sp.simplify(Q_phys-(alpha+s*u))==0

    kinetic_sign_ratio=sp.simplify((3*lam-1)/(lam-1))
    omega_prefactor=sp.simplify((lam-1)/(2*(3*lam-1)))
    cs2=sp.factor(omega_prefactor*(P_expected/alpha))
    cs2_expected=sp.simplify(ell/(z*(2+3*ell)))
    assert sp.simplify(cs2-cs2_expected)==0

    # The physical rational-pole scale follows from the independent source
    # higher-derivative scale M_*: Mdisp^2=alpha Muv^2/s.
    Mdisp2=sp.simplify(alpha*Muv**2/s)
    p2=sp.symbols('p2', nonnegative=True, finite=True, real=True)
    u_phys=sp.simplify(p2/Muv**2)
    dispersion=sp.simplify(omega_prefactor*(P_phys/Q_phys).subs(u,u_phys)*p2)
    target_dispersion=sp.simplify(cs2*p2/(1+p2/Mdisp2))
    assert sp.simplify(dispersion-target_dispersion)==0

    branches.append({
      'sign':sign,'f2_over_f3':sp.sstr(ratio),'f2':sp.sstr(f2),'f1':sp.sstr(f1),
      'P':sp.sstr(P),'Q':sp.sstr(Q),'kinetic_sign_ratio':sp.sstr(kinetic_sign_ratio),
      'cs2':sp.sstr(cs2),'Mdisp2':sp.sstr(Mdisp2),
    })

assert sp.simplify(4-2*alpha-4/(1+z))==0
assert sp.simplify((3*lam-1)/(lam-1)-(2+3*ell)/ell)==0

out={
  'classification':'RTK_ROUTE_B_BPS_EXACT_RATIONAL_EMBEDDING_PASS',
  'primary_source':'Blas-Pujolas-Sibiryakov arXiv:1007.3503 Eqs. (5.1)-(5.8)',
  'higher_derivative_scale_semantics':'Muv is source-paper M_* and is independent of Planck mass',
  'source_polynomial_degree':{'P':4,'Q':2},
  'constructive_family':{
    'free_positive_parameters':['z','s','ell','Muv'],
    'alpha':'2 z/(1+z) in (0,2)','lambda':'1+ell > 1','f3':'-s < 0',
    'g1=g2=g3':0,'two_f2_over_f3_branches':'(-2 +/- 2/sqrt(1+z))/alpha','f1':'f2^2/f3'
  },
  'exact_reduced_polynomials':{
    'P':'4-2 alpha = 4/(1+z)','Q':'alpha+f3*x',
    'Q_physical':'Q(-p^2/Muv^2)=alpha+s p^2/Muv^2 > 0'
  },
  'exact_dispersion':{
    'form':'omega^2 = cs^2 p^2/(1+p^2/Mdisp^2)',
    'cs2':'ell/[z(2+3ell)] > 0','Mdisp2':'alpha Muv^2/s > 0'
  },
  'source_paper_stability_conditions':{
    'ghost_ratio':'(3lambda-1)/(lambda-1)=(2+3ell)/ell > 0',
    'gradient_ratio':'P(x)/Q(x)>0 for x<0 because P>0 and Q(-u)>0','alpha_interval':'0<alpha<2 by construction'
  },
  'theorem':'The healthy nonprojectable Horava quadratic scalar sector contains a continuous two-branch coefficient family whose exact pole/dispersion is the RTK target rational mixed-kinetic form, while satisfying the BPS Minkowski scalar ghost/gradient stability conditions.',
  'relation_to_previous_nogo':'This broader higher-spatial-operator BPS class is outside the previously excluded constant-ci c4=2 khronometric subspace.',
  'next_required_proofs':[
    'off-shell field/source/observable mapping between BPS scalar and intended RTK Khronon sector',
    'full nonlinear constraint and physical-DOF count for the selected family',
    'FLRW and generic smooth-background scalar/tensor stability',
    'map Mdisp and Muv to the RTK phenomenological scale and assess hierarchy/naturalness',
    'specialize cubic/strong-coupling analysis to the selected family',
    'radiative stability and matter-sector Lorentz-violation constraints'
  ],
  'non_claims':['not yet a full RTK nonlinear completion','not an observational fit','not a generic-background hyperbolicity theorem','not a strong-coupling or loop-stability result','not a UV-completion proof'],
  'branches':branches
}
print('RTK_ROUTE_B_BPS_EXACT_RATIONAL_EMBEDDING_PASS',json.dumps(out,sort_keys=True))
