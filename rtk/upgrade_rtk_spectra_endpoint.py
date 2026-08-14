#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else 'class_public')
sp = root / 'source/spectra.c'
s = sp.read_text()
needle = "  ln_tau = log(tau);\n"
replacement = """  ln_tau = log(tau);\n\n  /** RTK precision guard: for z=0 use the exact final tabulated ln(tau).\n      Old CLASS 2.4.5 can otherwise exceed x_max by roundoff when z_max_pk>0. */\n  if ((z == 0.) && (psp->ln_tau_size > 1))\n    ln_tau = psp->ln_tau[psp->ln_tau_size-1];\n"""
if 'RTK precision guard' in s:
    print('RTK_SPECTRA_ENDPOINT_ALREADY_PATCHED')
    raise SystemExit(0)
if needle not in s:
    raise SystemExit('spectra ln_tau assignment not found')
s = s.replace(needle, replacement, 1)
sp.write_text(s)
print('RTK_SPECTRA_ENDPOINT_PATCHED')
