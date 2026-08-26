#!/usr/bin/env python3
"""C10.65s4a2 read-only exact-onset geometry audit.

This patch only adds a dormant diagnostic call after CLASS has constructed the
ordinary approximation intervals.  The diagnostic measures the inverse-spline
round trip and a forward-spline-consistent root for a_on, and reports interval
membership.  It does not alter the integration state, metric workspace,
physics kernel, tolerances, timescale, approximation criteria, or interval
construction.
"""
from pathlib import Path
import sys

root=Path(sys.argv[1] if len(sys.argv)>1 else 'class_public')
pt=root/'source'/'perturbations.c'
mk=root/'Makefile'
ps=pt.read_text(); ms=mk.read_text()
marker='RTK_C10_65S4A2_EXACT_ONSET_GEOMETRY_AUDIT_V1'
if marker in ps:
    print('C10_65S4A2_GEOMETRY_AUDIT_PATCH_ALREADY_APPLIED')
    raise SystemExit(0)

src=r'''/* RTK_C10_65S4A2_EXACT_ONSET_GEOMETRY_AUDIT_V1 */
#include "perturbations.h"
#include <stdlib.h>
#include <stdio.h>
#include <math.h>

#if defined(__GNUC__)
#define RTK_GEO_NOINLINE __attribute__((noinline,noclone))
#else
#define RTK_GEO_NOINLINE
#endif

static int rtk_geo_target_k(double k) {
  const double k1=1.e-3,k2=3.e-3;
  return (fabs(k-k1) <= 5.e-12*k1) || (fabs(k-k2) <= 5.e-12*k2);
}

static int rtk_geo_bg_at_tau(struct background *pba,double tau,double *buf,double *a,ErrorMsg error_message) {
  int last=0;
  class_call(background_at_tau(pba,tau,pba->short_info,pba->inter_normal,&last,buf),
             pba->error_message,error_message);
  *a=buf[pba->index_bg_a];
  return _SUCCESS_;
}

RTK_GEO_NOINLINE int rtk_c10_65s4a2_geometry_observe(
  struct background *pba,
  struct perturb_workspace *ppw,
  double k,
  int interval_number,
  double *interval_limit,
  int **interval_approx,
  ErrorMsg error_message) {
  const char *path=getenv("RTK_C10_65S4A2_GEOMETRY_FILE");
  const double aon=0.0002203229136467;
  double tauz,az,relz,lo,hi,alo,ahi,mid,amid,tauc,ac,relc;
  double *buf;
  int it,iz=-1,ic=-1,i,same=-1,tca=-1,rsa=-1,ufa=-1;
  FILE *f;
  if (path==NULL || path[0]=='\0' || !rtk_geo_target_k(k)) return _SUCCESS_;
  buf=(double*)malloc((size_t)pba->bg_size_short*sizeof(double));
  class_test(buf==NULL,error_message,"C10.65s4a2 background buffer allocation failed");
  class_call(background_tau_of_z(pba,1./aon-1.,&tauz),pba->error_message,error_message);
  class_call(rtk_geo_bg_at_tau(pba,tauz,buf,&az,error_message),error_message,error_message);
  relz=fabs(az-aon)/aon;

  lo=pba->tau_table[0]; hi=pba->tau_table[pba->bt_size-1];
  class_call(rtk_geo_bg_at_tau(pba,lo,buf,&alo,error_message),error_message,error_message);
  class_call(rtk_geo_bg_at_tau(pba,hi,buf,&ahi,error_message),error_message,error_message);
  class_test(!(alo <= aon && aon <= ahi),error_message,
             "C10.65s4a2 a_on not bracketed by background table: [%g,%g] target=%g",alo,ahi,aon);
  mid=0.5*(lo+hi); amid=0.;
  for (it=0;it<96;it++) {
    mid=0.5*(lo+hi);
    class_call(rtk_geo_bg_at_tau(pba,mid,buf,&amid,error_message),error_message,error_message);
    if (fabs(amid-aon)/aon <= 1.e-13) break;
    if (amid < aon) lo=mid; else hi=mid;
  }
  tauc=mid; ac=amid; relc=fabs(ac-aon)/aon;

  for (i=0;i<interval_number;i++) {
    if (tauz >= interval_limit[i] && tauz <= interval_limit[i+1]) iz=i;
    if (tauc >= interval_limit[i] && tauc <= interval_limit[i+1]) ic=i;
  }
  if (iz>=0 && ic>=0) same=(iz==ic)?1:0;
  if (ic>=0) {
    tca=interval_approx[ic][ppw->index_ap_tca];
    rsa=interval_approx[ic][ppw->index_ap_rsa];
    ufa=interval_approx[ic][ppw->index_ap_ufa];
  }
  f=fopen(path,"a");
  class_test(f==NULL,error_message,"C10.65s4a2 cannot open geometry file");
  fprintf(f,"%.17e,%.17e,%.17e,%.17e,%.17e,%.17e,%.17e,%.17e,%.17e,%d,",
          k,tauz,az,relz,tauc,ac,relc,interval_limit[0],interval_limit[interval_number],iz);
  if (iz>=0) fprintf(f,"%.17e,%.17e,",interval_limit[iz],interval_limit[iz+1]);
  else fprintf(f,"nan,nan,");
  fprintf(f,"%d,",ic);
  if (ic>=0) fprintf(f,"%.17e,%.17e,",interval_limit[ic],interval_limit[ic+1]);
  else fprintf(f,"nan,nan,");
  fprintf(f,"%d,%d,%d,%d\n",same,tca,rsa,ufa);
  fclose(f); free(buf);
  return _SUCCESS_;
}
'''
(root/'source'/'rtk_c10_65s4a2_geometry.c').write_text(src)

decl=('extern int rtk_c10_65s4a2_geometry_observe(struct background*,struct perturb_workspace*,double,int,double*,int**,ErrorMsg); /* '+marker+' */\n')
inc='#include "perturbations.h"\n'
if inc not in ps: raise SystemExit('perturbations include anchor missing')
ps=ps.replace(inc,inc+decl,1)
anchor='  free(interval_number_of);\n'
if ps.count(anchor)!=1: raise SystemExit(f'interval-number free anchor count={ps.count(anchor)}')
call='''  if (getenv("RTK_C10_65S4A2_GEOMETRY_FILE") != NULL) {
    class_call(rtk_c10_65s4a2_geometry_observe(pba,ppw,k,interval_number,interval_limit,interval_approx,ppt->error_message),
               ppt->error_message,ppt->error_message);
  }
'''
ps=ps.replace(anchor,anchor+call,1)
pt.write_text(ps)

if 'rtk_c10_65s4a2_geometry.o' not in ms:
    anchor_m='SOURCE = input.o background.o thermodynamics.o perturbations.o primordial.o nonlinear.o transfer.o spectra.o lensing.o'
    if anchor_m not in ms: raise SystemExit('Makefile SOURCE anchor missing')
    ms=ms.replace(anchor_m,anchor_m+' rtk_c10_65s4a2_geometry.o',1)
    mk.write_text(ms)
print('C10_65S4A2_GEOMETRY_AUDIT_PATCH_APPLIED')
