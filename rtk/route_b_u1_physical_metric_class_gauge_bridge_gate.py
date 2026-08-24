#!/usr/bin/env python3
"""C10 exact linear physical-metric map and CLASS gauge-bridge theorem."""
import json
from pathlib import Path
import sympy as sp

a=sp.symbols('a', positive=True, finite=True, real=True)
phi,dA,varphi,alpha=sp.symbols('phi deltaA delta_varphi alpha', finite=True, real=True)
B,E,Ls,Lsp=sp.symbols('B E L Lprime', finite=True, real=True)
Ep=sp.symbols('Eprime', finite=True, real=True)
Ahat,k,Lg=sp.symbols('Ahat k Lambda_g', finite=True, real=True)

# Frozen universal-matter slice a1=1,a2=0:
# tilde N = (1-sigma)N = N-(A-mathcalA); tilde N^i=N^i+N g^ij grad_j varphi; tilde gij=gij.
# At linear order on Nbar=a, gij=a^2 deltaij, the physical scalar shift is B+varphi/a.
Bphys=sp.expand(B+varphi/a)
# U1: delta N_i = N grad_i alpha => delta B=alpha/a; delta varphi=-alpha.
Bphys_u1=sp.expand((B+alpha/a)+(varphi-alpha)/a)
assert sp.simplify(Bphys_u1-Bphys)==0

# Allowed scalar spatial FDiff convention: E->E-L, Bphys->Bphys-L'.
# Hence physical shear Sigma=Bphys-E' is invariant.
Sigma=sp.expand(Bphys-Ep)
Sigma_spatial=sp.expand((Bphys-Lsp)-(Ep-Lsp))
assert sp.simplify(Sigma_spatial-Sigma)==0

# In quasilongitudinal U1 gauge E=0,varphi=0, physical shift is B.
assert sp.simplify(Bphys.subs(varphi,0)-B)==0

# Production-matching flat homogeneous branch: the background Ahat term in primary Eq.(6.10)
# is proportional to a*Ahat*(k/a^2-Lambda_g), so it vanishes for k=Lambda_g=0.
Ahat_background_term=sp.expand(a*Ahat*(k/a**2-Lg))
assert sp.simplify(Ahat_background_term.subs({k:0,Lg:0}))==0

# Choose the admissible Ahat=0 branch to keep physical conformal lapse equal to a.
# Then N=a(1+phi), A=deltaA and tildeN=N-A=a[1+Phi_matter].
Phi_matter=sp.expand(phi-dA/a)
Ntilde=sp.expand(a*(1+phi)-dA)
assert sp.simplify(Ntilde-a*(1+Phi_matter))==0
Psi_matter=sp.symbols('psi', finite=True, real=True)  # a2=0 => tilde gij=gij exactly

out={
  'classification':'C10_U1_PHYSICAL_METRIC_MAP_PASS_CLASS_NEWTONIAN_DIRECT_IDENTIFICATION_BLOCKED_SCOPED',
  'status_scope':'GREEN_PHYSICAL_METRIC_MAP_YELLOW_CLASS_GAUGE_BRIDGE_REQUIRED',
  'universal_matter_map_a1_1_a2_0':{
    'tilde_N':'N-A+mathcalA',
    'tilde_N_i_upper':'N^i+N g^ij nabla_j varphi',
    'tilde_g_ij':'g_ij'
  },
  'linear_physical_shift':'B_phys=B+delta_varphi/a',
  'u1_invariance_check':'delta B=alpha/a and delta varphi=-alpha => delta B_phys=0',
  'physical_shear':'Sigma_phys=B_phys-E_prime; invariant under allowed scalar spatial FDiff E->E-L, B_phys->B_phys-L_prime',
  'quasilongitudinal_gauge':'E=0 and delta_varphi=0 => B_phys=B; no remaining k>0 scalar gauge transformation may set B_phys=0 unless Sigma_phys vanishes dynamically',
  'background_Ahat_statement':'for flat k=0 and Lambda_g=0, the Ahat term a*Ahat*(k/a^2-Lambda_g) in the homogeneous dynamical equation vanishes. Ahat=0 is therefore an admissible production-matching branch choice, not a forced equation and not an additional U1 gauge fixing after varphi=0.',
  'production_matching_branch_physical_potentials':{
    'Phi_matter':'phi-deltaA/a',
    'Psi_matter':'psi',
    'B_matter':'B in quasilongitudinal gauge'
  },
  'class_bridge_conclusion':'Standard CLASS newtonian gauge assumes the physical scalar shift/shear has been gauged to zero. The completed preferred-foliation U1 system cannot be identified directly with CLASS newtonian phi/psi unless Sigma_phys=0 follows dynamically. A shear-aware or gauge-invariant Boltzmann bridge is mandatory otherwise.',
  'non_claims':[
    'not a no-go for CLASS or Boltzmann implementation',
    'not a claim that physical shear is observationally large',
    'not a completed photon/baryon hierarchy',
    'not a likelihood result',
    'not an exact k=0 perturbation gauge statement'
  ],
  'target':'research/theory_targets/RTK_C10_U1_PHYSICAL_METRIC_CLASS_GAUGE_BRIDGE_TARGET_v1.json'
}
Path('u1_physical_metric_class_gauge_bridge_result.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
