#!/usr/bin/env python3
from __future__ import annotations
import argparse,glob
from pathlib import Path

# r2g materializes R1 first and appends R2 from a separate observer.
# The original frozen C10.65r2 analyzer predates that engineering isolation and
# parses the diagnostic tail as R2+R1.  This adapter performs ONLY the exact
# token permutation (R1,R2)->(R2,R1) in disposable copies.  No numeric token is
# parsed, rounded, recomputed or changed.
# C10.65r2 frozen full-rerun dispatch marker; semantics unchanged.
N_R1=16
N_R2=13
N=N_R1+N_R2

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--glob',required=True)
    ap.add_argument('--output-dir',required=True)
    a=ap.parse_args()
    out=Path(a.output_dir); out.mkdir(parents=True,exist_ok=True)
    fs=sorted(glob.glob(a.glob));
    if not fs: raise SystemExit('no input files')
    for src in fs:
        dst=out/Path(src).name
        lines=[]
        for raw in Path(src).read_text().splitlines():
            s=raw.strip()
            if not s or s.startswith('#'):
                lines.append(raw)
                continue
            tok=raw.split()
            if len(tok)<N: raise RuntimeError(f'row too short in {src}')
            pre=tok[:-N]; r1=tok[-N:-N_R2]; r2=tok[-N_R2:]
            assert len(r1)==N_R1 and len(r2)==N_R2
            lines.append(' '.join(pre+r2+r1))
        dst.write_text('\n'.join(lines)+'\n')
    print(f'R2G_LOSSLESS_LAYOUT_ADAPTER_OK files={len(fs)}')

if __name__=='__main__': main()
