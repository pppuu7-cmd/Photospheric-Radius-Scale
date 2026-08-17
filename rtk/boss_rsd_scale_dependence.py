#!/usr/bin/env python3
"""Measure linear f*sigma8(k,z) scale dependence for RTK and matched LCDM.

Diagnostic only: no likelihood optimization and no survey-window claim.
The output directly quantifies how much the compressed BOSS growth observable can
vary across a representative linear k range under the current model centers.
"""
from pathlib import Path
from bisect import bisect_left
import json, math, re, subprocess

STATE=json.loads(Path('../research/state/current.json').read_text())
OUT=Path('output/boss_rsd_scale_dependence');OUT.mkdir(parents=True,exist_ok=True)
Z_TARGETS=(0.38,0.51,0.61)
K_TARGETS=(0.02,0.03,0.05,0.07,0.10,0.15,0.20)
DENSE=STATE['objective']['dense_z_pk']
ULTRA={k:str(v) for k,v in STATE['objective']['ultra'].items()}

rtk=dict(STATE['rtk']['accepted_center'])
lcdm=dict(STATE['lcdm'].get('accepted_score_params') or STATE['lcdm']['accepted_center'])
MODELS={'RTK':rtk,'LCDM':lcdm}

def ini_text(model,p,root):
    lines=[
      f"h = {p['h']}",
      "T_cmb = 2.7255",
      f"Omega_b = {p['Ob']}",
    ]
    if model=='RTK':
        lines += [f"Omega_khronon = {p['Om']}",f"lambda_D = {p['lam']}","Omega_Lambda = 0.","model = 2."]
    else:
        lines += [f"Omega_cdm = {p['Om']}","model = 0."]
    lines += [
      "N_ur = 3.046","N_ncdm = 0","Omega_k = 0.","Omega_fld = 0.","Omega_scf = 0.",
      "recombination = RECFAST","reio_parametrization = reio_camb",f"z_reio = {p['zre']}",
      "output = mPk","gauge = newtonian",f"A_s = {p['As']}",f"n_s = {p['ns']}",
      "P_k_max_h/Mpc = 5.0",f"z_pk = {DENSE}","z_max_pk = 1.0",f"root = {root}",
      "background_verbose = 1","perturbations_verbose = 0",
    ]
    for k,v in ULTRA.items(): lines.append(f'{k} = {v}')
    return '\n'.join(lines)+'\n'

def pk_load(path):
    rows=[]; header=[]
    for line in Path(path).read_text().splitlines():
        s=line.strip()
        if not s: continue
        if s.startswith('#'):
            header.append(s);continue
        a=s.split();rows.append((float(a[0]),float(a[1])))
    if len(rows)<10: raise RuntimeError(f'too few P(k) rows in {path}')
    return rows,header

def z_from_header(header):
    for line in header:
        m=re.search(r'redshift z=([+\-0-9.eE]+)',line)
        if m:return float(m.group(1))
    raise RuntimeError('P(k) header missing exact redshift')

def interp_logpk(rows,k):
    xs=[r[0] for r in rows];j=bisect_left(xs,k)
    if j<=0 or j>=len(rows):raise RuntimeError(f'k={k} outside P(k) table [{xs[0]},{xs[-1]}]')
    x0,y0=rows[j-1];x1,y1=rows[j]
    lx0,lx1,lk=math.log(x0),math.log(x1),math.log(k)
    ly=math.log(y0)+(math.log(y1)-math.log(y0))*(lk-lx0)/(lx1-lx0)
    return ly

def top_hat(x):
    if abs(x)<1e-3:
        x2=x*x;return 1-x2/10+x2*x2/280
    return 3*(math.sin(x)-x*math.cos(x))/(x*x*x)

def sigma8(rows):
    terms=[]
    for k,p in rows:
        W=top_hat(8*k);terms.append((math.log(k),k**3*p*W*W))
    integ=sum(.5*(terms[i-1][1]+terms[i][1])*(terms[i][0]-terms[i-1][0]) for i in range(1,len(terms)))
    return math.sqrt(integ/(2*math.pi**2))

def derivative3(x0,y0,x1,y1,x2,y2,xt):
    return (y0*(2*xt-x1-x2)/((x0-x1)*(x0-x2))+
            y1*(2*xt-x0-x2)/((x1-x0)*(x1-x2))+
            y2*(2*xt-x0-x1)/((x2-x0)*(x2-x1)))

