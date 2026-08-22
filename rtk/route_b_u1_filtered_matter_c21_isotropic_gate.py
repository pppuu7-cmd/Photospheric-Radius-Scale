#!/usr/bin/env python3
"""Isotropic FLRW leading filtered-matter coefficient for c={Jhat,Hperp}.

After exact auxiliary Dirac projection on the regular D_i nu=0 slice,

    Jhat = Jg + Jm,     Jm=-a_eff H0,
    Hperp = Hg + H0 + neutral-RTK support,
    a_eff=q/(M_c^2+q), q=|k|^2.

Previously proved support facts used here:
  * Jg is gravity-coordinate/metric-only on the exceptional U(1) branch;
  * H0 has no gravity canonical momentum, so {Jg,H0}=0;
  * the direct matter self bracket from Jm,H0 vanishes in the frozen reduced
    matter support;
  * neutral RTK is handled separately.

Therefore the filtered-matter correction to
    c={Jhat,Hperp}
is
    delta c_m={Jm,Hg}.

On an isotropic gravitational canonical background write
    delta Hg/delta pi^{ij}=V g_{ij}
and define the metric-trace derivative at fixed matter canonical variables
    tau_H := g_{ij} delta H0/delta g_{ij}.
For q=g^{ij}k_i k_j,
    D_g q := g_{ij} delta q/delta g_{ij} = -q.
Hence
    D_g Jm = -[(D_g a_eff)H0+a_eff tau_H]
             = M_c^2 q H0/(M_c^2+q)^2 - q tau_H/(M_c^2+q),
and
    delta c_m = V D_g Jm
              = (q/M_c^2) V(H0-tau_H)+O(q^2/M_c^4).

Thus the leading sparse-matrix coefficient is
    k21 = V (H0-tau_H)
for the canonical Poisson-bracket orientation used above, and
    |k21| <= |V| (|H0|+|tau_H|).

This isolates one action/background coefficient; k12 and k22 remain pending.
"""
import json
import sympy as sp

q,M2,V,H,tau=sp.symbols('q M_c_squared V H0 tau_H', real=True, finite=True)
# Positive M2/q are imposed only where limits are taken.
M2p,qp=sp.symbols('M2p qp', positive=True, finite=True)
a=qp/(M2p+qp)
Da=sp.simplify(sp.diff(a,qp)*(-qp))
DJm=sp.simplify(-(Da*H+a*tau))
expected=sp.simplify(M2p*qp*H/(M2p+qp)**2-qp*tau/(M2p+qp))
assert sp.simplify(DJm-expected)==0
lead=sp.simplify(sp.limit(DJm/qp,qp,0,dir='+'))
assert sp.simplify(lead-(H-tau)/M2p)==0

delta_c=sp.simplify(V*DJm)
lead_c=sp.simplify(sp.limit(delta_c/qp,qp,0,dir='+'))
assert sp.simplify(lead_c-V*(H-tau)/M2p)==0

# Define K coefficient after Delta c = (q/Mc^2) k21 + ...
k21=sp.expand(V*(H-tau))
assert sp.simplify(M2p*lead_c-k21)==0

out={
  'classification':'RTK_ROUTE_B_U1_FILTERED_MATTER_C21_ISOTROPIC_PASS',
  'status_scope':'GREEN_ACTION_LEVEL_C21_LOWK_COEFFICIENT_K12_K22_PENDING',
  'domain':'regular D_i nu=0 Dirac-projected Fourier patch; isotropic gravity canonical background delta H_g/delta pi^{ij}=V g_{ij}; fixed matter canonical variables in the metric trace derivative',
  'source_decomposition':'Jhat=Jg-a_eff H0, Hperp=Hg+H0+neutral-RTK; direct filtered-matter delta c={-a_eff H0,Hg}',
  'metric_trace_definitions':['D_g q=-q for q=g^{ij}k_i k_j','tau_H=g_{ij} delta H0/delta g_{ij}'],
  'exact_Dg_Jm':'M_c^2 q H0/(M_c^2+q)^2 - q tau_H/(M_c^2+q)',
  'lowk_delta_c':'delta c_m=(q/M_c^2) V(H0-tau_H)+O(q^2/M_c^4)',
  'K21':'k21=V(H0-tau_H)',
  'absolute_bound':'|k21| <= |V| (|H0|+|tau_H|)',
  'interpretation':'One of the three potentially nonzero leading filtered-matter rank-correction coefficients is fixed by the isotropic gravitational canonical velocity V and the trace metric response of the matter Hamiltonian. It is explicitly independent of M_c once the universal 1/M_c^2 factor is extracted.',
  'non_claims':[
    'does not evaluate H0 or tau_H for a specific matter species/background',
    'does not yet derive k12={pi_N,phi} or k22={Jhat,phi} corrections',
    'does not include neutral-RTK e11 conditioning in this coefficient formula',
    'does not choose M_c or certify intermediate/high-k rank'
  ],
  'next_gate':'derive the preservation descendant phi_hat to leading filtered-matter order and use it to obtain k12 and k22; then combine all three coefficients in the sparse Frobenius/operator-norm bound.'
}
with open('u1_filtered_matter_c21_isotropic_result.json','w') as f:
    json.dump(out,f,indent=2,sort_keys=True); f.write('\n')
print(out['classification'],json.dumps(out,sort_keys=True))
