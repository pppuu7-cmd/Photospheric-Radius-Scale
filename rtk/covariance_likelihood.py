#!/usr/bin/env python3
"""Covariance-aware Pantheon + BOSS DR12 diagnostic for RT+DBI-Khronon.

This stage upgrades the previous diagonal coarse ranking:
  * Pantheon 40-bin: official systematic covariance + diagonal statistical dmb^2;
    the additive SN magnitude/H0 nuisance offset is minimized analytically.
  * BOSS DR12 final consensus: official 9x9 covariance of
    [DM*r_fid/r_d, H*r_d/r_fid, f*sigma8] at z=0.38,0.51,0.61.

RTK has scale-dependent growth, so compressed BOSS f*sigma8 is not a strictly
survey-independent observable for this model. We therefore report two mappings:
  (a) fs8_eff = d sigma8 / d ln a,
  (b) fs8_k0p1 = f(k=0.1 h/Mpc)*sigma8.
Neither substitutes for a full survey-window reanalysis.
"""
from pathlib import Path
from bisect import bisect_left
import csv
import math
import re

OUT = Path('output')
PANTHEON = Path('pantheon/Binned_data')
BOSS_DATA = Path('boss_DR12Consensus_final.dat')
BOSS_COV = Path('final_consensus_covtot_dM_Hz_fsig.txt')
C_KM_S = 299792.458
R_FID = 147.78

MODELS = [
    ('LCDM', None, 'lcdm', Path('../lcdm_run.log')),
    ('RTK', 1000.0, 'rtk1', Path('../rtk1_run.log')),
    ('RTK', 2000.0, 'rtk2', Path('../rtk2_run.log')),
    ('RTK', 3000.0, 'rtk3', Path('../rtk3_run.log')),
    ('RTK', 4000.0, 'rtk4', Path('../rtk4_run.log')),
    ('RTK', 5000.0, 'rtk5', Path('../rtk5_run.log')),
    ('RTK', 6000.0, 'rtk6', Path('../rtk6_run.log')),
    ('RTK', 7000.0, 'rtk7', Path('../rtk7_run.log')),
    ('RTK', 8000.0, 'rtk8', Path('../rtk8_run.log')),
    ('RTK', 10000.0, 'rtk', Path('../rtk_run.log')),
    ('RTK', 12500.0, 'rtk125', Path('../rtk125_run.log')),
    ('RTK', 15000.0, 'rtk15', Path('../rtk15_run.log')),
    ('RTK', 20000.0, 'rtk20', Path('../rtk20_run.log')),
]


def numeric_rows(path, min_cols=1):
    rows=[]
    for line in Path(path).read_text().splitlines():
        s=line.strip()
        if not s or s.startswith('#'):
            continue
        vals=[float(x) for x in s.split()]
        if len(vals)>=min_cols:
            rows.append(vals)
    return rows


