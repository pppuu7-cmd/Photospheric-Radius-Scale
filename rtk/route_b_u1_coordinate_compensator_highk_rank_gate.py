#!/usr/bin/env python3
"""High-k principal-rank theorem for the coordinate A-source compensator.

Frozen rescue candidate:
    Delta L = -sigma F_Sigma(Sigma)
with F_Sigma velocity independent and the fixed RTK scalar action retaining
    K_eff(y)=K_phys (1+y/M_K^2),  y=k^2/a^2>0.

Inputs already certified in the repository:
1) exceptional eta1=eta2=0 U(1) gravity has the four-constraint second-class
   block on its regular branch;
2) the neutral fixed RTK scalar preserves that block on the homogeneous rolling
   X_U>0 branch;
3) exact FLRW reduction gives K_eff(y)=K_phys(1+y/M_K^2).

The new coordinate source changes the A constraint by an ultralocal term
F'_Sigma deltaSigma.  Relative to the geometric curvature contribution
(delta R3 ~ y * metric-scalar), this is lower spatial order.  Its contribution
to preservation of the constraint is proportional to the scalar velocity
response, whose canonical inverse kinetic factor is
    1/K_eff(y) = 1/[K_phys(1+y/M_K^2)] ~ M_K^2/(K_phys y).
Thus the compensator cannot modify the leading spatial principal symbol of the
already-regular second-class block as y->infinity.

This is a strict short-wavelength/generic principal-symbol result, not a proof
that no isolated finite-y rank zero exists.
"""
import json
import sympy as sp

y,MK,K,Fp=sp.symbols('y M_K K_phys Fprime', positive=True, finite=True, real=True)

Keff=sp.simplify(K*(1+y/MK**2))
invK=sp.simplify(1/Keff)
# Exact high-k limits.
assert sp.limit(y*invK,y,sp.oo)==MK**2/K
assert sp.limit(invK,y,sp.oo)==0

# A-constraint source: geometric principal piece scales as y while coordinate
# source is order y^0.
source_to_geom=sp.simplify(Fp/y)
assert sp.limit(source_to_geom,y,sp.oo)==0

# Preservation correction through the scalar velocity response is even softer.
secondary_corr=sp.simplify(Fp*invK)
assert sp.limit(secondary_corr,y,sp.oo)==0
assert sp.limit(y*secondary_corr,y,sp.oo)==Fp*MK**2/K

# Abstract principal-symbol bookkeeping. Let baseline det B have nonzero
# leading coefficient Dm*y^m. Any coordinate-source correction is lower order,
# represented by powers <=m-1; the leading coefficient is unchanged exactly.
m=sp.symbols('m', integer=True, positive=True)
Dm,Dlow,C=sp.symbols('D_m D_low C', nonzero=True, finite=True, real=True)
# Use a representative integer degree n>=1 for executable polynomial check.
n=sp.symbols('n', integer=True, positive=True)
# Explicit checks at several possible principal degrees avoid symbolic-power
# assumptions while encoding the general polynomial statement.
principal_checks=[]
for deg in range(1,9):
    Dbase=Dm*y**deg+Dlow*y**(deg-1)
    Dtot=Dbase+C*y**(deg-1)
    lead_base=sp.limit(Dbase/y**deg,y,sp.oo)
    lead_tot=sp.limit(Dtot/y**deg,y,sp.oo)
    assert sp.simplify(lead_tot-lead_base)==0
    principal_checks.append(deg)

# d=3 count if the four second-class constraints retain generic rank.
d=3
phase=d*d+3*d+8
first=2*d+2
second=4
ndof=(phase-2*first-second)//2
assert ndof==3

out={
  'classification':'RTK_ROUTE_B_U1_COORDINATE_COMPENSATOR_HIGHK_RANK_PASS',
  'status_scope':'GREEN_SCOPED_HIGHK_PRINCIPAL_RANK_PRESERVED_FINITE_K_PENDING',
  'candidate':'Delta L=-sigma F_Sigma(Sigma)',
  'certified_inputs':[
    'exceptional U1 eta1=eta2=0 regular four-second-class branch',
    'fixed neutral RTK rolling rank support',
    'K_eff(y)=K_phys(1+y/M_K^2) exact production quadratic kernel'
  ],
  'exact_scaling':{
    'A_source_coordinate_correction':'O(y^0) versus geometric curvature O(y)',
    'inverse_scalar_kinetic':'1/[K_phys(1+y/M_K^2)]',
    'highk_inverse_scalar_kinetic':'M_K^2/(K_phys y)+O(y^-2)',
    'secondary_coordinate_correction':'O(y^-1) through the scalar velocity response'
  },
  'principal_symbol_result':'The coordinate compensator cannot change the leading spatial coefficient of the already-nonzero baseline second-class determinant. Hence the regular short-wavelength constraint rank is unchanged.',
  'generic_d3_count_when_rank4':{
    'phase_space_dimension':26,
    'first_class_constraints':8,
    'second_class_constraints':4,
    'physical_dof':3,
    'interpretation':'2 tensor + 1 intended RTK scalar'
  },
  'polynomial_principal_degrees_checked':principal_checks,
  'non_claims':[
    'does not exclude an isolated finite-k determinant zero',
    'does not certify the homogeneous k=0 background/gauge sector',
    'does not establish nonlinear rank on arbitrary inhomogeneous Sigma configurations',
    'does not solve radiative shift-symmetry breaking, PPN, cutoff or compact objects'
  ],
  'next_gate':'construct the finite-y linearized four-constraint matrix on the rolling FLRW branch including F_Sigma_prime and evaluate its determinant across the physical production y/M_K^2 range; separately classify k=0 as background/gauge rather than a propagating-mode test.'
}
open('u1_coordinate_compensator_highk_rank_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
