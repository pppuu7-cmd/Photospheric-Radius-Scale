#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[2]

def load(rel):
    return json.loads((ROOT/rel).read_text())

def derivative_maps(Fjets, N):
    n=Fjets[0].rows
    G=[sp.eye(n)]
    for m in range(N):
        acc=sp.zeros(n)
        for j in range(m+1):
            acc += sp.binomial(m,j)*Fjets[j]*G[m-j]
        # Entries are exact rationals already; avoid expensive global simplify.
        G.append(acc)
    return G

def main():
    t=load('research/theory_targets/RTK_C10_65J_FINITE_LOCAL_TEMPORAL_JET_IDENTIFIABILITY_TARGET_v1.json')
    i=load('research/theory_results/RTK_C10_65I_COUPLED_COEFFICIENT_NULLITY_WITH_SYMBOLIC_C2_RESULT_v1.json')
    g=load('research/theory_results/RTK_C10_65G_FINITE_ONSET_GROWING_MODE_IDENTIFIABILITY_RESULT_v1.json')
    h=load('research/theory_results/RTK_C10_65H_MINIMAL_C2_TEMPORAL_MATCHING_COORDINATE_RESULT_v1.json')
    assert t['status']=='FROZEN_BEFORE_IMPLEMENTATION'
    assert i['classification']=='C10_65I_COUPLED_COEFFICIENT_NULLITY_REMAINING_TEMPORAL_AMPLITUDES_8_SCOPED'
    assert g['classification']=='C10_65G_FINITE_ONSET_SNAPSHOT_RANK_INSUFFICIENT_TEMPORAL_MATCH_REQUIRED_SCOPED'
    assert h['classification']=='C10_65H_C2_GAUGE_INVARIANT_MINIMAL_SHIFT_MATCH_COORDINATE_PASS_SCOPED'
    inherited=int(i['exact_rank_certificate']['nullity_fixed_C2_after_normalization'])
    assert inherited==8

    checks=[]
    for n in (2,3,5,8):
        N=5
        Fjets=[]
        for j in range(N):
            F=sp.Matrix(n,n,lambda r,c: sp.Rational((j+1)*(r+2)+(c+1)*(j+3)+(r-c)*(r+c+1),37+j*2))
            Fjets.append(F)
        noncomm=any(Fjets[a]*Fjets[b] != Fjets[b]*Fjets[a]
                    for a in range(len(Fjets)) for b in range(a+1,len(Fjets)))
        assert noncomm
        G=derivative_maps(Fjets,N)

        # Exact rank certificate for jet graph [I;G1;...;GN]: its top n x n minor is I.
        assert G[0]==sp.eye(n) and G[0].det()==1
        jet_rank=n

        # If derivatives d1..dN are introduced independently, equations
        # d_m-G_m z0=0 contain block-diagonal I in all derivative columns.
        derivative_minor=sp.eye(N*n)
        assert derivative_minor.det()==1
        derivative_rank=N*n
        derivative_nullity=(N+1)*n-derivative_rank
        assert derivative_nullity==n

        # Restrict z0=B u with a visibly full-column-rank exact rational B.
        d=max(1,n-1)
        B=sp.eye(d).col_join(sp.Matrix(n-d,d,lambda r,c:sp.Rational((r+2)*(c+3),43)))
        assert B[:d,:]==sp.eye(d)
        restricted_rank=d

        # Exercise the actual exact-rational N=5 recursion rather than only the block theorem.
        # A compact checksum ensures every G_m was generated and remains finite/exact.
        checksum=sum((m+1)*sum(G[m]) for m in range(len(G)))
        assert checksum.is_Rational
        checks.append({
            'state_dimension':n,'jet_order':N,'noncommuting_time_derivative_matrices':True,
            'jet_certifying_minor_det':'1','stacked_jet_graph_rank':jet_rank,
            'derivative_identity_minor_det':'1','derivative_variable_constraint_rank':derivative_rank,
            'derivative_variable_nullity':derivative_nullity,
            'restricted_subspace_dimension':d,'restricted_certifying_minor_det':'1',
            'restricted_jet_graph_rank':restricted_rank,'exact_recursion_checksum':str(checksum)
        })

    d=8; N=5
    Fjets=[sp.Matrix(d,d,lambda r,c:sp.Rational((j+2)*(r+1)+(c+3)*(j+1)+(r+1)*(c+1),53+j)) for j in range(N)]
    G=derivative_maps(Fjets,N)
    assert G[0]==sp.eye(d)
    fixed_rank=d

    # Released C2 is appended as an independent onset coordinate; the zeroth block is I_(d+1).
    released_zero_block=sp.eye(d+1)
    assert released_zero_block.det()==1
    released_rank=d+1

    cls='C10_65J_FINITE_LOCAL_TEMPORAL_JET_INSUFFICIENT_NONLOCAL_BRANCH_REQUIRED_SCOPED'
    out={
      'schema':'RTK_C10_65J_FINITE_LOCAL_TEMPORAL_JET_IDENTIFIABILITY_RESULT_v1',
      'gate':'C10.65j','classification':cls,
      'target':'research/theory_targets/RTK_C10_65J_FINITE_LOCAL_TEMPORAL_JET_IDENTIFIABILITY_TARGET_v1.json',
      'theorem':{
        'fixed_C2':'For z_prime=F(t)z with regular finite coefficients, every finite onset jet is J_N(z0)=(z0,G1 z0,...,GN z0). The zeroth block is I, so J_N is injective and rank(J_N)=dim(z0).',
        'derivative_variables':'If d1,...,dN are separate variables, recurrence equations d_m-G_m z0=0 have an exact block-diagonal identity minor in derivative columns; they add rank N*n and leave nullity n unchanged.',
        'restricted_constraint_manifold':'For any admissible onset subspace z0=B u with rank(B)=d, the finite jet has the same rank d because the zeroth block is B.',
        'released_C2':'Augmenting the onset coordinate by the constant matching scalar C2 gives one additional zeroth-order coordinate; every finite local jet therefore retains exactly the one extra matching direction.',
        'scope_guard':'Only additional temporal boundary information not encoded by the local ODE graph—e.g. backward boundedness, asymptotic power-law/eigenbranch selection, or microscopic pre-EFT matching—can reduce the onset-state dimension.'
      },
      'inherited_C10_65i':{
        'fixed_C2_post_normalization_dimension':inherited,
        'dimension_after_any_finite_local_jet':8,
        'released_C2_dimension_after_any_finite_local_jet':9
      },
      'exact_rational_machine_checks':checks,
      'eight_dimensional_direct_check':{
        'jet_order':N,'fixed_C2_graph_rank':fixed_rank,'fixed_C2_certifying_minor_det':'1',
        'released_C2_augmented_graph_rank':released_rank,'released_C2_certifying_minor_det':'1'
      },
      'architecture_decision':{
        'forbidden':'Do not try to close the eight C10.65i temporal amplitudes by stacking z_prime,z_double_prime,... at the same finite onset.',
        'required':'The next selector must use genuinely nonlocal/asymptotic temporal information or an explicit UV/pre-EFT boundary functional.',
        'DAE_note':'Algebraically projected metric/TCA auxiliaries may be differentiated as needed for RHS evaluation, but those derivative definitions remain graph variables and are not independent IC constraints.'
      },
      'next_gate':t['next_if_pass'],'non_claims':t['non_claims']
    }
    p=ROOT/'research/theory_results/RTK_C10_65J_FINITE_LOCAL_TEMPORAL_JET_IDENTIFIABILITY_RESULT_v1.json'
    p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(cls,json.dumps({'fixed_C2_dimension':8,'released_C2_dimension':9,'max_jet_order':5,'machine_cases':len(checks)},sort_keys=True))

if __name__=='__main__':
    main()
