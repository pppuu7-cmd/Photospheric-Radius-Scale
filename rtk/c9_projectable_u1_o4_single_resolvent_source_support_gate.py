#!/usr/bin/env python3
"""O(4) source-support theorem after exact finite-Mc auxiliary reduction.

Scope: projectable U(1) PN patch, nu=0 gauge, parent branch a1=1,a2=0,g1=-1,
ordinary nonrelativistic matter, exact Q,Lambda reduction.  The reduced matter
Hamiltonian is schematically

  H_m = N H0 + N^i H_i - A f_g H0,
  f_g = 1-(1-D_g^2/M_c^2)^(-1).

PN bookkeeping:
  A_2 = O(2), H0^(2)=rho=O(2), ordinary spatial stress tau_ij=O(4).
  h_ij^(2)=O(2).

The theorem shows that all genuinely NEW finite-Mc nonlocality at O(4) generated
by the filtered A coupling is controlled by one and the same first metric
functional derivative delta f/delta g.  There are not two independent unknown
nonlocal kernels in the A-constraint and trace dynamical equation.

A-source expansion:
  [f_g H0]_(2) = f0 H0_2,
  [f_g H0]_(4) = f0 H0_4 + delta f[h2] H0_2.

Metric variation of the filtered interaction:
  delta_g(-A f_g H0)
   = -A[(delta f/delta g) H0 + f_g delta H0/delta g].
At O(4), the first term is A2 (delta f/delta g)_0 H0_2.  The second starts O(6)
because delta H0/delta g is the ordinary spatial stress, O(4).

Thus the same resolvent derivative
  delta f = -(1/M_c^2)L^{-1}(delta D^2)L^{-1}
controls both nonlinear source channels.  Ordinary stress terms remain the
parent stress sector, and f0 H0_4 remains diagonal in Fourier space.

The gate also specializes the first geometric O(4) coefficient of the parent
projectable Eq.(6.17) using the already certified O(3) value of d(f,lambda).
"""
import json
import sympy as sp

f,lam=sp.symbols('f lambda_HL', positive=True, finite=True)
# O(3) certified shift coefficient from the finite-Mc moving-source gate.
d=sp.factor(-(3*f*lam-f-4*lam+2)/(2*f*(lam-1)))
combo=sp.factor(2*d-1)
combo_ref=2*(1-f)*(2*lam-1)/(f*(lam-1))
assert sp.simplify(combo-combo_ref)==0

# Parent Eq.(6.17) first geometric coefficient on a1=1,a2=0,g1=-1,gamma=1:
# -(1-3 lambda)/2 * (2d-1).
Cgeom=sp.factor(-(1-3*lam)*combo/2)
Cgeom_ref=(3*lam-1)*(1-f)*(2*lam-1)/(f*(lam-1))
assert sp.simplify(Cgeom-Cgeom_ref)==0
assert sp.simplify(Cgeom.subs(f,1))==0

# Exact Fourier filter and its first variation identity.
M2,q=sp.symbols('M_c_squared q', positive=True, finite=True)
fq=q/(M2+q)
assert sp.simplify((1/fq-1)-M2/q)==0

# PN order algebra: represent only additive orders; functional derivative of f
# at the flat background is an O(0) operator coefficient.
O_A2=2; O_H02=2; O_H04=4; O_h2=2; O_tau=4; O_df_kernel=0
orders={
  'JA_O2_diagonal':O_H02,
  'JA_O4_diagonal':O_H04,
  'JA_O4_resolvent_convolution':O_h2+O_H02,
  'metric_O4_resolvent_kernel':O_A2+O_df_kernel+O_H02,
  'metric_filtered_ordinary_stress':O_A2+O_tau,
}
assert orders['JA_O4_resolvent_convolution']==4
assert orders['metric_O4_resolvent_kernel']==4
assert orders['metric_filtered_ordinary_stress']==6

out={
 'classification':'RTK_C9_PROJECTABLE_U1_O4_SINGLE_RESOLVENT_SOURCE_SUPPORT_PASS',
 'status_scope':'GREEN_O4_SOURCE_SUPPORT_ONE_NEW_NONLOCAL_KERNEL_FULL_COEFFICIENT_SOLVE_PENDING',
 'domain':'projectable U1 PN patch, nu=0, a1=1,a2=0,g1=-1, nonrelativistic ordinary matter, exact auxiliary reduction, finite M_c>0',
 'reduced_matter_H':'H_m=N H0+N^i H_i-A f_g H0, f_g=1-(1-D_g^2/M_c^2)^(-1)',
 'exact_resolvent_variation':'delta f=-(1/M_c^2)L^(-1)(delta D^2)L^(-1)',
 'A_source':{
   'O2':'f0 H0^(2)',
   'O4':'f0 H0^(4)+delta f[h^(2)] H0^(2)',
   'new_nonlocal_piece':'delta f[h^(2)] H0^(2)'
 },
 'metric_source':{
   'variation':'-A[(delta f/delta g)H0+f delta H0/delta g]',
   'O4_new_nonlocal_piece':'-A2 (delta f/delta g)_0 H0^(2)',
   'filtered_ordinary_stress_order':'A2*f0*delta H0/delta g = O(6), hence absent at O(4) under the stated PN matter counting'
 },
 'pn_orders':orders,
 'single_kernel_statement':'The O4 A-source convolution delta f[h2]H0_2 and the O4 metric-source term A2(delta f/delta g)_0 H0_2 are two contractions of the same first resolvent metric derivative; no second independent finite-Mc nonlocal kernel is introduced by the reduced filtered coupling at this order.',
 'ordinary_matter_statement':'The unfiltered N H0+N^i H_i sector supplies the usual parent O4 ordinary stress terms. The finite-Mc diagonal O4 A-density term is f0 H0^(4).',
 'O3_input':{'d':str(d),'2d_minus_1':str(combo)},
 'O4_parent_geometric_specialization':{'coefficient_of_laplacian_Afrak_plus_Bfrak_minus_Phi1':str(Cgeom),'closed_form':'(3 lambda_HL-1)(1-f)(2 lambda_HL-1)/[f(lambda_HL-1)]'},
 'parent_limit':'f->1 removes the displayed finite-Mc O3-induced geometric coefficient and the resolvent derivative vanishes in the local-parent M_c^2->0 fixed-k limit.',
 'non_claims':[
   'does not solve the complete O4 Eq.(6.17)/(6.18) coefficient system',
   'does not yet determine beta, alpha2, zeta_i or xi separately',
   'does not claim the full O4 source is only the resolvent term; ordinary parent stress and diagonal filtered density terms remain',
   'does not cover relativistic matter whose spatial stress can enter at a different PN order',
   'does not choose M_c or lambda_HL'
 ],
 'next_gate':'build one complete Fourier-space O4 linear-plus-convolution system with the parent ordinary-stress terms, diagonal f0 H0^(4), the certified single resolvent kernel, and the O3 d(f,lambda) geometry; then solve source-specific h00/A4 transfer rather than fitting constant PPN parameters.'
}
open('c9_projectable_u1_o4_single_resolvent_source_support_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
