# RTK C10.65s4a moderate-k onset-state domain preflight

Classification: `C10_65S4A_MODERATE_K_ONSET_STATE_DOMAIN_PREFLIGHT_FAIL_SCOPED`. New anchors: `1e-3, 3e-3 Mpc^-1`; max k/Hc: `2.31429153649836961e-01`; max |A2 k^2/J|: `3.36271969156682433e-03`.

Historical first attempt run 33008095108 remains a scoped FAIL because the inherited observer did not materialize exact onset at the new k anchors. The successful sampling repair, if used here, changes only observer sampling geometry and no frozen scientific guard.

This gate checks state-domain availability only; no completed-U1 seed or production trajectory at the new k values is certified here.
