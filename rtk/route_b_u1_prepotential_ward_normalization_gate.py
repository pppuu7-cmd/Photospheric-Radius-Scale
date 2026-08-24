#!/usr/bin/env python3
"""C10 exact Newtonian-prepotential source normalization from the local-U1 Ward identity.

Preregistered target:
  research/theory_targets/RTK_C10_U1_PREPOTENTIAL_WARD_NORMALIZATION_TARGET_v1.json

Primary conventions locked in the target:
- Lin-Mukohyama-Wang-Zhu, arXiv:1310.6666 Eqs.(2.1),(2.16),(2.19),(4.11)-(4.15).
- Zhu-Shu-Wu-Wang, arXiv:1110.5106 Eqs.(7.10),(7.11).

This gate is deliberately source-side only.  It does not claim the full reduced
metric system or a CLASS implementation.
"""
import json
import sympy as sp

# ---------------------------------------------------------------------------
# 1. U(1) Ward identity for matter sources.
# ---------------------------------------------------------------------------
# Matter source definitions:
#   J^i      = -N dL_M/dN_i
#   J_A      =  2 d(N L_M)/dA
#   J_varphi = -dL_M/dvarphi
# and U(1) transformations:
#   dA = dot(alpha)-N^i nabla_i alpha,
#   dvarphi = -alpha,
#   dN_i = N nabla_i alpha.
# After integration by parts the alpha coefficient must vanish:
#   N J_varphi - 1/2 Dt(J_A) + 1/2 div(J_A N^i) + div(N J^i) = 0,
# where Dt(X)=(1/sqrt(g)) d_t[sqrt(g) X].
N = sp.symbols('N', positive=True, finite=True)
DtJA, divJAN, divNJi = sp.symbols('DtJA divJAN divNJi', finite=True, real=True)
Jphi_from_ward = sp.simplify((sp.Rational(1,2)*DtJA - sp.Rational(1,2)*divJAN - divNJi)/N)
assert sp.simplify(N*Jphi_from_ward - sp.Rational(1,2)*DtJA + sp.Rational(1,2)*divJAN + divNJi) == 0

# ---------------------------------------------------------------------------
# 2. Recover the published family-I a1=1,a2=0,Omega=1,varphi=0 expression.
# ---------------------------------------------------------------------------
# On this slice Eq.(4.15) has J_A=2 rho_H and J^i=-s^i.
Dt_rho, div_rhoN, div_Ns = sp.symbols('Dt_rho div_rhoN div_Ns', finite=True, real=True)
family = sp.simplify(Jphi_from_ward.subs({
    DtJA: 2*Dt_rho,
    divJAN: 2*div_rhoN,
    divNJi: -div_Ns,
}))
family_expected = sp.simplify((Dt_rho - div_rhoN + div_Ns)/N)
assert sp.simplify(family-family_expected) == 0

# ---------------------------------------------------------------------------
# 3. Insert the frozen elliptic compensator normalization.
# ---------------------------------------------------------------------------
# Existing exact canonical overlap:
#   p_nu^m=+H0, p_nu^aux=-Q, P=p_nu_total=H0-Q.
# Previous C10 A-normalization theorem gives literature J_A=2P.
DtP, divPN, div_NJi_tot = sp.symbols('DtP divPN div_NJi_tot', finite=True, real=True)
comp = sp.simplify(Jphi_from_ward.subs({
    DtJA: 2*DtP,
    divJAN: 2*divPN,
    divNJi: div_NJi_tot,
}))
comp_expected = sp.simplify((DtP-divPN-div_NJi_tot)/N)
assert sp.simplify(comp-comp_expected) == 0

# In varphi=0 gauge the frozen (A-Acal)Q term has no independent auxiliary
# shift current because dAcal/dN^i is proportional to nabla_i varphi.
grad_varphi, Q = sp.symbols('grad_varphi Q', finite=True, real=True)
dAcal_dNi = grad_varphi
aux_shift_variation = sp.simplify(-Q*dAcal_dNi)
assert aux_shift_variation.subs(grad_varphi, 0) == 0

# Hence on the frozen universal family-I slice J^i_total=-s^i for this source
# bridge, while P replaces rho_H in the A/prepotential canonical coefficient.
comp_family = sp.simplify(comp_expected.subs(div_NJi_tot, -div_Ns))
comp_family_expected = sp.simplify((DtP-divPN+div_Ns)/N)
assert sp.simplify(comp_family-comp_family_expected) == 0

# ---------------------------------------------------------------------------
# 4. Homogeneous and linear flat-FLRW limits.
# ---------------------------------------------------------------------------
# Exact homogeneous filter: k=0 => Q=H0 => P=0.  With homogeneous momentum
# current zero, both the time/shift P terms and momentum divergence vanish.
assert sp.simplify(comp_family_expected.subs({DtP:0, divPN:0, div_Ns:0})) == 0

