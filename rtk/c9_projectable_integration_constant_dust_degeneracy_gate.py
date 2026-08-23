#!/usr/bin/env python3
"""Background identifiability gate for the projectable Hamiltonian integration constant.

In projectable Hořava gravity the local integrated Friedmann equation may contain
an integration-constant contribution rho_int=C_int/a^3.  The RTK large-lambda_D
tail and ordinary cold matter are also dust-like at the background level.
This gate proves the exact amplitude degeneracy of such a^-3 components and
records the condition needed before the projectable C9 escape can be promoted.
"""
import json
import sympy as sp

a,K,Dc,Dr,Di=sp.symbols('a K D_cdm D_rtk_tail D_int', positive=True, finite=True)
Hdust=sp.factor(K*(Dc+Dr+Di)/a**3)
J=sp.Matrix([[sp.diff(Hdust,x) for x in (Dc,Dr,Di)]])
assert J.rank()==1
# Two independent null directions leave every pure-background dust contribution unchanged.
v1=sp.Matrix([1,-1,0]); v2=sp.Matrix([1,0,-1])
assert (J*v1)[0]==0 and (J*v2)[0]==0

# RTK-tail/integration-constant two-amplitude subproblem.
J2=sp.Matrix([[sp.diff(Hdust,x) for x in (Dr,Di)]])
assert J2.rank()==1
assert (J2*sp.Matrix([1,-1]))[0]==0

out={
  'classification':'RTK_C9_PROJECTABLE_INTEGRATION_CONSTANT_DUST_DEGENERACY_PASS',
  'status_scope':'YELLOW_EXACT_BACKGROUND_DEGENERACY_PROJECTABLE_INITIAL_GLOBAL_CONDITION_OR_PERTURBATION_DISCRIMINANT_REQUIRED',
  'projectable_term':'rho_int=C_int/a^3 from the locally integrated projectable Friedmann equation when the global Hamiltonian constraint is not imposed pointwise',
  'background_dust_sum':'rho_dust=(D_cdm+D_rtk_tail+D_int)/a^3',
  'background_jacobian_rank':'1 for three dust amplitudes; there are two exact amplitude-null directions',
  'rtk_tail_vs_integration_constant':'The two-amplitude Jacobian has rank 1 with null direction delta D_rtk_tail=-delta D_int. Pure background observables cannot separate them when the RTK sector is in its exact dust tail.',
  'existing_B10_context':'The preregistered nonprojectable/production B10 analysis already found finite lambda_D not numerically identifiable from the tested dust-like tail at raw-objective resolution 0.005; an unconstrained projectable dust integration constant therefore creates an additional identifiability burden rather than resolving B10.',
  'allowed_resolution_routes':[
    'derive from the global state/boundary conditions that C_int=0 for the production cosmology and keep that condition fixed before fitting',
    'retain C_int as a physical parameter and use perturbations/non-background observables to seek a discriminant from RTK/CDM',
    'reinterpret the observed dust sector as a constrained combination and relinquish separate RTK dust-amplitude identifiability'
  ],
  'non_claims':[
    'does not prove C_int must be nonzero',
    'does not prove perturbations of integration-constant dark matter are identical to RTK or particle CDM',
    'does not invalidate the globally homogeneous branch where the global Hamiltonian condition can set the integration constant consistently',
    'does not reopen the already closed B10 protocol v1; this is a new projectable-architecture gate'
  ],
  'next_gate':'derive the projectable linear perturbation equations for the integration-constant mode and RTK scalar on the same action; test whether growth/lensing distinguishes them. In parallel define the global boundary/initial-condition principle required for a frozen C_int=0 branch.'
}
open('c9_projectable_integration_constant_dust_degeneracy_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
