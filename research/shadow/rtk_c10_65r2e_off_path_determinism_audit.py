#!/usr/bin/env python3
from __future__ import annotations
import argparse, glob, json
from pathlib import Path


def numeric(path):
    return [s.strip() for s in Path(path).read_text().splitlines()
            if s.strip() and not s.lstrip().startswith('#')]


def compare(pa,pb):
    a=sorted(glob.glob(pa)); b=sorted(glob.glob(pb))
    if len(a)!=4 or len(b)!=4:
        raise RuntimeError(f'expected four files per side: {pa} -> {len(a)}, {pb} -> {len(b)}')
    rec=[]; exact=True; shape=True; gabs=0.; grel=0.
    for af,bf in zip(a,b):
        ar=numeric(af); br=numeric(bf)
        same_rows=len(ar)==len(br); shape &= same_rows
        fexact=(ar==br); exact &= fexact
        ma=0.; mr=0.; first=None; token_shape=True
        for ri,(x,y) in enumerate(zip(ar,br)):
            xs=x.split(); ys=y.split()
            if len(xs)!=len(ys):
                token_shape=False; shape=False
                if first is None: first={'row':ri,'kind':'token_count','a':len(xs),'b':len(ys)}
                continue
            for ci,(sx,sy) in enumerate(zip(xs,ys)):
                if sx==sy: continue
                try:
                    vx=float(sx); vy=float(sy)
                    da=abs(vx-vy); dr=da/max(abs(vx),abs(vy),1e-300)
                    ma=max(ma,da); mr=max(mr,dr); gabs=max(gabs,da); grel=max(grel,dr)
                    if first is None: first={'row':ri,'column_index':ci,'a':vx,'b':vy,'abs':da,'rel':dr}
                except ValueError:
                    if first is None: first={'row':ri,'column_index':ci,'a_text':sx,'b_text':sy}
        rec.append({'a':af,'b':bf,'exact_numeric_text_identity':fexact,
                    'same_row_count':same_rows,'token_shape_same':token_shape,
                    'max_abs':ma,'max_rel':mr,'first_difference':first})
    return {'exact_numeric_text_identity_all_four':exact,'shape_same_all_four':shape,
            'max_abs_all_four':gabs,'max_rel_all_four':grel,'files':rec}


def main():
    ap=argparse.ArgumentParser()
    for n in ('same2a','same2b','build2a','build2b','r1_2','r2_2',
              'same1a','same1b','build1a','build1b','r1_1','r2_1'):
        ap.add_argument('--'+n.replace('_','-'),dest=n,required=True)
    ap.add_argument('--output',required=True)
    a=ap.parse_args()
    tests={
      'same_binary_2threads':compare(a.same2a,a.same2b),
      'independent_r1_builds_2threads':compare(a.build2a,a.build2b),
      'r1_vs_dormant_r2_2threads':compare(a.r1_2,a.r2_2),
      'same_binary_1thread':compare(a.same1a,a.same1b),
      'independent_r1_builds_1thread':compare(a.build1a,a.build1b),
      'r1_vs_dormant_r2_1thread':compare(a.r1_1,a.r2_1),
    }
    same_exact=tests['same_binary_2threads']['exact_numeric_text_identity_all_four'] and tests['same_binary_1thread']['exact_numeric_text_identity_all_four']
    builds_exact=tests['independent_r1_builds_2threads']['exact_numeric_text_identity_all_four'] and tests['independent_r1_builds_1thread']['exact_numeric_text_identity_all_four']
    r2_exact=tests['r1_vs_dormant_r2_2threads']['exact_numeric_text_identity_all_four'] and tests['r1_vs_dormant_r2_1thread']['exact_numeric_text_identity_all_four']
    if not same_exact:
        cls='C10_65R2E_BASELINE_RUNTIME_NONDETERMINISM_SCOPED'
    elif not builds_exact:
        cls='C10_65R2E_BUILD_LAYOUT_OR_COMPILER_NONREPRODUCIBILITY_SCOPED'
    elif not r2_exact:
        cls='C10_65R2E_DORMANT_R2_CODEGEN_PERTURBATION_SCOPED'
    else:
        cls='C10_65R2E_EXACT_OFF_PATH_REPRODUCIBLE_PASS_SCOPED'
    out={'schema':'RTK_C10_65R2E_OFF_PATH_DETERMINISM_AUDIT_RESULT_v1',
         'gate':'C10.65r2e','classification':cls,'tests':tests,
         'summary':{'same_binary_exact_both_thread_modes':same_exact,
                    'independent_r1_builds_exact_both_thread_modes':builds_exact,
                    'r1_vs_dormant_r2_exact_both_thread_modes':r2_exact},
         'interpretation':'Diagnostic only. Original frozen C10.65r2 criteria remain unchanged.',
         'next':'If same-binary and independent-r1 controls are exact while r2 OFF is not, isolate code-generation perturbation by moving diagnostic arithmetic out of the production perturbations translation unit and rerun the original frozen C10.65r2 target unchanged.'}
    Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(cls,json.dumps(out['summary'],sort_keys=True))

if __name__=='__main__': main()
