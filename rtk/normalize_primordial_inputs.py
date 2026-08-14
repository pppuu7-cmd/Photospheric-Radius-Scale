#!/usr/bin/env python3
"""Normalize primordial scalar input names for the legacy CLASS branch.

The public nonlocal CLASS branch reads A_s and n_s. Earlier RTK staging files
used A_s_ad/n_s_ad, which are silently unused by this CLASS version.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
changed = 0
for p in root.glob('*.ini'):
    text = p.read_text()
    new = text.replace('A_s_ad', 'A_s').replace('n_s_ad', 'n_s')
    if new != text:
        p.write_text(new)
        changed += 1
print(f'PRIMORDIAL_INPUT_NAMES_NORMALIZED files={changed}')