def qval(xs,ys,x):
    val=0.
    for i in range(3):
        w=1.
        for j in range(3):
            if i!=j:w*=(x-xs[j])/(xs[i]-xs[j])
        val+=ys[i]*w
    return val

def run_model(model,p):
    tag=model.lower();ini=Path(f'{tag}_boss_rsd.ini');root=str(OUT/f'{tag}_')
    ini.write_text(ini_text(model,p,root))
    log=OUT/f'{tag}.log'
    cp=subprocess.run(['./class',str(ini)],stdout=log.open('w'),stderr=subprocess.STDOUT)
    if cp.returncode:raise RuntimeError(f'{model} CLASS failed; see {log}')
    fam={}
    for path in sorted(OUT.glob(f'{tag}_z*_pk.dat')):
        rows,header=pk_load(path);z=z_from_header(header)
        if z in fam:raise RuntimeError(f'duplicate P(k) z={z}')
        fam[z]=rows
    requested=[float(x) for x in DENSE.split(',') if x.strip()]
    for z in requested:
        if not any(abs(zz-z)<1e-12 for zz in fam):raise RuntimeError(f'{model}: missing requested exact z={z}')
    sig={z:sigma8(rows) for z,rows in fam.items()}
    out={}
    for z0 in Z_TARGETS:
        zs=sorted(fam,key=lambda z:abs(z-z0))[:3];zs=sorted(zs)
        # Dense grid is designed so each BOSS target is bracketed by +/-0.01.
        if not (zs[0] < z0 <= zs[-1] and any(abs(z-z0)<1e-12 for z in zs)):
            raise RuntimeError(f'{model}: invalid local z stencil for {z0}: {zs}')
        xs=[math.log(1/(1+z)) for z in zs];xt=math.log(1/(1+z0))
        svals=[sig[z] for z in zs];s8=qval(xs,svals,xt)
        fs8_eff=derivative3(xs[0],svals[0],xs[1],svals[1],xs[2],svals[2],xt)
        vals={}
        for k in K_TARGETS:
            lp=[interp_logpk(fam[z],k) for z in zs]
            f=.5*derivative3(xs[0],lp[0],xs[1],lp[1],xs[2],lp[2],xt)
            vals[str(k)]={'f':f,'fs8':f*s8}
        fs=[v['fs8'] for v in vals.values()]
        mean=sum(fs)/len(fs);spread=max(fs)-min(fs)
        out[str(z0)]={
          'z_stencil':zs,'sigma8':s8,'fs8_eff_dsigma8_dloga':fs8_eff,
          'fs8_by_k_hMpc':vals,'fs8_min':min(fs),'fs8_max':max(fs),'fs8_mean':mean,
          'peak_to_peak_fraction_of_mean':spread/abs(mean),
          'k01_minus_eff':vals['0.1']['fs8']-fs8_eff,
          'k01_minus_eff_fraction':(vals['0.1']['fs8']-fs8_eff)/abs(fs8_eff),
        }
    return out

summary={'stage':'boss-rsd-scale-dependence','objective':STATE['objective']['name'],'state_iteration':STATE.get('iteration'),
         'k_targets_hMpc':K_TARGETS,'z_targets':Z_TARGETS,'centers':MODELS,'models':{}}
for model,p in MODELS.items():summary['models'][model]=run_model(model,p)
for z in map(str,Z_TARGETS):
    r=summary['models']['RTK'][z];l=summary['models']['LCDM'][z]
    summary.setdefault('comparison',{})[z]={
      'RTK_peak_to_peak_percent':100*r['peak_to_peak_fraction_of_mean'],
      'LCDM_peak_to_peak_percent':100*l['peak_to_peak_fraction_of_mean'],
      'RTK_k01_minus_eff_percent':100*r['k01_minus_eff_fraction'],
      'LCDM_k01_minus_eff_percent':100*l['k01_minus_eff_fraction'],
    }
Path('boss_rsd_scale_dependence_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('RTK_BOSS_RSD_SCALE_DEPENDENCE_COMPLETE',json.dumps(summary['comparison'],sort_keys=True))
