# RT+DBI-Khronon covariance-likelihood stage

The lower-lambda scan and full-covariance diagnostic were completed on the patched RT-CLASS pipeline.

## Stage 1: lambda_D = 1000, 2000, 3000

The extended fixed-parameter scan completed successfully. The diagonal coarse diagnostic gave its lowest tested score at lambda_D=1000, but this trend did not survive the covariance-aware analysis below.

Selected z=0 results:

| lambda_D | gamma | r_d [Mpc] | sigma8 | fs8_eff | P/P_LCDM k=0.2 | k=0.5 | k=1.0 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1000 | 0.05104432776 | 147.423051 | 0.8029049 | 0.3338698 | 0.9007249 | 0.7874204 | 0.6929461 |
| 2000 | 0.05104804642 | 147.441175 | 0.8201857 | 0.3602287 | 0.9471389 | 0.8514468 | 0.7622916 |
| 3000 | 0.05104929345 | 147.447259 | 0.8280889 | 0.3760462 | 0.9689141 | 0.8859115 | 0.8021902 |
| LCDM | - | 147.459518 | 0.8388853 | 0.4378945 | 1 | 1 | 1 |

## Stage 2: full covariance

Pantheon uses the official 40-bin systematic covariance plus diagonal statistical dmb^2, with the additive magnitude/H0 offset minimized analytically. BOSS DR12 uses the final consensus 9x9 covariance of DM, H and f sigma8 at z=0.38, 0.51 and 0.61.

Because RTK growth is scale dependent, the compressed BOSS f sigma8 observable is not uniquely survey independent for this model. Two diagnostic mappings were therefore evaluated: fs8_eff = d sigma8/d ln a and f(k=0.1 h/Mpc)*sigma8.

| model | lambda_D | chi2_SN | chi2_BOSS_eff | chi2_BOSS_k0.1 | Delta total eff | Delta total k0.1 |
|---|---:|---:|---:|---:|---:|---:|
| LCDM | - | 39.7149 | 7.6539 | 7.6686 | 0 | 0 |
| RTK | 1000 | 39.2757 | 13.7093 | 12.5510 | 5.6162 | 4.4432 |
| RTK | 2000 | 39.2772 | 12.2657 | 11.9956 | 4.1740 | 3.8893 |
| RTK | 3000 | 39.2777 | 11.9649 | 11.8751 | 3.8738 | 3.7693 |
| RTK | 4000 | 39.2780 | 11.8641 | 11.8259 | 3.7732 | 3.7204 |
| RTK | 8000 | 39.2784 | 11.7683 | 11.7637 | 3.6779 | 3.6586 |
| RTK | 10000 | 39.2785 | 11.7538 | 11.7528 | 3.6634 | 3.6477 |
| RTK | 15000 | 39.2786 | 11.7345 | 11.7390 | 3.6442 | 3.6340 |
| RTK | 20000 | 39.2786 | 11.7244 | 11.7325 | **3.6342** | **3.6276** |

The full covariance qualitatively reverses the earlier diagonal coarse ranking. On this fixed-parameter grid the best tested RTK point is lambda_D=20000, but it still has a positive Delta chi2 relative to the matched LCDM control. Pantheon alone improves slightly, while the BOSS joint covariance is the dominant penalty. No observational confidence interval or best-fit lambda_D is claimed from this stage.