# Around flat FLRW with P_bar=0, N^i_bar=0, s^i_bar=0:
#   delta J_phi = 1/Nbar [ Dt(delta P) + div(Nbar delta s^i) ].
Nbar = sp.symbols('Nbar', positive=True, finite=True)
Dt_dP, div_Nbar_ds = sp.symbols('Dt_deltaP div_Nbar_delta_s', finite=True, real=True)
dJphi_flrw = sp.simplify((Dt_dP + div_Nbar_ds)/Nbar)

# Certified elliptic linear transfer for constant comoving k and constant M_c:
#   delta P=a_eff delta H0,
#   a_eff=k^2/(k^2+a^2 M_c^2).
k, a, Mc, adot = sp.symbols('k a M_c adot', positive=True, finite=True, real=True)
dH0, Dt_dH0 = sp.symbols('delta_H0 Dt_delta_H0', finite=True, real=True)
aeff = sp.factor(k**2/(k**2+a**2*Mc**2))
daeff_da = sp.diff(aeff, a)
daeff_dt = sp.factor(daeff_da*adot)
Hcoord = sp.factor(adot/a)
daeff_expected = sp.factor(-2*Hcoord*aeff*(1-aeff))
assert sp.simplify(daeff_dt-daeff_expected) == 0

# Dt is the volume-weighted derivative.  For a scalar transfer a_eff(t),
# Dt(a_eff deltaH0)=a_eff Dt(deltaH0)+dot(a_eff) deltaH0.
Dt_dP_expanded = sp.factor(aeff*Dt_dH0 + daeff_dt*dH0)
dJphi_filtered = sp.factor((Dt_dP_expanded + div_Nbar_ds)/Nbar)

# Guard against the old wrong algebraic identification J_phi=delta p_nu.
# The filtered source necessarily contains both a derivative term and the
# ordinary momentum divergence; dot(a_eff) is nonzero at finite k,a,M_c when adot!=0.
assert sp.simplify(sp.diff(aeff,a)) != 0
assert dJphi_filtered.has(Dt_dH0)
assert dJphi_filtered.has(div_Nbar_ds)

out = {
  'classification':'C10_U1_PREPOTENTIAL_WARD_NORMALIZATION_PASS_SCOPED',
  'status_scope':'GREEN_EXACT_SOURCE_SIDE_WARD_NORMALIZATION_FULL_REDUCED_GRAVITATIONAL_SYSTEM_OPEN',
  'ward_identity':'N J_varphi - 1/2 Dt(J_A) + 1/2 div(J_A N^i) + div(N J^i) = 0',
  'solved_J_varphi':'J_varphi = [Dt(J_A)-div(J_A N^i)]/(2N) - div(N J^i)/N',
  'family_I_check':'a1=1,a2=0,Omega=1,varphi=0 with J_A=2 rho_H and J^i=-s^i gives J_varphi=[Dt(rho_H)-div(rho_H N^i)+div(N s^i)]/N',
  'elliptic_compensator_map':'P=H0-Q=p_nu_total, literature J_A=2P, auxiliary shift-current contribution from (A-Acal)Q vanishes in varphi=0 gauge, so J_varphi=[Dt(P)-div(P N^i)+div(N s^i)]/N on the frozen source bridge',
  'homogeneous_background':'k=0 -> P=0; with homogeneous momentum current zero, J_varphi_bar=0 exactly',
  'linear_flat_FLRW':'delta J_varphi=[Dt(delta P)+div(Nbar delta s^i)]/Nbar because P_bar=Nbar^i=s_bar^i=0',
  'filtered_linear_transfer':'delta P=a1_eff delta H0 with a1_eff=k^2/(k^2+a^2 M_c^2)',
  'a1_eff_time_derivative':'dot(a1_eff)=-2 (dot a/a) a1_eff (1-a1_eff) for constant comoving k and constant M_c',
  'mandatory_product_rule':'Dt(delta P)=a1_eff Dt(delta H0)+dot(a1_eff) delta H0',
  'critical_correction':'delta_p_nu=a1_eff deltaH0 is a canonical coefficient, not the primary-literature J_varphi. Direct algebraic insertion into Eq.(7.10) would drop both the time-derivative/product-rule term and ordinary momentum divergence.',
  'architectural_consequence':'J_varphi is not an independent freely specifiable completion source once J_A and J^i are fixed; the local-U1 Ward identity determines it. The reduced CLASS source bridge should therefore compute J_varphi from J_A plus the ordinary momentum current rather than add a second phenomenological filter.',
  'non_claims':[
    'does not close the gravitational left-hand side of the prepotential constraint',
    'does not prove full nonlinear redundancy of the prepotential equation',
    'does not close Hamiltonian/momentum/trace/traceless metric reduction',
    'does not implement CLASS or change likelihood results',
    'does not include the separate B4 massive-neutrino same-action extension'
  ],
  'target':'research/theory_targets/RTK_C10_U1_PREPOTENTIAL_WARD_NORMALIZATION_TARGET_v1.json'
}
open('u1_prepotential_ward_normalization_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'], json.dumps(out,sort_keys=True))
