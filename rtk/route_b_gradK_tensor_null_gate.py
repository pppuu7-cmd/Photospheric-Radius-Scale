#!/usr/bin/env python3
"""C8 exact theorem: tensor contamination of the static-safe grad-K escape.

Context
-------
The full scalar one-spatial-gradient extrinsic-curvature basis can realize the
exact RTK scalar kinetic kernel pointwise with

    y [U A^2 + 2 V A q + W q^2],
    A = dot(zeta)-H n, q=y psi,

provided

    U W = V^2,
    V/W = (6 H^2 M_*^2-Kc)/(4 H^2 M_*^2),
    W = 2 H^2 M_*^4/(Kc M_K^2).

Here Kc is the positive clock scalar kinetic coefficient, not the trace of the
extrinsic curvature.

At quadratic scalar order the three independent flat-FLRW contractions

    O_T = D_l K^i_j D^l K^j_i,
    O_K = D_i K D^i K,
    O_D = D_i K^i_j D_k K^{kj}

map to (U,V,W) as

    O_T -> (3,1,1),
    O_K -> (9,3,1),
    O_D -> (1,1,1).

For a transverse-traceless tensor h_ij,

    delta K^i_j = 1/2 dot(h)^i_j,
    D_i delta K^i_j = 0,
    delta K = 0.

Therefore O_K and O_D vanish in the TT sector, while

    O_T -> (1/4) p^2 dot(h_ij)^2.

So the coefficient c_T multiplying O_T is the unique tensor-contaminating
coefficient inside this basis.

The exact inverse scalar map gives

    c_T = (U-4V+3W)/2.

On the exact scalar RTK branch define

    R := Kc/(H^2 M_*^2) > 0.

Then V/W=(6-R)/4 and U/W=(V/W)^2, hence

    c_T = W (R-2)(R+6)/32.

Because R>0 and W>0, c_T=0 iff R=2.  At that unique tensor-null point

    U=V=W,
    c_T=0,
    c_K=0,
    c_D=W,

so the entire static-safe scalar correction collapses to the pure divergence
operator O_D.

If c_T != 0, the TT kinetic term becomes

    (M_*^2/8) [1 + 2 c_T p^2/M_*^2] dot(h_ij)^2,

while the Einstein-Hilbert tensor gradient remains -(M_*^2/8)p^2 h_ij^2,
so locally (ignoring Hubble damping for the high-frequency dispersion test)

    omega_T^2 = p^2 / [1 + 2 c_T p^2/M_*^2].

This theorem is structural, not yet an observational exclusion: a physical
completion may add a separate tensor-only cancellation, may sit on R=2 over a
controlled domain, or may use a different operator/auxiliary-field mechanism.
The next numerical/action-level gate must evaluate R(a) for the same normalized
candidate and apply GW constraints to the same coefficient tuple.
"""

import json
import sympy as sp

R,W,M2,y = sp.symbols('R W M2 y', positive=True, finite=True, real=True)
U,V = sp.symbols('U V', finite=True, real=True)
cT,cK,cD = sp.symbols('cT cK cD', finite=True, real=True)

# Exact scalar map from the three spatially covariant grad-K invariants.
map_U = 3*cT + 9*cK + cD
map_V = cT + 3*cK + cD
map_W = cT + cK + cD
mat = sp.Matrix([[3,9,1],[1,3,1],[1,1,1]])
assert mat.det() == 4
sol = sp.solve([
    sp.Eq(U,map_U), sp.Eq(V,map_V), sp.Eq(W,map_W)
], [cT,cK,cD], dict=True)
assert len(sol) == 1
inv = sol[0]
assert sp.simplify(inv[cT]-(U-4*V+3*W)/2) == 0
assert sp.simplify(inv[cK]-(V-W)/2) == 0
assert sp.simplify(inv[cD]-(3*V-U)/2) == 0

# Exact RTK pointwise branch parameterized by R=Kc/(H^2 M_*^2).
r = sp.factor((6-R)/4)  # V/W
V_rtk = sp.factor(r*W)
U_rtk = sp.factor(r**2*W)  # UW=V^2
cT_rtk = sp.factor(inv[cT].subs({U:U_rtk,V:V_rtk}))
cK_rtk = sp.factor(inv[cK].subs({U:U_rtk,V:V_rtk}))
cD_rtk = sp.factor(inv[cD].subs({U:U_rtk,V:V_rtk}))