def cholesky(A):
    n=len(A)
    L=[[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1):
            s=sum(L[i][k]*L[j][k] for k in range(j))
            if i==j:
                v=A[i][i]-s
                if not (v>0.0 and math.isfinite(v)):
                    raise RuntimeError(f'covariance not positive definite at {i}: {v}')
                L[i][j]=math.sqrt(v)
            else:
                L[i][j]=(A[i][j]-s)/L[j][j]
    return L


def chol_solve(L,b):
    n=len(L)
    y=[0.0]*n
    for i in range(n):
        y[i]=(b[i]-sum(L[i][j]*y[j] for j in range(i)))/L[i][i]
    x=[0.0]*n
    for i in range(n-1,-1,-1):
        x[i]=(y[i]-sum(L[j][i]*x[j] for j in range(i+1,n)))/L[i][i]
    return x


def quad(L,v):
    x=chol_solve(L,v)
    return sum(a*b for a,b in zip(v,x))


def load_background(prefix):
    rows=numeric_rows(OUT/f'{prefix}_background.dat',8)
    rows.sort(key=lambda r:r[0])
    return rows


def interp_rows(rows,col,z):
    zs=[r[0] for r in rows]
    if z<=zs[0]: return rows[0][col]
    if z>=zs[-1]: return rows[-1][col]
    j=bisect_left(zs,z)
    z0,z1=zs[j-1],zs[j]
    y0,y1=rows[j-1][col],rows[j][col]
    return y0+(z-z0)*(y1-y0)/(z1-z0)


def parse_drag(log_path):
    z_d=r_d=None
    zr=re.compile(r'baryon drag stops at z\s*=\s*([0-9eE+\-.]+)')
    rr=re.compile(r'with comoving sound horizon rs\s*=\s*([0-9eE+\-.]+)\s*Mpc')
    for line in Path(log_path).read_text().splitlines():
        m=zr.search(line)
        if m: z_d=float(m.group(1))
        m=rr.search(line)
        if m and z_d is not None: r_d=float(m.group(1))
    if z_d is None or r_d is None:
        raise RuntimeError(f'could not parse z_d/r_d from {log_path}')
    return z_d,r_d


def load_pantheon():
    dat=numeric_rows(PANTHEON/'lcparam_DS17f.txt',6)
    if len(dat)!=40: raise RuntimeError(f'expected 40 Pantheon bins, got {len(dat)}')
    raw=[]
    for line in (PANTHEON/'sys_DS17f.txt').read_text().splitlines():
        s=line.strip()
        if s and not s.startswith('#'): raw.extend(float(x) for x in s.split())
    n=int(raw[0]); vals=raw[1:]
    if n!=40 or len(vals)!=n*n:
        raise RuntimeError(f'bad Pantheon covariance dimensions n={n}, vals={len(vals)}')
    C=[vals[i*n:(i+1)*n] for i in range(n)]
    for i,row in enumerate(dat):
        dmb=row[5]
        C[i][i]+=dmb*dmb
    return dat,cholesky(C)


def sn_fullcov(bg,dat,L):
    d=[]
    for r in dat:
        z,mb=r[1],r[4]
        dl=interp_rows(bg,6,z)
        mu=5.0*math.log10(dl)+25.0
        d.append(mb-mu)
    ones=[1.0]*len(d)
    Cid=chol_solve(L,d); Ci1=chol_solve(L,ones)
    denom=sum(Ci1)
    offset=sum(Cid)/denom
    res=[x-offset for x in d]
    return quad(L,res),offset,max(abs(x) for x in res)


def load_growth():
    with (OUT/'growth_scan.csv').open(newline='') as f:
        return list(csv.DictReader(f))


def growth_subset(growth,model,lam):
    rows=[]
    for r in growth:
        if r['model']!=model: continue
        if model=='RTK' and abs(float(r['lambda_D'])-lam)>1e-6: continue
        rows.append(r)
    rows.sort(key=lambda r:float(r['z']))
    return rows


def interp_growth(rows,col,z):
    pts=[(float(r['z']),float(r[col])) for r in rows]
    zs=[x for x,_ in pts]
    if z<=zs[0]: return pts[0][1]
    if z>=zs[-1]: return pts[-1][1]
    j=bisect_left(zs,z)
    z0,y0=pts[j-1]; z1,y1=pts[j]
    return y0+(z-z0)*(y1-y0)/(z1-z0)


def load_boss():
    obs=[]
    for line in BOSS_DATA.read_text().splitlines():
        s=line.strip()
        if not s or s.startswith('#'): continue
        z,val,kind=s.split()[:3]
        obs.append((float(z),float(val),kind))
    C=numeric_rows(BOSS_COV,9)
    if len(obs)!=9 or len(C)!=9 or any(len(r)!=9 for r in C):
        raise RuntimeError('BOSS vector/covariance must be 9-dimensional')
    return obs,cholesky(C)


def boss_prediction(bg,r_d,grows,fscol,obs):
    pred=[]
    for z,_,kind in obs:
        if kind=='DM_over_rs':
            dm=interp_rows(bg,4,z)
            pred.append(dm*R_FID/r_d)
        elif kind=='bao_Hz_rs':
            h_km=interp_rows(bg,3,z)*C_KM_S
            pred.append(h_km*r_d/R_FID)
        elif kind=='f_sigma8':
            pred.append(interp_growth(grows,fscol,z))
        else:
            raise RuntimeError(f'unknown BOSS observable {kind}')
    return pred


def boss_fullcov(bg,r_d,grows,fscol,obs,L):
    pred=boss_prediction(bg,r_d,grows,fscol,obs)
    data=[v for _,v,_ in obs]
    res=[p-d for p,d in zip(pred,data)]
    return quad(L,res),pred,res


def write_csv(path,rows):
    with Path(path).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

pantheon,Lsn=load_pantheon()
boss_obs,Lboss=load_boss()
growth=load_growth()
rows=[]; boss_rows=[]
for model,lam,prefix,log_path in MODELS:
    bg=load_background(prefix)
    zd,rd=parse_drag(log_path)
    sn,off,maxres=sn_fullcov(bg,pantheon,Lsn)
    grows=growth_subset(growth,model,lam)
    b_eff,p_eff,r_eff=boss_fullcov(bg,rd,grows,'fs8_eff',boss_obs,Lboss)
    b_k01,p_k01,r_k01=boss_fullcov(bg,rd,grows,'fs8_k0p1',boss_obs,Lboss)
    rows.append({
        'model':model,'lambda_D':'' if lam is None else lam,'z_drag':zd,'rd_Mpc':rd,
        'chi2_SN_fullcov':sn,'chi2_BOSS_fullcov_eff':b_eff,'chi2_BOSS_fullcov_k0p1':b_k01,
        'chi2_SNplusBOSS_eff':sn+b_eff,'chi2_SNplusBOSS_k0p1':sn+b_k01,
        'SN_offset':off,'SN_max_abs_residual_mag':maxres})
    for i,(z,val,kind) in enumerate(boss_obs):
        boss_rows.append({'model':model,'lambda_D':'' if lam is None else lam,'index':i,
                          'z':z,'observable':kind,'data':val,
                          'pred_eff':p_eff[i],'residual_eff':r_eff[i],
                          'pred_k0p1':p_k01[i],'residual_k0p1':r_k01[i]})

lcdm=rows[0]
for r in rows:
    for col in ['chi2_SN_fullcov','chi2_BOSS_fullcov_eff','chi2_BOSS_fullcov_k0p1',
                'chi2_SNplusBOSS_eff','chi2_SNplusBOSS_k0p1']:
        r['delta_'+col]=r[col]-lcdm[col]

write_csv(OUT/'covariance_likelihood_summary.csv',rows)
write_csv(OUT/'boss_fullcov_predictions.csv',boss_rows)

print('COVARIANCE LIKELIHOOD DIAGNOSTIC')
print('Pantheon: official 40-bin systematic covariance + diagonal dmb^2; additive magnitude offset minimized analytically.')
print('BOSS DR12: official final-consensus 9x9 covariance for DM, H, f*sigma8.')
print('RTK f*sigma8 mapping remains an approximation because growth is scale dependent; eff and k=0.1 versions are both reported.')
print('model lambda chi2_SN chi2_BOSS_eff chi2_BOSS_k01 delta_total_eff delta_total_k01')
for r in rows:
    lam='-' if r['lambda_D']=='' else f"{float(r['lambda_D']):.0f}"
    print(f"{r['model']:4s} {lam:6s} {r['chi2_SN_fullcov']:10.4f} {r['chi2_BOSS_fullcov_eff']:14.4f} "
          f"{r['chi2_BOSS_fullcov_k0p1']:14.4f} {r['delta_chi2_SNplusBOSS_eff']:15.4f} "
          f"{r['delta_chi2_SNplusBOSS_k0p1']:16.4f}")
rtk=[r for r in rows if r['model']=='RTK']
best_eff=min(rtk,key=lambda r:r['chi2_SNplusBOSS_eff'])
best_k=min(rtk,key=lambda r:r['chi2_SNplusBOSS_k0p1'])
print(f"BEST_EFF lambda_D={float(best_eff['lambda_D']):.0f} delta={best_eff['delta_chi2_SNplusBOSS_eff']:.6f}")
print(f"BEST_K01 lambda_D={float(best_k['lambda_D']):.0f} delta={best_k['delta_chi2_SNplusBOSS_k0p1']:.6f}")
print('COVARIANCE_LIKELIHOOD_PASS')
