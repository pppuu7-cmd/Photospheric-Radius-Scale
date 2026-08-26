# RTK C10.65s2i adaptive-step trace checkpoint

Classification: `C10_65S2I_ADAPTIVE_STEP_TRACE_PASS_SCOPED`. Original C10.65s2 remains FAIL_SCOPED. The run reused the original 1e-4 Mpc interval and unchanged perturbation tolerance; only integrator bookkeeping was logged.

- k=1e-05: accepted=9, rejected=8, first_hdid=1.47674160386346544e-09, min_hdid=1.47674160386346544e-09
- k=3e-05: accepted=10, rejected=9, first_hdid=7.07987222954994042e-10, min_hdid=7.07987222954994042e-10
- k=0.0001: accepted=10, rejected=8, first_hdid=1.03188215788510024e-09, min_hdid=9.76420204417817679e-10
- k=0.0003: accepted=9, rejected=7, first_hdid=1.11352665641022328e-09, min_hdid=1.11352665641022328e-09

Total accepted substeps: 38; total rejected RKCK trials: 32. Minimum first accepted hdid across anchors: 7.07987222954994042e-10.

No retry width was selected in this gate. Next: freeze C10.65s2j prospective retry-width contract from this trace, then execute a separate retry with unchanged tolerance and exactly-one-accepted-step requirement.
