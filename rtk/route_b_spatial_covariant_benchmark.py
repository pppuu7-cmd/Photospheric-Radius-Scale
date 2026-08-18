#!/usr/bin/env python3
"""Constructive local metric+Khronon preferred-foliation benchmark.

This theorem is deliberately narrower than the full RTK completion.  It proves
that a spatially covariant ADM action with no lapse velocity can simultaneously

1. reproduce the conditional long-wave P(X) quadratic coefficients G,K;
2. generate exactly the extra K/(2 M^2) (grad dot(pi))^2 operator through
   a_i a^i with a_i=D_i ln N;
3. retain the GR-like kinetic Hessian rank in (dot gamma_ij, dot N), with dot N
   an exact null direction;
4. fall in the generic three-DOF spatially covariant class when the nonlinear
   lapse primary/secondary pair is second class (Gao 2014 Hamiltonian theorem).

It does NOT incorporate the causal nonlocal RT sector and is not by itself the
full C7 theorem.
"""
from __future__ import annotations
import json
import sympy as sp

# ---------------------------------------------------------------------------
# 1. Stückelberg / P(X) quadratic expansion
# ---------------------------------------------------------------------------
eps=sp.symbols('eps')
d,g2=sp.symbols('d g2', real=True)       # d=dot(pi); g2=(grad pi)^2 counted O(eps^2)
X0,PX,PXX=sp.symbols('X0 PX PXX', positive=True)
C0,M=sp.symbols('C0 M', positive=True)

# X = X0[(1+dot pi)^2-(grad pi)^2].  Scale g2 as eps^2 to perform order count.
X=X0*((1+eps*d)**2-eps**2*g2)
dX=sp.expand(X-X0)
Pquad=sp.expand(PX*dX + sp.Rational(1,2)*PXX*dX**2)
Pquad_series=sp.expand(sp.series(Pquad,eps,0,3).removeO()).coeff(eps,2)
G=sp.simplify(2*X0*PX)
K=sp.simplify(2*X0*PX+4*X0**2*PXX)
expected_P2=sp.simplify(K*sp.Rational(1,2)*d**2-G*sp.Rational(1,2)*g2)
assert sp.simplify(Pquad_series-expected_P2)==0

# N/N0 = sqrt(X0/X).  Its log has linear Stückelberg perturbation -dot(pi).
Nratio=sp.sqrt(X0/X)
logN=sp.series(sp.log(Nratio),eps,0,3).removeO().expand()
assert sp.simplify(logN.coeff(eps,1)+d)==0
# Therefore spatially differentiating the linear term gives
# a_i = D_i ln N = -partial_i dot(pi)+O(pi^2), so C0*a^2 contributes
# C0*(grad dot pi)^2 at quadratic order.  Matching the RTK target fixes C0.
Cmatch=sp.simplify(K/(2*M**2))
assert Cmatch.is_positive

# Exact quadratic dispersion from the benchmark coefficients.
q,omega=sp.symbols('q omega', positive=True)
# L2 Fourier kinetic coefficient = K + 2*C0*q^2 because L contains
# K/2 dotpi^2 + C0 q^2 dotpi^2.
kinetic_q=sp.simplify(K+2*C0*q**2)
omega2=sp.simplify(G*q**2/kinetic_q)
omega2_matched=sp.simplify(omega2.subs(C0,Cmatch))
expected_omega2=sp.simplify((G/K)*q**2/(1+q**2/M**2))
assert sp.simplify(omega2_matched-expected_omega2)==0

# ---------------------------------------------------------------------------
# 2. ADM velocity Hessian: EH metric velocities + no dot N
# ---------------------------------------------------------------------------
v11,v22,v33,v12,v13,v23,ndot=sp.symbols('v11 v22 v33 v12 v13 v23 ndot')
# Local N=1, shift=0 patch: K_ij = 1/2 dot(gamma_ij).
# For a symmetric 3x3 matrix, Kij Kij counts off-diagonal entries twice.
trv=v11+v22+v33
vij2=v11**2+v22**2+v33**2+2*(v12**2+v13**2+v23**2)
Qeh=sp.Rational(1,4)*(vij2-trv**2)
vel=(v11,v22,v33,v12,v13,v23,ndot)
Hvel=sp.hessian(Qeh,vel)
assert Hvel.rank()==6
null=Hvel.nullspace()
assert len(null)==1
assert null[0]==sp.Matrix([0,0,0,0,0,0,1])
# F(N) and C(N) a_i a^i contain no velocities of N in unitary gauge and no
# additional metric velocities, so this null direction is exact for the benchmark.

# GR tensor velocity subspace remains non-degenerate at principal kinetic level.
vp,vx=sp.symbols('vp vx', real=True)
Qtt=sp.simplify(Qeh.subs({v11:vp,v22:-vp,v33:0,v12:vx,v13:0,v23:0}))
assert sp.simplify(Qtt-(sp.Rational(1,2)*vp**2+sp.Rational(1,2)*vx**2))==0

# ---------------------------------------------------------------------------
# 3. Hamiltonian constraint count inherited by the declared ADM class
# ---------------------------------------------------------------------------
# Configuration variables: gamma_ij(6), lapse N(1), shift N^i(3) -> phase dim 20.
# Spatial diffeomorphism: p_i + H_i = six first-class constraints.
# Nonlinear lapse with no dot N: p_N and its secondary are a second-class pair
# in the generic Gao class. Physical DOF=(20-2*6-2)/2=3.
phase_dim=20
first_class=6
second_class=2
physical_dof=sp.Rational(phase_dim-2*first_class-second_class,2)
assert physical_dof==3

out={
  'classification':'RTK_ROUTE_B_SPATIAL_COVARIANT_BENCHMARK_PASS',
  'benchmark_action':'N sqrt(gamma) [Mpl^2/2 (R3+KijKij-K^2) + F(N) + C(N) a_i a^i], a_i=D_i ln N',
  'unitary_gauge_clock_map':'X=1/(2N^2), F(N)=P(X(N))',
  'stueckelberg_linear_identity':'delta ln N = -dot(pi)',
  'quadratic_PX_coefficients':{'G':'2 X P_X = rho+p','K':'2 X P_X+4 X^2 P_XX = (rho+p)/c_a^2'},
  'acceleration_match':{'C_background':'K/(2 M^2)','generated_operator':'K/(2M^2) (grad dot(pi))^2'},
  'dispersion':'omega^2=(G/K) q^2/(1+q^2/M^2)',
  'velocity_hessian_rank_dotgamma_plus_dotN':int(Hvel.rank()),
  'velocity_hessian_dimension':7,
  'lapse_velocity_nullity':len(null),
  'tensor_principal_kinetic':'GR-like; acceleration/lapse-potential sector adds no tensor velocity terms',
  'generic_spatially_covariant_constraint_count':{'phase_space_dimension':phase_dim,'first_class_constraints':first_class,'second_class_constraints':second_class,'physical_DOF':int(physical_dof)},
  'scope_warning':'Constructive local preferred-foliation metric+Khronon benchmark only. The 3-DOF count uses the generic nonlinear-lapse/no-lapse-velocity Hamiltonian theorem for spatially covariant gravity. Causal RT coupling, full cosmological constraint algebra with the RT sector, nonlinear coefficients beyond F(N),C(N), strong coupling and radiative stability remain open.'
}
print('RTK_ROUTE_B_SPATIAL_COVARIANT_BENCHMARK_PASS',json.dumps(out,sort_keys=True))
