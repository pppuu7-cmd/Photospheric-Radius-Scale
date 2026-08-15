#!/usr/bin/env python3
"""Aggregate Stage 4D1 fixed-lambda local profile summaries.

Usage:
  python3 aggregate_stage4d1_profile.py SUMMARY.json [SUMMARY.json ...] --out OUTDIR

The tool converts lambda_D to two useful boundary coordinates,
  epsilon_D = lambda_D^(-1/2),
  delta_D   = lambda_D^(-1),
computes Delta S relative to the best supplied fixed-lambda point separately
for each RSD mapping, checks boundary hits, and records nominal threshold
crossings only as shape diagnostics.

For the highest-lambda tail it also performs a simple unweighted diagnostic
fit S(lambda_D) = S_inf + C/lambda_D.  This is motivated by the exact
large-lambda expansion of the normalized Khronon background: although x0 has
an O(epsilon_D) term, the physical density combination x(1+t) cancels at first
order and its leading departure from dust is O(epsilon_D^2)=O(1/lambda_D).
The tail fit is not an inference result and is not used to manufacture a
confidence limit.

The script does not claim Wilks confidence limits because the preferred
direction can terminate at the epsilon_D=0 boundary and the profile points are
local rather than proven global minima.
"""
from pathlib import Path
import csv,json,math,sys

args=sys.argv[1:]
if '--out' in args:
    i=args.index('--out'); out=Path(args[i+1]); files=[Path(x) for x in args[:i]]
else:
    out=Path('stage4d1_profile'); files=[Path(x) for x in args]
if not files: raise SystemExit(__doc__)
out.mkdir(parents=True,exist_ok=True)
rows=[]
for p in files:
    d=json.loads(p.read_text())
    if d.get('stage')!='4D1-fixed-lambda-profile': raise SystemExit(f'{p}: wrong stage')
    lam=float(d['lambda_D']); mapping=d['mapping']
    c=d.get('best_components') or {}; bp=d.get('best_params') or {}
    row={'mapping':mapping,'lambda_D':lam,'epsilon_D':lam**-0.5,'delta_D':1.0/lam,
         'best_S':float(d['best_S']),'status':d.get('status'),
         'boundary_axes':';'.join(d.get('boundary_axes') or []),
         'poll_improvement':d.get('poll_improvement'),'exact_likelihood_calls':d.get('exact_likelihood_calls')}
    for k in ('h','Ob','Om','As','ns','zre'):row[k]=bp.get(k)
    for k in ('logL_planck','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','rd'):row[k]=c.get(k)
    rows.append(row)
if {r['mapping'] for r in rows}!={'eff','k01'}: raise SystemExit('both mappings required')


def linear_fit(xs,ys):
    n=len(xs)
    if n<2:return None
    xb=sum(xs)/n; yb=sum(ys)/n
    den=sum((x-xb)**2 for x in xs)
    if den==0:return None
    slope=sum((x-xb)*(y-yb) for x,y in zip(xs,ys))/den
    intercept=yb-slope*xb
    residuals=[y-(intercept+slope*x) for x,y in zip(xs,ys)]
    rms=math.sqrt(sum(r*r for r in residuals)/n)
    return {'S_inf_intercept':intercept,'C_over_lambda_slope':slope,'rms_residual':rms,'n_points':n}

report={'stage':'4D1-profile-aggregate',
        'scope':'assembled local fixed-lambda profile; not global posterior/evidence',
        'boundary_coordinates':{'epsilon_D':'lambda_D^(-1/2)','delta_D':'lambda_D^(-1)'},
        'mappings':{}}
