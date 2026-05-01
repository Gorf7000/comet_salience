# Validation Results
_Generated 2026-05-01 16:58 UTC_

Four independent checks: external-peak comparison, hand calculation,
manual-CSV path test, and artifact inspection. Designed to be readable
in 5 minutes and to surface issues that the pipeline's internal
validation does not catch.

## 1. External peak-magnitude comparison

External-peak check: 8/13 within ±1.5 mag of observed.
  - 2P 1898: observed +6.0, modeled 4.052215290428391, diff -1.947784709571609 — Encke 1898; mid-range estimate, Encke varies +5 to +7
  - 3D 1852: observed +5.0, modeled 8.219189513968946, diff 3.2191895139689457 — Biela 1852 final intact return; Kronk: peak ~+5
  - 17P 1892: observed +5.0, modeled 13.831119414599986, diff 8.831119414599986 — Holmes 1892; famous outburst, peak ~+5 (M1/K1 model will not capture)
  - C/1882 R1 1882: observed -10.0, modeled -13.132751984921372, diff -3.132751984921372 — Great September Comet 1882; sungrazer, peak ~-17 in daylight (single-law model will under-predict)
  - C/1910 A1 1910: observed -1.0, modeled -3.770183864478436, diff -2.770183864478436 — Great January Comet 1910; widely reported peak ~-1 to -5

Detailed comparison table:

| comet_id | year | observed peak | modeled peak | diff | within ±1.5? | notes |
|---|---|---|---|---|---|---|
| 1P | 1910 | +0.0 | -0.12 | -0.12 | yes | Halley 1910; Kronk: peak ~0, briefly -0.5 in early May |
| 109P | 1862 | +2.0 | 1.54 | -0.46 | yes | Swift-Tuttle 1862 discovery; Kronk: peak ~+2 |
| 12P | 1884 | +3.0 | 3.01 | +0.01 | yes | Pons-Brooks 1884; Kronk: peak +3 to +3.5 |
| 2P | 1898 | +6.0 | 4.05 | -1.95 | **no** | Encke 1898; mid-range estimate, Encke varies +5 to +7 |
| 3D | 1852 | +5.0 | 8.22 | +3.22 | **no** | Biela 1852 final intact return; Kronk: peak ~+5 |
| 5D | 1879 | +6.0 | 5.67 | -0.33 | yes | Brorsen 1879; Kronk: peak ~+5 to +6 |
| 23P | 1919 | +5.0 | 5.93 | +0.93 | yes | Brorsen-Metcalf 1919; Kronk: peak ~+5 |
| 8P | 1858 | +7.0 | 7.56 | +0.56 | yes | Tuttle 1858 discovery; Kronk: peak ~+7 |
| 17P | 1892 | +5.0 | 13.83 | +8.83 | **no** | Holmes 1892; famous outburst, peak ~+5 (M1/K1 model will not capture) |
| C/1858 L1 | 1858 | -1.0 | -0.19 | +0.81 | yes | Donati 1858; widely reported peak ~-1 |
| C/1861 J1 | 1861 | +0.0 | -0.99 | -0.99 | yes | Tebbutt 1861; widely reported peak ~0 |
| C/1882 R1 | 1882 | -10.0 | -13.13 | -3.13 | **no** | Great September Comet 1882; sungrazer, peak ~-17 in daylight (single-law model will under-predict) |
| C/1910 A1 | 1910 | -1.0 | -3.77 | -2.77 | **no** | Great January Comet 1910; widely reported peak ~-1 to -5 |

## 2. Hand calculation of magnitude formula

Hand-calc on 1P_1910 near-perihelion row (manual_M1K1.csv (provenance=manual_curated_override)):
  date=1910-04-20, days_from_perihelion=0.0
  r=0.587223 AU, Δ=1.214662 AU
  SBDB M1=4.6, K1=10.0
  pipeline apparent_mag = 2.7103
  hand calc m = 4.6 + 5·log10(1.2147) + 10.0·log10(0.5872) = 2.7103
  diff = +0.0000 mag
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
  size: 16700 bytes, 268 lines
  contains 'Manual M1/K1 candidates': True
  contains 'Tier 3 non-periodic candidates: ': True
  contains 'Validation failures': True

Diagnostic figures in C:\Users\grfai\Documents\0_Dissertation\Code\Ch 5 Comet Salience\figures\comet_visibility_diagnostics:
  OK   01_peak_mag_histogram.png (25877 bytes)
  OK   02_peak_vs_duration.png (41366 bytes)
  OK   03_integrated_vs_spectacle_mag.png (35287 bytes)
  OK   04_mag_vs_flux_families.png (31452 bytes)
  OK   05_event_case_counts.png (39426 bytes)
  OK   06_main_sample_candidate.png (17610 bytes)
  OK   07a_top_by_integrated_mag.png (146920 bytes)
  OK   07b_top_by_spectacle_mag.png (148315 bytes)
  OK   07c_top_by_flux.png (153716 bytes)
