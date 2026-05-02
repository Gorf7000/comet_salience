# Validation Results
_Generated 2026-05-02 05:22 UTC_

Four independent checks: external-peak comparison, hand calculation,
manual-CSV path test, and artifact inspection. Designed to be readable
in 5 minutes and to surface issues that the pipeline's internal
validation does not catch.

## 1. External peak-magnitude comparison

External-peak check: 10/10 counted entries pass (tolerance: within ±1.5 mag; range: modeled inside reported range).
  + 3 additional entries excluded from the pass-rate as documented model limitations (outburst, disintegration, apparition-to-apparition variability):
      2P 1898: observed +6.0, modeled +4.05, diff -1.95 — Encke 1898; Encke varies +5 to +7 across returns — apparition-to-apparition variability exceeds tolerance
      3D 1852: observed +5.0, modeled +8.22, diff +3.22 — Biela 1852 final intact return; comet was visibly disintegrating, single-law fit cannot track activity collapse
      17P 1892: observed +5.0, modeled +13.83, diff +8.83 — Holmes 1892; famous outburst — M1/K1 model cannot capture stochastic outbursts by design

Detailed comparison table:

| comet_id | year | observed peak | modeled peak | diff | category | status | notes |
|---|---|---|---|---|---|---|---|
| 1P | 1910 | +0.0 | -0.12 | -0.12 | tolerance | pass | Halley 1910; Kronk: peak ~0, briefly -0.5 in early May |
| 109P | 1862 | +2.0 | 1.54 | -0.46 | tolerance | pass | Swift-Tuttle 1862 discovery; Kronk: peak ~+2 |
| 12P | 1884 | +3.0 | 3.01 | +0.01 | tolerance | pass | Pons-Brooks 1884; Kronk: peak +3 to +3.5 |
| 2P | 1898 | +6.0 | 4.05 | -1.95 | model_limit | model_limit | Encke 1898; Encke varies +5 to +7 across returns — apparition-to-apparition variability exceeds tolerance |
| 3D | 1852 | +5.0 | 8.22 | +3.22 | model_limit | model_limit | Biela 1852 final intact return; comet was visibly disintegrating, single-law fit cannot track activity collapse |
| 5D | 1879 | +6.0 | 5.67 | -0.33 | tolerance | pass | Brorsen 1879; Kronk: peak ~+5 to +6 |
| 23P | 1919 | +5.0 | 5.93 | +0.93 | tolerance | pass | Brorsen-Metcalf 1919; Kronk: peak ~+5 |
| 8P | 1858 | +7.0 | 7.56 | +0.56 | tolerance | pass | Tuttle 1858 discovery; Kronk: peak ~+7 |
| 17P | 1892 | +5.0 | 13.83 | +8.83 | model_limit | model_limit | Holmes 1892; famous outburst — M1/K1 model cannot capture stochastic outbursts by design |
| C/1858 L1 | 1858 | -1.0 | -0.19 | +0.81 | tolerance | pass | Donati 1858; widely reported peak ~-1 |
| C/1861 J1 | 1861 | +0.0 | -0.99 | -0.99 | tolerance | pass | Tebbutt 1861; widely reported peak ~0 |
| C/1882 R1 | 1882 | -10.0 | -13.13 | -3.13 | range | in_range | Great September Comet 1882; sungrazer — peaks reported -17 (in-daylight forward scattering near Sun) to -10 (post-perihelion night-sky) |
| C/1910 A1 | 1910 | -1.0 | -3.77 | -2.77 | range | in_range | Great January Comet 1910; reports range -1 to -5 |

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
