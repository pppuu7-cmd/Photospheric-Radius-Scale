#!/usr/bin/env python3
"""Scoped no-go for the naive velocity-dependent sigma*F(X_U) compensator.

External Hamiltonian input (Mukohyama, Namba, Saitou, Watanabe,
arXiv:1504.07357): on the exceptional nonprojectable local-U(1) surface
eta1=eta2=0, pure gravity has the primary constraint

    pi_nu + J_A ~= 0,

because J_A is independent of velocities.  Its preservation supplies the
secondary phi_A.  Together (pi_N, J_A, H_perp, phi_A) are four second-class
constraints, and this is exactly what removes the scalar graviton.  With only
two second-class constraints the scalar graviton is present.

The first RTK FLRW-source escape candidate was

    Delta L = -sqrt(g) (A-Acal) F(X_U),

with F=rho_comp and, on a homogeneous zero-gradient slice,

    A-Acal = A + dot(nu),
    X_U = dot(Sigma)^2/(2 N^2).

Because F_X != 0 on the rolling production branch, the coefficient of dot(nu)
is velocity dependent.  The (dot(nu),dot(Sigma)) Hessian has nonzero
determinant, so pi_nu+J_A+F cannot remain a primary constraint.  U(1) gauge
symmetry itself survives (separate gauge-pair theorem), but the *additional*
primary degeneracy responsible for phi_A and the fourth second-class constraint
is lost.

This rejects only the naive sigma F(X_U) implementation.  It motivates an
auxiliary/degenerate implementation in which the coefficient of sigma is an
independent non-velocity variable off shell and is constrained to track X_U.
"""

import json
import sympy as sp

N, vnu, vS, A = sp.symbols('N v_nu v_Sigma A', nonzero=True, finite=True, real=True)
J0, m = sp.symbols('J0 m', finite=True, real=True, nonzero=True)
X = vS**2/(2*N**2)
F = sp.Function('F')
B = A + vnu

# Minimal local velocity model: regular intended scalar kinetic term plus the
# gravity/matter A-source coefficient J0 and the new clock-dependent source.
L = sp.Rational(1,2)*m*vS**2 - B*(J0 + F(X))

pnu = sp.diff(L, vnu)
pS = sp.diff(L, vS)
Hvv = sp.hessian(L, (vnu, vS))
detH = sp.factor(Hvv.det())

Y = sp.symbols('Y', positive=True, finite=True, real=True)
FY = sp.Function('F')(Y)
FX = sp.diff(FY,Y).subs(Y,X)
expected_det = -vS**2*FX**2/N**4
assert sp.simplify(detH-expected_det)==0

# Pure-gravity/velocity-independent limit F_X=0 is degenerate and has a
# velocity-independent p_nu relation.  Rolling clock F_X !=0 is regular.
assert sp.simplify(sp.diff(pnu,vS) + vS*FX/N**2)==0

# The actual reconstructed rho_comp is state dependent on the production
# branch: x(u)=(u-1)/sqrt(1-lambda(u-1)^2), u=sqrt(X/Xstar).
u,lam,Xstar=sp.symbols('u lambda_D X_star', positive=True, finite=True, real=True)
x_u=(u-1)/sp.sqrt(1-lam*(u-1)**2)
dx_du=sp.simplify(sp.diff(x_u,u))
du_dX=1/(2*Xstar*u)
dx_dX=sp.simplify(dx_du*du_dX)
assert dx_dX != 0

# Constraint-count comparison in d spatial dimensions.
d=sp.symbols('d', integer=True, positive=True)
dimP_gravity=d**2+3*d+6
dimP_with_sigma=dimP_gravity+2
C1=2*d+2
C2_special=4
C2_lost_degeneracy=2
Ndof_special_plus_sigma=sp.simplify((dimP_with_sigma-2*C1-C2_special)/2)
Ndof_lost=sp.simplify((dimP_with_sigma-2*C1-C2_lost_degeneracy)/2)
assert Ndof_special_plus_sigma.subs(d,3)==3
assert Ndof_lost.subs(d,3)==4

out={
  'classification':'RTK_ROUTE_B_U1_CLOCK_COMPENSATOR_PRIMARY_CONSTRAINT_LOSS',
  'status_scope':'BLACK_SCOPED_NAIVE_SIGMA_FX_COMPENSATOR_EXTRA_SCALAR_GENERIC_ROLLING_BRANCH',
  'candidate':'Delta L=-sigma rho_comp(X_U)',
  'external_hamiltonian_anchor':'arXiv:1504.07357 Eqs.(23),(48)-(50),(64)-(69): eta1=eta2=0 needs four second-class constraints; pi_nu+J_A is primary and its preservation supplies phi_A',
  'exact_local_velocity_result':{
    'p_nu':'-(J0+F(X_U))',
    'd_pnu_d_dotSigma':'-dot(Sigma) F_X/N^2',
    'velocity_hessian_det':'-dot(Sigma)^2 F_X^2/N^4',
    'rolling_condition':'dot(Sigma)!=0 and F_X!=0 -> nonzero determinant'
  },
  'constraint_consequence':'The velocity-independent primary pi_nu+J_A≈0 of the exceptional gravity branch is lifted. The U1 gauge pair survives, but the separate degeneracy chain that generated phi_A is not inherited.',
  'generic_count_if_no_accidental_new_constraints':{
    'phase_space_dimension':'d^2+3d+8 (gravity plus one Sigma pair)',
    'first_class':'2d+2',
    'second_class':'2 rather than 4 after loss of the exceptional nu-primary chain',
    'd3_dof':4,
    'content':'2 tensors + intended RTK/DBI scalar + restored gravity scalar'
  },
  'comparison':{
    'velocity_independent_sigma_coefficient':'preserves pi_nu+J_A-type primary degeneracy',
    'velocity_dependent_F_X_nonzero':'lifts that primary degeneracy on a regular rolling branch'
  },
  'non_claims':[
    'not a no-go for all A-source compensators',
    'not a no-go for auxiliary/degenerate implementations that keep the sigma coefficient velocity-independent off shell',
    'not a statement about the X_U=0 boundary',
    'not a radiative or PPN conclusion'
  ],
  'next_gate':'replace F(X_U) in the coefficient of sigma by an independent auxiliary state y with no velocity, impose y=f(X_U) through a separate constrained/degenerate sector, and perform an exact primary/secondary constraint count. Require preservation of the pi_nu+J_A+F(y) primary and removal of all auxiliary pairs without adding physical DOF.'
}
open('u1_clock_compensator_primary_constraint_loss_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
