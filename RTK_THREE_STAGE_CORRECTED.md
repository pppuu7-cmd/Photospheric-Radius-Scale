# RT+DBI-Khronon — corrected three-stage observational test

This report supersedes the earlier absolute-amplitude/likelihood numbers that used `A_s_ad` and `n_s_ad`. The public legacy `dirian/class_public` nonlocal branch reads `A_s` and `n_s`; all three stages below were rerun with the correct primordial parameter names.

## Stage 1 — lower lambda_D scan

Corrected fixed-baseline runs were completed for lambda_D = 1000, 2000, 3000 and the previous higher grid.

| lambda_D | gamma | sigma8(z=0) | fs8_eff(z=0) | P/P_LCDM k=0.2 | k=0.5 | k=1.0 |
|---:|---:|---:|---:|---:|---:|---:|
| 1000 | 0.0510443278 | 0.7826523 | 0.3253920 | 0.9007249 | 0.7874203 | 0.6929438 |
| 2000 | 0.0510480464 | 0.7995114 | 0.3510926 | 0.9471389 | 0.8514467 | 0.7622895 |
| 3000 | 0.0510492935 | 0.8072230 | 0.3665180 | 0.9689141 | 0.8859114 | 0.8021882 |
| LCDM | - | 0.8177740 | 0.4268745 | 1 | 1 | 1 |

Lower lambda_D produces stronger late scale-dependent suppression. These fixed-baseline growth numbers are predictions of the tested parameter points, not constraints.

## Stage 2 — Pantheon + BOSS DR12 full covariance

Pantheon uses the official 40-bin systematic covariance plus diagonal statistical errors, with the additive magnitude/H0 offset minimized analytically. BOSS DR12 uses the final consensus 9x9 covariance of DM, H and f sigma8 at z=0.38, 0.51 and 0.61.

Because RTK growth is scale dependent, the compressed BOSS f sigma8 observable is not strictly survey independent. Two mappings are reported: `fs8_eff=d sigma8/d ln a` and `f(k=0.1 h/Mpc)*sigma8`.

| model | lambda_D | chi2_SN | chi2_BOSS_eff | chi2_BOSS_k0.1 | Delta total eff | Delta total k0.1 |
|---|---:|---:|---:|---:|---:|---:|
| LCDM | - | 39.7149 | 7.1703 | 7.1761 | 0 | 0 |
| RTK | 1000 | 39.2757 | 14.6142 | 12.7159 | 7.0047 | 5.1006 |
| RTK | 2000 | 39.2772 | 12.4658 | 11.6456 | 4.8578 | 4.0317 |
| RTK | 3000 | 39.2777 | 11.8507 | 11.3481 | 4.2433 | 3.7348 |
| RTK | 4000 | 39.2780 | 11.5756 | 11.2149 | 3.9684 | 3.6019 |
| RTK | 8000 | 39.2784 | 11.2062 | 11.0423 | 3.5994 | 3.4296 |
| RTK | 10000 | 39.2785 | 11.1383 | 11.0131 | 3.5316 | 3.4006 |
| RTK | 15000 | 39.2786 | 11.0518 | 10.9783 | 3.4452 | 3.3658 |
| RTK | 20000 | 39.2786 | 11.0112 | 10.9631 | 3.4047 | 3.3507 |

The full covariance reverses the earlier diagonal-coarse trend. At fixed baseline parameters the best tested RTK point is at the high-lambda edge, but it remains worse than the matched LCDM control. Pantheon mildly improves RTK; BOSS is the dominant penalty.

## Stage 3A — official Planck 2018 fixed-parameter likelihood

The official Planck 2018 baseline package was evaluated using Commander low-T, SimAll low-E and nuisance-marginalized Plik-lite TTTEEE. Lensed CLASS spectra were run to ell=2600.

