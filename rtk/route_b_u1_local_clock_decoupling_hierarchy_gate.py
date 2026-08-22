#!/usr/bin/env python3
"""C8 scoped local-clock hierarchy gate for the fixed U(1)+RTK scalar action.

For the reconstructed P(X_U) clock, the homogeneous quadratic kinetic/stiffness
normalization obeys exactly

    K_phys = 2 M_Pl^2 M_K^2.

A local weak-field spatial gravitational operator is of order M_Pl^2 k^2.
Thus the dimensionless hierarchy comparing the P(X) background stiffness to a
local spatial-gradient operator is

    epsilon_clock(k) = K_phys/(M_Pl^2 k^2) = 2 (M_K/k)^2.

This is a scale-separation theorem only. It does NOT by itself prove that every
1PN PPN coefficient receives a correction exactly equal to epsilon_clock; the
full O(v^4) source/constraint system is still required for beta_PPN and the
moving-source system for alpha_1, alpha_2.
"""
import json, math

MK0=1.1681315109161161 # Mpc^-1, Actions run 32568333920
RUN_ID=32568333920
ARTIFACT_ID=9474667297
DIGEST='sha256:7337f02e8f217e22decf8b425e87e9f730cb3189fa1baad981c8b5ae566f74e8'
MPC_M=3.085677581491367e22
AU_M=1.495978707e11
RSUN_M=6.957e8

scales={
  'solar_radius':RSUN_M/MPC_M,
  '1_AU':AU_M/MPC_M,
  '100_AU':100*AU_M/MPC_M,
  '1_pc':1e-6,
  '1_kpc':1e-3,
}
rows={}
for name,L in scales.items():
    k=1.0/L
    eps=2.0*(MK0/k)**2
    rows[name]={'L_Mpc':L,'k_Mpc_inv':k,'M_K_over_k':MK0/k,'epsilon_clock_2MK2_over_k2':eps}
    assert math.isfinite(eps) and eps>0

# Explicit local-solar-system hierarchy requirements.
assert rows['solar_radius']['epsilon_clock_2MK2_over_k2'] < 1e-20
assert rows['1_AU']['epsilon_clock_2MK2_over_k2'] < 1e-20
assert rows['100_AU']['epsilon_clock_2MK2_over_k2'] < 1e-15
assert rows['1_pc']['epsilon_clock_2MK2_over_k2'] < 1e-10

out={
 'classification':'RTK_ROUTE_B_U1_LOCAL_CLOCK_DECOUPLING_HIERARCHY_PASS',
 'scale_dictionary_provenance':{'run_id':RUN_ID,'artifact_id':ARTIFACT_ID,'artifact_digest':DIGEST,'M_K_z0_Mpc_inv':MK0,'M_K_inverse_Mpc':1.0/MK0},
 'exact_input_identity':'K_phys=2 M_Pl^2 M_K^2',
 'hierarchy_definition':'epsilon_clock=K_phys/(M_Pl^2 k^2)=2(M_K/k)^2',
 'rows':rows,
 'result':'At Solar-System and parsec spatial scales the reconstructed P(X_U) background stiffness is parametrically tiny compared with the local M_Pl^2 k^2 spatial operator; the hierarchy becomes cosmologically relevant only toward k~M_K.',
 'interpretation':'This provides quantitative scale separation supporting a controlled local-clock expansion around the static U1 solution.',
 'non_claims':[
   'does not set beta_PPN=1 by itself',
   'does not compute alpha_1 or alpha_2 for moving sources',
   'does not replace the exact static acceleration identity C(X)(D Theta)^2=M_Pl^2 a_i a^i',
   'does not address X_U->0 compact-object configurations, radiative protection, or the EFT cutoff'
 ],
 'next_gate':'derive the complete O(v^4) static source/constraint equations for the fixed scalar action, retaining the P(X_U) stress terms through the first nonvanishing order, and solve for beta_PPN; then treat moving-source preferred-frame parameters separately'
}
open('u1_local_clock_decoupling_hierarchy_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
