#!/usr/bin/env python3
"""Preliminary coordinate profile of RTK and LCDM against Planck+Pantheon+BOSS.

This is a deterministic local profile, not an MCMC/posterior. Planck uses the
official 2018 baseline Commander lowT + SimAll lowE + nuisance-marginalized
Plik-lite TTTEEE through clipy. Remaining likelihood calibration/default
parameters are fixed to the distributed likelihood defaults. Pantheon uses its
40-bin full covariance. BOSS DR12 uses the full 9x9 consensus covariance with
the RTK fs8_eff mapping; the alternative k=0.1 mapping is also recorded.
"""
from pathlib import Path
from bisect import bisect_left
import csv, math, os, re, subprocess, sys
os.environ.setdefault('CLIPY_NOJAX','1')
import numpy as np
import clipy

ROOT=Path('.')
OUT=Path('output/profile'); OUT.mkdir(parents=True,exist_ok=True)
PLANCK=Path(sys.argv[1]) if len(sys.argv)>1 else Path('planck_data')
BASE=PLANCK/'baseline'
TCMB=2.7255; UK2=(TCMB*1e6)**2; C_KM_S=299792.458; R_FID=147.78
PANTHEON=Path('pantheon/Binned_data')
BOSS_DATA=Path('boss_DR12Consensus_final.dat'); BOSS_COV=Path('final_consensus_covtot_dM_Hz_fsig.txt')

LIKES={
 'lowT':clipy.clik(str(BASE/'plc_3.0/low_l/commander/commander_dx12_v3_2_29.clik')),
 'lowE':clipy.clik(str(BASE/'plc_3.0/low_l/simall/simall_100x143_offlike5_EE_Aplanck_B.clik')),
 'high':clipy.clik(str(BASE/'plc_3.0/hi_l/plik_lite/plik_lite_v22_TTTEEE.clik')),
}


def numeric_rows(path,min_cols=1):
    rows=[]
    for line in Path(path).read_text().splitlines():
        s=line.strip()
        if not s or s.startswith('#'): continue
        vals=[float(x) for x in s.split()]
        if len(vals)>=min_cols: rows.append(vals)
    return rows

