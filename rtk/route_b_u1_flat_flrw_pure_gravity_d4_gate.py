#!/usr/bin/env python3
"""Exact flat-FLRW q^2 coefficient of {J_A,phi_A} from published Eq. (58).

External Hamiltonian input: Mukohyama et al., arXiv:1504.07357 Eq. (58),
special eta1=eta2=0 branch. On a flat homogeneous background R_ij=0 and a
Fourier smearing mode with q=|k|^2,

 T^ij=(g^ij D^2-D^iD^j) -> -q g^ij+k^i k^j.

Contracting two T tensors with the inverse DeWitt metric
 G_ijkl=1/2(g_ik g_jl+g_il g_jk)-lambda/(d lambda-1) g_ij g_kl
fixes the exact q^2 kernel. This is a scoped low-k symbol theorem, not a full
field-theory rank proof.
"""
import json
import sympy as sp

d,lam,q,eta0,Mpl,sqrtg,N=sp.symbols('d lambda q eta0 M_Pl sqrtg N', finite=True)
# Projector invariants in d dimensions for T_ij=-q P^T_ij.
T2=sp.expand(q**2*(d-1))
trT=sp.expand(-q*(d-1))
contract=sp.factor(T2-lam/(d*lam-1)*trT**2)
expected=sp.factor(q**2*(d-1)*(lam-1)/(d*lam-1))
assert sp.simplify(contract-expected)==0

d4=sp.factor(eta0**2*Mpl**2*sqrtg*N*(d-1)*(lam-1)/(d*lam-1))
kernel=sp.factor(d4*q**2)
assert sp.simplify(kernel-eta0**2*Mpl**2*sqrtg*N*contract)==0
# In GR kinetic normalization lambda=1 this particular q^2 coefficient vanishes.
assert sp.simplify(d4.subs(lam,1))==0

out={
  'classification':'RTK_ROUTE_B_U1_FLAT_FLRW_PURE_GRAVITY_D4_PASS',
  'status_scope':'GREEN_EXACT_PURE_GRAVITY_D4_SYMBOL_A_SUBLEADING_AND_RTK_REMAINDER_PENDING',
  'external_input':'Mukohyama et al. arXiv:1504.07357 Eq. (58), eta1=eta2=0',
  'domain':'flat homogeneous spatial background, Fourier smearing q=|k|^2, d lambda != 1',
  'projector_invariants':{
    'TijTij':'q^2(d-1)',
    'trace_T':'-q(d-1)',
    'T_G_T':'q^2(d-1)(lambda-1)/(d lambda-1)'
  },
  'd_kernel':'{J_A,phi_A}=d4 q^2 with d4=eta0^2 M_Pl^2 sqrt(g) N (d-1)(lambda-1)/(d lambda-1)',
  'lambda_one':'d4=0 at lambda=1 for this Eq.(58) flat-background kernel',
  'interpretation':'The pure-gravity (2,2) cross-block remainder coefficient is fixed exactly on the flat-FLRW Fourier patch; it is not an unknown Wilson-coefficient contribution.',
  'non_claims':[
    'does not determine the lapse-potential contribution to a={pi_N,Hperp}',
    'does not bound neutral-RTK higher-order corrections',
    'does not include curved-background R_ij terms',
    'does not choose lambda, M_c, or any UV Wilson coefficient'
  ],
  'next_gate':'derive the flat-background a(q) symbol from the frozen lapse-gradient potential and separate its q and q^2 Wilson coefficients; combine with the neutral-RTK a-only remainder.'
}
open('u1_flat_flrw_pure_gravity_d4_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
