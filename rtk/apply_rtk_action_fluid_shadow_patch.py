#!/usr/bin/env python3
"""Opt-in patch: replace only RTK lower-derivative GDM terms by action-derived ones.

The script is intentionally not part of the production patch chain.  It is used
only in frozen shadow-comparison workflows.
"""
from pathlib import Path
import sys

root=Path(sys.argv[1] if len(sys.argv)>1 else 'class_public')
p=root/'source/khronon_perturbations.c'
s=p.read_text()
original=s

s=s.replace('double onepw,k2,entropy;', 'double onepw,k2;', 1)
s=s.replace('onepw=1.0+bg->w; if(!(onepw>0.0)) return KHR_UNPHYSICAL;\n  k2=bg->k*bg->k; entropy=bg->cs2-bg->ca2;',
            'onepw=1.0+bg->w; if(!(onepw>0.0)) return KHR_UNPHYSICAL;\n  k2=bg->k*bg->k;',1)
s=s.replace('dy->delta_prime=-onepw*(y->theta-3.0*m->phi_prime)-3.0*m->Hc*(bg->cs2-bg->w)*y->delta-9.0*m->Hc*m->Hc*onepw*entropy*y->theta/k2;',
            'dy->delta_prime=-onepw*(y->theta-3.0*m->phi_prime)-3.0*m->Hc*(bg->ca2-bg->w)*y->delta;',1)
s=s.replace('dy->theta_prime=-m->Hc*(1.0-3.0*bg->cs2)*y->theta+k2*(bg->cs2*y->delta/onepw+m->psi);',
            'dy->theta_prime=-m->Hc*(1.0-3.0*bg->ca2)*y->theta+k2*(bg->cs2*y->delta/onepw+m->psi);',1)
s=s.replace('double onepw,k2,pb;', 'double onepw,pb;', 1)
s=s.replace('onepw=1.0+bg->w; if(!(onepw>0.0)) return KHR_UNPHYSICAL; k2=bg->k*bg->k;\n  pb=bg->cs2*y->delta+3.0*Hc*onepw*(bg->cs2-bg->ca2)*y->theta/k2;',
            'onepw=1.0+bg->w; if(!(onepw>0.0)) return KHR_UNPHYSICAL;\n  pb=bg->cs2*y->delta;',1)

if s==original:
    raise SystemExit('action-fluid shadow patch made no changes')
# Hard guards: production-GDM entropy/friction patterns must be gone only in this copied tree.
if '9.0*m->Hc*m->Hc*onepw*entropy' in s: raise SystemExit('entropy term still present')
if '(1.0-3.0*bg->cs2)*y->theta' in s: raise SystemExit('production Euler friction still present')
if 'pb=bg->cs2*y->delta+3.0*Hc' in s: raise SystemExit('production pressure entropy source still present')
if '(bg->ca2-bg->w)*y->delta' not in s: raise SystemExit('action density friction missing')
if '(1.0-3.0*bg->ca2)*y->theta' not in s: raise SystemExit('action Euler friction missing')
if 'pb=bg->cs2*y->delta;' not in s: raise SystemExit('action pressure source missing')
p.write_text(s)
print('RTK_ACTION_FLUID_SHADOW_PATCH_APPLIED')
