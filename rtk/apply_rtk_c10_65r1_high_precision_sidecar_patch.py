#!/usr/bin/env python3
"""Add a C10.65r1-only 17-digit scalar perturbation sidecar in output.c.

The standard CLASS perturbation file remains byte-for-byte untouched.  CLASS v2.4.5
serializes standard numeric columns with _OUTPUTPRECISION_=12; this opt-in sidecar
writes the same stored double array with %.17e only when c10_65r1_diag=1.  It is a
measurement channel, not a dynamics/RHS/state modification.
"""
from pathlib import Path
import sys

root=Path(sys.argv[1] if len(sys.argv)>1 else 'class_public')
outc=root/'source'/'output.c'
s=outc.read_text()
marker='RTK_C10_65R1_HIGH_PRECISION_SIDECAR_V1'
if marker in s:
    print('C10_65R1_HIGH_PRECISION_SIDECAR_ALREADY_APPLIED')
    raise SystemExit(0)

anchor='''      output_print_data(out,
                        ppt->scalar_titles,
                        ppt->scalar_perturbations_data[index_ikout],
                        ppt->size_scalar_perturbation_data[index_ikout]);

      fclose(out);'''
if anchor not in s:
    raise SystemExit('scalar output anchor not found in pinned output.c')
replacement='''      output_print_data(out,
                        ppt->scalar_titles,
                        ppt->scalar_perturbations_data[index_ikout],
                        ppt->size_scalar_perturbation_data[index_ikout]);

      fclose(out);

      /* RTK_C10_65R1_HIGH_PRECISION_SIDECAR_V1
       * Standard CLASS output above intentionally stays unchanged.  The sidecar
       * serializes the identical stored double array at round-trip precision so
       * cancellation-sensitive diagnostic parity is not limited by the legacy
       * _OUTPUTPRECISION_=12 text format. */
      if ((pba->model == 2.) && (pba->c10_65r1_diag > 0.5)) {
        int r1hp_nt, r1hp_row, r1hp_col, r1hp_rows;
        r1hp_nt = get_number_of_titles(ppt->scalar_titles);
        class_test(r1hp_nt <= 0,pop->error_message,"C10.65r1 high-precision sidecar has no scalar titles");
        class_test((ppt->size_scalar_perturbation_data[index_ikout] % r1hp_nt) != 0,
                   pop->error_message,"C10.65r1 high-precision sidecar shape mismatch");
        r1hp_rows = ppt->size_scalar_perturbation_data[index_ikout]/r1hp_nt;
        sprintf(file_name,"%s%s%d%s",pop->root,"perturbations_k",index_ikout,"_s_r1hp.dat");
        class_open(out,file_name,"w",pop->error_message);
        fprintf(out,"# RTK C10.65r1 full-precision scalar diagnostic for k = %.17e Mpc^(-1)\\n",k);
        fprintf(out,"# identical in-memory scalar_perturbations_data, serialized with %%.17e\\n");
        for (r1hp_row=0; r1hp_row<r1hp_rows; r1hp_row++) {
          for (r1hp_col=0; r1hp_col<r1hp_nt; r1hp_col++) {
            fprintf(out," %.17e",ppt->scalar_perturbations_data[index_ikout][r1hp_row*r1hp_nt+r1hp_col]);
          }
          fprintf(out,"\\n");
        }
        fclose(out);
      }'''
s=s.replace(anchor,replacement,1)
outc.write_text(s)
print('C10_65R1_HIGH_PRECISION_SIDECAR_APPLIED')
