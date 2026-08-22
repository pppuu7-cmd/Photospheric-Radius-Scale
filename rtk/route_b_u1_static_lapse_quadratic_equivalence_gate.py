#!/usr/bin/env python3
"""C8 static weak-field bridge: explicit rolling S_mix versus beta0_eff=2.

On a static weak-field perturbation of the homogeneous rolling background,
write N=1+n and keep Sigma_bar=q t, shift/prepotential gradients zero in the
pure lapse channel. Then

  Theta_bar(n)=q/(1+n),
  N C (D Theta)^2 = C q^2 (D n)^2/(1+n)^3.

Exact RTK matching gives C q^2=M_Pl^2.

A Hořava acceleration term represented by beta0_eff=2 gives

  (M_Pl^2/2) beta0_eff N a_i a^i
    = M_Pl^2 (D n)^2/(1+n).

The two actions therefore coincide at quadratic weak-field order, which is the
order controlling linear static/Newtonian equations, but differ starting at
cubic action order.  The cubic difference contributes to O(4) / 1PN field
equations and forbids importing the published pure-U1 full PPN values as a
same-action certification.
"""
import json
import sympy as sp

n, Mpl2, X = sp.symbols('n Mpl2 X', finite=True, real=True)
# X denotes (D_i n)(D^i n), already quadratic in weak-field amplitude.
Lmix = Mpl2*X/(1+n)**3
Leff = Mpl2*X/(1+n)

# Expand only the algebraic n dependence. Since X=O(n^2), constant term is
# quadratic action, n*X cubic action, n^2*X quartic action.
smix=sp.series(Lmix,n,0,3).removeO().expand()
seff=sp.series(Leff,n,0,3).removeO().expand()
assert smix == Mpl2*X - 3*Mpl2*n*X + 6*Mpl2*n**2*X
assert seff == Mpl2*X - Mpl2*n*X + Mpl2*n**2*X

quad_mix=smix.coeff(n,0)
quad_eff=seff.coeff(n,0)
cubic_mix=smix.coeff(n,1)*n
cubic_eff=seff.coeff(n,1)*n
assert sp.simplify(quad_mix-quad_eff)==0
cubic_delta=sp.simplify(cubic_mix-cubic_eff)
assert cubic_delta == -2*Mpl2*n*X

# First variation of the quadratic functional has the same principal Laplace
# operator.  Track its coefficient abstractly: delta int A (Dn)^2 -> -2A Delta n.
A_mix=sp.simplify(quad_mix/X)
A_eff=sp.simplify(quad_eff/X)
lin_laplace_mix=-2*A_mix
lin_laplace_eff=-2*A_eff
assert sp.simplify(lin_laplace_mix-lin_laplace_eff)==0
assert lin_laplace_mix==-2*Mpl2

out={
  'classification':'RTK_ROUTE_B_U1_STATIC_LAPSE_QUADRATIC_EQUIVALENCE_PASS',
  'representative':'research/RTK_C8_U1_FIXED_IR_REPRESENTATIVE_v3.json',
  'static_channel_assumptions':['N=1+n','Sigma_bar=q t','D_i q=0','pure lapse channel','C q^2=M_Pl^2'],
  'explicit_Smix_lapse_density':'M_Pl^2 (D n)^2/(1+n)^3',
  'effective_beta0_2_density':'M_Pl^2 (D n)^2/(1+n)',
  'quadratic_action_match':str(quad_mix),
  'linear_laplace_coefficient':'-2 M_Pl^2 for both representations',
  'first_nonlinear_action_difference':str(cubic_delta),
  'weak_field_interpretation':'The explicit S_mix and beta0_eff=2 representations are identical in the pure-lapse quadratic action, so this channel has the same linear static/Newtonian principal operator. They differ at cubic action order, which feeds 1PN/O(4) equations.',
  'literature_bridge_scope':'Published pure-U1 family-I Newtonian/O(2) relations may be used only as a linear principal reference after checking the remaining A/metric/source equations; published full PPN values are not inherited.',
  'status_scope':'STATIC_LINEAR_PRINCIPAL_BRIDGE_GREEN_ONLY',
  'non_claims':[
    'does not by itself fix the measured Newton constant because the A constraint and physical matter metric source normalization must be included',
    'does not certify gamma_PPN until the full linear A/metric system is assembled',
    'does not certify beta_PPN or any complete 1PN parameter because the cubic actions differ',
    'does not cover time-dependent preferred-frame terms alpha1/alpha2',
    'does not establish radiative stability or EFT cutoff'
  ],
  'next_gate':'assemble the complete O(2) static scalar system for n, spatial curvature potential and U1 gauge field A on v3; verify the physical metric Newton normalization and gamma_PPN before proceeding to the O(4) cubic mismatch calculation for beta_PPN'
}
open('u1_static_lapse_quadratic_equivalence_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
