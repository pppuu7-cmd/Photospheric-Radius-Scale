#!/usr/bin/env python3
"""Measure numerical repeatability of one exact RTK/LCDM objective point.

Usage:
  python3 stage4d1_repeatability.py PLANCK_DIR MODEL LAMBDA H OB OM AS NS ZRE NREP

MODEL is RTK or LCDM.  Each repetition deliberately clears the in-process
likelihood cache and therefore launches a fresh CLASS calculation.
"""
import json, math, statistics, sys
import inference_core as L

if len(sys.argv)!=12:
    raise SystemExit(__doc__)
model=sys.argv[2].upper(); lam=float(sys.argv[3]); nrep=int(sys.argv[11])
if model not in ('RTK','LCDM') or nrep<2: raise SystemExit('bad model or NREP')
p={'lam':lam,'h':float(sys.argv[4]),'Ob':float(sys.argv[5]),'Om':float(sys.argv[6]),
   'As':float(sys.argv[7]),'ns':float(sys.argv[8]),'zre':float(sys.argv[9])}
# argv[10] is retained as explicit zre? Guard against accidental layout drift.
# Canonical command supplies exactly MODEL LAMBDA H OB OM AS NS ZRE NREP after PLANCK_DIR.
# Reparse from tail to avoid ambiguity introduced by the legacy PLANCK_DIR argv consumer.
p={'lam':lam,'h':float(sys.argv[4]),'Ob':float(sys.argv[5]),'Om':float(sys.argv[6]),
   'As':float(sys.argv[7]),'ns':float(sys.argv[8]),'zre':float(sys.argv[9])}
# sys.argv[10] is the requested repeat count in the intended 11-argument form.
# Accept both old accidental 12-field form and canonical form below.
