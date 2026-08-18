#!/usr/bin/env python3
"""Final-center early-universe / BBN-era background robustness diagnostic.

This is not an added likelihood and does not modify the frozen matched result.
It compares the final RTK background to (i) a model=0 same-parameter control and
(ii) the final matched LCDM point, while preserving the frozen radiation and
recombination baseline.
"""
from __future__ import annotations
from bisect import bisect_left
from pathlib import Path
import json, math, re, subprocess

STATE=json.loads(Path('../research/state/current.json').read_text())
assert STATE.get('final_replay_certification')=='INDEPENDENT_FRESH_TREE_REPLAY_PASS'
assert STATE.get('comparison',{}).get('final_replay_certified') is True
OUT=Path('output/final_early_universe');OUT.mkdir(parents=True,exist_ok=True)
ULTRA={k:str(v) for k,v in STATE['objective']['ultra'].items()}
Z_TARGETS=[1e3,1e4,1e6,1e8,1e9,1e10]


def make_ini(model,p,tag):
    lines=[f"h = {p['h']}","T_cmb = 2.7255",f"Omega_b = {p['Ob']}"]
    if model=='RTK':
        lines += [f"Omega_khronon = {p['Om']}",f"lambda_D = {p['lam']}","Omega_Lambda = 0.","model = 2."]
    else:
        lines += [f"Omega_cdm = {p['Om']}","model = 0."]
    lines += [
      "N_ur = 3.046","N_ncdm = 0","Omega_k = 0.","Omega_fld = 0.","Omega_scf = 0.",
      "recombination = RECFAST","reio_parametrization = reio_camb",f"z_reio = {p['zre']}",
      "output = mPk","gauge = newtonian",f"A_s = {p['As']}",f"n_s = {p['ns']}",
      "P_k_max_h/Mpc = 0.2","z_pk = 0.","z_max_pk = 0.",
      f"root = output/final_early_universe/{tag}_","background_verbose = 1","thermodynamics_verbose = 0",
      "perturbations_verbose = 0","write background = yes",
    ]
    lines += [f"{k} = {v}" for k,v in ULTRA.items()]
    path=Path(f'early_{tag}.ini');path.write_text('\n'.join(lines)+'\n');return path


def rows(path):
    out=[]
    for line in Path(path).read_text().splitlines():
        s=line.strip()
        if not s or s.startswith('#'):continue
        a=[float(x) for x in s.split()]
        if len(a)>=5:out.append(a)
    out.sort(key=lambda r:r[0])
    return out


def interp_logz(rr,col,z):
    zs=[r[0] for r in rr]
    if not (zs[0] <= z <= zs[-1]):
        raise RuntimeError(f'z={z} outside background coverage [{zs[0]},{zs[-1]}]')
    j=bisect_left(zs,z)
    if j<len(zs) and zs[j]==z:return rr[j][col]
    z0,z1=zs[j-1],zs[j];y0,y1=rr[j-1][col],rr[j][col]
    # H is very close to a power law over a short background-table interval;
    # interpolate log H in log(1+z) to avoid high-z linear interpolation bias.
    x=math.log1p(z);x0=math.log1p(z0);x1=math.log1p(z1)
    if y0>0 and y1>0:
        return math.exp(math.log(y0)+(x-x0)*(math.log(y1)-math.log(y0))/(x1-x0))
    return y0+(x-x0)*(y1-y0)/(x1-x0)


def parse_gamma(log):
    vals=[]
    for line in Path(log).read_text().splitlines():
        m=re.search(r'RTK_LOG_GAMMA_ROOT[^0-9+\-.]*([+\-0-9.eE]+)',line)
        if m:vals.append(float(m.group(1)))
    return vals[-1] if vals else None


def run_model(model,p,tag):
    ini=make_ini(model,p,tag);log=Path(f'early_{tag}.log')
    with log.open('w') as f:cp=subprocess.run(['./class',str(ini)],stdout=f,stderr=subprocess.STDOUT)
    if cp.returncode:raise RuntimeError(f'{tag} CLASS failed; see {log}')
    rr=rows(OUT/f'{tag}_background.dat')
    return {'params':p,'background_z_min':rr[0][0],'background_z_max':rr[-1][0],
            'H_over_c_Mpc_inv':{str(z):interp_logz(rr,3,z) for z in Z_TARGETS},
            'gamma':parse_gamma(log) if model=='RTK' else None}


def main():
    rtkp=dict(STATE['rtk']['accepted_score_params'])
    lcdmp=dict(STATE['lcdm']['accepted_score_params'])
    rtk=run_model('RTK',rtkp,'rtk_final')
    same=run_model('LCDM',rtkp,'lcdm_same_rtk_params')
    lcdm=run_model('LCDM',lcdmp,'lcdm_final')
    ratios={}
    for z in Z_TARGETS:
        k=str(z);hr=rtk['H_over_c_Mpc_inv'][k];hs=same['H_over_c_Mpc_inv'][k];hl=lcdm['H_over_c_Mpc_inv'][k]
        ratios[k]={'RTK_over_same_params_LCDM_minus_1':hr/hs-1.0,'RTK_over_final_LCDM_minus_1':hr/hl-1.0}
    payload={
      'classification':'FINAL_RTK_EARLY_UNIVERSE_BACKGROUND_DIAGNOSTIC',
      'objective':STATE['objective']['name'],'state_iteration':STATE.get('iteration'),
      'final_replay_run_id':STATE['comparison']['final_replay_run_id'],
      'frozen_baseline':{'T_cmb':2.7255,'N_ur':3.046,'N_ncdm':0,'recombination':'RECFAST'},
      'omega_b_h2':{'RTK':rtkp['Ob']*rtkp['h']**2,'LCDM':lcdmp['Ob']*lcdmp['h']**2},
      'omega_nonbaryonic_h2':{'RTK':rtkp['Om']*rtkp['h']**2,'LCDM':lcdmp['Om']*lcdmp['h']**2},
      'rtk':rtk,'same_params_lcdm_control':same,'final_lcdm':lcdm,'H_ratios':ratios,
      'warning':'Background robustness diagnostic only; not a primordial-abundance likelihood or a replacement for a dedicated BBN code.'
    }
    (OUT/'summary.json').write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
    print('RTK_FINAL_EARLY_UNIVERSE_DIAGNOSTIC',json.dumps(payload,sort_keys=True))

if __name__=='__main__':main()
