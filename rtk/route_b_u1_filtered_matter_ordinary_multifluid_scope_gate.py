#!/usr/bin/env python3
"""Ordinary-matter source scope and multifluid rank bound for the frozen compensator.

Frozen candidate RTK_U1_ELLIPTIC_MATTER_COMPENSATOR_CANONICAL_v1 defines

  ordinary_matter_H = [N-(A-Acal)] H0 + (N^i+N D^i nu) H_i

while the RTK scalar is separately retained as its existing neutral
P(X_U)+C(X_U) action. Therefore H0 in the elliptic constraint L Q=H0 is the
ordinary universally-coupled matter generator, not the neutral RTK scalar
Hamiltonian and not, by default, a gravity-potential cosmological term.

For independent ordinary matter sectors s,
  H0=sum_s H0_s,
  tau_H=sum_s tau_H_s.
For isotropic perfect-fluid species,
  tau_H_s/sqrt(g)=-(d/2)p_s.
Hence
  rho_H-tau_rho=sum_s [rho_s+(d/2)p_s].
The conservative flat-FLRW leading rank condition is

  M_c^2 > 2 |sum_s(rho_s+d p_s/2)|/[|eta0|(d-1)M_Pl^2].

For d=3, eta0=1:
  M_c^2 > |sum_s(rho_s+3 p_s/2)|/M_Pl^2.
Dust contributes rho; radiation contributes 3 rho/2; a massive species uses
its actual time-dependent rho+3p/2 rather than a hard-coded w=0 or 1/3.
"""
import json
import sympy as sp

# Symbolic three-species linearity check with arbitrary equations of state.
d,eta,Mpl2=sp.symbols('d eta0 M_Pl_squared', positive=True, finite=True)
r1,r2,r3=sp.symbols('rho1 rho2 rho3', positive=True, finite=True)
w1,w2,w3=sp.symbols('w1 w2 w3', real=True, finite=True)
rs=[r1,r2,r3]; ws=[w1,w2,w3]
trace_sum=sp.expand(sum(r*(1+d*w/2) for r,w in zip(rs,ws)))
component_sum=sp.expand(sum(r+d*(w*r)/2 for r,w in zip(rs,ws)))
assert sp.simplify(trace_sum-component_sum)==0

# d=3 special contribution weights.
d3=sp.Integer(3)
dust=sp.simplify(1+d3*0/2)
rad=sp.simplify(1+d3*sp.Rational(1,3)/2)
vac=sp.simplify(1+d3*(-1)/2)
assert dust==1
assert rad==sp.Rational(3,2)
assert vac==-sp.Rational(1,2)

out={
  'classification':'RTK_ROUTE_B_U1_FILTERED_MATTER_ORDINARY_MULTIFLUID_SCOPE_PASS',
  'status_scope':'GREEN_FROZEN_H0_SCOPE_AND_MULTIFLUID_LINEARITY_BACKGROUND_SOURCE_AUDIT_PENDING',
  'frozen_candidate_scope':{
    'included':'H0 is the ordinary universally coupled matter Hamiltonian generator appearing in [N-(A-Acal)]H0',
    'excluded_by_architecture':'the neutral RTK scalar is retained as a separate P(X_U)+C(X_U) sector and is not automatically part of H0',
    'gravity_vacuum_note':'a cosmological term in the gravity potential L_V is not automatically part of H0; include vacuum energy only if it is explicitly represented as an ordinary matter sector in the same action'
  },
  'linearity':'rho_H-tau_rho=sum_s[rho_s+(d/2)p_s] for independent isotropic ordinary-matter sectors',
  'multifluid_rank_bound':'M_c^2 > 2|sum_s(rho_s+d p_s/2)|/[|eta0|(d-1)M_Pl^2]',
  'd3_eta0_1_bound':'M_c^2 > |sum_s(rho_s+3 p_s/2)|/M_Pl^2',
  'd3_weights':{'dust_w0':'1*rho','radiation_w1over3':'(3/2)*rho','vacuum_wminus1':'-(1/2)*rho if and only if vacuum energy is explicitly in ordinary H0'},
  'massive_species_rule':'use the actual rho_s(a)+3 p_s(a)/2 contribution; do not hard-code a dust or radiation limit through the relativistic transition',
  'interpretation':'The low-k rank bound couples only to the ordinary-matter source actually filtered by the frozen elliptic architecture. This prevents double-counting the neutral RTK scalar or a gravity-potential cosmological constant when estimating the rank scale.',
  'non_claims':['does not yet map the production CLASS species one-by-one into the future U(1) completed action','does not choose M_c','does not assume vacuum energy belongs to H0','does not certify subleading/intermediate-k rank'],
  'next_gate':'construct a source-composition dictionary for baryons, CDM, photons and neutrinos in the intended completed cosmology; retain massive-neutrino rho(a),p(a) symbolically unless a production background is explicitly frozen.'
}
with open('u1_filtered_matter_ordinary_multifluid_scope_result.json','w') as f:
    json.dump(out,f,indent=2,sort_keys=True); f.write('\n')
print(out['classification'],json.dumps(out,sort_keys=True))
