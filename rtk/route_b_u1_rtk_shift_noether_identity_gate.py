#!/usr/bin/env python3
"""C8 Noether/constraint identity for any RTK sector built from invariant shift.

In one spatial direction let v = Ni-N*nu_x and allow a local Lagrangian
L=L(v,v_x,other U(1)-neutral jets). This covers the shift dependence of
Theta_U and D_x Theta_U: the latter introduces v_x but no higher derivative of
v. Writing P0=dL/dv and P1=dL/dv_x, the Euler derivative with respect to Ni is
E_Ni=P0-D_x P1. Direct variation with respect to nu gives

  E_nu = D_x[N E_Ni].

Thus the nu equation supplied by the neutral RTK DBI/mixed sector is the spatial
divergence of its shift equation and is not an independent constraint once the
momentum/shift equation is imposed. This is the local Noether identity behind
U(1) invariance of the invariant-shift construction.
"""
import json
import sympy as sp

N,Nx,Nxx=sp.symbols('N Nx Nxx', real=True, finite=True)
P0,P0x=sp.symbols('P0 P0x', real=True, finite=True)
P1,P1x,P1xx=sp.symbols('P1 P1x P1xx', real=True, finite=True)

# For L(v,vx): partial derivatives with respect to nu_x and nu_xx follow from
# v=Ni-N nu_x and vx=Ni_x-Nx nu_x-N nu_xx.
dL_dnux=-N*P0-Nx*P1
dL_dnuxx=-N*P1

# Total spatial derivative rules on the abstract jet symbols.
def Dx(expr):
    return sp.expand(
        sp.diff(expr,N)*Nx + sp.diff(expr,Nx)*Nxx +
        sp.diff(expr,P0)*P0x + sp.diff(expr,P1)*P1x +
        sp.diff(expr,P1x)*P1xx
    )

E_Ni=sp.expand(P0-P1x)
E_nu=sp.expand(-Dx(dL_dnux)+Dx(Dx(dL_dnuxx)))
identity_rhs=sp.expand(Dx(N*E_Ni))
assert sp.simplify(E_nu-identity_rhs)==0

# On the shift equation the nu equation vanishes, including its first spatial
# derivative consequence encoded by P0=P1x and P0x=P1xx.
on_shift=sp.simplify(E_nu.subs({P0:P1x,P0x:P1xx}))
assert on_shift==0

out={
  'classification':'RTK_ROUTE_B_U1_RTK_SHIFT_NOETHER_IDENTITY_PASS',
  'scope':'local one-direction jet proof for L(v,Dv,neutral jets), v=Ni-N Dnu; tensor generalization is E_nu=D_i(N E_Ni)',
  'E_Ni':str(E_Ni),
  'E_nu':str(E_nu),
  'identity_rhs_Dx_N_ENi':str(identity_rhs),
  'identity_residual':str(sp.simplify(E_nu-identity_rhs)),
  'on_shift_constraint':str(on_shift),
  'interpretation':'The neutral RTK DBI/mixed sector contributes no independent nu equation beyond the divergence of its shift/momentum equation, so its invariant-shift dependence does not by itself add a new independent constraint equation in the U1 chain.',
  'non_claims':[
    'does not prove the full secondary second-class Poisson matrix is nonsingular',
    'does not include non-U1-invariant matter couplings',
    'does not establish global nonlinear DOF count by itself'
  ],
  'next_gate':'combine this Noether identity with the surviving pi_N-J_A primary bracket and evaluate the modified four-constraint submatrix (pi_N,J_A,H_perp,phi_A) on the coupled phase space'
}
open('u1_rtk_shift_noether_identity_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print('RTK_ROUTE_B_U1_RTK_SHIFT_NOETHER_IDENTITY_PASS',json.dumps(out,sort_keys=True))