def cholesky(A):
    n=len(A); L=[[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1):
            s=sum(L[i][k]*L[j][k] for k in range(j))
            if i==j:
                v=A[i][i]-s
                if not v>0: raise RuntimeError('non-positive covariance')
                L[i][j]=math.sqrt(v)
            else: L[i][j]=(A[i][j]-s)/L[j][j]
    return L

def chol_solve(L,b):
    n=len(L); y=[0.0]*n; x=[0.0]*n
    for i in range(n): y[i]=(b[i]-sum(L[i][j]*y[j] for j in range(i)))/L[i][i]
    for i in range(n-1,-1,-1): x[i]=(y[i]-sum(L[j][i]*x[j] for j in range(i+1,n)))/L[i][i]
    return x

def quad(L,v):
    x=chol_solve(L,v); return sum(a*b for a,b in zip(v,x))

def load_pantheon():
    dat=numeric_rows(PANTHEON/'lcparam_DS17f.txt',6)
    raw=[]
    for line in (PANTHEON/'sys_DS17f.txt').read_text().splitlines():
        s=line.strip()
        if s and not s.startswith('#'): raw.extend(float(x) for x in s.split())
    n=int(raw[0]); vals=raw[1:]; C=[vals[i*n:(i+1)*n] for i in range(n)]
    for i,r in enumerate(dat): C[i][i]+=r[5]*r[5]
    return dat,cholesky(C)
PANTH,L_SN=load_pantheon()

def load_boss():
    obs=[]
    for line in BOSS_DATA.read_text().splitlines():
        s=line.strip()
        if not s or s.startswith('#'): continue
        z,v,k=s.split()[:3]; obs.append((float(z),float(v),k))
    C=numeric_rows(BOSS_COV,9); return obs,cholesky(C)
BOSS,L_BOSS=load_boss()

def interp_rows(rows,col,z):
    zs=[r[0] for r in rows]
    if z<=zs[0]: return rows[0][col]
    if z>=zs[-1]: return rows[-1][col]
    j=bisect_left(zs,z); z0,z1=zs[j-1],zs[j]; y0,y1=rows[j-1][col],rows[j][col]
    return y0+(z-z0)*(y1-y0)/(z1-z0)

def top_hat(x):
    if abs(x)<1e-3:
        x2=x*x; return 1-x2/10+x2*x2/280
    return 3*(math.sin(x)-x*math.cos(x))/(x*x*x)

def sigma8(rows):
    terms=[]
    for k,p in rows:
        W=top_hat(8*k); terms.append((math.log(k),k**3*p*W*W))
    integ=sum(.5*(terms[i-1][1]+terms[i][1])*(terms[i][0]-terms[i-1][0]) for i in range(1,len(terms)))
    return math.sqrt(integ/(2*math.pi**2))

def pk_load(path):
    rows=[]
    for line in Path(path).read_text().splitlines():
        s=line.strip()
        if not s or s.startswith('#'): continue
        a=s.split(); rows.append((float(a[0]),float(a[1])))
    return rows

def z_from_pk(path):
    for line in Path(path).read_text().splitlines()[:10]:
        m=re.search(r'redshift z=([+\-0-9.eE]+)',line)
        if m: return float(m.group(1))
    raise RuntimeError('no z in pk header')
def derivative3(x0,y0,x1,y1,x2,y2,xt):
    return (y0*(2*xt-x1-x2)/((x0-x1)*(x0-x2))+
            y1*(2*xt-x0-x2)/((x1-x0)*(x1-x2))+
            y2*(2*xt-x0-x1)/((x2-x0)*(x2-x1)))
def local_deriv(pts,xt):
    pts=sorted(pts); i=min(range(len(pts)),key=lambda j:abs(pts[j][0]-xt))
    sel=pts[0:3] if i==0 else pts[-3:] if i==len(pts)-1 else pts[i-1:i+2]
    return derivative3(*sel[0],*sel[1],*sel[2],xt)
def interp_pk(rows,k):
    xs=[r[0] for r in rows]; j=bisect_left(xs,k)
    if j==0:return rows[0][1]
    if j>=len(rows):return rows[-1][1]
    x0,y0=rows[j-1];x1,y1=rows[j];return y0+(k-x0)*(y1-y0)/(x1-x0)

def growth_from_prefix(prefix):
    fam={}
    for p in sorted(OUT.glob(prefix+'z*_pk.dat')):
        fam[z_from_pk(p)]=pk_load(p)
    if not fam: raise RuntimeError('no pk family '+prefix)
    sig={z:sigma8(r) for z,r in fam.items()}
    spts=[(math.log(1/(1+z)),s) for z,s in sig.items()]
    result={}
    for z0 in [0.38,0.51,0.61]:
        # interpolate derivative from surrounding requested z grid; target itself need not be tabulated.
        znear=sorted(fam,key=lambda z:abs(z-z0))[:3]
        znear=sorted(znear)
        xp=[math.log(1/(1+z)) for z in znear]
        sp=[sig[z] for z in znear]
        # quadratic derivative at target x
        xt=math.log(1/(1+z0))
        fs=derivative3(xp[0],sp[0],xp[1],sp[1],xp[2],sp[2],xt)
        # sigma8 value quadratic/interp is sufficient; use Lagrange value explicitly
        def qval(xs,ys,x):
            val=0.0
            for i in range(3):
                w=1.0
                for j in range(3):
                    if i!=j:w*= (x-xs[j])/(xs[i]-xs[j])
                val+=ys[i]*w
            return val
        s8=qval(xp,sp,xt)
        lp=[]
        for z in znear: lp.append((math.log(1/(1+z)), math.log(interp_pk(fam[z],0.1))))
        f01=.5*derivative3(lp[0][0],lp[0][1],lp[1][0],lp[1][1],lp[2][0],lp[2][1],xt)
        result[z0]=(fs,f01*s8)
    return result

def planck_cls(path):
    vals={}
    for line in Path(path).read_text().splitlines():
        s=line.strip()
        if not s or s.startswith('#'):continue
        a=s.split(); ell=int(float(a[0])); dl=[float(x) for x in a[1:5]]
        fac=2*math.pi/(ell*(ell+1))*UK2
        vals[ell]=(dl[0]*fac,dl[1]*fac,dl[3]*fac,dl[2]*fac,0.,0.)
    return vals

def clik_vector(L,cls):
    lmax=list(L.get_lmax()); v=np.array(L.default_par,dtype=float,copy=True); off=0
    for spec,lm in enumerate(lmax):
        if lm<0:continue
        arr=np.zeros(lm+1)
        for ell in range(2,lm+1):arr[ell]=cls[ell][spec]
        v[off:off+lm+1]=arr;off+=lm+1
    return v

def planck_loglike(path):
    cls=planck_cls(path); parts={}
    for name,L in LIKES.items(): parts[name]=float(np.asarray(L(clik_vector(L,cls))).reshape(-1)[0])
    return parts,sum(parts.values())
def parse_drag(log):
    zd=rd=None
    for line in Path(log).read_text().splitlines():
        m=re.search(r'baryon drag stops at z\s*=\s*([0-9eE+\-.]+)',line)
        if m:zd=float(m.group(1))
        m=re.search(r'with comoving sound horizon rs\s*=\s*([0-9eE+\-.]+)',line)
        if m and zd is not None:rd=float(m.group(1))
    if rd is None:raise RuntimeError('no drag horizon')
    return zd,rd

def sn_chi2(bg):
    d=[]
    for r in PANTH:
        dl=interp_rows(bg,6,r[1]); d.append(r[4]-(5*math.log10(dl)+25))
    one=[1.]*len(d); Cid=chol_solve(L_SN,d); Ci1=chol_solve(L_SN,one); off=sum(Cid)/sum(Ci1)
    return quad(L_SN,[x-off for x in d])
def boss_chi2(bg,rd,growth,which):
    pred=[]; data=[]
    for z,val,kind in BOSS:
        data.append(val)
        if kind=='DM_over_rs':pred.append(interp_rows(bg,4,z)*R_FID/rd)
        elif kind=='bao_Hz_rs':pred.append(interp_rows(bg,3,z)*C_KM_S*rd/R_FID)
        else:pred.append(growth[z][0 if which=='eff' else 1])
    return quad(L_BOSS,[p-d for p,d in zip(pred,data)])

def make_ini(model,p,tag):
    lines=[
      f"h = {p['h']}","T_cmb = 2.7255",f"Omega_b = {p['Ob']}",
    ]
    if model=='RTK':
        lines += [f"Omega_khronon = {p['Om']}",f"lambda_D = {p['lam']}","Omega_Lambda = 0.","model = 2."]
    else:
        lines += [f"Omega_cdm = {p['Om']}","model = 0."]
    lines += [
      "N_ur = 3.046","N_ncdm = 0","Omega_k = 0.","Omega_fld = 0.","Omega_scf = 0.",
      "recombination = RECFAST","reio_parametrization = reio_camb",f"z_reio = {p['zre']}",
      "output = tCl,pCl,lCl,mPk","lensing = yes","gauge = newtonian",f"A_s_ad = {p['As']}",f"n_s_ad = {p['ns']}",
      "l_max_scalars = 2600","P_k_max_h/Mpc = 5.0",
      "z_pk = 0.,0.25,0.3,0.4,0.5,0.6,0.7,0.75,1.0","z_max_pk = 1.0",
      f"root = output/profile/{tag}_","background_verbose = 1","thermodynamics_verbose = 1","perturbations_verbose = 0","write background = yes"
    ]
    path=Path(f'profile_{tag}.ini');path.write_text('\n'.join(lines)+'\n');return path

CACHE={}; HISTORY=[]; COUNTER=0
def evaluate(model,p):
    global COUNTER
    key=(model,)+tuple(round(float(p[k]),12) for k in ['lam','h','Ob','Om','As','ns','zre'])
    if key in CACHE:return CACHE[key]
    COUNTER+=1; tag=f"{model.lower()}{COUNTER:03d}"
    ini=make_ini(model,p,tag); log=Path(f'profile_{tag}.log')
    cp=subprocess.run(['./class',str(ini)],stdout=log.open('w'),stderr=subprocess.STDOUT)
    if cp.returncode!=0:
        r={'ok':False,'score':1e30,'score_k01':1e30,'model':model,**p,'tag':tag};CACHE[key]=r;HISTORY.append(r);return r
    prefix=tag+'_'
    try:
        bg=numeric_rows(OUT/f'{prefix}background.dat',8); bg.sort(key=lambda r:r[0])
        zd,rd=parse_drag(log); growth=growth_from_prefix(prefix)
        parts,ll=planck_loglike(OUT/f'{prefix}cl_lensed.dat')
        sn=sn_chi2(bg); be=boss_chi2(bg,rd,growth,'eff'); bk=boss_chi2(bg,rd,growth,'k01')
        r={'ok':True,'model':model,**p,'tag':tag,'z_drag':zd,'rd':rd,
           'logL_lowT':parts['lowT'],'logL_lowE':parts['lowE'],'logL_high':parts['high'],'logL_planck':ll,
           'chi2_SN':sn,'chi2_BOSS_eff':be,'chi2_BOSS_k01':bk,
           'score':-2*ll+sn+be,'score_k01':-2*ll+sn+bk}
    except Exception as e:
        r={'ok':False,'score':1e30,'score_k01':1e30,'model':model,**p,'tag':tag,'error':repr(e)}
    CACHE[key]=r;HISTORY.append(r)
    print('EVAL',model,tag,'score',r['score'],'params',p,flush=True)
    return r

RTK0={'lam':1000.,'h':.67556,'Ob':.049,'Om':.26,'As':2.1e-9,'ns':.965,'zre':8.}
LCDM0={'lam':0.,'h':.67556,'Ob':.049,'Om':.26,'As':2.1e-9,'ns':.965,'zre':8.}
COARSE_RTK={
 'lam':[500.,1000.,2000.,5000.,10000.,20000.],
 'h':[.64,.66,.67556,.69,.71], 'Ob':[.045,.047,.049,.051,.053], 'Om':[.22,.24,.26,.28,.30],
 'As':[1.9e-9,2.0e-9,2.1e-9,2.2e-9,2.3e-9], 'ns':[.94,.955,.965,.975,.99], 'zre':[6.,7.,8.,9.,10.]
}
COARSE_LCDM={k:v for k,v in COARSE_RTK.items() if k!='lam'}
REFINE={
 'lam':lambda x:[max(100.,x*.7),x,x*1.3], 'h':lambda x:[x-.0075,x,x+.0075],
 'Ob':lambda x:[x-.0015,x,x+.0015], 'Om':lambda x:[x-.01,x,x+.01],
 'As':lambda x:[x*.97,x,x*1.03], 'ns':lambda x:[x-.005,x,x+.005], 'zre':lambda x:[max(4.,x-.5),x,x+.5]
}

def coordinate_profile(model,start,grid):
    cur=dict(start); best=evaluate(model,cur)
    order=['lam','h','Ob','Om','As','ns','zre'] if model=='RTK' else ['h','Ob','Om','As','ns','zre']
    for par in order:
        cands=[]
        for v in grid[par]:
            q=dict(cur);q[par]=v;cands.append(evaluate(model,q))
        b=min(cands,key=lambda r:r['score'])
        if b['score']<best['score']:
            cur={k:b[k] for k in start};best=b
        print('COORD_BEST',model,par,best['score'],cur,flush=True)
    # one smaller refinement round around accumulated point
    for par in order:
        cands=[]
        for v in REFINE[par](cur[par]):
            q=dict(cur);q[par]=v;cands.append(evaluate(model,q))
        b=min(cands,key=lambda r:r['score'])
        if b['score']<best['score']:
            cur={k:b[k] for k in start};best=b
        print('REFINE_BEST',model,par,best['score'],cur,flush=True)
    return best

best_lcdm=coordinate_profile('LCDM',LCDM0,COARSE_LCDM)
best_rtk=coordinate_profile('RTK',RTK0,COARSE_RTK)

def dump(path,rows):
    fields=sorted(set().union(*(r.keys() for r in rows)))
    with Path(path).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
dump(OUT/'joint_profile_history.csv',HISTORY)
dump(OUT/'joint_profile_best.csv',[best_lcdm,best_rtk])
print('JOINT_PROFILE_RESULT')
print('LCDM',best_lcdm)
print('RTK',best_rtk)
print('DELTA_SCORE_RTK_MINUS_LCDM',best_rtk['score']-best_lcdm['score'])
print('DELTA_SCORE_K01_RTK_MINUS_LCDM',best_rtk['score_k01']-best_lcdm['score_k01'])
print('JOINT_PROFILE_PASS')
