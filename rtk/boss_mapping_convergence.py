#!/usr/bin/env python3
"""Numerical convergence audit for RTK BOSS eff/k01 growth mappings.

Runs CLASS repeatedly at one RTK parameter point while varying only the
redshift sampling used for d/d ln(a) and P_k_max_h/Mpc used in the sigma8
integral.  All other CLASS settings match the production likelihood harness.
The BAO distance convention and the full 9x9 covariance are kept fixed.
This is a numerical-systematics test, not a fit or significance calculation.
"""
from pathlib import Path
from bisect import bisect_left
import csv,json,math,re,subprocess

OUT=Path('output/boss_convergence'); OUT.mkdir(parents=True,exist_ok=True)
BOSS_DATA=Path('boss_DR12Consensus_final.dat')
BOSS_COV=Path('final_consensus_covtot_dM_Hz_fsig.txt')
C_KM_S=299792.458; R_FID=147.78

P={'lam':54804.51998233707,'h':0.6905121965689395,'Ob':0.046831928061712685,
   'Om':0.2529636778757895,'As':2.069477450200849e-9,
   'ns':0.9641699662731723,'zre':6.855358068811081}

SETTINGS=[
 ('legacy_p5',5.0,[0.,.25,.3,.4,.5,.6,.7,.75,1.0]),
 ('dense02_p5',5.0,[.34,.36,.38,.40,.42,.47,.49,.51,.53,.55,.57,.59,.61,.63,.65]),
 ('dense01_p5',5.0,[.36,.37,.38,.39,.40,.49,.50,.51,.52,.53,.59,.60,.61,.62,.63]),
 ('dense01_p10',10.0,[.36,.37,.38,.39,.40,.49,.50,.51,.52,.53,.59,.60,.61,.62,.63]),
 ('dense01_p20',20.0,[.36,.37,.38,.39,.40,.49,.50,.51,.52,.53,.59,.60,.61,.62,.63]),
]

def numeric_rows(path,min_cols=1):
    rows=[]
    for line in Path(path).read_text().splitlines():
        s=line.strip()
        if not s or s.startswith('#'):continue
        vals=[float(x) for x in s.split()]
        if len(vals)>=min_cols:rows.append(vals)
    return rows

