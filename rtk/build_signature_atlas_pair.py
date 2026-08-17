#!/usr/bin/env python3
"""Build a provisional matched RTK-vs-LCDM observable signature fingerprint.

This is a theory-output comparison at the current accepted centers.  It is not
an additional likelihood, optimizer, posterior, or model-selection statistic.
Both models are run with the same frozen dense-z and ultra precision settings.
"""
from __future__ import annotations

from bisect import bisect_left
from pathlib import Path
import json, math, re, subprocess

ROOT=Path('.')
STATE=json.loads(Path('../research/state/current.json').read_text())
OUT=Path('output/signature_atlas');OUT.mkdir(parents=True,exist_ok=True)
DENSE=STATE['objective']['dense_z_pk']
ULTRA={k:str(v) for k,v in STATE['objective']['ultra'].items()}
ELL_TARGETS=[30,100,500,1000,2000]
K_TARGETS=[0.01,0.05,0.1,0.2,0.5]
Z_TARGETS=[0.0,0.38,0.51,0.61,1.0]
GROWTH_Z=[0.38,0.51,0.61]


def make_ini(model,p,tag):
    lines=[f"h = {p['h']}","T_cmb = 2.7255",f"Omega_b = {p['Ob']}"]
    if model=='RTK':
        lines += [f"Omega_khronon = {p['Om']}",f"lambda_D = {p['lam']}","Omega_Lambda = 0.","model = 2."]
    else:
        lines += [f"Omega_cdm = {p['Om']}","model = 0."]
    lines += [
        "N_ur = 3.046","N_ncdm = 0","Omega_k = 0.","Omega_fld = 0.","Omega_scf = 0.",
        "recombination = RECFAST","reio_parametrization = reio_camb",f"z_reio = {p['zre']}",
        "output = tCl,pCl,lCl,mPk","lensing = yes","gauge = newtonian",
        f"A_s_ad = {p['As']}",f"n_s_ad = {p['ns']}","l_max_scalars = 2600","P_k_max_h/Mpc = 5.0",
        f"z_pk = {DENSE}","z_max_pk = 1.0",f"root = output/signature_atlas/{tag}_",
        "background_verbose = 1","thermodynamics_verbose = 1","perturbations_verbose = 0","write background = yes"
    ]
    lines += [f"{k} = {v}" for k,v in ULTRA.items()]
    path=Path(f'signature_{tag}.ini');path.write_text('\n'.join(lines)+'\n');return path


def numeric_rows(path,min_cols=1):
    rows=[]
    for line in Path(path).read_text().splitlines():
        s=line.strip()
        if not s or s.startswith('#'):continue
        a=[float(x) for x in s.split()]
        if len(a)>=min_cols:rows.append(a)
    return rows


def interp_rows(rows,col,z):
    zs=[r[0] for r in rows]
    if z<=zs[0]:return rows[0][col]
    if z>=zs[-1]:return rows[-1][col]
    j=bisect_left(zs,z);z0,z1=zs[j-1],zs[j];y0,y1=rows[j-1][col],rows[j][col]
    return y0+(z-z0)*(y1-y0)/(z1-z0)


def pk_load(path):
    rows=[]
    for line in Path(path).read_text().splitlines():
        s=line.strip()
        if not s or s.startswith('#'):continue
        a=s.split();rows.append((float(a[0]),float(a[1])))
    return rows


def z_from_pk(path):
    for line in Path(path).read_text().splitlines()[:12]:
        m=re.search(r'redshift z=([+\-0-9.eE]+)',line)
        if m:return float(m.group(1))
    raise RuntimeError(f'no z in {path}')


def interp_pk(rows,k):
    xs=[r[0] for r in rows];j=bisect_left(xs,k)
    if j==0:return rows[0][1]
    if j>=len(rows):return rows[-1][1]
    x0,y0=rows[j-1];x1,y1=rows[j];return y0+(k-x0)*(y1-y0)/(x1-x0)


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


def growth(fam):
    sig={z:sigma8(r) for z,r in fam.items()};out={}
    for z0 in GROWTH_Z:
        znear=sorted(fam,key=lambda z:abs(z-z0))[:3];znear=sorted(znear)
        xp=[math.log(1/(1+z)) for z in znear];sp=[sig[z] for z in znear]
        xt=math.log(1/(1+z0))
        fs8=derivative3(xp[0],sp[0],xp[1],sp[1],xp[2],sp[2],xt)
        lp=[(math.log(1/(1+z)),math.log(interp_pk(fam[z],0.1))) for z in znear]
        f01=.5*derivative3(lp[0][0],lp[0][1],lp[1][0],lp[1][1],lp[2][0],lp[2][1],xt)
        # quadratic interpolation sigma8 at target
        s8=0.0
        for i in range(3):
            w=1.0
            for j in range(3):
                if i!=j:w*=(xt-xp[j])/(xp[i]-xp[j])
            s8+=sp[i]*w
        out[str(z0)]={'fs8_eff':fs8,'fs8_k01':f01*s8,'sigma8':s8}
    return out


