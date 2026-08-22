#!/usr/bin/env python3
"""Homogeneous-mode ordinary-matter rank-inheritance theorem.

After exact auxiliary Dirac projection the matter source is

    J_m = -a_eff H0,  a_eff=1-L^{-1}.

For the spatial homogeneous mode k=0, L=1 and a_eff=0.  On the regular
D_i nu=0 slice the ordinary matter Hamiltonian is then simply N H0, with H0
independent of N,A,nu after the Legendre transform.  On the special gravity
surface eta1=eta2=0, J_A^(g) is a functional of the spatial metric (and its
spatial derivatives) but contains no gravitational canonical momentum.
Ordinary H0 also contains no gravitational canonical momentum.

Consequently ordinary matter gives no direct correction to any of the four
published special-branch cross-block entries

 B=[[{pi_N,Hperp},{pi_N,phi_A}],
    [{J_A,Hperp},{J_A,phi_A}]]

at k=0.  This proves that the FLRW source rescue does not by itself destroy the
special-U(1) rank block.  The neutral rolling RTK sector is separate: an older
support theorem allows it to modify only {pi_N,Hperp}; this gate does not set
that independent correction to zero.
"""
import json
import sympy as sp

# Minimal nontrivial canonical representative: gravity (g,pg), matter (q,pq),
# prepotential (nu,pnu), lapse N.  Special-branch Jg and H0 have no pg.
g,pg,q,pq,nu,pnu,N,pN,A,pA=sp.symbols('g p_g q p_q nu p_nu N pi_N A p_A', finite=True)
coords=[g,q,nu,N,A]
moms=[pg,pq,pnu,pN,pA]
def PB(f,h):
    return sp.simplify(sum(sp.diff(f,x)*sp.diff(h,px)-sp.diff(f,px)*sp.diff(h,x)
                           for x,px in zip(coords,moms)))

# Representatives with genuine metric/matter dependence but no gravity momentum.
Jg=g+g**2
H0=(1+g)*pq**2/2 + q**2/(2*(1+g))
assert sp.diff(Jg,pg)==0
assert sp.diff(H0,pg)==0
assert sp.diff(H0,N)==0 and sp.diff(H0,A)==0 and sp.diff(H0,nu)==0
assert PB(Jg,H0)==0

# k=0 projected ordinary matter.
aeff0=sp.Integer(0)
Jm=-aeff0*H0
Hm=N*H0
Hperp_m=sp.diff(Hm,N)
assert Jm==0
assert sp.simplify(Hperp_m-H0)==0
assert PB(pN,Hperp_m)==0  # delta B_11

# Matter descendant in preservation of Ghat=pnu+Jg at k=0.
Ghat=pnu+Jg
phi_m=PB(Ghat,Hm)
assert phi_m==0
assert PB(pN,phi_m)==0    # delta B_12
assert PB(Jg,Hperp_m)==0  # delta B_21
assert PB(Jg,phi_m)==0    # delta B_22

# Algebraic inheritance of the published B block, keeping the already-known
# independent neutral-RTK lapse-stability correction delta_a explicit.
ag,bg,cg,dg,delta_rtk=sp.symbols('a_g b_g c_g d_g delta_a_RTK', finite=True)
Bg=sp.Matrix([[ag,bg],[cg,dg]])
Bordinary=Bg
BwithRTK=sp.Matrix([[ag+delta_rtk,bg],[cg,dg]])
assert sp.simplify(Bordinary.det()-Bg.det())==0
assert sp.simplify(BwithRTK.det()-Bg.det()-delta_rtk*dg)==0

out={
  'classification':'RTK_ROUTE_B_U1_ELLIPTIC_COMPENSATOR_K0_MATTER_RANK_INHERITANCE_PASS',
  'status_scope':'GREEN_K0_ORDINARY_MATTER_CROSSBLOCK_INHERITANCE_NEUTRAL_RTK_LAPSE_ENTRY_PENDING',
  'domain':'k=0 homogeneous projected mode, regular D_i nu=0 slice, special eta1=eta2=0 gravity surface',
  'exact_k0_results':{
    'a1_eff':'0',
    'J_A_m':'0',
    'Hperp_m':'H0',
    'delta_{pi_N,Hperp}_ordinary':'0 because H0 is lapse independent',
    'phi_A_m':'0 because {p_nu+J_A^(g), N H0}=0 on the stated support',
    'delta_{pi_N,phi_A}_ordinary':'0',
    'delta_{J_A,Hperp}_ordinary':'0',
    'delta_{J_A,phi_A}_ordinary':'0'
  },
  'published_special_branch_input':'For eta1=eta2=0, J_A^(g) is spatial-metric-only and the second-class rank is controlled by B=(({pi_N,Hperp},{pi_N,phi_A}),({J_A,Hperp},{J_A,phi_A})).',
  'ordinary_matter_crossblock':'B_k0^(gravity+ordinary)=B_gravity exactly on this support slice',
  'with_neutral_RTK_support_theorem':'B_total_k0=[[a_g+delta_a_RTK,b_g],[c_g,d_g]], det B_total=det B_g+delta_a_RTK d_g',
  'interpretation':'Exact homogeneous matter A-source cancellation is compatible with inheritance of the published special-U1 rank block from the ordinary-matter sector. Any remaining k=0 classical rank risk is therefore localized to the independent neutral RTK lapse-stability correction or to leaving the stated regular support slice.',
  'non_claims':[
    'does not prove the neutral rolling RTK correction delta_a_RTK vanishes on the physical cosmological branch',
    'does not prove rank at finite k where a_eff and metric variation of L^{-1} are nonzero',
    'does not establish the global zero-mode boundary-condition subtleties of the full elliptic Green operator',
    'does not choose M_c'
  ],
  'next_gate':'derive delta_a_RTK on the homogeneous rolling FLRW branch from the frozen RTK Hamiltonian; in parallel derive finite-k metric-resolvent corrections to the other B entries.'
}
with open('u1_elliptic_compensator_k0_matter_rank_inheritance_result.json','w') as f:
    json.dump(out,f,indent=2,sort_keys=True); f.write('\n')
print(out['classification'],json.dumps(out,sort_keys=True))
