#!/usr/bin/env python3
"""Retarget joint_profile_runner.py to a focused validation sweep around the
first corrected minima for both LCDM and RTK, using comparable local resolution.
"""
from pathlib import Path
import re, sys
p=Path(sys.argv[1]) if len(sys.argv)>1 else Path('joint_profile_runner.py')
text=p.read_text()
text=text.replace("RTK0={'lam':1000.,'h':.67556,'Ob':.049,'Om':.26,'As':2.1e-9,'ns':.965,'zre':8.}",
                  "RTK0={'lam':650.,'h':.6825,'Ob':.047,'Om':.26,'As':2.037e-9,'ns':.97,'zre':6.5}")
text=text.replace("LCDM0={'lam':0.,'h':.67556,'Ob':.049,'Om':.26,'As':2.1e-9,'ns':.965,'zre':8.}",
                  "LCDM0={'lam':0.,'h':.67556,'Ob':.0475,'Om':.26,'As':2.1e-9,'ns':.965,'zre':8.}")
text=re.sub(r"COARSE_RTK=\{.*?\n\}\nCOARSE_LCDM=\{k:v for k,v in COARSE_RTK.items\(\) if k!='lam'\}",
'''COARSE_RTK={
 'lam':[400.,500.,650.,800.,1000.],
 'h':[.6775,.68,.6825,.685,.6875],
 'Ob':[.0455,.046,.0465,.047,.0475],
 'Om':[.25,.255,.26,.265,.27],
 'As':[1.98e-9,2.01e-9,2.037e-9,2.06e-9,2.09e-9],
 'ns':[.965,.9675,.97,.9725,.975],
 'zre':[5.5,6.,6.5,7.,7.5]
}
COARSE_LCDM={
 'h':[.67,.673,.67556,.678,.681],
 'Ob':[.0465,.047,.0475,.048,.0485],
 'Om':[.25,.255,.26,.265,.27],
 'As':[2.04e-9,2.07e-9,2.1e-9,2.13e-9,2.16e-9],
 'ns':[.96,.9625,.965,.9675,.97],
 'zre':[7.25,7.5,7.75,8.,8.25]
}''', text, flags=re.S)
text=re.sub(r"REFINE=\{.*?\n\}",
'''REFINE={
 'lam':lambda x:[max(100.,x*.85),x,x*1.15],
 'h':lambda x:[x-.0015,x,x+.0015],
 'Ob':lambda x:[x-.0005,x,x+.0005],
 'Om':lambda x:[x-.005,x,x+.005],
 'As':lambda x:[x*.985,x,x*1.015],
 'ns':lambda x:[x-.002,x,x+.002],
 'zre':lambda x:[max(4.,x-.25),x,x+.25]
}''', text, count=1, flags=re.S)
if "RTK0={'lam':650." not in text or "'h':[.67,.673,.67556" not in text:
    raise SystemExit('focused validation transformation failed')
p.write_text(text)
print('JOINT_PROFILE_VALIDATION_GRID_PREPARED')
