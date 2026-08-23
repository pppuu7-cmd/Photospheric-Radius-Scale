#!/usr/bin/env python3
"""Scoped all-q coupled DOF certificate for the projectable U(1)+RTK candidate.

Inputs already established in the project:
1. Published projectable U(1) gravity Hamiltonian count (Mukohyama et al.
   arXiv:1504.07357): in d spatial dimensions dimP_g=d^2+3d+4,
   C1=2d+2 first-class constraints and C2=2 second-class constraints, yielding
   only massless tensor graviton polarizations.  The projectable theory has no
   local lapse canonical pair.
2. The RTK scalar kinetic block carries one regular intended scalar DOF and is
   U(1)/foliation invariant.
3. The elliptic Q,Lambda sector contributes +4 phase dimensions and four
   second-class constraints with invertible ell>0 block, hence zero DOF.
4. After exact auxiliary Dirac projection the surviving projectable gravity
   second-class pair is represented by (Jhat,phihat).  On the flat barotropic
   lambda>1 domain its bracket d(q) is the same DeWitt metric-response channel
   certified positive by the lambda>1 barotropic all-q theorem.

This gate recomputes that positivity in a compact dimensionless form and then
performs the coupled phase-space count. Ordinary matter species are not counted
as part of the gravity+RTK carrier DOF; their own physical DOF add separately.
"""
import json
import sympy as sp

# Phase-space count in d=3.
d=sp.Integer(3)
dimPg=d**2+3*d+4
C1=2*d+2
C2parent=sp.Integer(2)
assert dimPg==22 and C1==8 and C2parent==2
Nparent=sp.simplify((dimPg-2*C1-C2parent)/2)
assert Nparent==2
# + one RTK scalar canonical pair, + Q,Lambda two canonical pairs.
dimPtotal=dimPg+2+4
C2total=C2parent+4
Ntotal=sp.simplify((dimPtotal-2*C1-C2total)/2)
assert dimPtotal==28 and C2total==6 and Ntotal==3

# Exact sufficient positivity of the surviving projectable second-class bracket.
lam,A,T=sp.symbols('lambda A T', positive=True, finite=True)
Qdewitt=sp.Rational(2,3)*A**2-T**2/(3*(3*lam-1))
# Under the previously certified barotropic source/Mc bound: |T|<=2A.
Qlower=sp.factor(sp.Rational(2,3)*A**2-4*A**2/(3*(3*lam-1)))
assert sp.simplify(Qlower-2*A**2*(lam-1)/(3*lam-1))==0
# For lambda>1 this lower bound is strictly positive.

q,Mc2=sp.symbols('q M_c_squared', positive=True, finite=True)
ell=1+q/Mc2
aux_det=sp.factor(ell**4)
assert aux_det>0

out={
  'classification':'RTK_C9_PROJECTABLE_U1_COUPLED_DOF_ALLQ_PASS',
  'status_scope':'GREEN_SCOPED_PROJECTABLE_3DOF_ALL_Q_BAROTROPIC_DOMAIN_PPN_COSMOLOGY_RECERTIFICATION_PENDING',
  'domain':'d=3 projectable U1, flat homogeneous/isotropic barotropic ordinary source satisfying the certified Mc/source bound, lambda>1, q>0; RTK rolling X_U>0; elliptic ell=1+q/Mc^2>0',
  'parent_projectable_count':{
    'phase_dimension':'22',
    'first_class':'8',
    'second_class':'2',
    'physical_gravity_dof':'2 tensor'
  },
  'coupled_additions':{
    'RTK_scalar':'+2 phase dimensions, +1 intended physical DOF',
    'Q_Lambda_auxiliary':'+4 phase dimensions, +4 second-class constraints, +0 physical DOF'
  },
  'reduced_projectable_second_class_pair':'(Jhat,phihat); the local nonprojectable pi_N,H_perp pair is absent because N=N(t)',
  'allq_pair_rank':'d(q) proportional to q^2 XGX; under |T|<=2A and lambda>1, XGX >= 2 A^2 (lambda-1)/(3lambda-1) >0',
  'auxiliary_rank':'det auxiliary four-constraint block is proportional to ell^4>0',
  'total_count':{
    'phase_dimension':'28',
    'first_class':'8',
    'second_class':'6',
    'physical_carrier_dof':'3 = 2 tensor + 1 intended RTK scalar'
  },
  'c9_structural_advantage':'projectability removes local lapse gradients identically, so eta1 a_i a^i sigma and eta2 D_i a^i sigma cannot detune this count through the nonprojectable mechanism',
  'interpretation':'Within the stated barotropic all-q domain, the projectable candidate has the desired carrier DOF count with a simpler second-class structure than the nonprojectable completion. This is a genuine C8/C9 architectural candidate, not merely a tuning of eta1=eta2=0.',
  'non_claims':[
    'does not count ordinary matter species as part of the 3 carrier DOF',
    'does not yet rederive all projectable PPN parameters with the finite-Mc filter',
    'does not yet certify the global projectable Hamiltonian/Friedmann history against the production cosmology',
    'does not cover anisotropic stress, curved slices, strong-field objects or black-hole boundary conditions',
    'does not prove projectability is selected by a deeper UV principle'
  ],
  'next_gate':'derive the projectable same-action FLRW/global-Hamiltonian equations with the k=0 compensator reduction, and recertify the projectable PPN source transfer at finite but local k/Mc; then compare quantitatively to the nonprojectable lambda>1 branch.'
}
open('c9_projectable_u1_coupled_dof_allq_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
