#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
files = [
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
    if 'write_background' not in text:
        text += '\nwrite_background = yes\n'
    path.write_text(text)
print('RTK_BACKGROUND_OUTPUT_ENABLED')
