#!/usr/bin/env python3
import base64, io, json, math, os, re, sys, urllib.request, urllib.error, zipfile
from pathlib import Path

REPO=os.environ.get('GITHUB_REPOSITORY','pppuu7-cmd/Photospheric-Radius-Scale')
GH_TOKEN=os.environ.get('GITHUB_TOKEN','')
OPENAI_KEY=os.environ.get('OPENAI_API_KEY','')
MODEL=os.environ.get('OPENAI_MODEL') or 'gpt-5'
STATE_PATH=Path('rtk/agent/frontier_state.json')
GATE_WORKFLOW='rtk-agent-scientific-gate.yml'
ALLOWED={'WAIT','RECENTER','STATIONARITY','REDISCOVERY_FOLLOWUP'}

if not GH_TOKEN: raise SystemExit('GITHUB_TOKEN missing')
if not OPENAI_KEY:
    print('RTK_AGENT_DISABLED_NO_OPENAI_API_KEY')
    raise SystemExit(0)
state=json.loads(STATE_PATH.read_text())


def req(url, method='GET', body=None, headers=None):
    h={'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'}
    if url.startswith('https://api.github.com/'): h['Authorization']='Bearer '+GH_TOKEN
    if headers:h.update(headers)
    data=None if body is None else json.dumps(body).encode()
    if data is not None:h['Content-Type']='application/json'
    r=urllib.request.Request(url,data=data,headers=h,method=method)
    with urllib.request.urlopen(r,timeout=120) as f:return f.read(), dict(f.headers)

def gh_json(path):
    b,_=req('https://api.github.com/repos/'+REPO+path);return json.loads(b)

def recent_runs(): return gh_json('/actions/runs?per_page=100')['workflow_runs']

def active_blocker(runs):
    names=set(state['frontier_workflows'])|{'RTK agent scientific gate'}
    return [r for r in runs if r['name'] in names and r['status'] in ('queued','in_progress','waiting','pending')]

def choose_source(runs):
    names=set(state['frontier_workflows'])|{'RTK agent scientific gate'}
    cand=[r for r in runs if r['name'] in names and r['status']=='completed' and r.get('conclusion')=='success' and int(r['id'])>int(state.get('last_processed_run_id',0))]
    return max(cand,key=lambda r:int(r['id'])) if cand else None

def compact_json(x):
    keep={'stage','status','scope','mapping','lambda_D','lambda0','center_S','best_S','best_params','best_components','boundary_axes','poll_improvement','poll_improvement_from_pre_poll_best','failed_points','transient_retries','timeout_retries','scale','step_scale','gradient','scaled_gradient','max_abs_gradient','max_abs_scaled_gradient','eigenvalues','hessian_eigenvalues','newton_improvement','stencil_best_improvement','warning'}
    if isinstance(x,dict):
        y={}
        for k,v in x.items():
            if k in keep or 'poll' in k.lower() or 'gradient' in k.lower() or 'eigen' in k.lower() or 'improvement' in k.lower():
                y[k]=compact_json(v)
        if not y:
            for k in ('S_eff','S_k01','score','score_k01','params'):
                if k in x:y[k]=compact_json(x[k])
        return y
    if isinstance(x,list):return [compact_json(v) for v in x[:20]]
    return x

def artifact_context(run_id):
    arts=gh_json(f'/actions/runs/{run_id}/artifacts').get('artifacts',[])
    out=[]; files=0
    for a in arts[:20]:
        try:
            b,_=req(a['archive_download_url'])
            with zipfile.ZipFile(io.BytesIO(b)) as z:
                for n in z.namelist():
                    if files>=80:break
                    if n.endswith('.json'):
                        try:
                            x=json.loads(z.read(n));out.append({'artifact':a['name'],'file':n,'summary':compact_json(x)});files+=1
                        except Exception:pass
        except Exception as e:
            out.append({'artifact':a.get('name'),'error':repr(e)})
    return out

def output_text(resp):
    parts=[]
    for item in resp.get('output',[]):
        for c in item.get('content',[]) if isinstance(item,dict) else []:
            if c.get('type')=='output_text':parts.append(c.get('text',''))
    return '\n'.join(parts).strip()

def call_openai(source, summaries):
    system='''You are the decision layer of a guarded cosmology research pipeline for RTK Stage4D3. You do NOT execute code. Choose only a scientifically justified next gate. Never claim a global minimum from a local optimizer. Never advance failed/incomplete work. STATIONARITY is allowed only after an exact local poll is zero or negligible (<=1e-5). If a clean-room fixed-lambda rediscovery grid has finished, prefer REDISCOVERY_FOLLOWUP from its best independently discovered interior seed(s), not the historical best. If a stationarity stencil shows a real exact descent, choose RECENTER from the best exact point. Return only strict JSON, no markdown.'''
    schema='''Return exactly: {"action":"WAIT|RECENTER|STATIONARITY|REDISCOVERY_FOLLOWUP","reason":"short scientific reason","dispatches":[{"mapping":"eff|k01","lambda_D":number,"h":number,"Ob":number,"Om":number,"As":number,"ns":number,"zre":number,"expected_s":number,"scale":number}]} . Maximum 6 dispatches. WAIT must have an empty dispatches array.'''
    user=json.dumps({'frontier_state':state,'source_run':{'id':source['id'],'name':source['name'],'conclusion':source['conclusion']},'artifact_summaries':summaries},separators=(',',':'))
    payload={'model':MODEL,'input':[{'role':'system','content':[{'type':'input_text','text':system+'\n'+schema}]},{'role':'user','content':[{'type':'input_text','text':user}]}]}
    data=json.dumps(payload).encode(); h={'Authorization':'Bearer '+OPENAI_KEY,'Content-Type':'application/json'}
    r=urllib.request.Request('https://api.openai.com/v1/responses',data=data,headers=h,method='POST')
    with urllib.request.urlopen(r,timeout=300) as f:resp=json.loads(f.read())
    txt=output_text(resp)
    txt=re.sub(r'^```(?:json)?\s*|\s*```$','',txt.strip())
    return json.loads(txt), resp.get('id')

