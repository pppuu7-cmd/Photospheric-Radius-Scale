#!/usr/bin/env python3
"""Full finite-k scalar-constraint gate on the exact local U(1)+RTK rest vacuum.

The gate combines the standard nonprojectable U(1) flat-background multiplier
structure with the already frozen RTK scalar action.  It is scoped to k>0,
Lambda_g=0, nu=0 gauge, lambda_HL=1 and the exact PPN rest point X=X_star.
"""
import json
import sympy as sp

TARGET='research/theory_targets/RTK_C8_U1_LOCAL_REST_FULL_SCALAR_CONSTRAINT_TARGET_v1.json'
PRINC='research/theory_results/RTK_C8_U1_LOCAL_REST_SCALAR_PRINCIPAL_RESULT_v1.json'
IR='research/RTK_C8_U1_FIXED_IR_REPRESENTATIVE_v3.json'
SC='research/RTK_C8_U1_FIXED_SCALAR_ACTION_v1.json'
t=json.load(open(TARGET)); p=json.load(open(PRINC)); ir=json.load(open(IR)); sc=json.load(open(SC))
assert t['classification']=='RTK_C8_U1_LOCAL_REST_FULL_SCALAR_CONSTRAINT_TARGET_V1_FROZEN'
assert p['classification']=='RTK_C8_U1_LOCAL_REST_SCALAR_SPATIAL_PRINCIPAL_DEGENERACY_EXACT_PASS'
g=ir['gravity_and_matter_frame']
assert g['lambda_HL']==1 and g['gamma1']==-1 and g['beta0_bare']==0
assert g['sigma1']==0 and g['sigma2']==0
assert sc['mixed_operator']['C']=='M_Pl^2/(2 X_U)'

# Plane-wave finite-k scalar algebra.  Variables: zeta, scalar shift B, lapse n,
# U(1) multiplier A, RTK perturbation phi.  k>0 and mu^2>0.
k,mu=sp.symbols('k mu', positive=True, finite=True, real=True)
zeta,B,n,dphi,A=sp.symbols('zeta B n dphi A', finite=True, real=True)

# Flat 3-curvature at linear scalar order for g_ij=(1+2 zeta)delta_ij:
# delta R^(3) = -4 Delta zeta -> +4 k^2 zeta in Fourier convention.
dR=4*k**2*zeta
# The frozen RTK scalar action has no direct A dependence, so A equation is dR=0.
sol_z=sp.solve(sp.Eq(dR,0),zeta)
assert sol_z==[0]

# With zeta=0 and N_i=partial_i B, K_ij=-partial_i partial_j B.
# For one Fourier scalar mode, KijKij=k^4 B^2 and K^2=k^4 B^2.
Kij2=k**4*B**2
K2=k**4*B**2
Lshift=sp.simplify(Kij2-g['lambda_HL']*K2)
assert Lshift==0

# Exact quadratic RTK scalar+lapse kernel at X=X_star.
chi=dphi-n
Lrtk=sp.expand((mu**2+k**2)*chi**2)
# No remaining pure-gravity lapse quadratic term exists on the zeta=0 flat branch
# for beta0_bare=0, Lambda_g=0 and nu=0.
eq_n=sp.factor(sp.diff(Lrtk,n))
assert sp.factor(eq_n + 2*(mu**2+k**2)*chi)==0
sol_n=sp.solve(sp.Eq(eq_n,0),n)
assert sol_n==[dphi]
Lred=sp.simplify(Lrtk.subs(n,dphi))
assert Lred==0
# phi equation is redundant once the lapse constraint holds.
eq_phi_momentum=sp.factor(sp.diff(Lrtk,dphi))
assert sp.simplify(eq_phi_momentum.subs(n,dphi))==0

out={
  'classification':'RTK_C8_U1_LOCAL_REST_FULL_SCALAR_QUADRATIC_RANK_ENHANCEMENT_EXACT_PASS',
  'status':'NO_FINITE_K_INTENDED_RTK_SCALAR_QUADRATIC_PROPAGATOR_ON_EXACT_LOCAL_REST_BRANCH_AT_TWO_DERIVATIVE_LEVEL',
  'target':TARGET,
  'prerequisite':PRINC,
  'external_structure':'standard nonprojectable U(1) flat-branch A multiplier equation R^(3)-2 Lambda_g=0 in vacuum; same action family used in the frozen PPN/DOF gates',
  'frozen_conditions':{
    'k':'k>0',
    'Lambda_g':0,
    'U1_gauge':'nu=0',
    'lambda_HL':1,
    'beta0_bare':0,
    'sigma1_sigma2':'0,0',
    'RTK_A_source':'zero by explicit fixed scalar action',
    'X_U':'X_star>0 local rest point'
  },
  'constraint_chain':{
    'A_equation':'delta R^(3)=4 k^2 zeta=0 -> zeta=0 for k>0',
    'scalar_shift_gravity':'KijKij-K^2 = k^4 B^2-k^4 B^2=0 at lambda_HL=1 after zeta=0',
    'RTK_quadratic_with_lapse':'L2/M_Pl^2=(mu_K^2+k^2)[dot(phi)-n]^2',
    'lapse_equation':'dot(phi)-n=0 since mu_K^2+k^2>0',
    'reduced_quadratic_action':'0 for the finite-k RTK scalar perturbation'
  },
  'interpretation':'The exact local rest point is a quadratic constraint-rank-enhanced surface relative to the rolling cosmological branch: after the U1 and lapse constraints are imposed, the intended finite-k RTK scalar has no quadratic propagator at the two-derivative level. This is a strong-coupling/constraint-bifurcation warning, not yet a numerical cutoff or a proof of pathology.',
  'relation_to_prior_DOF':'The prior 3-DOF classical certification was explicitly on a regular phase-space slice with X_U>0 and nonzero canonical scalar momentum/rolling branch. The exact local rest point has P_X=0 and is therefore a special rank surface; the two statements are not contradictory.',
  'non_claims':[
    'does not say the cosmological rolling branch lacks the intended scalar mode',
    'does not prove a ghost or exponential instability',
    'does not assign a physical strong-coupling energy scale',
    'does not decide whether nonlinear interactions make the local mode strongly coupled or whether an additional constraint removes it nonlinearly',
    'does not include higher-spatial UV operators',
    'does not cover k=0, rotation/nonzero invariant shift, X_U->0 or the DBI boundary'
  ],
  'next_gate':'derive the first nonvanishing fully constrained nonlinear local-rest scalar action (cubic/quartic) and its constraint rank; in parallel freeze a minimal higher-spatial completion basis and test whether it restores a controlled local quadratic mode without spoiling the cosmological RTK kernel, TT c_T=1, PPN quartet or classical rolling-branch DOF.'
}
open('u1_local_rest_full_scalar_constraint_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
