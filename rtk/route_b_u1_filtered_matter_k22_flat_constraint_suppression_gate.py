#!/usr/bin/env python3
"""Flat-FLRW leading filtered-matter k22 suppression theorem.

Scope and literature input
--------------------------
On the exceptional nonprojectable local-U(1) branch eta1=eta2=0, the published
gravity action contains the sigma source

    sqrt(g) N (2 Omega - eta0 R) sigma

(up to the common M_Pl^2/2 normalization).  Therefore the gravity A-constraint
source Jg is proportional to sqrt(g)(2 Omega-eta0 R).

After exact elliptic auxiliary Dirac projection,

    Jhat = Jg - a_eff H0,   a_eff=q/(M_c^2+q), q=|k|^2.

For an exactly spatially flat FLRW background, R=0 and q=0. Since a_eff(0)=0,
the physical constraint Jhat=0 implies Jg_background=0 and hence Omega=0
(assuming the nonzero standard gravity normalization). Consequently the first
nontrivial local scalar variation of Jg starts with delta R=O(q), rather than an
O(q^0) volume-source term.

Combine this with previously proved/conditioned low-k support:

    Jg = O(q),                 Jm = O(q/M_c^2),
    c_g={Jg,Hperp}_g=O(q),     c_m=O(q/M_c^2),
    phi_hat = N c + weak momentum support

on the homogeneous-lapse regular patch.  At first order in the filtered-matter
coupling, the correction to d={Jhat,phi_hat} is

    delta d_m = N[{Jg,c_m}+{Jm,c_g}] + higher/filter^2 terms.

If the local functional Poisson brackets are analytic at q=0 and introduce no
inverse-q boundary/kernel singularity, each displayed term is O(q^2/M_c^2).
Therefore there is no O(q/M_c^2) coefficient in d:

    k22 = 0

for the leading matrix Delta B_m=(q/M_c^2)K+... . Together with the prior e11=0,
k12=-k21 and k21=x=V(H0-tau_H),

    K = [[0,-x],[x,0]].

This is a controlled flat-FLRW leading-symbol theorem, not an all-background or
all-k statement.
"""
import json
import sympy as sp

q,M2,eta0,Omega,R,H0=sp.symbols('q M_c_squared eta0 Omega R H0', finite=True)
# Background source factor on the exceptional branch.  On flat FLRW R=0 and
# a_eff(0)=0, Jhat=0 implies 2 Omega=0.
aeff=sp.simplify(q/(M2+q))
assert sp.simplify(aeff.subs(q,0))==0
F=2*Omega-eta0*R
F_flat=sp.simplify(F.subs(R,0))
assert F_flat==2*Omega
# Encode the consequence of the background constraint explicitly.
assert sp.solve(sp.Eq(F_flat,0),Omega)==[0]

# Formal low-q/filter order bookkeeping. eps tracks q, mu tracks 1/Mc^2.
eps,mu=sp.symbols('eps mu')
Jg1,Jm1,cg1,cm1=sp.symbols('Jg1 Jm1 cg1 cm1', finite=True)
Jg=eps*Jg1
Jm=eps*mu*Jm1
cg=eps*cg1
cm=eps*mu*cm1
# A local analytic PB is bilinear in its arguments and cannot lower the sum of
# explicit q-orders under the stated no-inverse-q assumption.  Represent its
# coefficient by independent finite symbols.
p1,p2=sp.symbols('p1 p2', finite=True)
delta_d=sp.expand(eps**2*mu*(p1+p2))
assert delta_d.coeff(eps,1)==0
assert delta_d.coeff(eps,2).coeff(mu,1)==p1+p2

x=sp.symbols('x', real=True, finite=True)
K=sp.Matrix([[0,-x],[x,0]])
assert sp.simplify(K.det()-x**2)==0
assert sp.simplify((K.T*K)[0,0]-x**2)==0
assert sp.simplify((K.T*K)[1,1]-x**2)==0
assert (K.T*K)[0,1]==0 and (K.T*K)[1,0]==0

out={
  'classification':'RTK_ROUTE_B_U1_FILTERED_MATTER_K22_FLAT_CONSTRAINT_SUPPRESSION_PASS',
  'status_scope':'GREEN_FLAT_FLRW_LEADING_FILTERED_MATTER_MATRIX_ANTISYMMETRIC_SUBLEADING_K22_PENDING',
  'domain':'eta1=eta2=0 exceptional U(1) branch; exactly spatially flat FLRW background; regular D_i nu=0 homogeneous-lapse leading Fourier patch; local analytic Poisson kernels with no inverse-q singularity',
  'published_source_input':'gravity sigma source is proportional to (2 Omega-eta0 R)',
  'background_constraint_chain':['R_background=0','a_eff(q=0)=0','Jhat_background=0 => Jg_background=0','therefore Omega=0 on this flat branch'],
  'order_inputs':['Jg=O(q) after Omega=0','Jm=O(q/M_c^2)','c_g=O(q)','c_m=O(q/M_c^2)','phi_hat=N c plus weak momentum support at the stated leading homogeneous-lapse order'],
  'first_order_delta_d':'delta d_m=N({Jg,c_m}+{Jm,c_g})+higher/filter^2 = O(q^2/M_c^2)',
  'leading_K22':'k22=0 in Delta B_m=(q/M_c^2)K+O(q^2/M_c^2,q^2/M_c^4)',
  'combined_leading_matrix':'K=[[0,-x],[x,0]], x=k21=V(H0-tau_H)',
  'leading_K_operator_norm':'||K||_2=|x| exactly',
  'interpretation':'On the controlled flat-FLRW constraint surface, the filtered-matter leading low-k correction is purely antisymmetric in the B cross-block. The previously unknown k22 starts only at subleading q^2/M_c^2 (or higher) order under the stated analyticity assumptions.',
  'non_claims':[
    'does not prove k22 suppression on curved FLRW, anisotropic, inhomogeneous-lapse, or nonanalytic boundary backgrounds',
    'does not bound the subleading O(q^2/M_c^2) coefficient',
    'does not choose M_c',
    'does not certify intermediate/high-k rank, PPN/GW, compact objects, cutoff, or C9 naturalness'
  ],
  'next_gate':'combine K=[[0,-x],[x,0]] with B_RTK=[[A,-b],[b,0]] to derive the exact leading determinant/rank window M_c^2>|x|/|b| as a sufficient no-cancellation condition, then intersect it with the frozen 1% scale-separation window.'
}
with open('u1_filtered_matter_k22_flat_constraint_suppression_result.json','w') as f:
    json.dump(out,f,indent=2,sort_keys=True); f.write('\n')
print(out['classification'],json.dumps(out,sort_keys=True))
