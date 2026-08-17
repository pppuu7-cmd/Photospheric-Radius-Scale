# Restoration addendum — Stage4D3 dense stationarity prep

Use together with `rtk/RESTORE_POINT_2026-08-17_STAGE4D3_DENSE.md`.

## New developments after the base checkpoint

1. The two active scientific runs were still in progress when this addendum was written:
   - RTK dense 7D axis gate: run `31985345036`, job `95259287035`.
   - LCDM dense 6D Hessian: run `31985735749`, job `95260337088`.

2. The RTK and LCDM production codes were explicitly checked to use the same dense BOSS z-grid and the same matched-ultra CLASS overrides.

3. A gated RTK dense 7D Hessian workflow was prepared on `main` without auto-launching:
   - workflow: `.github/workflows/rtk-dense-7d-stationarity.yml`
   - commit: `1b74f8c82c24047277bc2880159eea4022283af5`
   - it triggers only when `rtk/TRIGGER_DENSE_RTK_7D_HESSIAN` is pushed (or manual workflow_dispatch).
   - do not create the trigger until RTK axis-gate scientific result is read.

4. Final comparison protocol was frozen before seeing the Hessian results:
   - file: `rtk/FINAL_MATCHED_COMPARISON_PROTOCOL.md`
   - mapping-specific clarification commit: `a9e9147cb4f1ba6cea502dae48b0351b104930f3`.

5. Important mapping rule: `eff` and `k01` are separate objective variants. A `k01` improvement cannot by itself recenter the `eff` branch, and vice versa. If they prefer different centers, preserve separate branches.

6. The prepared full RTK Hessian script was corrected so that `eff` and `k01` each receive their own Newton/trust proposal:
   - file: `rtk/dense_rtk_7d_stationarity.py`
   - corrected commit: `d0d26345b7fdef8b2f6acfe6624b89bcf39b857c`.

## Immediate continuation rule

- Read run `31985345036` first.
- For `eff`, if best exact axis improvement `> 0.005`, recenter/revalidate the `eff` branch before Hessian. If `<= 0.005`, trigger the prepared full dense RTK 7D Hessian at the frozen center.
- Apply the same decision independently to `k01`; do not mix mapping-specific centers.
- Read run `31985735749` and record LCDM center score, Hessian eigenvalues, positive-definite status, Newton score, and best exact improvement.
- Only compare RTK and LCDM raw scores after matched local certification on the same objective and same mapping.
