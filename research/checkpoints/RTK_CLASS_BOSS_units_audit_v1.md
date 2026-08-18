# RTK CLASS background / BOSS units audit v1

Status: **PASS** — production CLASS background-column interpretation and BOSS DR12 distance/Hubble rescalings are dimensionally and conventionally consistent.

## 1. Actual pinned CLASS output header

The successful standard-siren run `32083365308` retained the actual patched CLASS background file `class_public/output/rtk_gw_background.dat`. Its header states:

```text
# Densities are in units [Mpc^-2] while all distances are in [Mpc].
# 1:z  2:proper time [Gyr]  3:conf. time [Mpc]  4:H [1/Mpc]
# 5:comov. dist.  6:ang.diam.dist.  7:lum. dist.  8:comov.snd.hrz. ...
```

That run uses the production locked CLASS upstream commit
`36cf283628c4a3330ec9fd3d84239bf775f77317` plus the RTK patches.

Therefore, for zero-based Python rows:

- `row[3]` is `H` in `1/Mpc`;
- `row[4]` is comoving distance in `Mpc`;
- `row[6]` is luminosity distance in `Mpc`.

## 2. Production parser use

`rtk/joint_profile_runner.py` uses:

```python
# Pantheon
DL_Mpc = interp_rows(bg, 6, z)

# BOSS
if kind == 'DM_over_rs':
    pred = interp_rows(bg, 4, z) * R_FID / rd
elif kind == 'bao_Hz_rs':
    pred = interp_rows(bg, 3, z) * C_KM_S * rd / R_FID
```

with

```text
C_KM_S = 299792.458
R_FID  = 147.78 Mpc
```

Thus the code maps the actual CLASS columns exactly as intended.

## 3. Independent BOSS DR12 convention

The final BOSS DR12 consensus analysis (Alam et al., MNRAS 470, 2617, Table 7; DOI 10.1093/mnras/stx721) defines the reported observables as

```text
D_M(z) * (r_d,fid / r_d)              [Mpc]
H(z)   * (r_d / r_d,fid)              [km s^-1 Mpc^-1]
f(z) sigma8(z)
```

and states `r_d,fid = 147.78 Mpc`.

The repository data values

```text
z=0.38: 1518.36, 81.5095, 0.49749
z=0.51: 1977.44, 90.4474, 0.457523
z=0.61: 2283.18, 97.2556, 0.436148
```

are the full-precision consensus values in this convention.

## 4. Dimensional check

For `D_M`:

```text
[Mpc] * [Mpc]/[Mpc] = [Mpc]
```

For `H`, CLASS supplies `H_CLASS` in `1/Mpc`. Multiplying by `c` converts it to `km s^-1 Mpc^-1`, after which `rd/R_FID` is dimensionless:

```text
[1/Mpc] * [km/s] * [Mpc]/[Mpc] = [km s^-1 Mpc^-1].
```

Pantheon receives CLASS column 7 directly as luminosity distance in Mpc before `5 log10(D_L)+25`.

## Closure

- ✅ Actual production-like patched CLASS header independently inspected.
- ✅ `H` column index and units verified.
- ✅ comoving-distance column index and units verified.
- ✅ luminosity-distance column index and units verified.
- ✅ BOSS DR12 published observable convention independently verified.
- ✅ `r_d,fid = 147.78 Mpc` independently verified.
- ✅ Production BOSS formulas are dimensionally correct.

This closes the previously open `independent CLASS background header/unit verification` item. It does not address growth-mapping physics (`eff` vs `k01`), which remains a separately controlled model choice and is not mixed here.