def cholesky(A):
    n=len(A); L=[[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1):
            s=sum(L[i][k]*L[j][k] for k in range(j))
            if i==j:
                v=A[i][i]-s
                if not v>0:raise RuntimeError('non-positive covariance')
                L[i][j]=math.sqrt(v)
            else:L[i][j]=(A[i][j]-s)/L[j][j]
    return L

def chol_solve(L,b):
    n=len(L);y=[0.0]*n;x=[0.0]*n
    for i in range(n):y[i]=(b[i]-sum(L[i][j]*y[j] for j in range(i)))/L[i][i]
    for i in range(n-1,-1,-1):x[i]=(y[i]-sum(L[j][i]*x[j] for j in range(i+1,n)))/L[i][i]
    return x

def quad(L,v):
    x=chol_solve(L,v);return sum(a*b for a,b in zip(v,x))

def load_boss():
    obs=[]
    for line in BOSS_DATA.read_text().splitlines():
        s=line.strip()
        if not s or s.startswith('#'):continue
        z,v,k=s.split()[:3];obs.append((float(z),float(v),k))
    return obs,cholesky(numeric_rows(BOSS_COV,9))
BOSS,L_BOSS=load_boss()

def interp_rows(rows,col,z):
    zs=[r[0] for r in rows]
    if z<=zs[0]:return rows[0][col]
    if z>=zs[-1]:return rows[-1][col]
    j=bisect_left(zs,z);z0,z1=zs[j-1],zs[j];y0,y1=rows[j-1][col],rows[j][col]
    return y0+(z-z0)*(y1-y0)/(z1-z0)

def top_hat(x):
    if abs(x)<1e-3:
        x2=x*x;return 1-x2/10+x2*x2/280
    return 3*(math.sin(x)-x*math.cos(x))/(x*x*x)

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
    raise RuntimeError('no z in pk header '+str(path))

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
    v=0.0
    for i in range(3):
        w=1.0
        for j in range(3):
            if i!=j:w*=(x-xs[j])/(xs[i]-xs[j])
        v+=ys[i]*w
    return v

def interp_pk(rows,k):
    xs=[r[0] for r in rows];j=bisect_left(xs,k)
    if j==0:return rows[0][1]
    if j>=len(rows):return rows[-1][1]
    x0,y0=rows[j-1];x1,y1=rows[j]
    return y0+(k-x0)*(y1-y0)/(x1-x0)

def growth(prefix):
    fam={}
    for f in sorted(OUT.glob(prefix+'z*_pk.dat')):
        fam[z_from_pk(f)]=pk_load(f)
    if not fam:raise RuntimeError('no pk family '+prefix)
    sig={z:sigma8(r) for z,r in fam.items()};res={}
    for z0 in (.38,.51,.61):
        znear=sorted(fam,key=lambda z:abs(z-z0))[:3];znear=sorted(znear)
        xp=[math.log(1/(1+z)) for z in znear];sp=[sig[z] for z in znear]
        xt=math.log(1/(1+z0))
        fs=derivative3(xp[0],sp[0],xp[1],sp[1],xp[2],sp[2],xt)
        s8=qval(xp,sp,xt)
        lp=[(math.log(1/(1+z)),math.log(interp_pk(fam[z],.1))) for z in znear]
        f01=.5*derivative3(lp[0][0],lp[0][1],lp[1][0],lp[1][1],lp[2][0],lp[2][1],xt)
        res[z0]={'fs8_eff':fs,'fs8_k01':f01*s8,'sigma8':s8,'znear':znear}
    return res

def parse_drag(log):
    zd=rd=None
    for line in Path(log).read_text().splitlines():
        m=re.search(r'baryon drag stops at z\s*=\s*([0-9eE+\-.]+)',line)
        if m:zd=float(m.group(1))
        m=re.search(r'with comoving sound horizon rs\s*=\s*([0-9eE+\-.]+)',line)
        if m and zd is not None:rd=float(m.group(1))
    if rd is None:raise RuntimeError('no drag horizon')
    return zd,rd

def make_ini(tag,pmax,zgrid):
    # Match joint_profile_runner.make_ini exactly except for pmax and z_pk.
    lines=[f"h = {P['h']}","T_cmb = 2.7255",f"Omega_b = {P['Ob']}",
      f"Omega_khronon = {P['Om']}",f"lambda_D = {P['lam']}","Omega_Lambda = 0.","model = 2.",
      "N_ur = 3.046","N_ncdm = 0","Omega_k = 0.","Omega_fld = 0.","Omega_scf = 0.",
      "recombination = RECFAST","reio_parametrization = reio_camb",f"z_reio = {P['zre']}",
      "output = tCl,pCl,lCl,mPk","lensing = yes","gauge = newtonian",f"A_s_ad = {P['As']}",f"n_s_ad = {P['ns']}",
      "l_max_scalars = 2600",f"P_k_max_h/Mpc = {pmax}","z_pk = "+','.join(str(z) for z in zgrid),
      "z_max_pk = 1.0",f"root = output/boss_convergence/{tag}_",
      "background_verbose = 1","thermodynamics_verbose = 1","perturbations_verbose = 0","write background = yes"]
    f=Path('bossconv_'+tag+'.ini');f.write_text('\n'.join(lines)+'\n');return f

def boss_chi2(bg,rd,g,which):
    pred=[];data=[]
    for z,val,kind in BOSS:
        data.append(val)
        if kind=='DM_over_rs':pred.append(interp_rows(bg,4,z)*R_FID/rd)
        elif kind=='bao_Hz_rs':pred.append(interp_rows(bg,3,z)*C_KM_S*rd/R_FID)
        else:pred.append(g[z]['fs8_eff' if which=='eff' else 'fs8_k01'])
    return quad(L_BOSS,[p-d for p,d in zip(pred,data)]),pred

rows=[]
for label,pmax,zgrid in SETTINGS:
    ini=make_ini(label,pmax,zgrid);log=Path('bossconv_'+label+'.log')
    cp=subprocess.run(['./class',str(ini)],stdout=log.open('w'),stderr=subprocess.STDOUT)
    if cp.returncode:raise RuntimeError('CLASS failed '+label)
    bg=numeric_rows(OUT/(label+'_background.dat'),8);bg.sort(key=lambda r:r[0])
    zd,rd=parse_drag(log);g=growth(label+'_')
    ce,pe=boss_chi2(bg,rd,g,'eff');ck,pk=boss_chi2(bg,rd,g,'k01')
    row={'label':label,'pmax':pmax,'n_z':len(zgrid),'rd':rd,'chi2_eff':ce,'chi2_k01':ck}
    for z in (.38,.51,.61):
        key=str(z).replace('.','p')
        row['fs8eff_'+key]=g[z]['fs8_eff'];row['fs8k01_'+key]=g[z]['fs8_k01'];row['sigma8_'+key]=g[z]['sigma8']
    rows.append(row);print('BOSS_CONVERGENCE_POINT',json.dumps(row,sort_keys=True),flush=True)

base=rows[0]
for r in rows:
    r['delta_chi2_eff_vs_legacy']=r['chi2_eff']-base['chi2_eff']
    r['delta_chi2_k01_vs_legacy']=r['chi2_k01']-base['chi2_k01']
finest=rows[-1]
summary={'stage':'BOSS-growth-mapping-numerical-convergence','params':P,'settings':rows,
 'legacy_vs_finest':{'delta_chi2_eff':finest['chi2_eff']-base['chi2_eff'],
                     'delta_chi2_k01':finest['chi2_k01']-base['chi2_k01']},
 'production_baseline_expected':{'rd':146.967497,'chi2_eff':7.419950339366178,'chi2_k01':7.431368670906675},
 'warning':'Numerical-systematics audit only; eff/k01 remain alternative model-specific RSD mappings.'}
(OUT/'boss_convergence_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
with (OUT/'boss_convergence.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys()));w.writeheader();w.writerows(rows)
print('BOSS_MAPPING_CONVERGENCE_RESULT',json.dumps(summary,sort_keys=True),flush=True)
print('BOSS_MAPPING_CONVERGENCE_COMPLETE',flush=True)
