import csv

rows = [
    # 11: 1904 I (1904 H1 Brooks) - distant comet, M1=2.8
    {
        'pdes': '1904 H1',
        'popular_name': "Brooks's Comet (1904 I)",
        'M1': '2.8',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by name (Brooks) + Hercules 16 April 1904 -> 1904 H1; V.I H10=2m.9 and 2m.8 (from Holetschek and Wirtz observations); C.A.M. H10=2m.8; Bobrovnikoff y=8.12 H0=3m.6 (146 estimates); chose C.A.M. per sec 3.1; very distant comet (r=2.7 to 5.3 AU); observed for 40 months; non-standard photometric law y=8.12; sanity check: very bright intrinsically (M1=2.8) but distant — never naked-eye, peaked at m=8.5-9 (consistent); page-image proofread vs page 359-360: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1904 I',
        'bigv_page': '359',
        'ocr_excerpt': "V.I gave, according to observations of Holetschek and Wirtz, H10=2m.9 and 2m.8; in C.A.M., H10=2m.8. Bobrovnikoff... obtained y=8.12 and H0=3m.6.",
    },
    # 12: 1904 II (1904 Y1 Giacobini)
    {
        'pdes': '1904 Y1',
        'popular_name': "Giacobini's Comet (1904 II)",
        'M1': '6.6',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by name (Giacobini) + Corona Borealis 17 Dec 1904 -> 1904 Y1; absolute magnitude estimated in V.II; C.A.M. H10=6m.6; D1=1'.1 in Jan 1905; chose C.A.M. per sec 3.1; faint distant comet (r=1.95-2.99 AU); page-image proofread vs page 360: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1904 II',
        'bigv_page': '360',
        'ocr_excerpt': "Absolute magnitude estimated in V.II. In C.A.M., H10=6m.6. In Jan. 1905, D1=1'.1.",
    },
    # 13: 1904 III - 10P/Tempel 2 fifth apparition
    {
        'pdes': '10P',
        'popular_name': 'Tempel 2',
        'M1': '9.8',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by body — 'fifth recorded apparition of the short-period Comet Tempel(2)' = 10P; Holetschek H10=10m.5 (from m=12m.7-13m.0); M.N. 90:712 and C.A.M. H10=9m.8; chose C.A.M. per sec 3.1; periodic — will dedupe with other 10P apparitions; D1=3'.4 in Nov; page-image proofread vs page 361: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1904 III',
        'bigv_page': '361',
        'ocr_excerpt': "Holetschek, adopting m=12m.7 to 13m.0; got H10=10m.5; in M.N., 90:712 and C.A.M., H10=9m.8. In Nov., D1=3'.4.",
    },
    # 14: 1905 II - 19P/Borrelly first apparition
    {
        'pdes': '19P',
        'popular_name': 'Borrelly',
        'M1': '9.0',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by body — 'first recorded apparition of the short-period Comet Borrelly' = 19P; Holetschek H1 8m.7-11m.2 from own estimates; from Wirtz y=4.7, H0=10m.8; C.A.M. H10=9m.0; chose C.A.M. per sec 3.1; periodic — will dedupe with other 19P apparitions; non-standard y=4.7; page-image proofread vs page 362: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1905 II',
        'bigv_page': '362',
        'ocr_excerpt': "Holetschek obtained from his own estimates H1-values ranging from 8m.7 to 11m.2, from observations of Wirtz, y=4.7, H0=10m.8; in C.A.M., H10=9m.0.",
    },
    # 15: 1905 III - Giacobini 1905 F1
    {
        'pdes': '1905 F1',
        'popular_name': "Giacobini's Comet (1905 III)",
        'M1': '11.5',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by name (Giacobini) + Orion-Taurus 25 March 1905 -> 1905 F1; V.I y=11.1 H10=11m.4 (from Wirtz 10 obs); C.A.M. H10=11m.5; chose C.A.M. per sec 3.1; very faint telescopic comet; non-standard photometric law y=11.1; page-image proofread vs page 362: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1905 III',
        'bigv_page': '362',
        'ocr_excerpt': "V.I gave, according to Wirtz's 10 observations, y=11.1 and H10=11m.4; in C.A.M., H10=11m.5.",
    },
    # 16: 1905 IV - Kopff 1906 E1 (note: discovered 3 March 1906 but apparition is "1905 IV")
    {
        'pdes': '1906 E1',
        'popular_name': "Kopff's Comet (1905 IV)",
        'M1': '3.7',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, other',
        'notes': "matched by name (Kopff) + body text 3 March 1906 discovery in Virgo-Leo, plus prediscovery plates from 1904-1905 -> 1906 E1 per target list; V.I H10=4m.2 (from Wirtz); Big V comments 'most observers estimated the comet brighter by 0m.5, and therefore it would be better to take H10=3m.7'; from 1907 estimates m=13.8-15 -> H10=2m.8 to 3m.5; chose Big V's preferred synthesis 3m.7; observed 40 months, very distant comet (r=3.6-6.4 AU); non-standard implied y=10; page-image proofread vs page 363: confirmed",
        'match_confidence': 'medium',
        'bigv_designation_old': '1905 IV',
        'bigv_page': '363',
        'ocr_excerpt': "V.I obtained, according to Wirtz's observations, H10=4m.2. Most observers estimated the comet brighter by 0m.5, and therefore it would be better to take H10=3m.7; from Wirtz, h10 equal to 4m.7. From estimates for March to June 1907, m=13.8 to 15m; hence H10=2m.8 to 3m.5.",
    },
    # 17: 1905 V - Schaer 1905 W1
    {
        'pdes': '1905 W1',
        'popular_name': "Schaer's Comet (1905 V)",
        'M1': '8.9',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, other',
        'notes': "matched by name (Schaer) + Geneva 17 Nov 1905 -> 1905 W1; V.I y=18.5 H10=9m.5, h10=12m.4 (Wirtz/Nijland); C.A.M. H10=10m.3; Big V synthesis from Wolf binocular estimates 20-22 Dec gives H10=8m.9 (brighter — preferred per pattern); ASYMMETRIC implied (rapid fading after Dec); chose Big V preferred per V1 pattern (Big V's reappraisal supersedes); non-standard y=18.5; brief naked-eye visibility 5.5-6.5m; page-image proofread vs page 364: confirmed",
        'match_confidence': 'medium',
        'bigv_designation_old': '1905 V',
        'bigv_page': '364',
        'ocr_excerpt': "V.I gave, according to Wirtz and Nijland, y=18.5, H10=9m.5, h10=12m.4; in C.A.M., H10=10m.3. Making use of Wolf's estimates and other binocular observations for 20 Dec. to 22 Dec., we obtain H10=8m.9.",
    },
    # 18: 1905 VI - Brooks 1906 B1
    {
        'pdes': '1906 B1',
        'popular_name': "Brooks's Comet (1905 VI)",
        'M1': '7.5',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by name (Brooks) + Hercules 26 Jan 1906 -> 1906 B1; V.I y=24, H0=5m.1 (Wirtz); C.A.M. H10=7m.5; Holetschek H10=7m.7; chose C.A.M. per sec 3.1; non-standard y=24 (very steep brightness law); page-image proofread vs page 365: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1905 VI',
        'bigv_page': '365',
        'ocr_excerpt': "V.I gave, according to Wirtz's observations, y=24. H0=5m.1; in C.A.M., H10=7m.5; Holetschek estimated H10=7m.7.",
    },
    # 19: 1906 I - Giacobini 1905 X1
    {
        'pdes': '1905 X1',
        'popular_name': "Giacobini's Comet (1906 I)",
        'M1': '8.3',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by name (Giacobini) + Bootes 6 Dec 1905 -> 1905 X1; V.I pre-peri y=22, H0=8m.8 (Wirtz/Holetschek); post-peri y=18.2, H0=8m.1; ASYMMETRIC pre-peri 8m.8 vs post-peri 8m.1 (post is BRIGHTER); C.A.M. H10=8m.3 (synthesis); chose C.A.M. per sec 3.1; comet brightened unexpectedly to m=4 in Jan 1906; non-standard y; sanity check: peak m=4 with r_peri=0.22 fits M1=8.3 K=10 reasonably; page-image proofread vs page 365-366: confirmed",
        'match_confidence': 'medium',
        'bigv_designation_old': '1906 I',
        'bigv_page': '365',
        'ocr_excerpt': "V.I gave according to observations of Wirtz and Holetschek before the perihelion y=22, H0=8m.8. After the perihelion, y=18.2, H0=8m.1. In C.A.M., H10=8m.3.",
    },
    # 20: 1906 II - Ross 1906 F1
    {
        'pdes': '1906 F1',
        'popular_name': "Ross's Comet (1906 II)",
        'M1': '10.2',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by name (Ross) + Cetus 18 March 1906 -> 1906 F1; V.I H10=10m.2; C.A.M. H10=10m.2 (same value); D1=4'.5 in March; brief observation period (3 weeks); page-image proofread vs page 366-367: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1906 II',
        'bigv_page': '366',
        'ocr_excerpt': "In V.I, H10=10m.2; same figure given in C.A.M. In March, D1=4'.5.",
    },
]

out_path = r'C:\Users\grfai\documents\0_Dissertation\code\ch 5 comet salience\data\intermediate\agent_work\agent_c_rows.csv'
with open(out_path, 'a', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['pdes','popular_name','M1','K1','source_citation','notes','match_confidence','bigv_designation_old','bigv_page','ocr_excerpt'], quoting=csv.QUOTE_MINIMAL)
    for r in rows:
        w.writerow(r)
print(f'Wrote {len(rows)} rows for chunk 2')