def nums_from_summaries(summaries,key_terms):
    vals=[]
    def walk(x,k=''):
        if isinstance(x,dict):
            for a,b in x.items():walk(b,a)
        elif isinstance(x,list):
            for b in x:walk(b,k)
        elif isinstance(x,(int,float)) and math.isfinite(float(x)) and any(t in k.lower() for t in key_terms): vals.append(float(x))
    walk(summaries);return vals

def validate(dec, source, summaries):
    if not isinstance(dec,dict):raise ValueError('decision not object')
    action=dec.get('action'); ds=dec.get('dispatches')
    if action not in ALLOWED:raise ValueError('action not allowed')
    if not isinstance(ds,list) or len(ds)>6:raise ValueError('invalid dispatches')
    if action=='WAIT':
        if ds:raise ValueError('WAIT must not dispatch')
        return
    if not ds:raise ValueError('non-WAIT requires dispatch')
    if action=='REDISCOVERY_FOLLOWUP' and 'rediscovery' not in source['name'].lower():raise ValueError('rediscovery followup requires rediscovery source')
    polls=nums_from_summaries(summaries,['poll_improvement'])
    if action=='STATIONARITY':
        if 'rediscovery' in source['name'].lower():raise ValueError('fixed-lambda rediscovery must first get 7D followup')
        if not polls or min(abs(v) for v in polls)>1e-5:raise ValueError('stationarity gate not earned by poll')
    for d in ds:
        if d.get('mapping') not in ('eff','k01'):raise ValueError('bad mapping')
        q={k:float(d[k]) for k in ('lambda_D','h','Ob','Om','As','ns','zre','expected_s','scale')}
        if not all(math.isfinite(v) for v in q.values()):raise ValueError('nonfinite')
        if not 1e2<=q['lambda_D']<=1e10:raise ValueError('lambda range')
        if not 0.50<=q['h']<=0.90 or not 0.02<=q['Ob']<=0.08 or not 0.10<=q['Om']<=0.50:raise ValueError('cosmo range')
        if not 1e-10<=q['As']<=1e-8 or not 0.80<=q['ns']<=1.20 or not 0<=q['zre']<=30:raise ValueError('cosmo range2')
        if not 0.03125<=q['scale']<=2.0:raise ValueError('scale range')
        if action=='STATIONARITY' and not 900<=q['expected_s']<=1200:raise ValueError('expected_s range')

def dispatch(action,d):
    inputs={k:str(d[k]) for k in ('mapping','lambda_D','h','Ob','Om','As','ns','zre','expected_s','scale')}
    inputs['action']=action
    req('https://api.github.com/repos/'+REPO+'/actions/workflows/'+GATE_WORKFLOW+'/dispatches','POST',{'ref':'main','inputs':inputs})

def persist(source,decision,response_id):
    path='rtk/agent/frontier_state.json'
    meta=gh_json('/contents/'+path+'?ref=main')
    st=dict(state);st['last_processed_run_id']=int(source['id']);st['last_decision']={'source_run_id':int(source['id']),'source_workflow':source['name'],'decision':decision,'openai_response_id':response_id}
    content=json.dumps(st,indent=2,sort_keys=True)+'\n'
    body={'message':f"Advance RTK agent state after run {source['id']}",'content':base64.b64encode(content.encode()).decode(),'sha':meta['sha'],'branch':'main'}
    req('https://api.github.com/repos/'+REPO+'/contents/'+path,'PUT',body)

runs=recent_runs()
block=active_blocker(runs)
# Ignore the current agent's own run; it is not in frontier names.
if block:
    print('RTK_AGENT_WAIT_ACTIVE',[(r['name'],r['id'],r['status']) for r in block]);raise SystemExit(0)
source=choose_source(runs)
if not source:
    print('RTK_AGENT_WAIT_NO_NEW_COMPLETED_FRONTIER');raise SystemExit(0)
summaries=artifact_context(source['id'])
print('RTK_AGENT_SOURCE',source['id'],source['name'],'summaries',len(summaries))
dec,rid=call_openai(source,summaries)
print('RTK_AGENT_DECISION',json.dumps(dec,sort_keys=True))
validate(dec,source,summaries)
if dec['action']!='WAIT':
    for d in dec['dispatches']:dispatch(dec['action'],d)
persist(source,dec,rid)
print('RTK_AGENT_ADVANCE_PASS',source['id'],dec['action'])
