import csv

rows = [
    # 41: 1911 I - 16P/Brooks 2 4th apparition
    {
        'pdes': '16P',
        'popular_name': 'Brooks 2',
        'M1': '10.5',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by body — 'fourth recorded apparition of the short-period Comet Brooks(2)' = 16P; Holetschek H1=13m; C.A.M. H10=10 to 11m (took mid 10.5); Konopleva H10=11.7-12.7 (Big V flags 'erroneously assumed'); Big V synthesis from both observations H10=10-11.3 (mid 10.65); chose C.A.M. midpoint per sec 3.4 range-only; periodic — will dedupe with other 16P apparitions; very faint apparition (15-16m); page-image proofread vs page 387: confirmed",
        'match_confidence': 'medium',
        'bigv_designation_old': '1911 I',
        'bigv_page': '387',
        'ocr_excerpt': "Holetschek estimated H1=13m; in C.A.M., H10=10 to 11m. V.P. Konopleva, Publ. Kiev Obs., 5:75. 1953, erroneously assumed H10=11.7 to 12m.7. Making use of both observations we obtain H10=10 to 11m.3.",
    },
    # 42: 1911 II - Kies 1911 N1
    {
        'pdes': '1911 N1',
        'popular_name': "Kies (Beljawsky-Belopol'skii) Comet (1911 II)",
        'M1': '7.4',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by name (Kies, Beljawsky, Belopol'skii) + Auriga 6 July 1911 -> 1911 N1; bright comet, naked-eye visible 4-6m; Orlov y=8.5 H0=7m.2-7m.0; C.A.M. H10=7m.4; Vorontsov-Vel'yaminov y=14.3 H0=8m.6 h0=11m.2; Bobrovnikoff y=10.4 H10=7m.9; chose C.A.M. per sec 3.1; sanity check: photographic 4m on 9 July with stubby tail, naked-eye visible by 17 Aug — M1=7.4 with r_peri=0.69, Δ_min=0.26 -> peak ~ 7.4 + 5log(0.18) - 10log(0.69) = 7.4 - 3.72 + 1.61 ~ 5.3 — consistent with reported 4-5m peak; non-standard y values; meteor shower associated (radiant alpha=87 deg, delta=40.5 deg); page-image proofread vs page 387-388: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1911 II',
        'bigv_page': '387',
        'ocr_excerpt': "S.V. Orlov, A.N., 190:158, obtained from Holetschek's and his own estimates y=8.5, H0=7m.2 to 7m.0; in C.A.M., H10=7m.4; B.A. Vorontsov-Vel'yaminov obtained from 54 brightness estimates y=14.3, H0=8m.6, h0=11m.2; Bobrovnikoff obtained from 58 brightness estimates y=10.4, H10=7m.9.",
    },
    # 43: 1911 IV - Beljawsky 1911 S3 (FAMOUS, erroneous flag)
    {
        'pdes': '1911 S3',
        'popular_name': "Beljawsky's Comet (1911 IV)",
        'M1': '5.0',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, other',
        'notes': "matched by name (Beljawsky) + 28 Sept 1911 morning sky discovery -> 1911 S3; FAMOUS bright comet (peaked 1-1.5m, deep yellow, three-branch tail up to 15 deg long); Vorontsov y=2 H0=3m.3 (Big V flags as uncertain — based on only 0.016 a.u. range); C.A.M. H10=8m.7 'using Holetschek's estimates which were 2 to 3m below the rest' — Big V flags as ERRONEOUS based on underestimates; Big V's reappraisal from Chernyi/Barnard/Graff/Perrine y=9.3 H0=5m.7 H10=5m.0 (preferred); chose Big V's synthesis per V1 pattern; sanity check: peak m=1-1.5 with r_peri=0.30, Δ=1.00 -> peak ~ 5.0 + 0 + 10log(0.30) = 5.0 - 5.23 = -0.23, slightly brighter than reported 1m — reasonable for a bright forward-scattering geometry; ERRONEOUS C.A.M. flagged; page-image proofread vs page 388-389: confirmed",
        'match_confidence': 'low',
        'bigv_designation_old': '1911 IV',
        'bigv_page': '388',
        'ocr_excerpt': "B.A. Vorontsov-Vel'yaminov, A.Zh., 2:88, obtained from 15 intrinsic brightness estimates y=2, H0=3m.3, which refers however to a change of only 0.016 a.u., consequently, these parameters are uncertain; C.A.M., using Holetschek's estimates which were 2 to 3m below the rest, obtained H10=8m.7. Making use of the estimates of Chernyi, Barnard, Graff and Perrine, we obtain y=9.3, H0=5m.7, H10=5m.0.",
    },
    # 44: 1911 V - Brooks 1911 O1 (FAMOUS bright comet)
    {
        'pdes': '1911 O1',
        'popular_name': "Brooks's Comet (1911 V)",
        'M1': '5.1',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by name (Brooks) + Pegasus 20 July 1911 -> 1911 O1; FAMOUS bright comet — peaked m=2.0-2.7 with 6-7 deg tail in mid-Oct, naked-eye visible from 17 Aug; Orlov y=8.0 H0=5m.14; Lau y=9.4 H0=5m.18 (47 estimates); Vorontsov on average y=8.5 H0=5m.64 h0=8m.1; C.A.M. H0=5m.1; Bobrovnikoff y=9.1 H0=5m.64 — Big V flags as 'obvious underestimate (Bobrovnikoff mechanically took the average)'; chose C.A.M. per sec 3.1; brightness flares on multiple dates Aug-Oct; sanity check: peak m=2.0 with r_peri=0.49, Δ=0.85 -> peak ~ 5.1 + 5log(0.42) - 10log(0.49) = 5.1 - 1.89 + 3.10 = 6.3 — too faint vs reported 2.0; Bobrovnikoff's underestimate flag suggests true M1 may be ~1m brighter (~4.1) for bright forward-scattering; non-standard y values; page-image proofread vs page 389-391: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1911 V',
        'bigv_page': '389',
        'ocr_excerpt': "A.V. Orlov, A.N., 190:157, obtained from his own observations y=8.0, H0=5m.14; Lau's 47 estimates yielded y=9.4, H0=5m.18. B.A. Vorontsov-Vel'yaminov, A.Zh., 2:86... On the average y=8.5, H0=5m.64, h0=8m.1; in C.A.M., H0=5m.1. Bobrovnikoff obtained from 466 estimates y=9.1, H0=5m.64; absolute magnitude obvious underestimate.",
    },
    # 45: 1911 VI - Quenisset 1911 S2
    {
        'pdes': '1911 S2',
        'popular_name': "Quenisset's Comet (1911 VI)",
        'M1': '6.5',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by name (Quenisset) + Ursa Minor 23 Sept 1911 -> 1911 S2; bright comet visible to naked eye in mid-Oct (m=5-6); Lau y=8.6 H0=6m.5; Vorontsov y=3.32 H0=6m.5 (74 estimates); C.A.M. H10=6m.5; Bobrovnikoff y=9.1 H10=6m.31 (81 obs); chose C.A.M. per sec 3.1; type I tail; brightness fluctuations on 13, 14, 26 Oct; non-standard y; page-image proofread vs page 392-393: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1911 VI',
        'bigv_page': '392',
        'ocr_excerpt': "Lau, A.N., 191:29, obtained from his own observations y=8.6, H0=6m.5. B.A. Vorontsov-Vel'yaminov, A.Zh., 2:88, obtained from 74 estimates y=3.32, H0=6m.5; in C.A.M., H10=6m.5; Bobrovnikoff... obtained from 81 observations allowing for brightness fluctuations y=9.1, H10=6m.31.",
    },
    # 46: 1911 VII - 24P/Schaumasse first apparition - SKIP (no usable H10)
    # No row written; skip recorded below

    # 47: 1911 VIII - OVERRIDE: 19P/Borrelly second apparition (NOT 24P)
    {
        'pdes': '19P',
        'popular_name': 'Borrelly',
        'M1': '9.5',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "MANUAL DESIGNATION OVERRIDE — script gave 24P (wrong; 24P is the previous entry 1911 VII Schaumasse first apparition); body explicitly: 'second recorded apparition of the short-period Comet Borrelly' = 19P; target list 19P matches the 1911 second apparition (after 1905 II = 19P first); Holetschek H1=9m.2-11m.5 (adopted 10m.5); Vorontsov y=8.2 h0=10m.2; C.A.M. H10=9m.5 (in good agreement with y=10); chose C.A.M. per sec 3.1; periodic — will dedupe with other 19P apparitions; reached m=8.5-9 in late Nov; page-image proofread vs page 393: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1911 VIII',
        'bigv_page': '393',
        'ocr_excerpt': "Holetschek obtained from numerous brightness estimates H1=9m.2 to 11m.5 and adopted H=10m.5. B.A. Vorontsov-Vel'yaminov... found h0=10m.2; y=8.2. C.A.M. obtained H10=9m.5 from the averages calculated by Holetschek which are in good agreement with y=10.",
    },
    # 48: 1912 I - 14P/Wolf 4th apparition
    {
        'pdes': '14P',
        'popular_name': 'Wolf',
        'M1': '9.1',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, other',
        'notes': "matched by body — 'fourth recorded apparition of the periodic Comet Wolf(1)' = 14P; Vsekhsvyatskii V.I H10=9m.1; M.N. 90:713 Hb=8m.1 Hav=9m.1 Hs=10m.3; Bobrovnikoff Pop.Astr. 56(3) 1948 H=10m.5 'making use of erroneous reductions' — Big V flags; Vsekhsvyatskii reappraisal H10=9m.24 (full agreement with 1930); chose Vsekhsvyatskii's V.I=9m.1 (matches M.N. average); periodic — will dedupe with other 14P apparitions; ERRONEOUS Bobrovnikoff flagged; page-image proofread vs page 394: confirmed",
        'match_confidence': 'medium',
        'bigv_designation_old': '1912 I',
        'bigv_page': '394',
        'ocr_excerpt': "S.K. Vsekhsvyatskii, V.I, found H10=9m.1; in M.N., 90:713, he obtained Hb=8m.1, Hav=9m.1, Hs=10m.3. Bobrovnikoff, Pop.Astr., 56(3). 1948, making use of erroneous reductions, obtained H=10m.5. Reappraising all estimates, S.K. Vsekhsvyatskii obtained H10=9m.24.",
    },
    # 49: 1912 II - Gale 1912 R1 (naked-eye, two tails)
    {
        'pdes': '1912 R1',
        'popular_name': "Gale's Comet (1912 II)",
        'M1': '6.2',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by name (Gale) + Centaurus 8 Sept 1912 -> 1912 R1; visible to naked eye 5m; two tails at 50-60 deg angle, main 5+ deg; Kritzinger y=8 H0=5m.66; Vsekhsvyatskii y=8.1 H0=6m.08 h0=7m.2-7m.4 y0=10.0; Moiseev y=8.3 H0=6m.17; Bobrovnikoff y=7.8 H0=6m.31 (113 estimates); C.A.M. H10=6m.2; chose C.A.M. per sec 3.1; main tail type I, secondary type III synchrone (1 Sept ejecta); page-image proofread vs page 394-395: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1912 II',
        'bigv_page': '394',
        'ocr_excerpt': "Kritzinger's observations, A.N., 199:137, yielded y=8 and H0=5m.66. Vsekhsvyatskii, A.N., 221:13, obtained from observations of van Biesbroeck, Holetschek, Nijland and Silva y=8.1, H0=6m.08, h0=7.2 to 7m.4, y0=10.0. A.D. Moiseev... obtained y=8.3, H0=6m.17. Bobrovnikoff... obtained from 113 estimates of various observers y=7.8, H0=6m.31; in C.A.M., H10=6m.2.",
    },
    # 50: 1912 III - Borrelly 1912 V1
    {
        'pdes': '1912 V1',
        'popular_name': "Borrelly's Comet (1912 III)",
        'M1': '8.0',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by name (Borrelly) + Hercules 2 Nov 1912 -> 1912 V1; only C.A.M. H10=8m.0 cited (from November estimates); h10=9-10m (nucleus); Big V notes 'Brightness subsided more rapidly than according to y=10' (asymmetric fading); chose C.A.M. per sec 3.1; D=5'-4' in Nov, 2' in Dec; page-image proofread vs page 396: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1912 III',
        'bigv_page': '396',
        'ocr_excerpt': "In C.A.M., H10=8m.0 (November estimates); h10=9 to 10m. Brightness subsided more rapidly than according to y=10.",
    },
]

out_path = r'C:\Users\grfai\documents\0_Dissertation\code\ch 5 comet salience\data\intermediate\agent_work\agent_c_rows.csv'
with open(out_path, 'a', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['pdes','popular_name','M1','K1','source_citation','notes','match_confidence','bigv_designation_old','bigv_page','ocr_excerpt'], quoting=csv.QUOTE_MINIMAL)
    for r in rows:
        w.writerow(r)
print(f'Wrote {len(rows)} rows for chunk 5')

# Append skip
skip_path = r'C:\Users\grfai\documents\0_Dissertation\code\ch 5 comet salience\data\intermediate\agent_work\agent_c_skipped.txt'
with open(skip_path, 'a', encoding='utf-8') as f:
    f.write("1911 VII (1911h) — page 393 — modern_pdes 24P (Schaumasse first apparition)\n")
    f.write("  Reason: No reliable numeric H10 cited. Vorontsov-Vel'yaminov derived\n")
    f.write("  photometric parameters from 12 observations but Big V notes 'the mean\n")
    f.write("  error in H0 is 4m.4, which exceeds the figure itself by a factor of 2.5'.\n")
    f.write("  No C.A.M., V.I, V.II, E-II, E-I or other authority value cited. Per sec 3.5,\n")
    f.write("  skip rather than guess.\n")
    f.write("  Notes printed: D1=6'.2 in Dec 1911, 3'.1 in Feb 1912.\n\n")
print('Skip recorded')
