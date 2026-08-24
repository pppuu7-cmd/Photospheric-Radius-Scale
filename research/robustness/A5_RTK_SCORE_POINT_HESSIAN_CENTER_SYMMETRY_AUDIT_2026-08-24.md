# A5 RTK score-point / Hessian-center symmetry audit — 2026-08-24

Triggered by the LCDM historical stationarity-semantics correction.

Under the unchanged `matched-ultra-linstep2+dense-BOSS` objective, the RTK accepted-score parameters and accepted center are identical:

- `As=2.0877827951474356e-09`
- `Ob=0.046800730927437424`
- `Om=0.2522864064078236`
- `h=0.691103719964454`
- `lambda_D=219457.5727136581`
- `ns=0.9645577770978523`
- `zre=7.328459220286924`
- `S_eff=1050.249912429787`.

The final base-scale Hessian is centered at exactly this point, has best exact improvement `0.0`, is positive definite, and has minimum eigenvalue `0.0002539372582019114`.

The final half-scale Hessian is also centered at exactly this point, has best exact improvement `0.0`, is positive definite, and has minimum eigenvalue `0.0002755537750933801`.

Therefore the new score-point-versus-Hessian-center guard does not reopen the historical RTK A5 local certification. The LCDM correction is not applied symmetrically by assumption; it is applied symmetrically by checking exact parameter identity, and RTK passes that check.

This remains a local certificate only. It is not a global minimum, significance, posterior, AIC/BIC or Bayes statement.
