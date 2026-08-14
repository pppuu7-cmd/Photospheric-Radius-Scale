#!/usr/bin/env python3
from pathlib import Path
import sys

root=Path(sys.argv[1] if len(sys.argv)>1 else 'class_public')
hdr=root/'include/background.h'
inc=root/'source/input.c'
bg=root/'source/background.c'
pt=root/'source/perturbations.c'

hs=hdr.read_text(); ins=inc.read_text(); bs=bg.read_text(); ps=pt.read_text()

# Expose the DBI shape parameter as a real CLASS input parameter.
needle='  double gnl;/**gamma*/\n'
if 'double lambda_D;' not in hs:
    if needle not in hs: raise SystemExit('background.h gamma field not found')
    hs=hs.replace(needle,needle+'  double lambda_D;/** RT+DBI-Khronon shape parameter */\n',1)

# Defaults and parser hook. The public nonlocal branch already reads `model` here.
needle='''  class_read_double("model",pba->model);\n  if (pba->model != 0.)\n      pba->has_nlde = _TRUE_;'''
repl='''  class_read_double("model",pba->model);\n  if (pba->model != 0.)\n      pba->has_nlde = _TRUE_;\n  class_read_double("lambda_D",pba->lambda_D);\n  class_test((pba->model == 2.) && !(pba->lambda_D > 0.),errmsg,\n             "lambda_D must be strictly positive for RT+DBI-Khronon");'''
if 'class_read_double("lambda_D"' not in ins:
    if needle not in ins: raise SystemExit('model parser block not found')
    ins=ins.replace(needle,repl,1)

needle='  pba->Omega0_cdm = 0.; //NonLocal: Om_cdm set to zero by default. Useful for model comparison where Om_cdm is unspecified, and then derived by the filling condition.\n'
if 'pba->lambda_D = 1.e4;' not in ins:
    if needle not in ins: raise SystemExit('default Omega0_cdm line not found')
    ins=ins.replace(needle,needle+'  pba->lambda_D = 1.e4; /* RT+DBI-Khronon default; explicit in production runs */\n',1)

# User-facing Omega_khronon alias. Internally we retain the legacy CDM slot so the
# old CLASS indexing/allocation machinery can be reused without fake dust physics.
old='''  /* Omega_0_cdm (CDM) */\n  class_call(parser_read_double(pfc,"Omega_cdm",&param1,&flag1,errmsg),\n             errmsg,\n             errmsg);\n  class_call(parser_read_double(pfc,"omega_cdm",&param2,&flag2,errmsg),\n             errmsg,\n             errmsg);\n  class_test(((flag1 == _TRUE_) && (flag2 == _TRUE_)),\n             errmsg,\n             "In input file, you can only enter one of Omega_cdm or omega_cdm, choose one");\n  if (flag1 == _TRUE_)\n    pba->Omega0_cdm = param1;\n  if (flag2 == _TRUE_)\n    pba->Omega0_cdm = param2/pba->h/pba->h;\n\n  Omega_tot += pba->Omega0_cdm;'''
new='''  /* Omega_0_cdm / RT+DBI-Khronon density alias */\n  class_call(parser_read_double(pfc,"Omega_cdm",&param1,&flag1,errmsg),\n             errmsg,\n             errmsg);\n  class_call(parser_read_double(pfc,"omega_cdm",&param2,&flag2,errmsg),\n             errmsg,\n             errmsg);\n  class_call(parser_read_double(pfc,"Omega_khronon",&param3,&flag3,errmsg),\n             errmsg,\n             errmsg);\n  class_test(((flag1 == _TRUE_) && (flag2 == _TRUE_)) ||\n             ((flag3 == _TRUE_) && ((flag1 == _TRUE_) || (flag2 == _TRUE_))),\n             errmsg,\n             "Specify only one of Omega_cdm, omega_cdm, or Omega_khronon");\n  class_test((flag3 == _TRUE_) && (pba->model != 2.),errmsg,\n             "Omega_khronon is only defined for model=2 (RT+DBI-Khronon)");\n  if (flag1 == _TRUE_)\n    pba->Omega0_cdm = param1;\n  if (flag2 == _TRUE_)\n    pba->Omega0_cdm = param2/pba->h/pba->h;\n  if (flag3 == _TRUE_)\n    pba->Omega0_cdm = param3;\n\n  Omega_tot += pba->Omega0_cdm;'''
if 'Omega_khronon' not in ins:
    if old not in ins: raise SystemExit('CDM parser block not found')
    ins=ins.replace(old,new,1)

# Replace every temporary hard-coded DBI shape constant inserted by the first patch.
bs=bs.replace('(pba->gnl > 0. ? pba->gnl : 1.e-14), 1.e4, pba->Omega0_cdm',
              '(pba->gnl > 0. ? pba->gnl : 1.e-14), pba->lambda_D, pba->Omega0_cdm')
ps=ps.replace('(pba->gnl > 0. ? pba->gnl : 1.e-14),1.e4,pba->Omega0_cdm',
              '(pba->gnl > 0. ? pba->gnl : 1.e-14),pba->lambda_D,pba->Omega0_cdm')

hdr.write_text(hs); inc.write_text(ins); bg.write_text(bs); pt.write_text(ps)
print('RTK_INPUT_UPGRADE_APPLIED')