def parse_cls(path):
    d={}
    for r in numeric_rows(path,5):
        ell=int(r[0]);d[ell]={'TT':r[1],'EE':r[2],'BB':r[3],'TE':r[4]}
    return d


def parse_drag(log):
    rd=None
    for line in Path(log).read_text().splitlines():
        m=re.search(r'with comoving sound horizon rs\s*=\s*([0-9eE+\-.]+)',line)
        if m:rd=float(m.group(1))
    return rd


def run_model(model,p,tag):
    ini=make_ini(model,p,tag);log=Path(f'signature_{tag}.log')
    with log.open('w') as f:cp=subprocess.run(['./class',str(ini)],stdout=f,stderr=subprocess.STDOUT)
    if cp.returncode:raise RuntimeError(f'{model} CLASS failed; see {log}')
    bg=numeric_rows(OUT/f'{tag}_background.dat',8);bg.sort(key=lambda r:r[0])
    fam={}
    for path in OUT.glob(f'{tag}_z*_pk.dat'):fam[z_from_pk(path)]=pk_load(path)
    cls=parse_cls(OUT/f'{tag}_cl_lensed.dat')
    return {
        'params':p,'rd':parse_drag(log),
        'background':{str(z):{'H_over_c_Mpc_inv':interp_rows(bg,3,z),'D_M_Mpc':interp_rows(bg,4,z)} for z in Z_TARGETS},
        'cmb':{str(ell):cls[ell] for ell in ELL_TARGETS},
        'pk':{str(z):{str(k):interp_pk(fam[min(fam,key=lambda zz:abs(zz-z))],k) for k in K_TARGETS} for z in [0.0,0.38,0.61,1.0]},
        'growth':growth(fam),
        'available_pk_redshifts':sorted(fam)
    }


def ratio(a,b):return a/b-1.0

def build_residuals(rtk,lcdm):
    out={'background':{},'cmb':{},'pk':{},'growth':{},'rd_fractional':ratio(rtk['rd'],lcdm['rd'])}
    for z in rtk['background']:
        out['background'][z]={k:ratio(rtk['background'][z][k],lcdm['background'][z][k]) for k in rtk['background'][z]}
    for ell in rtk['cmb']:
        a=rtk['cmb'][ell];b=lcdm['cmb'][ell]
        norm=math.sqrt(abs(b['TT']*b['EE'])) if b['TT'] and b['EE'] else float('nan')
        out['cmb'][ell]={
            'TT_fractional':ratio(a['TT'],b['TT']),
            'EE_fractional':ratio(a['EE'],b['EE']),
            'TE_delta_over_LCDM_sqrt_TT_EE':(a['TE']-b['TE'])/norm
        }
    for z in rtk['pk']:
        out['pk'][z]={k:ratio(rtk['pk'][z][k],lcdm['pk'][z][k]) for k in rtk['pk'][z]}
    for z in rtk['growth']:
        out['growth'][z]={k:ratio(rtk['growth'][z][k],lcdm['growth'][z][k]) for k in rtk['growth'][z]}
    return out


def main():
    rtk_center=dict(STATE['rtk']['accepted_center'])
    lcdm_center=dict(STATE['lcdm']['accepted_center'])
    rtk=run_model('RTK',rtk_center,'rtk')
    lcdm=run_model('LCDM',lcdm_center,'lcdm')
    payload={
        'status':'PROVISIONAL_SIGNATURE_PAIR_NOT_MODEL_SELECTION',
        'objective':STATE['objective']['name'],'state_iteration':STATE.get('iteration'),
        'production_mapping':STATE.get('production_mapping'),'precision':STATE['objective']['ultra'],'dense_z_pk':DENSE,
        'parameter_semantics':'accepted_center for each model; RTK stationarity still pending at time of design',
        'rtk':rtk,'lcdm':lcdm,'residual_rtk_over_lcdm_minus_one':build_residuals(rtk,lcdm),
        'warning':'Observable fingerprint only. Do not interpret selected-bin residuals as preference/significance.'
    }
    (OUT/'current_pair.json').write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
    print('RTK_SIGNATURE_ATLAS_PAIR',json.dumps(payload['residual_rtk_over_lcdm_minus_one'],sort_keys=True))
    print('RTK_SIGNATURE_ATLAS_COMPLETE')

if __name__=='__main__':main()
