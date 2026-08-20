#!/usr/bin/env python3
"""No-go for globalizing the exact Route-B Minkowski rational embedding by
one fixed constant coefficient tuple across the replay-certified RTK history.

This is deliberately narrow. It does NOT exclude a nonlinear BPS/Hořava
completion on FLRW, where expansion/background-dependent quadratic effective
coefficients can arise from a fixed underlying action. It only forbids the
naive identification of the already-proved Minkowski formulas themselves with
the full time-dependent RTK cosmological pole using one constant tuple.
"""
import json
import sympy as sp

# Fixed positive Minkowski action coefficients.
ell,z,alpha,s,Mstar=sp.symbols('ell z alpha s Mstar', positive=True, finite=True, real=True)
C=sp.simplify(ell/(z*(2+3*ell)))
Mdisp2=sp.simplify(alpha*Mstar**2/s)
# No background/time variable appears: a fixed tuple gives fixed C and Mdisp.
a=sp.symbols('a', positive=True, finite=True, real=True)
assert sp.diff(C,a)==0
assert sp.diff(Mdisp2,a)==0

# Two independently replay-derived production rows from the validated current
# scale-dictionary/hierarchy chain (same objective fingerprint and gamma root).
rows={
  'z0':{'z':0.0,'C':1.4738358401883835e-08,'MK':1.1681315109161161},
  'z1':{'z':1.0,'C':2.302892011135705e-10,'MK':26.431663976834585},
}
assert rows['z0']['C']>0 and rows['z1']['C']>0
assert rows['z0']['MK']>0 and rows['z1']['MK']>0
assert rows['z0']['C'] != rows['z1']['C']
assert rows['z0']['MK'] != rows['z1']['MK']
C_ratio=rows['z0']['C']/rows['z1']['C']
MK_ratio=rows['z1']['MK']/rows['z0']['MK']
assert C_ratio>10 and MK_ratio>10

out={
  'classification':'RTK_ROUTE_B_FIXED_MINKOWSKI_GLOBALIZATION_NOGO_PASS',
  'validated_input_provenance':{
    'scale_dictionary_run_id':32320390501,
    'capped_hierarchy_run_id':32322717923,
    'objective_fingerprint':'754edb2ff5380eff314867b0ecb1a23a8b861a69f7e46070c4b8251c98573666',
    'gamma':0.05170371280716,
  },
  'fixed_minkowski_map':{
    'C':'ell/[z(2+3ell)]',
    'Mdisp2':'alpha M_*^2/s',
    'consequence':'one fixed constant tuple implies time-independent C and Mdisp in the proven Minkowski formula'
  },
  'replay_counterexample':{
    'z0':rows['z0'],'z1':rows['z1'],
    'C_z0_over_C_z1':C_ratio,
    'MK_z1_over_MK_z0':MK_ratio,
  },
  'theorem':'No single fixed constant coefficient tuple in the already-proved Minkowski exact-rational map can reproduce the replay-certified RTK C(a)=c_a^2(a) and Mdisp(a)=M_K(a) at both z=0 and z=1, hence not over the full cosmological history.',
  'interpretation':'The successful pointwise inverse/cutoff/hierarchy gates are instantaneous existence and scale-separation results, not yet a single global cosmological completion.',
  'escape_route':'Derive the scalar quadratic action of a fixed nonlinear BPS/Hořava completion on the RTK/FLRW background and test whether background-dependent effective coefficients reproduce C(a), M_K(a). Alternatively add a justified dynamical operator/field dependence; do not make Wilson coefficients time-dependent by hand.',
  'non_claims':['not a no-go for RTK phenomenology','not a no-go for BPS/Hořava on FLRW','not a statement that fixed microscopic couplings cannot generate background-dependent effective coefficients','does not invalidate the pointwise strong-coupling hierarchy PASS'],
}
print('RTK_ROUTE_B_FIXED_MINKOWSKI_GLOBALIZATION_NOGO_PASS',json.dumps(out,sort_keys=True))
