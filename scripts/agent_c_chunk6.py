import csv

rows = [
    # 51: 1912 IV - OVERRIDE: 8P/Tuttle (NOT 26P)
    {
        'pdes': '8P',
        'popular_name': 'Tuttle',
        'M1': '8.6',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "MANUAL DESIGNATION OVERRIDE — script gave 26P (wrong); body explicitly: 'sixth recorded apparition of the short-period Comet Tuttle' = 8P/Tuttle; target list 8P peri 1912-10-28 matches body's 18 Oct Schaumasse discovery; Holetschek H1=7m.6 to 9m.0 (mid 8.3); M.N. 90:714 Vsekhsvyatskii H10=8m.3 to 8m.6 (mid 8.45); C.A.M. H10=8m.6; chose C.A.M. per sec 3.1; periodic — will dedupe with other 8P apparitions; D1=3'.3; page-image proofread vs page 396-397: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1912 IV',
        'bigv_page': '396',
        'ocr_excerpt': "Holetschek, from his collection of estimates, obtained H1=7m.6 to 9m.0; in M.N., 90:714, Vsekhsvyatskii obtained H10=8m.3 to 8m.6; in C.A.M., H10=8m.6.",
    },
    # 52: 1913 I - Lowe Comet (no target list match — flag low)
    {
        'pdes': '1912 Y1?',
        'popular_name': "Lowe's Comet (1913 I)",
        'M1': '9.0',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, other',
        'notes': "MANUAL DESIGNATION OVERRIDE — script gave 15P (wrong; 15P/Finlay had no 1913 apparition per target list); body identifies as Lowe (Laura, S.Australia) discovery 31 Dec 1912 in Virgo, observed only 9 days, paren-id (1912d) suggests 4th comet of 1912 -> likely IAU C/1912 Y1 (last half Dec); NO MATCH found in target list — modern catalogs may have classified as doubtful; flagged with ? per sec 4; Vsekhsvyatskii from m=9m on 31 Dec obtained H10=11m, but Big V's 'better approximation' is H10=9m (preferred); LOW CONFIDENCE — pdes uncertain, requires manual review; page-image proofread vs page 397: confirmed",
        'match_confidence': 'low',
        'bigv_designation_old': '1913 I',
        'bigv_page': '397',
        'ocr_excerpt': "Taking m=9m on 31 Dec., S.K. Vsekhsvyatskii obtained H10=11m, better approximation: H10=9m.",
    },
    # 53: 1913 II - Schaumasse 1913 J1
    {
        'pdes': '1913 J1',
        'popular_name': "Schaumasse's Comet (1913 II)",
        'M1': '7.7',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by name (Schaumasse) + Delphinus 6 May 1913 -> 1913 J1; V.I y=7.0 H10=8m.2 (Holetschek), nuclear y=24; C.A.M. H10=7m.7; Bobrovnikoff y=11.4 H0=7m.9 (30 estimates); chose C.A.M. per sec 3.1; D1=4' in June-July; non-standard nuclear y=24; page-image proofread vs page 397-398: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1913 II',
        'bigv_page': '397',
        'ocr_excerpt': "V.I obtained, according to Holetschek's observations, y=7.0, H10=8m.2 and for the nuclear brightness y=24. In C.A.M., H10=7m.7. Bobrovnikoff... obtained from 30 estimates of Holetschek, Nijland and van Biesbroeck y=11.4 and H0=7m.9.",
    },
    # 54: 1913 III - 28P/Neujmin 1 first apparition
    {
        'pdes': '28P',
        'popular_name': 'Neujmin 1',
        'M1': '10.3',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by body — 'first recorded apparition of the short-period Comet Neujmin(1)' = 28P/Neujmin 1; V.I y=6.9 H0=9m.9 (van Biesbroeck/Millosewich); Graff y=11.0 h0=10m.8; C.A.M. H10=10m.3 (gives m=15m.2 on 30 Dec, good agreement); chose C.A.M. per sec 3.1; periodic — will dedupe with other 28P apparitions; near-asteroidal appearance (very faint envelope); page-image proofread vs page 398-399: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1913 III',
        'bigv_page': '398',
        'ocr_excerpt': "V.I obtained, according to van Biesbroeck, Millosewich et al., y=6.9; H0=9m.9. Graff's observations yielded y=11.0; h0=10m.8. In C.A.M., H10=10m.3, which gives m=15m.2 on 30 Dec. in good agreement with observations.",
    },
    # 55: 1913 IV - Metcalf 1913 R1
    {
        'pdes': '1913 R1',
        'popular_name': "Metcalf's Comet (1913 IV)",
        'M1': '8.0',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by name (Metcalf) + Lynx 1 Sept 1913 -> 1913 R1; V.I y=17.2 H0=6m.8 and y=10.5 h10=10m.3 (Holetschek); C.A.M. H10=8m.0; Bobrovnikoff y=16.9 H0=6m.8 (58 estimates); chose C.A.M. per sec 3.1; reached 7-8m visible to naked eye in Sept; brightness fluctuations; non-standard y=17.2; page-image proofread vs page 399: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1913 IV',
        'bigv_page': '399',
        'ocr_excerpt': "V.I obtained, according to Holetschek, y=17.2, H0=6m.8 and y=10.5, h10=10m.3; in C.A.M., H10=8m.0. Bobrovnikoff... obtained from 58 estimates of eight observers... y=16.9 and H0=6m.8.",
    },
    # 56: 1913 V - 21P/Giacobini-Zinner second apparition
    {
        'pdes': '21P',
        'popular_name': 'Giacobini-Zinner',
        'M1': '11.3',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by body — 'second recorded apparition of the short-period Comet Giacobini-Zinner' = 21P; Ebell/Viljev established identity with 1900 III orbit; Holetschek H1=10m.0-13m.3; V.II H10=10m.2; M.N. 90:714 Hm=11m.3 Hb=10m.4 Hs=12m.4; C.A.M. H10=11m.3 (matches M.N. Hm); chose C.A.M. per sec 3.1; periodic — will dedupe with other 21P apparitions; tail 25-30' long photographically; page-image proofread vs page 400: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1913 V',
        'bigv_page': '400',
        'ocr_excerpt': "Proceeding from various estimates, Holetschek gave H1=10m.0 to 13m.3; in V.II, H10=10m.2. After reappraisal in M.N., 90:714, Hm=11m.3, Hb=10m.4 and Hs=12m.4; in C.A.M., H10=11m.3.",
    },
    # 57: 1913 VI - OVERRIDE: 20D/Westphal second apparition (NOT 28P)
    {
        'pdes': '20D',
        'popular_name': 'Westphal',
        'M1': '8.8',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "MANUAL DESIGNATION OVERRIDE — script gave 28P (wrong; 28P first apparition was entry 1913 III); body explicitly: 'second recorded apparition of the periodic Comet Westphal' = 20D/Westphal; target list 20D peri 1913-11-26 matches body's 26 Sept Delavan discovery; HIGHLY UNUSUAL: brightness DROPPED with approach to perihelion (Holetschek noted 'abrupt drop in brightness, notwithstanding the approach to perihelion'); Holetschek H1=8m.3-8m.8 first period, then drop to 10m.7 by 27 Oct, 16m.4 by 22 Nov; V.I y=-5.2 (NEGATIVE) H0=9m.3 (Vsekhsvyatskii); C.A.M. H10=8m.8 (mean of Holetschek), comparable to H10=5m.0 for 1852 — fading; Bobrovnikoff y=-27.8 H0=14m.6 'only formal significance'; chose C.A.M. per sec 3.1; ASYMMETRIC pre-peri brighter; periodic — will dedupe with other 20D apparitions; non-standard y=-5.2 (decreasing); page-image proofread vs page 400-401: confirmed",
        'match_confidence': 'low',
        'bigv_designation_old': '1913 VI',
        'bigv_page': '400',
        'ocr_excerpt': "Holetschek obtained for the first observation period H1=8m.3 to 8m.8 and then a drop to 10m.7 on 27 Oct. and 28 Oct. and 16m.4 on 22 Nov. Vsekhsvyatskii, using observations of Holetschek and others in V.I, obtained y=-5.2, H0=9m.3 (brightness decreased with approach to perihelion). In C.A.M., H10=8m.8 as the mean of Holetschek's estimates, a result comparable to H10=5m.0 for 1852.",
    },
    # 58: 1914 I - Zlatinskii 1914 J1
    {
        'pdes': '1914 J1',
        'popular_name': "Zlatinskii's Comet (1914 I)",
        'M1': '8.3',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, other',
        'notes': "matched by name (Zlatinskii) + Persei 15 May 1914 -> 1914 J1; bright comet 4-5m, naked-eye visible, 12-deg tail by 22 May; only V.II Vsekhsvyatskii synthesis H10=8m.3 cited (using Graff/Nijland/Renault estimates); D1=1'.9; type I tail with traces of type III; sanity check: peak ~4m with r_peri~0.55, Δ~0.55 -> peak ~ 8.3 + 5log(0.30) - 10log(0.55) = 8.3 - 2.61 + 2.59 = 8.28 — too faint vs reported 4m; suggests the M1 from V.II may be ~3m too faint, but no other authority; LOW CONFIDENCE — discrepancy with reported peak; page-image proofread vs page 402-403: confirmed",
        'match_confidence': 'low',
        'bigv_designation_old': '1914 I',
        'bigv_page': '402',
        'ocr_excerpt': "Using the estimates of Graff, Nijland, Renault and other observers, S.K. Vsekhsvyatskii in V.II obtained H10=8m.3. In May, D1=1'.9; 22 May, Smax=0.126.",
    },
    # 59: 1914 II - Kritzinger 1914 F1
    {
        'pdes': '1914 F1',
        'popular_name': "Kritzinger's Comet (1914 II)",
        'M1': '9.3',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by name (Kritzinger) + Scorpio 29 March 1914 -> 1914 F1; V.I y=12.7 H0=9m.0 h0=9m.9 yn=13.9 (Holetschek); C.A.M. H10=9m.3; Big V synthesis with Aug-Dec H10=9m.4; Bobrovnikoff y=1.0 H0=10m.4 (Big V notes 'do not accord with actual variation'); chose C.A.M. per sec 3.1; reached m=8 in mid-April-May; faded slowly through Aug-Dec; non-standard y; page-image proofread vs page 403: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1914 II',
        'bigv_page': '403',
        'ocr_excerpt': "Holetschek's observations in V.I gave y=12.7, H0=9m.0, h=9m.9, yn=13.9; in C.A.M., H10=9m.3. Making use of additional estimates for August to December we obtain H10=9m.4. Bobrovnikoff making use of 46 estimates... obtained y=1.0, H0=10m.4, figures which do not accord with the actual variation in the comet's brightness.",
    },
    # 60: 1914 III - Neujmin 1914 M1 (distant comet, asymmetric)
    {
        'pdes': '1914 M1',
        'popular_name': "Neujmin's Comet (1914 III)",
        'M1': '4.7',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, other',
        'notes': "matched by name (Neujmin) + 24 June 1914 discovery -> 1914 M1; very distant comet (r=3.79-3.96 AU); V.II H10=4m.7 from June-July observations; in Dec, H10=5m.6; ASYMMETRIC fading post-discovery (took June-July brighter per sec 3.3); chose V.II 'other' source; observed only as 12-15m photographic object due to distance; page-image proofread vs page 404: confirmed",
        'match_confidence': 'medium',
        'bigv_designation_old': '1914 III',
        'bigv_page': '404',
        'ocr_excerpt': "V.II gave H10=4m.7 from observations in June and July; and in Dec., H10=5m.6. In July, D1=2'. S>0.001.",
    },
]

out_path = r'C:\Users\grfai\documents\0_Dissertation\code\ch 5 comet salience\data\intermediate\agent_work\agent_c_rows.csv'
with open(out_path, 'a', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['pdes','popular_name','M1','K1','source_citation','notes','match_confidence','bigv_designation_old','bigv_page','ocr_excerpt'], quoting=csv.QUOTE_MINIMAL)
    for r in rows:
        w.writerow(r)
print(f'Wrote {len(rows)} rows for chunk 6')
