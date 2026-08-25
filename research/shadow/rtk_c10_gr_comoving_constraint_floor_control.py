#!/usr/bin/env python3
from __future__ import annotations
import argparse,glob,json
from pathlib import Path
import numpy as np
COLS=['c10gr_k','c10gr_Ccom','c10gr_phi','c10gr_R']

def read(path):
    txt=Path(path).read_text()
    miss=[x for x in COLS if x not in txt]
    if miss: raise RuntimeError(f'missing {miss} in {path}')
    a=np.loadtxt(path); a=a[None,:] if a.ndim==1 else a
    tail=a[:,-len(COLS):]
    return {'a':a[:,1],'k':float(np.mean(tail[:,0])),'c':{n:tail[:,i] for i,n in enumerate(COLS)},'path':path}

def medabs(x): return float(np.median(np.abs(np.asarray(x,float))))
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--glob',required=True); ap.add_argument('--target',required=True); ap.add_argument('--output',required=True); q=ap.parse_args()
    t=json.load(open(q.target)); tabs=sorted([read(p) for p in glob.glob(q.glob)],key=lambda z:z['k'])
    req=list(map(float,t['k_ladder_Mpc_inv']))
    if len(tabs)!=len(req): raise SystemExit(f'k count {len(tabs)} != {len(req)}')
    for z,k in zip(tabs,req):
        if abs(z['k']-k)>1e-12*max(1.,abs(k)): raise SystemExit(f'k mismatch {z["k"]} != {k}')
    epochs=[]
    ref={float(k):float(v) for k,v in t['reference_RT_native_observed_aux_median_abs'].items()}
    for a0 in map(float,t['binding_scale_factors']):
        pts=[]
        for z in tabs:
            vals={n:float(np.interp(a0,z['a'],y)) for n,y in z['c'].items()}
            pts.append({'a':a0,'k':z['k'],**vals})
        gr=medabs([x['c10gr_R'] for x in pts]); rr=ref[a0]; ratio=gr/max(rr,1e-300)
        epochs.append({'a':a0,'median_abs_R_GR':gr,'reference_RT_median_abs':rr,'GR_over_RT_reference':ratio,'points':pts})
    late={e['a']:e for e in epochs if e['a'] in (0.1,0.5)}
    comparable=all(1/3 <= late[a]['GR_over_RT_reference'] <= 3 for a in (0.1,0.5))
    muchsmaller=all(late[a]['GR_over_RT_reference'] <= 0.1 for a in (0.1,0.5))
    if comparable: cls=t['classifications']['comparable']
    elif muchsmaller: cls=t['classifications']['much_smaller']
    else: cls=t['classifications']['otherwise']
    out={'schema':'RTK_C10_GR_COMOVING_CONSTRAINT_FLOOR_CONTROL_RESULT_v1','classification':cls,'target':q.target,'epochs':epochs,'actual_k_values_Mpc_inv':[z['k'] for z in tabs],'production_modified':False,'control_model':0}
    Path(q.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(cls)
    for e in epochs: print('EPOCH',e['a'],'GR=',e['median_abs_R_GR'],'RTref=',e['reference_RT_median_abs'],'ratio=',e['GR_over_RT_reference'])
if __name__=='__main__': main()
