import csv

rows = [
    # 71: 1917 I - Mellish 1917 F1
    {
        'pdes': '1917 F1',
        'popular_name': "Mellish's Comet (1917 I)",
        'M1': '7.3',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by name (Mellish) + Aries 19 March 1917 -> 1917 F1; bright comet 5-7m at discovery, naked-eye visible at moderate distance; V.I y=9.8 H0=7m.4 (Asklof); C.A.M. H10=7m.3; chose C.A.M. per sec 3.1; tail 5+ deg in late April; sanity check: peak ~5m with r_peri=0.19, Δ=0.87 -> peak ~ 7.3 + 5log(0.165) - 10log(0.19) = 7.3 - 3.91 + 7.21 = 10.6 — too faint vs reported 5m; may indicate underestimate of M1 due to coma-only photometry; type II or III tail; page-image proofread vs page 411-412: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1917 I',
        'bigv_page': '411',
        'ocr_excerpt': "According to Asklof's estimates, V.I gave y=9.8, H0=7m.4; in C.A.M., H10=7m.3.",
    },
    # 72: 1917 II - Schaumasse 1917 H1
    {
        'pdes': '1917 H1',
        'popular_name': "Schaumasse's Comet (1917 II)",
        'M1': '10.5',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by name (Schaumasse) + Pegasus 15 April 1917 -> 1917 H1; Moiseev y=-4 H0=9m.2 (Holetschek), y=3.5 H0=8m.6 (Abetti) — negative y indicates 'almost constant reduced brightness regardless of increasing r'; Bobrovnikoff y=-44 H0=9m.4; brightness flare at end of May/June; C.A.M. H10=10m.5; chose C.A.M. per sec 3.1; non-standard y (negative); page-image proofread vs page 412-413: confirmed",
        'match_confidence': 'medium',
        'bigv_designation_old': '1917 II',
        'bigv_page': '412',
        'ocr_excerpt': "N.D. Moiseev, A.N., 223:215, obtained from Holetschek's observations y=-4, H0=9m.2; from Abetti's observations, H0=8m.6, y=3.5. The negative y-value is merely a formal expression to indicate that after the perihelion passage the comet retained an almost constant reduced brightness regardless of the increasing r. Bobrovnikoff obtained almost the same result; y=-44, H0=9m.4. An obvious brightness flare at the end of May and in June; in C.A.M., H10=10m.5.",
    },
    # 73: 1918 I - 2P/Encke 34th apparition
    {
        'pdes': '2P',
        'popular_name': "Encke's Comet",
        'M1': '10.6',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by body — 'thirty-fourth recorded apparition of the short-period Comet Encke' = 2P; C.A.M. H10=10m.6; Vsekhsvyatskii A.Zh. 31:286 reapprasial: 'when r=0.6, H10=9m.9'; chose C.A.M. per sec 3.1; periodic — will dedupe with other 2P apparitions; D1=2'.5 in March; page-image proofread vs page 414: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1918 I',
        'bigv_page': '414',
        'ocr_excerpt': "In C.A.M., H10=10m.6. When r=0.6, H10=9m.9 according to Vsekhsvyatskii. — A.Zh., 31:286.",
    },
    # 74: 1918 III - OVERRIDE: 206P/Barnard-Boattini (NOT 14P)
    {
        'pdes': '206P',
        'popular_name': 'Barnard-Boattini',
        'M1': '11.0',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "MANUAL DESIGNATION OVERRIDE — script gave 14P (wrong; 'Wolf' name match was for the photographer Wolf, not eponymous discoverer; body says 'Discovered by Schorr (Bergedorf) on a plate taken on 23 Nov.' with no periodicity claim; body's orbit note 'Revolution period 6 to 7 years' suggests short-period comet); target list 206P/Barnard-Boattini peri 1918-10-20 matches 23 Nov 1918 discovery (post-peri faint object 14m); V.I H10=11m.0; C.A.M. H10=11m.0; chose C.A.M. per sec 3.1; periodic — will dedupe with other 206P apparitions; very faint; page-image proofread vs page 415: confirmed",
        'match_confidence': 'low',
        'bigv_designation_old': '1918 III',
        'bigv_page': '415',
        'ocr_excerpt': "In V.I, H10=11m.0; same figure in C.A.M. In Nov. and Dec., D1=1'. Revolution period 6 to 7 years.",
    },
    # 75: 1918 IV - OVERRIDE: 19P/Borrelly (NOT 4P) — per prompt's hint
    {
        'pdes': '19P',
        'popular_name': 'Borrelly',
        'M1': '10.2',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "MANUAL DESIGNATION OVERRIDE — script gave 4P (wrong; per parent thread brief, 'Fayet' name match misidentified — body explicitly: 'third recorded apparition of the short-period Comet Borelly(1)' = 19P/Borrelly); discoverer Fayet was the recovery observer using Tolnay's ephemeris on 7 Aug 1918; target list 19P peri 1918-11-17 matches body's August discovery (3 months pre-peri); V.I y=11.0 H0=10m.0 h0=11m.3 (Yerkes/Washington); C.A.M. H10=10m.2; chose C.A.M. per sec 3.1; periodic — will dedupe with other 19P apparitions; reached m=9-10 in Dec 1918; anomalous (sunward) tail observed; page-image proofread vs page 415: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1918 IV',
        'bigv_page': '415',
        'ocr_excerpt': "V.I gave, from observations at Yerkes and Washington Observatories, y=11.0, H0=10m.0, h10=11m.3. In C.A.M., H10=10m.2. This gives m=13m.6 upon discovery (y=10).",
    },
    # 76: 1918 V - OVERRIDE: 14P/Wolf (NOT 206P)
    {
        'pdes': '14P',
        'popular_name': 'Wolf',
        'M1': '9.9',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "MANUAL DESIGNATION OVERRIDE — script gave 206P (wrong; 'Barnard' name match was for the observer not discoverer); body explicitly: 'fifth recorded apparition of the short-period Comet Wolf(1)' = 14P/Wolf (Big V's count appears to differ from modern enumeration: 14P apparitions before 1918 were 1884, 1891, 1898, 1905, 1912 — should be 6th not 5th; Big V text simply has the count wrong); target list 14P peri 1918-12-13 matches body's 9 July 1918 Jonckheere recovery according to Kamienski's ephemeris; V.I y=20 H0=5m (Chofardet/van Biesbroeck); C.A.M. H10=9m.9; Kamienski adopted H10=9m.1; Vsekhsvyatskii later reappraisal A.Zh. 27:15 1950 gave H10(av)=8m.85; from Barnard h10=10m.4 (nucleus); chose C.A.M. per sec 3.1; periodic — will dedupe with other 14P apparitions; non-standard y=20; page-image proofread vs page 416: confirmed",
        'match_confidence': 'medium',
        'bigv_designation_old': '1918 V',
        'bigv_page': '416',
        'ocr_excerpt': "V.I gave, according to Chofardet's and van Biesbroeck's estimates y=20, H0=5; in C.A.M., H10=9m.9. Kamienski adopted H10=9m.1. After reappraisal of the entire data, Vsekhsvyatskii, A.Zh., 27:15, 1950, gave H10(av)=8m.85; from Barnard's estimate H10=10m.4 (nucleus).",
    },
    # 77: 1919 I - 22P/Kopff second apparition
    {
        'pdes': '22P',
        'popular_name': 'Kopff',
        'M1': '8.6',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by body — 'second recorded apparition of the short-period Comet Kopff (1906 IV)' = 22P; V.I H10=8m.9; C.A.M. H10=8m.6; chose C.A.M. per sec 3.1; periodic — will dedupe with other 22P apparitions; D1=3' in Sept; reached m=9-10; page-image proofread vs page 416-417: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1919 I',
        'bigv_page': '416',
        'ocr_excerpt': "In V.I, H10=8m.9; in C.A.M., H10=8m.6.",
    },
    # 78: 1919 III - OVERRIDE: 23P/Brorsen-Metcalf (NOT 15P)
    {
        'pdes': '23P',
        'popular_name': 'Brorsen-Metcalf',
        'M1': '9.6',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, other',
        'notes': "MANUAL DESIGNATION OVERRIDE — script gave 15P (wrong); body explicitly: 'second recorded apparition of the periodic Comet Brorsen-Metcalf (1847 V)' = 23P/Brorsen-Metcalf; target list confirms 23P peri 1919-10-17 matches body's 20 Aug Metcalf discovery; bright naked-eye comet, peaked at m=4.5 in Sept-Oct; Selivanov y=12.6 H0=8m.7 (22 estimates); V.II H10=9m.6 (Holetschek/Nijland); Bobrovnikoff y=13.8 H0=10m.4 (Big V flags as 2m off); chose V.II Big V synthesis; periodic — will dedupe with other 23P apparitions; sanity check: peak m=4.5 with r_peri~0.49, Δ~0.85 -> peak ~ 9.6 + 5log(0.42) - 10log(0.49) = 9.6 - 1.89 + 3.10 = 10.8 — too faint vs reported 4.5m; may indicate H10 underestimate; non-standard y; page-image proofread vs page 418: confirmed",
        'match_confidence': 'medium',
        'bigv_designation_old': '1919 III',
        'bigv_page': '418',
        'ocr_excerpt': "S. Selivanov, Lesgaft Inst., 1922, making use of 22 estimates from 1 Sept. to 7 Oct., gave y=12.6, H0=8m.7; in V.II, H10=9m.6, from observations of Holetschek, Nijland et al. Bobrovnikoff, from 64 estimates from 26 Aug. to 5 Oct., obtained y=13.8, H0=10m.4; these parameters, however, give m=7m.1 at the beginning of September, a difference of 2m from the observed value.",
    },
    # 79: 1919 IV - 24P/Schaumasse second apparition
    {
        'pdes': '24P',
        'popular_name': 'Schaumasse',
        'M1': '10.9',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, other',
        'notes': "matched by body — 'second recorded apparition of the short-period Comet Schaumasse' = 24P; only A.Zh. 7:217 H10=10m.9 cited (Vsekhsvyatskii); D1=1'.5; chose Vsekhsvyatskii Big V citation; periodic — will dedupe with other 24P apparitions; faint 10-12m; page-image proofread vs page 419: confirmed",
        'match_confidence': 'medium',
        'bigv_designation_old': '1919 IV',
        'bigv_page': '419',
        'ocr_excerpt': "In A.Zh., 7:217, H10=10m.9; D1=1'.5.",
    },
    # 80: 1919 V - OVERRIDE: 1919 Q2 (Metcalf) (NOT 24P)
    {
        'pdes': '1919 Q2',
        'popular_name': "Metcalf-Borrelly's Comet (1919 V)",
        'M1': '4.7',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, other',
        'notes': "MANUAL DESIGNATION OVERRIDE — script gave 24P (wrong; 24P was the previous entry 1919 IV Schaumasse); body says discovered by Metcalf 22 Aug 1919 in Bootes, also Borrelly 23 Aug -> 1919 Q2 (Metcalf) per target list peri 1919-12-07; bright comet, peaked m=4.5-5 in Oct; E-I H10=6m.7 (Holetschek/Luther/Pidoux); Big V's reappraisal 'with estimates given' H10=4m.7 (BRIGHTER, preferred per V1 pattern when Big V recommends brighter synthesis); chose Big V synthesis 4m.7; sanity check: peak m=4.7 (Big V's H10) with r_peri=1.15, Δ=1.90 -> peak ~ 4.7 + 5log(2.18) + 10log(1.15) = 4.7 + 1.69 + 0.61 = 6.99 — too faint vs reported 4.5m; M1=4.7 may still be conservative; page-image proofread vs page 419: confirmed; ASYMMETRIC potentially",
        'match_confidence': 'low',
        'bigv_designation_old': '1919 V',
        'bigv_page': '419',
        'ocr_excerpt': "In E-I, H10=6m.7 from estimates of Holetschek, Luther, Pidoux et al.; with estimates given, H10=4m.7. In Sept. and Nov., D1=6'.4 to 9'.0.",
    },
]

out_path = r'C:\Users\grfai\documents\0_Dissertation\code\ch 5 comet salience\data\intermediate\agent_work\agent_c_rows.csv'
with open(out_path, 'a', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['pdes','popular_name','M1','K1','source_citation','notes','match_confidence','bigv_designation_old','bigv_page','ocr_excerpt'], quoting=csv.QUOTE_MINIMAL)
    for r in rows:
        w.writerow(r)
print(f'Wrote {len(rows)} rows for chunk 8')
