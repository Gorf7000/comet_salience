import csv

rows = [
    # 21: 1906 III - 17P/Holmes 3rd apparition
    {
        'pdes': '17P',
        'popular_name': 'Holmes',
        'M1': '9.8',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, other',
        'notes': "matched by body — 'third recorded apparition of the short-period Comet Holmes' = 17P; Holetschek H10=11m.9 (photographic); Vsekhsvyatskii A.Zh. 7:215, 1930 obtained 10m, more precisely H10=9m.8 (from photographs); chose Big V's preferred Vsekhsvyatskii synthesis 9m.8 (more recent, more data); periodic — will dedupe; very faint apparition (15-16m); page-image proofread vs page 367: confirmed",
        'match_confidence': 'medium',
        'bigv_designation_old': '1906 III',
        'bigv_page': '367',
        'ocr_excerpt': "Holetschek from photographic estimates obtained H10=11m.9; S. Vsekhsvyatskii, A.Zh., 7:215. 1930, obtained 10m; more precisely, from photographs, H10=9m.8.",
    },
    # 22: 1906 IV - 22P/Kopff first apparition
    {
        'pdes': '22P',
        'popular_name': 'Kopff',
        'M1': '8.4',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by body — 'first recorded apparition of the short-period Comet Kopff' = 22P; V.I y=2.7 H0=10m.6 (Wirtz); other observations y=8.6 H0=9m.3 (Hartwig/Abetti/Nijland); M.N. 90:714 Hm=8m.4 Hb=7m.5 Hs=8m.9; C.A.M. H10=8m.4; chose C.A.M. per sec 3.1; periodic — will dedupe with other 22P apparitions; non-standard y=2.7 (Wirtz, very flat); page-image proofread vs page 367-368: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1906 IV',
        'bigv_page': '367',
        'ocr_excerpt': "V.I gave, according to Wirtz's estimates, y=2.7, H0=10m.6. According to other observations, (Hartwig, Abetti, Nijland et al.), y=8.6, H0=9m.3. In M.N., 90:714, Hm=8m.4, Hb=7m.5 and Hs=8m.9; in C.A.M., H10=8m.4.",
    },
    # 23: 1906 V - OVERRIDE: 15P/Finlay (NOT 22P), erroneous flag for C.A.M.
    {
        'pdes': '15P',
        'popular_name': 'Finlay',
        'M1': '9.0',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, other',
        'notes': "MANUAL DESIGNATION OVERRIDE — script gave 22P (wrong; that was the previous entry 1906 IV); body explicitly: 'third recorded apparition of the short-period Comet Finlay' = 15P; target list 15P/Finlay peri 1906-09-08 matches body's 16 July discovery; Holetschek H1=9m.3; M.N. 90:713 Hm=9m.9 Hb=9m.1 Hs=12m.6; C.A.M. H10=9m.9 'an apparent underestimate'; Big V synthesis H10=9m.0 preferred; chose Big V's value over flagged C.A.M. per V1 pattern; periodic — will dedupe with other 15P apparitions; ERRONEOUS C.A.M. flagged; page-image proofread vs page 368: confirmed",
        'match_confidence': 'medium',
        'bigv_designation_old': '1906 V',
        'bigv_page': '368',
        'ocr_excerpt': "Holetschek's data gave H1=9m.3. In M.N., 90:713, Hm=9m.9, Hb=9m.1 and Hs=12m.6. In C.A.M., H10=9m.9, an apparent underestimate; H10=9m.0 is in better agreement with the estimates above.",
    },
    # 24: 1906 VI - 97P/Metcalf-Brewington
    {
        'pdes': '97P',
        'popular_name': 'Metcalf-Brewington',
        'M1': '9.5',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, other',
        'notes': "matched by name (Metcalf) + Eridanus 14 Nov 1906 + target list 97P/Metcalf-Brewington peri 1906-10-10; V.I H10=7m.9 (from Wirtz, but based on erroneous ephemeris — Big V flags); for first visibility period H10=9m.5; for Dec 1906-Jan 1907 H10=10m.4; ASYMMETRIC (fading post-peri); chose Big V synthesis 9m.5 first period as brighter (post-peri 10.4 also cited); periodic — will dedupe; ERRONEOUS V.I (ephemeris) flagged; page-image proofread vs page 369: confirmed",
        'match_confidence': 'medium',
        'bigv_designation_old': '1906 VI',
        'bigv_page': '369',
        'ocr_excerpt': "V.I gave, according to Wirtz's observations, H10=7m.9, which however is based on an erroneous ephemeris. For the first visibility period the estimates above yield H10=9m.5; for Dec. 1906 and Jan. 1907, H10=10m.4.",
    },
    # 25: 1906 VII - Thiele 1906 V1
    {
        'pdes': '1906 V1',
        'popular_name': "Thiele's Comet (1906 VII)",
        'M1': '7.8',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by name (Thiele) + Cancer 10 Nov 1906 -> 1906 V1; V.I y=2.3 and 4.4, H0=8m.5 and 5m.3 (Holetschek/Wirtz); when y=10, H10=8m.1; C.A.M. H10=7m.8; Bobrovnikoff y=17.2 H10=7m.6 (37 estimates); chose C.A.M. per sec 3.1; non-standard y values (very flat for Holetschek); page-image proofread vs page 369-370: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1906 VII',
        'bigv_page': '369',
        'ocr_excerpt': "V.I gave, according to Holetschek and Wirtz, y=2.3 and 4.4; H0=8m.5 and 5m.3. When y=10, H10=8m.1. In C.A.M., H10=7m.8. Bobrovnikoff... obtained from 37 estimates of Holetschek, Wirtz, et al. y=17.2; H10=7m.6.",
    },
    # 26: 1907 I - Giacobini 1907 E1
    {
        'pdes': '1907 E1',
        'popular_name': "Giacobini's Comet (1907 I)",
        'M1': '6.5',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, other',
        'notes': "matched by name (Giacobini) + Canis Major 10 March 1907 -> 1907 E1; V.I/C.A.M. H10=4m.9 (from Wirtz, y=17.6) — but Big V's reappraisal yields March H10=7m.0-7m.8, April-May 6-6.7, beginning 1908 5m.7, average H10=6m.5; chose Big V's average synthesis 6m.5 as more representative across phases (C.A.M. 4.9 appears to be too bright relative to Big V's reappraisal of estimates); ASYMMETRIC (brightened post-peri); non-standard y=17.6; page-image proofread vs page 370-371: confirmed",
        'match_confidence': 'low',
        'bigv_designation_old': '1907 I',
        'bigv_page': '370',
        'ocr_excerpt': "V.I gave, according to Wirtz, et al., y=17.6, H0=4m.9; in C.A.M., H10=4m.9. Proceeding from the estimates above, in March, H10=7m.0 to 7m.8; in April and May, H10=6 to 6m.7; beginning of 1908, H10=5m.7. On an average, H10=6m.5.",
    },
    # 27: 1907 II - Grigg 1907 G1 (return of comet 1742)
    {
        'pdes': '1907 G1',
        'popular_name': "Grigg-Mellish (1907 II)",
        'M1': '10.4',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, other',
        'notes': "matched by name (Grigg) + Caelum 8 April 1907 -> 1907 G1; V.I y=21 H10=9m.7 (Wirtz); C.A.M. H10=10m.6; from first estimates Big V synthesis H10=10m.4; chose Big V synthesis as primary (sits between Wirtz V.I and C.A.M.); apparently a return of comet 1742 (165-yr period); non-standard y=21; page-image proofread vs page 371: confirmed",
        'match_confidence': 'medium',
        'bigv_designation_old': '1907 II',
        'bigv_page': '371',
        'ocr_excerpt': "V.I gave, according to Wirtz, y=21, H10=9m.7; in C.A.M., H10=10m.6; from first estimates, we obtain H10=10m.4.",
    },
    # 28: 1907 III - 21P/Giacobini-Zinner first recovery (presumed 2nd apparition)
    {
        'pdes': '21P',
        'popular_name': 'Giacobini-Zinner',
        'M1': '12.3',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by body — 'Presumably the second recorded apparition of the short-period Comet Tuttle-Giacobini-Kresak' — but body wording is wrong: this is actually 21P/Giacobini-Zinner per target list (Giacobini 1 June 1907 discovery in Leo); script accepted 21P; only C.A.M. H10=12m.3 cited; D=1.5-2'; very faint apparition near visibility threshold (13m); periodic — will dedupe with other 21P apparitions; page-image proofread vs page 371-372: confirmed",
        'match_confidence': 'medium',
        'bigv_designation_old': '1907 III',
        'bigv_page': '371',
        'ocr_excerpt': "In C.A.M., H10=12m.3. D=1.5 to 2'.",
    },
    # 29: 1907 IV - Daniel 1907 L2 (famous bright comet)
    {
        'pdes': '1907 L2',
        'popular_name': "Daniel's Comet (1907 IV)",
        'M1': '4.0',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by name (Daniel) + 9 June 1907 vernal equinox discovery -> 1907 L2; Orlov y=19-6.4 H0=3m.6-3m.7 h10=7m.4; V.I y=9.8 H0=4m.2 H10=4m.0 (Nijland/Wirtz et al); Bobrovnikoff y=9.0 H0=4m.4 (from 98 estimates); first period y=17 H0=3m.6; C.A.M. is not explicitly stated but V.I H10=4m.0 matches catalog convention — used as the canonical synthesis; sanity check: famous bright Daniel comet of 1907, peaked m=2.1-2.3 in mid-Aug, naked-eye 17 degree tail; M1=4.0 with r_peri=0.51, Δ=0.93 -> peak ~ 4.0 + 5log(0.474) - 10log(0.51) ~ 4.0 - 1.62 + 2.92 ~ 5.3 - too faint vs reported 2.1; using full r,Δ peak (Aug) r=0.6 Δ=0.93 -> peak ~4.0 + 5log(0.558) - 10log(0.6) ~ 4.0 - 1.27 + 2.22 ~ 4.95 - still too faint; possible underestimate by V.I — but per priority it remains preferred without explicit Big V flag; notable type II or III tail; page-image proofread vs page 372-373: confirmed",
        'match_confidence': 'medium',
        'bigv_designation_old': '1907 IV',
        'bigv_page': '372',
        'ocr_excerpt': "S.V. Orlov, A.N., 195:303, obtained from Holetschek's observations y=19 to 6.4, H0=3m.6 to 3m.7, h10=7m.4. V.I gave according to Nijland, Wirtz, and others y=9.8, H0=4m.2, H10=4m.0. From all the 98 estimates Bobrovnikoff... obtained y=9.0 (on the average), H0=4m.4 and for the first period (June and July) y=17, H0=3m.6.",
    },
    # 30: 1907 V - Mellish - JSONL says 26P, but body suggests single-apparition comet
    {
        'pdes': '1907 T1',
        'popular_name': "Mellish's Comet (1907 V)",
        'M1': '8.4',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, other',
        'notes': "MANUAL DESIGNATION OVERRIDE — script gave 26P (wrong; 26P/Grigg-Skjellerup 1907 apparition would be a separate entry); body says 'Discovered in Hydra by Mellish (Madison, U.S.A.) on 13 Oct.' — a single Mellish 1907 discovery, no periodicity claim; perihelion ~mid-Nov 1907 from r,delta data; this is likely C/1907 T1 (Mellish) per IAU designation conventions (Mellish discovered Oct 13 -> half-month T = Oct 1-15, suffix 1); V.I y=20 H0=8m.4 (Holetschek/Wirtz); C.A.M. H10=9m.8; chose V.I/Big V's first synthesis 8m.4 over C.A.M. since the Wirtz/Holetschek data come from same observations summarized; brief naked-eye 8-9m comet; page-image proofread vs page 374: confirmed; LOW CONFIDENCE — pdes guess based on conventions, may need manual designation review",
        'match_confidence': 'low',
        'bigv_designation_old': '1907 V',
        'bigv_page': '374',
        'ocr_excerpt': "From Holetschek and Wirtz, V.I obtained y=20; H0=8m.4; in C.A.M., H10=9m.8.",
    },
]

out_path = r'C:\Users\grfai\documents\0_Dissertation\code\ch 5 comet salience\data\intermediate\agent_work\agent_c_rows.csv'
with open(out_path, 'a', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['pdes','popular_name','M1','K1','source_citation','notes','match_confidence','bigv_designation_old','bigv_page','ocr_excerpt'], quoting=csv.QUOTE_MINIMAL)
    for r in rows:
        w.writerow(r)
print(f'Wrote {len(rows)} rows for chunk 3')
