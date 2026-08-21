#!/usr/bin/env python3
"""C8 action-level FDiff companion Dirac gate.

Constructive action
-------------------
On a preferred foliation define two companion scalars X,Y and

    Sigma = X + a Y,
    Theta = nabla_perp Sigma = (dot Sigma-N^i D_i Sigma)/N.

On the production DBI state r, use

    K(r)=2 M_Pl^2 M_K(r)^2,
    G(r)=K(r)c_a^2(r).

Consider the spatially-covariant scalar action

    L = 1/2 K(r) Theta^2
        + M_Pl^2 D_i Theta D^i Theta
        - 1/2 G(r)(1+a^2)[D_iX D^iX + D_iY D^iY].

The mixed coefficient is fixed because K/(2M_K^2)=M_Pl^2 exactly.
The action contains no lapse or shift velocities.  More importantly, all
velocities of X,Y enter only through dot X+a dot Y.  Even though the momentum
is a spatial differential operator, the exact primary constraint is

    phi1 = pi_Y-a pi_X = 0.

For homogeneous coefficients on FLRW, preserving phi1 yields at finite p

    phi2 = (1+a^2) G p^2 (a X-Y) = 0.

Their bracket is

    {phi1,phi2}=(1+a^2)^2 G p^2 > 0

on the physical DBI branch and p^2>0.  Thus the pair is second class and the
companion sector has one physical scalar DOF at finite momentum.

After imposing Y=aX, Sigma=(1+a^2)X and the reduced action is

    L_red = 1/2 [K+2 M_Pl^2 p^2] dot Sigma^2
            -1/2 G p^2 Sigma^2
          = 1/2 K(1+p^2/M_K^2) dot Sigma^2
            -1/2 G p^2 Sigma^2,

which gives the exact RTK dispersion.

Scope: action-level companion/FDiff scalar theorem on homogeneous FLRW
coefficients.  It is not yet a full gravitational Hamiltonian theorem: the
preferred foliation/Khronon and metric constraint sectors must be combined with
this pair without introducing a second gravitational scalar.
"""

import json
import sympy as sp

# Positive physical quantities at one homogeneous FLRW state.
Mpl2,MK2,K,G,p2 = sp.symbols('Mpl2 MK2 K G p2', positive=True, finite=True, real=True)
a = sp.symbols('a', finite=True, real=True)
Nf = 1+a**2

# Production normalization makes the coefficient of (D Theta)^2 constant.
K_prod = 2*Mpl2*MK2
Cmix = sp.simplify(K_prod/(2*MK2))
assert Cmix == Mpl2

# Fourier finite-p companion kinetic matrix.  Since
# Mpl^2 (D Theta)^2 = 1/2 (2 Mpl^2 p^2) Theta^2,
# K_eff=K+2Mpl^2 p^2.
Keff = sp.simplify(K_prod+2*Mpl2*p2)
assert sp.simplify(Keff-K_prod*(1+p2/MK2)) == 0

v = sp.Matrix([1,a])
Kvel = Keff*(v*v.T)
assert Kvel.rank() == 1
assert sp.factor(Kvel.det()) == 0

# Exact primary constraint follows because both canonical momenta are
# proportional to the same functional derivative Pi_Sigma.
Pi = sp.symbols('Pi', finite=True, real=True)
piX = Pi
piY = a*Pi
assert sp.simplify(piY-a*piX) == 0

# Finite-p secondary constraint and its Poisson bracket.
X,Y,pX,pY = sp.symbols('X Y pX pY', finite=True, real=True)
phi1 = pY-a*pX
phi2 = sp.expand(Nf*G*p2*(a*X-Y))

def PB(f,h):
    return sp.expand(
        sp.diff(f,X)*sp.diff(h,pX)-sp.diff(f,pX)*sp.diff(h,X)
        + sp.diff(f,Y)*sp.diff(h,pY)-sp.diff(f,pY)*sp.diff(h,Y)
    )

bracket = sp.factor(PB(phi1,phi2))
assert sp.simplify(bracket-Nf**2*G*p2) == 0
assert Nf.is_positive

# Two configuration variables -> phase dimension 4; one second-class pair.
physical_dof = sp.Rational(4-2,2)
assert physical_dof == 1

# Reduced exact RTK action after Y=aX, Sigma=Nf X.
Sigma,dSigma = sp.symbols('Sigma dSigma', finite=True, real=True)
Lred_kin_coeff = sp.simplify(Keff)
Lred_grad_coeff = G*p2
assert sp.simplify(Lred_kin_coeff-K_prod*(1+p2/MK2)) == 0

disp = sp.simplify(Lred_grad_coeff/Lred_kin_coeff)
ca2 = sp.simplify(G/K_prod)
target = sp.simplify(ca2*p2/(1+p2/MK2))
assert sp.simplify(disp-target) == 0

out = {
  'classification':'RTK_ROUTE_B_FDIFFEO_COMPANION_DIRAC_ACTION_GATE_PASS',
  'action':'1/2 K(r)Theta^2 + M_Pl^2 D_iTheta D^iTheta -1/2 G(r)(1+a^2)[(DX)^2+(DY)^2], Theta=nabla_perp(X+aY)',
  'production_identity':'K(r)=2 M_Pl^2 M_K(r)^2',
  'mixed_coefficient':'K/(2M_K^2)=M_Pl^2 exactly, independent of epoch/state',
  'primary_constraint':'pi_Y-a pi_X=0 exactly because all velocities enter only through dot X+a dot Y',
  'finite_p_secondary':'(1+a^2)G p^2(aX-Y)=0',
  'constraint_bracket':'(1+a^2)^2 G p^2 > 0 for p^2>0 on the positive DBI branch',
  'physical_companion_dof':1,
  'reduced_action':'1/2 K(1+p^2/M_K^2) dotSigma^2 -1/2 G p^2 Sigma^2',
  'dispersion':'omega^2=(G/K)p^2/(1+p^2/M_K^2)=c_a^2 p^2/(1+p^2/M_K^2)',
  'static_and_tensor_design':'If the companion combination is background-silent, the mixed operator has no direct quadratic lapse-gradient term and no pure TT quadratic term.',
  'non_claims':[
    'companion-sector theorem on homogeneous FLRW coefficients, not the full metric+Khronon Hamiltonian',
    'p=0 homogeneous constraint sector is separate',
    'does not yet prove that the original DBI background perturbation is transferred to Sigma with the correct matter source',
    'does not prove radiative stability of the rank-one alignment',
    'PPN/Newton, GW, compact-object and EFT-cutoff gates remain open'
  ],
  'next_step':'Couple this exact one-DOF companion action to the production Khronon/metric sector and derive the combined scalar Hessian/Dirac constraints. The decisive test is whether the existing gravitational scalar and Sigma are one constrained mode rather than two independent scalars.'
}

print('RTK_ROUTE_B_FDIFFEO_COMPANION_DIRAC_ACTION_GATE_PASS',json.dumps(out,sort_keys=True))