for mapping in ('eff','k01'):
    rr=sorted([r for r in rows if r['mapping']==mapping],key=lambda r:r['lambda_D'])
    best=min(r['best_S'] for r in rr)
    for r in rr:r['DeltaS_from_best_supplied']=r['best_S']-best
    boundaries=[r['lambda_D'] for r in rr if r['boundary_axes']]
    monotonic=all(rr[i+1]['best_S']<=rr[i]['best_S']+0.03 for i in range(len(rr)-1))

    # Diagnostic interpolation in log lambda only. Not a confidence construction.
    crossings={}
    for T in (1.0,2.71,3.84):
        cross=None
        for a,b in zip(rr[:-1],rr[1:]):
            da=a['DeltaS_from_best_supplied'];db=b['DeltaS_from_best_supplied']
            if (da-T)*(db-T)<=0 and da!=db:
                x0=math.log(a['lambda_D']);x1=math.log(b['lambda_D'])
                t=(T-da)/(db-da);cross=math.exp(x0+t*(x1-x0));break
        crossings[str(T)]=cross

    # Leading large-lambda background departures are O(1/lambda_D).  Use the
    # three largest supplied lambda values only, keeping this explicitly
    # diagnostic rather than treating the intercept as a measured likelihood.
    tail=rr[-min(3,len(rr)):]
    tailfit=linear_fit([1.0/r['lambda_D'] for r in tail],[r['best_S'] for r in tail])
    if tailfit:
        tailfit['lambda_values']=[r['lambda_D'] for r in tail]
        tailfit['last_point_minus_S_inf']=rr[-1]['best_S']-tailfit['S_inf_intercept']
        tailfit['warning']='Unweighted asymptotic-shape diagnostic only; not a confidence or evidence calculation.'

    report['mappings'][mapping]={
        'best_supplied_S':best,
        'best_supplied_lambda_D':min(rr,key=lambda r:r['best_S'])['lambda_D'],
        'monotonic_nonincreasing_with_lambda_with_0p03_tolerance':monotonic,
        'boundary_hit_lambda_values':boundaries,
        'diagnostic_loglambda_threshold_crossings':crossings,
        'diagnostic_inverse_lambda_tail_fit':tailfit,
        'warning':'Threshold crossings and asymptotic fits are numerical profile-shape diagnostics, not confidence limits.'}

fields=[]
for r in rows:
    for k in r:
        if k not in fields:fields.append(k)
with (out/'stage4d1_profile.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(sorted(rows,key=lambda r:(r['mapping'],r['lambda_D'])))
(out/'stage4d1_profile.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')

md=['# RT+DBI-Khronon — Stage 4D1 fixed-lambda profile','',
    'This is an assembled set of locally optimized fixed-lambda points. It is not a global posterior, global profile likelihood, confidence interval, exclusion significance, or Bayesian evidence.','',
    'Boundary coordinates: `epsilon_D=lambda_D^(-1/2)` and `delta_D=1/lambda_D`. The latter tracks the leading large-lambda departure of the normalized Khronon density from dust.','']
for mapping in ('eff','k01'):
    md += [f'## {mapping}','','| lambda_D | epsilon_D | delta_D | S | Delta S | boundary |','|---:|---:|---:|---:|---:|---|']
    for r in sorted([x for x in rows if x['mapping']==mapping],key=lambda x:x['lambda_D']):
        md.append(f"| {r['lambda_D']:.8g} | {r['epsilon_D']:.8g} | {r['delta_D']:.8g} | {r['best_S']:.8f} | {r['DeltaS_from_best_supplied']:.6f} | {r['boundary_axes'] or 'none'} |")
    info=report['mappings'][mapping]
    md += ['',f"Monotonic non-increasing with lambda (0.03 tolerance): **{info['monotonic_nonincreasing_with_lambda_with_0p03_tolerance']}**.",'']
    tf=info.get('diagnostic_inverse_lambda_tail_fit')
    if tf:
        md += [f"Diagnostic high-lambda fit: `S ~= {tf['S_inf_intercept']:.8f} + ({tf['C_over_lambda_slope']:.8g})/lambda_D`, RMS={tf['rms_residual']:.4g}.",
               f"Largest supplied point minus fitted S_inf: `{tf['last_point_minus_S_inf']:.6g}`.",
               'This extrapolation is a tail-shape diagnostic only.','']
(out/'STAGE4D1_PROFILE.md').write_text('\n'.join(md)+'\n')
print(json.dumps(report,indent=2,sort_keys=True))
