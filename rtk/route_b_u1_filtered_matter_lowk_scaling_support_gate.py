#!/usr/bin/env python3
"""Filtered-matter low-k scaling/sparse-support theorem after Dirac projection.

Domain: regular D_i nu=0 translational Fourier patch after eliminating
(p_Q,C_Lambda), with analytic local gravity/matter brackets at k=0 and no
additional inverse-|k| singularity introduced by boundary conditions.

Exact projected matter source:
    J_m=-a_eff H0,
    a_eff=q/(M_c^2+q), q=|k|^2.
The reduced-chain theorem gives Hperp_m=H0 with no lapse dependence. Hence the
direct filtered-matter correction to a={pi_N,Hperp} is exactly zero on this
slice.

At low q,
    a_eff=q/M_c^2+O(q^2/M_c^4),
and for a fractional metric variation delta q=m q,
    delta a_eff=(m q)/M_c^2+O(q^2/M_c^4).
Thus every remaining leading correction generated linearly by J_m or its
metric variation carries q/M_c^2, provided the unfiltered bracket coefficients
are finite at q=0. The leading scaled matter matrix therefore has sparse form

    Delta B_m=q/M_c^2 K + O(q^2),
    K=[[0,k12],[k21,k22]].

If |k12|,|k21|,|k22|<=kappa, then
    ||K||_2 <= ||K||_F <= sqrt(3) kappa,
so a sufficient rank condition around the RTK-shifted baseline is
    M_c^2 > sqrt(3) kappa/sigma_min(B_RTK).

This is a support/scaling theorem; it does not yet compute k12,k21,k22 from a
specific matter stress tensor/background.
"""
import json
import sympy as sp

q,M2,m=sp.symbols('q M_c_squared m', positive=True, finite=True)
aeff=sp.simplify(q/(M2+q))
# Exact low-q coefficients without relying on a formal series parser.
lead_aeff=sp.simplify(sp.limit(aeff/q,q,0,dir='+'))
assert sp.simplify(lead_aeff-1/M2)==0

dadq=sp.diff(aeff,q)
delta_aeff=sp.simplify(dadq*(m*q))
lead_delta=sp.simplify(sp.limit(delta_aeff/q,q,0,dir='+'))
assert sp.simplify(lead_delta-m/M2)==0

# Sparse leading correction: e11=0 exactly on the regular reduced a2=0 slice.
k12,k21,k22=sp.symbols('k12 k21 k22', real=True, finite=True)
K=sp.Matrix([[0,k12],[k21,k22]])
assert K[0,0]==0
frob_sq=sp.expand(sum(x**2 for x in K))
assert sp.simplify(frob_sq-(k12**2+k21**2+k22**2))==0

# Entrywise bound implication is recorded as an exact worst-case Frobenius
# coefficient for three nonzero entries.
kappa,sigma=sp.symbols('kappa sigma_min', positive=True, finite=True)
frob_entry_bound=sp.sqrt(3)*kappa
rank_lower_M2=sp.simplify(frob_entry_bound/sigma)

out={
  'classification':'RTK_ROUTE_B_U1_FILTERED_MATTER_LOWK_SCALING_SUPPORT_PASS',
  'status_scope':'GREEN_LOWK_ONE_OVER_MC2_SCALING_AND_E11_ZERO_ACTION_COEFFICIENTS_PENDING',
  'domain':'regular D_i nu=0 Fourier-symbol patch after exact auxiliary Dirac projection; analytic finite unfiltered bracket coefficients near k=0; no extra inverse-k boundary singularity',
  'exact_source':'J_m=-a_eff H0, a_eff=q/(M_c^2+q), q=|k|^2',
  'lowk_source_scaling':'a_eff=q/M_c^2+O(q^2/M_c^4)',
  'lowk_metric_variation_scaling':'for delta q=m q, delta a_eff=m q/M_c^2+O(q^2/M_c^4)',
  'sparse_support':'Delta B_m=(q/M_c^2) K+O(q^2), K=[[0,k12],[k21,k22]]',
  'e11_reason':'Hperp_m=H0 is lapse-independent on the reduced regular slice, so {pi_N,Hperp_m}=0; metric variation does not create a lapse canonical bracket',
  'entrywise_bound':'if |k12|,|k21|,|k22|<=kappa then ||K||_2<=||K||_F<=sqrt(3) kappa',
  'sufficient_rank_condition':'M_c^2 > sqrt(3) kappa/sigma_min(B_RTK)',
  'baseline_note':'B_RTK uses A=a2+r2 in its (1,1) entry; sigma_min must include the neutral-RTK conditioning shift even though the leading determinant stays b2^2',
  'interpretation':'The projected elliptic matter sector enters the punctured-low-k rank problem with explicit 1/M_c^2 suppression and no leading e11 correction. Only three leading coefficients require an action/background bound, sharpening the generic four-entry Frobenius estimate.',
  'non_claims':[
    'does not compute k12,k21,k22 from H0 or a specific stress tensor',
    'does not prove absence of nonanalytic inverse-k behavior outside the stated patch/boundary assumptions',
    'does not choose M_c',
    'does not certify intermediate/high-k rank or PPN/GW/C9 viability'
  ],
  'next_gate':'derive k12,k21,k22 or a common kappa bound from the functional Poisson brackets of Jhat=Jg-a_eff H0, Hperp_hat and phi_hat on a controlled FLRW matter background; then insert sqrt(3)kappa/sigma_min into the symbolic M_c window.'
}
with open('u1_filtered_matter_lowk_scaling_support_result.json','w') as f:
    json.dump(out,f,indent=2,sort_keys=True); f.write('\n')
print(out['classification'],json.dumps(out,sort_keys=True))
