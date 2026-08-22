#!/usr/bin/env python3
"""C8 scoped rolling-background rank theorem for the corrected U(1)+RTK action.

Goal
----
Determine whether the explicit mixed operator

    S_mix = int N sqrt(g) C D_i Theta_U D^i Theta_U

introduces, on the exactly homogeneous rolling RTK background, a new operator
in the lapse-stability cross bracket a={pi_N,H_perp}, or only the same
lapse-gradient structure already covered by the exceptional pure-U(1)
Hamiltonian theorem.

Inputs already CI-verified in this project:
  * corrected full-action bookkeeping: beta0_bare=0 and C q^2=M_Pl^2;
  * neutral RTK sector changes only a={pi_N,H_perp} in the 2x2 cross block B;
  * b,c,d remain the pure-gravity operators weakly.

External Hamiltonian input: Mukohyama et al. arXiv:1504.07357, Eqs. (55)-(63),
state that only a depends on coefficients of L_V[g,a] (including a_i a^i),
while b,c,d do not, and det B is weakly nonzero for arbitrary choices of
those L_V coupling constants on the exceptional eta1=eta2=0 theory.

This gate proves the matching of the rolling S_mix pure-lapse Hessian to an
effective a_i a^i coefficient shift. It therefore establishes rank support on
the homogeneous rolling background at the constraint-Hessian level. It is not
a full nonlinear inhomogeneous coupled-DOF proof.
"""
import json
import sympy as sp

# Homogeneous background quantities; eps tracks perturbative order and n is a
# dimensionless lapse perturbation N=N0(1+eps*n).  dn2 stands for D_i n D^i n.
eps,N0,C,q,Mpl2,dn2=sp.symbols('eps N0 C q Mpl2 dn2', positive=True, finite=True, real=True)
n=sp.symbols('n', finite=True, real=True)

# Holding the homogeneous rolling background dot(Sigma)=N0*q fixed while
# varying the lapse gives Theta=q/(1+eps*n). Its spatial gradient is
# -q*eps*D_i n/(1+eps*n)^2 because q and N0 are spatially homogeneous.
# Hence the exact pure-lapse-gradient density (apart from sqrt(g)) is:
Lmix_grad = N0*C*q**2*eps**2*dn2/(1+eps*n)**3

# The standard acceleration invariant a_i a^i=(D ln N)^2 gives:
Lacc_unit = N0*eps**2*dn2/(1+eps*n)

# Compare their quadratic coefficients in eps.
def coeff2(expr):
    return sp.expand(sp.series(expr,eps,0,3).removeO()).coeff(eps,2)

mix2=sp.simplify(coeff2(Lmix_grad))
acc2=sp.simplify(coeff2(Lacc_unit))
assert mix2 == N0*C*q**2*dn2
assert acc2 == N0*dn2
ratio=sp.simplify(mix2/acc2)
assert ratio == C*q**2

# Exact production RTK matching and corrected bare/effective split.
ratio_rtk=sp.simplify(ratio.subs(C,Mpl2/q**2))
assert ratio_rtk == Mpl2
beta0_bare=sp.Integer(0)
beta0_eff_shift=sp.simplify(2*ratio_rtk/Mpl2)
beta0_eff_total=sp.simplify(beta0_bare+beta0_eff_shift)
assert beta0_eff_shift == 2 and beta0_eff_total == 2

# Cross-block algebra: previous source-support theorem gives only a->a+da.
# The external pure-gravity theorem covers arbitrary coefficients multiplying
# the same a_i a^i operator. We record this as a conditional structural input,
# not as a newly derived statement from SymPy.
ag,bg,cg,dg,da=sp.symbols('a_g b_g c_g d_g delta_a', finite=True)
det_g=sp.expand(ag*dg-bg*cg)
det_c=sp.expand((ag+da)*dg-bg*cg)
assert sp.simplify(det_c-det_g-da*dg)==0

out={
  'classification':'RTK_ROUTE_B_U1_ROLLING_HOMOGENEOUS_RANK_SHIFT_PASS',
  'background':['D_i Sigma_bar=0','D_i q=0','D_i C=0','q=nabla_perp Sigma_bar != 0'],
  'lapse_parameterization':'N=N0(1+eps*n)',
  'quadratic_Smix_lapse_gradient':str(mix2),
  'quadratic_unit_N_a2':str(acc2),
  'effective_acceleration_coefficient':str(ratio_rtk),
  'beta0_bare':0,
  'beta0_eff_shift_from_explicit_Smix':str(beta0_eff_shift),
  'beta0_eff_total':str(beta0_eff_total),
  'cross_block_update':'B_coupled=[[a_g+delta_a,b_g],[c_g,d_g]]',
  'delta_det_B':'delta_a*d_g',
  'external_rank_input':'arXiv:1504.07357 Eqs.(55)-(63): on eta1=eta2=0, only {pi_N,H_perp} depends on L_V[g,a] coefficients and det B is weakly nonzero for arbitrary choices of those coefficients.',
  'result':'On the exactly homogeneous rolling RTK background, the pure-lapse Hessian induced by S_mix is the same a_i a^i operator class as an L_V acceleration-coefficient shift; exact matching gives beta0_eff shift=2 while beta0_bare=0.',
  'interpretation':'Together with the previous source-support theorem and the external arbitrary-L_V rank theorem, the explicit rolling S_mix lapse-gradient contribution does not by itself force a second-class rank loss on the homogeneous RTK background.',
  'non_claims':[
    'does not derive the full nonlinear inhomogeneous Sigma-dependent cross bracket',
    'does not prove absence of rank-changing exceptional inhomogeneous scalar configurations',
    'does not establish PPN, radiative stability, tensor stability, or EFT cutoff',
    'does not turn the published pure-gravity PPN formulae into a full-action PPN certification'
  ],
  'next_gate':'combine generic-rank-slice and homogeneous-rolling-rank results into a scoped classical coupled-DOF certification; then freeze an admissible lambda_HL representative only after checking the DeWitt-metric singular value lambda=1/d and the same-action tensor/IR normalization.'
}
open('u1_rolling_homogeneous_rank_shift_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
