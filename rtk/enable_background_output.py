#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
files = [
    'rtk_lambda4000.ini',
    'rtk_lambda5000.ini',
    'rtk_lambda6000.ini',
    'rtk_lambda7000.ini',
    'rtk_lambda8000.ini',
    'rtk_baseline.ini',
    'rtk_lambda12500.ini',
    'rtk_lambda15000.ini',
    'rtk_lambda20000.ini',
    'lcdm_baseline.ini',
]
for name in files:
    path = root / name
    text = path.read_text()
    if 'write background' not in text:
        text += '\nwrite background = yes\n'
    if 'thermodynamics_verbose' not in text:
        text += 'thermodynamics_verbose = 1\n'
    path.write_text(text)
print('RTK_BACKGROUND_OUTPUT_ENABLED')
print('RTK_DRAG_HORIZON_LOGGING_ENABLED')