| model | lambda_D | logL lowT | logL lowE | logL high-l | Delta(-2 ln L) vs LCDM |
|---|---:|---:|---:|---:|---:|
| LCDM | - | -11.59637 | -198.40663 | -332.64907 | 0 |
| RTK | 1000 | -11.46382 | -198.42616 | -554.18520 | +442.84623 |
| RTK | 2000 | -11.45997 | -198.42616 | -560.50302 | +455.47416 |
| RTK | 3000 | -11.45888 | -198.42616 | -562.64953 | +459.76500 |

At the unretuned baseline cosmology the large penalty is almost entirely high-l Plik-lite. This fixed-parameter result is not a final constraint because the cosmological parameters must be reprofiled.

## Stage 3B — corrected joint local profile and focused validation

Objective:

S = -2 ln L_Planck + chi2_Pantheon + chi2_BOSS.

The RTK local profile varied lambda_D, h, Omega_b, Omega_K0, A_s, n_s and z_reio, with gamma derived from the one-scale closure. A comparable LCDM profile varied h, Omega_b, Omega_cdm, A_s, n_s and z_reio.

A first broad coordinate profile appeared to favor RTK, but this was identified as coordinate-order/optimizer bias. A second focused symmetric validation around both minima is the result to use.

### Focused best LCDM

- h = 0.678
- Omega_b = 0.048
- Omega_cdm = 0.26
- A_s = 2.1e-9
- n_s = 0.9675
- z_reio = 8.0
- r_d = 147.564527 Mpc
- Planck total logL = -506.55012364
- chi2_SN = 39.66108246
- chi2_BOSS_eff = 6.36128397
- chi2_BOSS_k0.1 = 6.36294170
- S_eff = 1059.12261372
- S_k0.1 = 1059.12427144

### Focused best RTK

- lambda_D = 1150
- h = 0.684
- Omega_b = 0.0475
- Omega_K0 = 0.26
- A_s = 2.037e-9
- n_s = 0.963
- z_reio = 6.0
- r_d = 146.793878 Mpc
- Planck total logL = -505.52544773
- chi2_SN = 39.29103390
- chi2_BOSS_eff = 10.07375768
- chi2_BOSS_k0.1 = 8.82437252
- S_eff = 1060.41568704
- S_k0.1 = 1059.16630188

### Focused comparison

Using the effective-growth BOSS mapping:

Delta S_RTK-LCDM = +1.29307333.

Using the k=0.1 h/Mpc BOSS mapping:

Delta S_RTK-LCDM = +0.04203044.

Thus the validated local profile does not establish an RTK preference. It shows that, after retuning cosmological parameters, the large fixed-parameter Planck penalty can disappear and RTK can approach the LCDM objective closely. The residual result is dominated by the treatment of BOSS/RSD scale-dependent growth.

A useful decomposition for the effective-growth mapping is approximately:
- Planck primary: RTK improves the objective by 2.05;
- Pantheon: RTK improves by 0.37;
- BOSS: RTK worsens by 3.71;
- net: RTK is worse by 1.29.

## What is and is not established

Established at this stage:
1. The full RT+DBI-Khronon linear CLASS implementation can be run through official Planck primary likelihood pieces and full-covariance Pantheon/BOSS diagnostics.
2. The enormous fixed-baseline high-l CMB mismatch is not invariant under cosmological parameter retuning.
3. A focused local profile finds RTK within Delta S roughly 0 to 1.3 of LCDM depending on how compressed scale-dependent RSD is mapped.
4. BOSS/RSD treatment is currently the decisive ambiguity in the joint comparison.

Not established:
1. No global posterior, global best fit, confidence interval or Bayesian evidence has been obtained.
2. The BOSS compressed f sigma8 likelihood is not formally exact for scale-dependent RTK growth without survey-window reanalysis.
3. Planck lensing likelihood, CMB lensing reconstruction, DESI/eBOSS, cosmic shear and nonlinear structure are not yet included.
4. No observational preference for RTK over LCDM is claimed.
