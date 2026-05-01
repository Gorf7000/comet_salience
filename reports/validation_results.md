# Validation Results
_Generated 2026-05-01 01:31 UTC_

Four independent checks: external-peak comparison, hand calculation,
manual-CSV path test, and artifact inspection. Designed to be readable
in 5 minutes and to surface issues that the pipeline's internal
validation does not catch.

## TL;DR

**Pipeline implementation is correct; SBDB photometric data quality is uneven.**

- Hand calc: pipeline `apparent_mag` matches the formula `m = M1 + 5·log10(Δ) + K1·log10(r)` to within 0.0003 mag using SBDB's stored (M1, K1) for Halley. **Tier 1 path is implemented correctly.**
- Tier 1.5 path: a test entry for Donati 1858 (Vsekhsvyatskij M1=4.7, K1=10) correctly engaged the manual_curated provenance, generated 361 daily rows, peak mag 1.21, 84 days naked-eye. **Manual CSV ingestion works end-to-end.**
- All 9 diagnostic figures rendered. Audit report includes the manual-entry candidate list as designed.
- External peak comparison: 5 of 10 reference comets agree within ±1.5 mag (Halley 1910, Swift-Tuttle 1862, Pons-Brooks 1884, Brorsen 1879, Brorsen-Metcalf 1919). The misses are mostly **SBDB data-quality issues, not pipeline bugs** — see check 1 below for breakdown.

**One benchmark-table bug on my side**: I accidentally included Halley 1835 in the reference set (out of scope, correctly absent from the summary). Counted as a "miss" in the table; ignore that row.

**Headline implication**: even the periodic dataset has uneven photometric quality. The chapter analysis should be aware that some periodic comets (Encke 2P, Tuttle 8P) are systematically too dim by 5–7 magnitudes in this dataset due to SBDB-stored parameters that look biased toward modern less-active returns. If desired, a future increment could add a Tier 1.5-style override mechanism *for* periodic comets too — but that would require amending §8.2 rule 3 ("no manual overrides").


## 1. External peak-magnitude comparison

External-peak check: 5/10 within ±1.5 mag of observed.
  - 1P 1835: observed +1.0, modeled nan, diff nan — MISSING from summary
  - 2P 1898: observed +6.0, modeled 12.686, diff 6.686 — Encke 1898; mid-range estimate, Encke varies +5 to +7
  - 3D 1852: observed +5.0, modeled 7.319, diff 2.319 — Biela 1852 final intact return; Kronk: peak ~+5
  - 8P 1858: observed +7.0, modeled 14.211, diff 7.211 — Tuttle 1858 discovery; Kronk: peak ~+7
  - 17P 1892: observed +5.0, modeled 15.411, diff 10.411 — Holmes 1892; famous outburst, peak ~+5 (M1/K1 model will not capture)

Detailed comparison table:

| comet_id | year | observed peak | modeled peak | diff | within ±1.5? | notes |
|---|---|---|---|---|---|---|
| 1P | 1910 | +0.0 | 1.00 | +1.00 | yes | Halley 1910; Kronk: peak ~0, briefly -0.5 in early May |
| 1P | 1835 | +1.0 | nan | +nan | **no** | MISSING from summary |
| 109P | 1862 | +2.0 | 1.97 | -0.03 | yes | Swift-Tuttle 1862 discovery; Kronk: peak ~+2 |
| 12P | 1884 | +3.0 | 2.60 | -0.40 | yes | Pons-Brooks 1884; Kronk: peak +3 to +3.5 |
| 2P | 1898 | +6.0 | 12.69 | +6.69 | **no** | Encke 1898; mid-range estimate, Encke varies +5 to +7 |
| 3D | 1852 | +5.0 | 7.32 | +2.32 | **no** | Biela 1852 final intact return; Kronk: peak ~+5 |
| 5D | 1879 | +6.0 | 5.97 | -0.03 | yes | Brorsen 1879; Kronk: peak ~+5 to +6 |
| 23P | 1919 | +5.0 | 4.30 | -0.70 | yes | Brorsen-Metcalf 1919; Kronk: peak ~+5 |
| 8P | 1858 | +7.0 | 14.21 | +7.21 | **no** | Tuttle 1858 discovery; Kronk: peak ~+7 |
| 17P | 1892 | +5.0 | 15.41 | +10.41 | **no** | Holmes 1892; famous outburst, peak ~+5 (M1/K1 model will not capture) |

## 2. Hand calculation of magnitude formula

Hand-calc on 1P_1910 near-perihelion row:
  date=1910-04-20, days_from_perihelion=0.0
  r=0.587223 AU, Δ=1.214662 AU
  SBDB M1=5.5, K1=8.0
  pipeline apparent_mag = 4.0730
  hand calc m = 5.5 + 5·log10(1.2147) + 8.0·log10(0.5872) = 4.0727
  diff = +0.0003 mag
  RESULT: agreement within 0.1 mag — Tier 1 formula path is consistent.

## 3. Manual M1/K1 CSV path (Tier 1.5)

Manual-CSV check on C/1858 L1 with Vsekhsvyatskij M1=4.7, K1=10:
  magnitude_provenance = manual_curated
  manual_curated_source_citation = 'Vsekhsvyatskij 1958 (test entry)'
  generated daily rows: 361
  modeled peak_mag = 1.21 (observed peak ~-1)
  days_mag_le_6 = 84
  integrated_mag6_excess = 213.3
  RESULT: Tier 1.5 path engaged correctly.

## 4. Audit report + diagnostic figures

Audit report: C:\Users\grfai\Documents\0_Dissertation\Code\Ch 5 Comet Salience\reports\comet_visibility_audit.md
  size: 13179 bytes, 294 lines
  contains 'Manual M1/K1 candidates': True
  contains 'Tier 3 non-periodic candidates: ': True
  contains 'Validation failures': True

Diagnostic figures in C:\Users\grfai\Documents\0_Dissertation\Code\Ch 5 Comet Salience\figures\comet_visibility_diagnostics:
  OK   01_peak_mag_histogram.png (24588 bytes)
  OK   02_peak_vs_duration.png (31474 bytes)
  OK   03_integrated_vs_spectacle_mag.png (31859 bytes)
  OK   04_mag_vs_flux_families.png (32145 bytes)
  OK   05_event_case_counts.png (39426 bytes)
  OK   06_main_sample_candidate.png (18581 bytes)
  OK   07a_top_by_integrated_mag.png (145617 bytes)
  OK   07b_top_by_spectacle_mag.png (146549 bytes)
  OK   07c_top_by_flux.png (147759 bytes)
