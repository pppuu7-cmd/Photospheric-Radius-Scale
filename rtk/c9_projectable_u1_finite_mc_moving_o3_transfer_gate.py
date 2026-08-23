#!/usr/bin/env python3
"""Finite-Mc projectable O(3) moving-source transfer after exact auxiliary reduction.

Scope: projectable U(1), Minkowski/solar-system PN patch, phi=0 gauge, parent
metric branch a1=1,a2=0,g1=-1, regular lambda_HL != 1, and a spatial Fourier
mode for which the elliptic filter f=k^2/(M_c^2+k^2) is time-independent to the
PN order considered.

Primary parent equations are Lin-Mukohyama-Wang-Zhu arXiv:1310.6666,
Sec. VI: momentum constraint Eq.(6.13), dynamical/A constraints Eqs.(6.14,6.15),
and prepotential constraint Eq.(6.16).  For a2=0 the specialized momentum
relation is unambiguous:
  gamma+2d-lambda(3gamma+2d-4kappa)-2kappa=0,
and c=-4kappa.

Our reduced matter+auxiliary Hamiltonian has coefficient
  (A-Acal)(Q-H0) = -f (A-Acal) H0.
Thus J_A is filtered by f.  In the prepotential source, the density/time part
coming from Acal is also filtered by f, while the ordinary momentum-divergence
term from N D^i nu H_i is not.  Continuity gives
  f rho_dot + div(rho v) = (f-1) rho_dot.
Therefore the parent RHS 2 kappa(a1-1) in Eq.(6.16) becomes 2 kappa(f-1),
while its geometric LHS retains the physical-metric a1=1,a2=0 coefficients.

This gate determines alpha1 and the O(3) combination alpha2-zeta1+2xi. It does
NOT split alpha2 from zeta1,xi; that requires the O(4) system.
"""
import json
import sympy as sp

f,lam=sp.symbols('f lambda_HL', positive=True, finite=True)
d,c,kappa,gamma=sp.symbols('d c kappa gamma', real=True, finite=True)
# Certified O(2): gamma=1 and 1=kappa*f.
vals={gamma:sp.Integer(1),kappa:1/f}

# Projectable O(3) momentum equation specialized to a2=0.
Emom=sp.expand(gamma+2*d-lam*(3*gamma+2*d-4*kappa)-2*kappa)
d_mom=sp.factor(sp.solve(sp.Eq(Emom.subs(vals),0),d)[0])

# Filtered prepotential equation.
Ephi=sp.expand((1-lam)*(3*gamma+2*d-4*kappa)-2*kappa*(f-1))
d_phi=sp.factor(sp.solve(sp.Eq(Ephi.subs(vals),0),d)[0])
assert sp.simplify(d_mom-d_phi)==0

d_exact=sp.factor(d_mom)
# c=-4kappa from the transverse/vector part of the parent momentum constraint.
c_exact=-4/f

# With chi_,0i=V_i-W_i, h0i=(c+d)V_i-d W_i.  Compare to the standard PPN
# metric (5.22):
# V coefficient = -1/2(3+4gamma+alpha1-alpha2+zeta1-2xi)
# W coefficient = -1/2(1+alpha2-zeta1+2xi).
# Eliminating the second combination gives alpha1=-4-4gamma-2c.
alpha1=sp.factor(-4-4*sp.Integer(1)-2*c_exact)
combo=sp.factor(2*d_exact-1) # alpha2-zeta1+2xi
assert sp.simplify(alpha1-8*(1/f-1))==0
assert sp.simplify(combo-2*(1-f)*(2*lam-1)/(f*(lam-1)))==0

# Replace f=q/(M2+q): the deviations are exactly proportional to M2/q.
q,M2=sp.symbols('q M_c_squared', positive=True, finite=True)
fq=q/(M2+q)
alpha1_q=sp.factor(alpha1.subs(f,fq))
combo_q=sp.factor(combo.subs(f,fq))
assert sp.simplify(alpha1_q-8*M2/q)==0
assert sp.simplify(combo_q-2*M2*(2*lam-1)/(q*(lam-1)))==0

# Parent limit.
assert sp.simplify(alpha1.subs(f,1))==0
assert sp.simpl(combo.subs(f,1))==0
assert sp.simplify(d_exact.subs(f,1)-sp.Rational(1,2))==0

out={
  'classification':'RTK_C9_PROJECTABLE_U1_FINITE_MC_MOVING_O3_TRANSFER_PASS',
  'status_scope':'GREEN_O3_ALPHA1_AND_PREFERRED_FRAME_COMBINATION_O4_SPLIT_PENDING',
  'domain':'projectable U1 PN patch; a1=1,a2=0,g1=-1; regular lambda_HL!=1; fixed spatial Fourier mode; exact Q,Lambda reduction; continuity; no incoming RTK scalar source beyond the filtered matter response',
  'filter':'f(k)=k^2/(M_c^2+k^2)',
  'source_transfer':{
    'A_source':'J_A is multiplied by f relative to the parent a1=1 source',
    'prepotential_density_part':'rho_dot term is multiplied by f because it comes from Acal',
    'prepotential_momentum_part':'div(rho v) is unfiltered because it comes from the ordinary N D^i nu H_i term',
    'continuity_result':'f rho_dot + div(rho v)=(f-1) rho_dot'
  },
  'O2_inputs':['gamma_PPN=1','kappa=G/G_N(k)=1/f'],
  'constraint_consistency':{
    'd_from_momentum':str(d_mom),
    'd_from_filtered_prepotential':str(d_phi),
    'result':'identical exactly'
  },
  'shift_coefficients':{'c':'-4/f','d':str(d_exact)},
  'O3_results':{
    'alpha1':'8(1/f-1)=8 M_c^2/k^2',
    'alpha2_minus_zeta1_plus_2xi':'2(1-f)(2lambda_HL-1)/[f(lambda_HL-1)] = 2 M_c^2(2lambda_HL-1)/[k^2(lambda_HL-1)]'
  },
  'near_GR_lambda_warning':'For fixed finite M_c/k, the second O3 PPN combination is enhanced as 1/(lambda_HL-1) when lambda_HL approaches 1 from above. This must be combined with the cosmological G_cos/G_N bound before choosing lambda_HL.',
  'parent_limit':'f->1 gives c=-4,d=1/2,alpha1=0 and alpha2-zeta1+2xi=0',
  'non_claims':[
    'does not claim alpha2 separately because zeta1 and xi are only split by the O4/full PPN system',
    'does not yet include finite-size source form factors or a distribution of Fourier modes',
    'does not identify k with one universal Solar-System scale',
    'does not prove the O4 beta,zeta,xi sector remains GR-like',
    'does not set M_c or lambda_HL'
  ],
  'next_gate':'derive the finite-Mc projectable A-constraint plus trace-dynamical equations at O4, including metric variation of the elliptic filter, to split alpha2,zeta1,xi and determine beta; then combine the resulting experimental tolerances with the cosmological lambda window.'
}
open('c9_projectable_u1_finite_mc_moving_o3_transfer_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
