#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')

growth = root / 'analyze_growth_scan.py'
text = growth.read_text()
old = '''MODELS = [\n    (8000,  "rtk8_",  Path("../rtk8_run.log")),\n    (10000, "rtk_",   Path("../rtk_run.log")),\n    (12500, "rtk125_",Path("../rtk125_run.log")),\n    (15000, "rtk15_", Path("../rtk15_run.log")),\n    (20000, "rtk20_", Path("../rtk20_run.log")),\n]\n'''
new = '''MODELS = [\n    (4000,  "rtk4_",  Path("../rtk4_run.log")),\n    (5000,  "rtk5_",  Path("../rtk5_run.log")),\n    (6000,  "rtk6_",  Path("../rtk6_run.log")),\n    (7000,  "rtk7_",  Path("../rtk7_run.log")),\n    (8000,  "rtk8_",  Path("../rtk8_run.log")),\n    (10000, "rtk_",   Path("../rtk_run.log")),\n    (12500, "rtk125_",Path("../rtk125_run.log")),\n    (15000, "rtk15_", Path("../rtk15_run.log")),\n    (20000, "rtk20_", Path("../rtk20_run.log")),\n]\n'''
if old in text:
    text = text.replace(old, new)
elif new not in text:
    raise SystemExit('growth MODELS block not found')
growth.write_text(text)

coarse = root / 'coarse_likelihood.py'
text = coarse.read_text()
old = '''MODELS = [\n    ('LCDM', None, 'lcdm', Path('../lcdm_run.log')),\n    ('RTK', 8000.0, 'rtk8', Path('../rtk8_run.log')),\n    ('RTK', 10000.0, 'rtk', Path('../rtk_run.log')),\n    ('RTK', 12500.0, 'rtk125', Path('../rtk125_run.log')),\n    ('RTK', 15000.0, 'rtk15', Path('../rtk15_run.log')),\n    ('RTK', 20000.0, 'rtk20', Path('../rtk20_run.log')),\n]\n'''
new = '''MODELS = [\n    ('LCDM', None, 'lcdm', Path('../lcdm_run.log')),\n    ('RTK', 4000.0, 'rtk4', Path('../rtk4_run.log')),\n    ('RTK', 5000.0, 'rtk5', Path('../rtk5_run.log')),\n    ('RTK', 6000.0, 'rtk6', Path('../rtk6_run.log')),\n    ('RTK', 7000.0, 'rtk7', Path('../rtk7_run.log')),\n    ('RTK', 8000.0, 'rtk8', Path('../rtk8_run.log')),\n    ('RTK', 10000.0, 'rtk', Path('../rtk_run.log')),\n    ('RTK', 12500.0, 'rtk125', Path('../rtk125_run.log')),\n    ('RTK', 15000.0, 'rtk15', Path('../rtk15_run.log')),\n    ('RTK', 20000.0, 'rtk20', Path('../rtk20_run.log')),\n]\n'''
if old in text:
    text = text.replace(old, new)
elif new not in text:
    raise SystemExit('coarse MODELS block not found')
coarse.write_text(text)

print('RTK_LOWER_LAMBDA_SCAN_EXTENDED')