assert sp.simplify(cT_rtk - W*(R-2)*(R+6)/32) == 0
assert sp.simplify(cK_rtk + W*(R-2)/8) == 0
assert sp.simplify(cD_rtk - W*(36-R**2)/32) == 0

# Unique tensor-null positive-R branch.
assert sp.factor(cT_rtk) == W*(R-2)*(R+6)/32
# R+6 cannot vanish on positive domain, W>0, so tensor-null iff R=2.
vals_R2 = {
    'r': sp.simplify(r.subs(R,2)),
    'U_over_W': sp.simplify((U_rtk/W).subs(R,2)),
    'V_over_W': sp.simplify((V_rtk/W).subs(R,2)),
    'cT_over_W': sp.simplify((cT_rtk/W).subs(R,2)),
    'cK_over_W': sp.simplify((cK_rtk/W).subs(R,2)),
    'cD_over_W': sp.simplify((cD_rtk/W).subs(R,2)),
}
assert vals_R2 == {
    'r': sp.Integer(1),
    'U_over_W': sp.Integer(1),
    'V_over_W': sp.Integer(1),
    'cT_over_W': sp.Integer(0),
    'cK_over_W': sp.Integer(0),
    'cD_over_W': sp.Integer(1),
}

# TT kinetic/dispersion identity.  EH coefficient is M2/8.  O_T contributes
# cT*(1/4)y dot(h)^2, so the kinetic multiplier is 1+2 cT y/M2.
kinetic_multiplier = sp.factor(1 + 2*cT*y/M2)
omega2_over_y = sp.factor(1/kinetic_multiplier)
assert sp.simplify(omega2_over_y - 1/(1+2*cT*y/M2)) == 0

out = {
    'classification':'RTK_ROUTE_B_GRADK_TENSOR_NULL_GATE_PASS',
    'scalar_basis':{
        'O_T':'D_l K^i_j D^l K^j_i -> (U,V,W)=(3,1,1)',
        'O_K':'D_i K D^i K -> (9,3,1)',
        'O_D':'D_i K^i_j D_k K^{kj} -> (1,1,1)',
        'inverse':{
            'c_T':'(U-4V+3W)/2',
            'c_K':'(V-W)/2',
            'c_D':'(3V-U)/2'
        }
    },
    'exact_rtk_branch':{
        'R':'K_clock/(H^2 M_*^2) > 0',
        'V_over_W':'(6-R)/4',
        'U_over_W':'[(6-R)/4]^2',
        'c_T_over_W':'(R-2)(R+6)/32',
        'c_K_over_W':'-(R-2)/8',
        'c_D_over_W':'(36-R^2)/32'
    },
    'tensor_null':{
        'condition':'c_T=0 iff R=2 on the positive physical branch',
        'unique_operator_at_R2':'W D_i K^i_j D_k K^{kj}',
        'U_V_W_at_R2':'U=V=W',
        'status':'SPECIAL_SURFACE_ONLY'
    },
    'tt_sector':{
        'O_T_quadratic':'(c_T/4) p^2 dot(h_ij)^2',
        'kinetic_multiplier':'1 + 2 c_T p^2/M_*^2',
        'local_dispersion':'omega_T^2=p^2/[1+2 c_T p^2/M_*^2]'
    },
    'theorem':'Within the full one-grad-K quadratic basis, a pointwise exact scalar RTK match is tensor-clean only on the special surface K_clock/(H^2 M_*^2)=2; otherwise the same coefficient tuple necessarily induces momentum-dependent TT kinetic propagation.',
    'non_claims':[
        'not yet an observational GW exclusion',
        'not a no-go for an additional tensor-only cancellation operator',
        'not a no-go for auxiliary constrained fields',
        'not a no-go for nonminimal/disformal matter',
        'not a proof that R(a) never crosses 2 at an isolated epoch'
    ],
    'next_step':'Evaluate R(a) with the same gravitational normalization as the candidate over the frozen production epoch grid; if R is not identically 2, quantify the induced TT coefficient and test whether any fixed tensor-only companion can cancel it without spoiling the scalar kernel.'
}
print('RTK_ROUTE_B_GRADK_TENSOR_NULL_GATE_PASS', json.dumps(out,sort_keys=True))
