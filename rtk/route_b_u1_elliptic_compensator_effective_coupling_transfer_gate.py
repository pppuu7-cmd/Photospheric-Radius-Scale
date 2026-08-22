#!/usr/bin/env python3
"""Exact reduced effective-coupling transfer gate for the frozen elliptic U(1) compensator.

Algebraically eliminate the nondynamical auxiliary pair on its second-class
branch:
  Q=H0/ell,
  Lambda=-(A-Acal)/ell,
  ell=1+k_phys^2/M_c^2.

The matter+auxiliary Hamiltonian then reduces to
  H_red = N H0 - a1_eff(k) (A-Acal) H0 + shift,
with
  a1_eff = 1-1/ell = k_phys^2/(M_c^2+k_phys^2).

This gives an exact scale transfer: a1_eff(0)=0 (background A-source rescue),
while a1_eff -> 1 at high k (recovery of the published local family-I a1=1
matter coupling).  No value of M_c is selected here.
"""
import json
import sympy as sp

k,Mc,H0,N,A,Acal=sp.symbols('k M_c H0 N A Acal', positive=True, finite=True)
y=sp.symbols('y', nonnegative=True, finite=True)
ell=1+k**2/Mc**2
Q=H0/ell
Lam=-(A-Acal)/ell
Hm=N*H0-(A-Acal)*H0
Haux=(A-Acal)*Q+Lam*(ell*Q-H0)
Hred=sp.factor(Hm+Haux)
aeff=sp.factor(1-1/ell)
assert sp.simplify(aeff-k**2/(Mc**2+k**2))==0
assert sp.simplify(Hred-(N*H0-aeff*(A-Acal)*H0))==0
JAred=sp.simplify(sp.diff(Hred,A))
assert sp.simplify(JAred+aeff*H0)==0
assert sp.simplify(aeff.subs(k,0))==0
assert sp.simplify(sp.limit(aeff,k,sp.oo)-1)==0
assert sp.simplify(aeff.subs(k,Mc)-sp.Rational(1,2))==0

# Dimensionless transfer and monotonicity.
aeff_y=sp.factor(y/(1+y))
comp_y=sp.factor(1/(1+y))
assert sp.simplify(aeff_y+comp_y-1)==0
assert sp.simplify(sp.diff(aeff_y,y)-1/(1+y)**2)==0

# Exact 1% window conditions. Low-k source fraction <=1%, high-k source
# recovery >=99%.
eps=sp.Rational(1,100)
y_low_max=sp.simplify(eps/(1-eps))      # 1/99
y_high_min=sp.simplify((1-eps)/eps)     # 99
assert y_low_max==sp.Rational(1,99)
assert y_high_min==sp.Integer(99)
ratio_needed=sp.simplify(sp.sqrt(y_high_min/y_low_max))
assert ratio_needed==sp.Integer(99)

out={
  'classification':'RTK_ROUTE_B_U1_ELLIPTIC_COMPENSATOR_EFFECTIVE_COUPLING_TRANSFER_PASS',
  'status_scope':'GREEN_EXACT_SCALE_TRANSFER_NO_PARAMETER_FIT_FULL_DIRAC_AND_OBSERVABLES_PENDING',
  'frozen_parent':'research/RTK_U1_ELLIPTIC_MATTER_COMPENSATOR_CANONICAL_v1.json',
  'auxiliary_branch':{
    'Q':'H0/ell',
    'Lambda':'-(A-Acal)/ell',
    'ell':'1+k_phys^2/M_c^2'
  },
  'reduced_hamiltonian':'H_red=N H0-a1_eff(k)(A-Acal)H0+shift',
  'effective_family_I_coupling':'a1_eff(k)=k_phys^2/(M_c^2+k_phys^2)',
  'source':'J_A_red=-a1_eff H0',
  'exact_limits':{
    'k=0':'a1_eff=0',
    'k=M_c':'a1_eff=1/2',
    'k>>M_c':'a1_eff->1'
  },
  'transfer_properties':{
    'compensation_fraction':'1-a1_eff=1/(1+k_phys^2/M_c^2)',
    'monotonicity':'d a1_eff/d(k^2/M_c^2)=1/(1+k^2/M_c^2)^2 > 0',
    'boundedness':'0 <= a1_eff < 1 for finite k and M_c>0'
  },
  'one_percent_scale_separation':{
    'cosmological_rescue':'a1_eff(k_cos)<=0.01 -> M_c>=sqrt(99) k_cos',
    'local_family_I_recovery':'a1_eff(k_local)>=0.99 -> M_c<=k_local/sqrt(99)',
    'window_exists_iff':'k_local/k_cos>=99'
  },
  'interpretation':'After exact elimination of the nondynamical auxiliary pair, the construction is equivalent at source level to a monotone scale-dependent family-I coupling: zero on the homogeneous mode and asymptotically the published a1=1 coupling locally. This sharpens the intended scale-separation mechanism without choosing M_c.',
  'non_claims':[
    'integrating out Q,Lambda is not a substitute for proving the unreduced full Dirac rank',
    'does not establish that cosmological perturbation data tolerate the intermediate transition',
    'does not establish PPN, equivalence-principle, radiative-stability, cutoff or compact-object bounds',
    'does not choose or fit M_c'
  ],
  'next_gate':'after full coupled Dirac rank passes, confront a1_eff(k) with cosmological perturbation and local/PPN scales and fit or exclude an allowed M_c interval.'
}
with open('u1_elliptic_compensator_effective_coupling_transfer_result.json','w') as f:
    json.dump(out,f,indent=2,sort_keys=True); f.write('\n')
print(out['classification'],json.dumps(out,sort_keys=True))
