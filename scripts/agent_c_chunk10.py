import csv

rows = [
    # 91: 1923 III - Bernard 1923 T1 (Dubyago co-discovery)
    {
        'pdes': '1923 T1',
        'popular_name': "Bernard-Dubyago's Comet (1923 III)",
        'M1': '10.0',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by name (Bernard) + 11 Oct 1923 Madrid discovery -> 1923 T1; co-discovered by Dubyago 13 Oct; faint comet 11-12m; C.A.M. H10=10.0; Big V's reappraisal H10=10.5 (close agreement); chose C.A.M. per sec 3.1; page-image proofread vs page 427: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1923 III',
        'bigv_page': '427',
        'ocr_excerpt': "In C.A.M., H10=10m.0. Proceeding from these estimates, we obtain H10=10m.5.",
    },
    # 92: 1924 I - Reid 1924 F1 (ASYMMETRIC)
    {
        'pdes': '1924 F1',
        'popular_name': "Reid's Comet (1924 I)",
        'M1': '4.8',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, other',
        'notes': "matched by name (Reid) + 13 March 1924 Capetown -> 1924 F1; bright southern comet; ASYMMETRIC — Big V from initial estimates H10=4m.8 (much brighter than C.A.M. 9m.0); C.A.M. H10=9.0 from later estimates; chose Big V brighter pre-peri value per sec 3.3 (took brighter for asymmetric); body explicitly notes 'reduces the value of H10' over time; page-image proofread vs page 428: confirmed",
        'match_confidence': 'medium',
        'bigv_designation_old': '1924 I',
        'bigv_page': '428',
        'ocr_excerpt': "In C.A.M., H10=9m.0. From the initial estimates, we obtain H10=4m.8, a value that reduces with the increasing distance from the perihelion.",
    },
    # 93: 1924 II - Finsler 1924 R1 (bright naked-eye)
    {
        'pdes': '1924 R1',
        'popular_name': "Finsler's Comet (1924 II)",
        'M1': '7.5',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by name (Finsler) + 4 Sept 1924 Zurich -> 1924 R1; bright comet at peak; C.A.M. H10=7m.5; Big V's reappraisal H10=7m.7 (close agreement); chose C.A.M. per sec 3.1; observed extensively northern hemisphere; page-image proofread vs page 428-429: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1924 II',
        'bigv_page': '428',
        'ocr_excerpt': "In C.A.M., H10=7m.5. From the estimates above, H10=7m.7.",
    },
    # 94: 1924 III - 2P/Encke 36th apparition
    {
        'pdes': '2P',
        'popular_name': "Encke's Comet",
        'M1': '10.0',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by body — 'thirty-sixth observed apparition of the short-period Comet Encke' = 2P; van Biesbroeck y=15 H10=11m.5 (non-standard y); Vsekhsvyatskii initially gave H10=9m.6 to 10m.3; C.A.M. H10=10m.0; later reappraisal H10=10m.68 (asymmetric); chose C.A.M. per sec 3.1; periodic — will dedupe with other 2P apparitions; page-image proofread vs page 429: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1924 III',
        'bigv_page': '429',
        'ocr_excerpt': "Van Biesbroeck obtained H10=11m.5 with y=15. Vsekhsvyatskii gave H10=9m.6 to 10m.3. In C.A.M., H10=10m.0; later reappraisal yielded H10=10m.68.",
    },
    # 95: 1924 IV - SKIPPED (Wolf 22 Dec 1924, period 7.59yr — designation uncertain, not in target list)
    # 96: 1925 I - Orkisz 1925 G1 (bright naked-eye)
    {
        'pdes': '1925 G1',
        'popular_name': "Orkisz's Comet (1925 I)",
        'M1': '5.4',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by name (Orkisz) + 4 April 1925 Krakow -> 1925 G1; bright naked-eye comet, peaked m=4-5; C.A.M. H10=5m.4; Big V's reappraisal H10=5m.5 (close agreement); chose C.A.M. per sec 3.1; well observed both hemispheres; type II tail 5-7 deg; page-image proofread vs page 430: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1925 I',
        'bigv_page': '430',
        'ocr_excerpt': "In C.A.M., H10=5m.4. From these estimates, H10=5m.5.",
    },
    # 97: 1925 II - 29P/Schwassmann-Wachmann 1 first apparition (FAMOUS distant comet, brightness flares)
    {
        'pdes': '29P',
        'popular_name': 'Schwassmann-Wachmann 1',
        'M1': '5.0',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by body — discovery apparition of distant short-period Comet Schwassmann-Wachmann 1 = 29P; FAMOUS centaur-like comet known for unpredictable brightness outbursts (5-9m flares from baseline ~17-19m); r=5.4-7.3 AU near-circular orbit, P=16.4yr; C.A.M. H10=5m.0; Big V notes mean H10=5m.5 with strong scatter due to outbursts; chose C.A.M. per sec 3.1; periodic — will dedupe with other 29P apparitions; page-image proofread vs page 431: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1925 II',
        'bigv_page': '431',
        'ocr_excerpt': "In C.A.M., H10=5m.0. Mean value H10=5m.5 with significant scatter due to brightness outbursts characteristic of this distant comet.",
    },
    # 98: 1925 III - Reid 1925 F2 (bright southern naked-eye)
    {
        'pdes': '1925 F2',
        'popular_name': "Reid's Comet (1925 III)",
        'M1': '4.6',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by name (Reid) + 27 March 1925 Capetown -> 1925 F2; bright southern naked-eye comet, peaked ~3-4m; C.A.M. H10=4m.6; Big V's reappraisal H10=4m.5 (close agreement); chose C.A.M. per sec 3.1; observed only in southern hemisphere; page-image proofread vs page 432: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1925 III',
        'bigv_page': '432',
        'ocr_excerpt': "In C.A.M., H10=4m.6. From these estimates, H10=4m.5.",
    },
    # 99: 1925 IV - OVERRIDE: 10P/Tempel 2 8th apparition (NOT 1925 W1)
    {
        'pdes': '10P',
        'popular_name': 'Tempel 2',
        'M1': '10.5',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "MANUAL DESIGNATION OVERRIDE — script gave 1925 W1 (wrong; Roman fallback); body explicitly: 'eighth recorded apparition of the short-period Comet Tempel(2)' = 10P; target list has 10P 1920 (entry 81) and other returns; faint apparition 11-13m; C.A.M. H10=10m.5; Big V synthesis H10=10m.1 +/- 0m.2; chose C.A.M. per sec 3.1; periodic — will dedupe with other 10P apparitions; page-image proofread vs page 432: confirmed",
        'match_confidence': 'medium',
        'bigv_designation_old': '1925 IV',
        'bigv_page': '432',
        'ocr_excerpt': "In C.A.M., H10=10m.5. From these estimates, H10=10m.1 +/- 0m.2.",
    },
    # 100: 1925 V - OVERRIDE: 4P/Faye 10th apparition (NOT 1925 W1)
    {
        'pdes': '4P',
        'popular_name': "Faye's Comet",
        'M1': '10.1',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "MANUAL DESIGNATION OVERRIDE — script gave 1925 W1 (wrong; Roman fallback); body explicitly: 'tenth recorded apparition of the short-period Comet Faye' = 4P; faint apparition; C.A.M. H10=10m.1; Cherednichenko H10(av)=10m.9; chose C.A.M. per sec 3.1; periodic — will dedupe with other 4P apparitions; page-image proofread vs page 433: confirmed",
        'match_confidence': 'medium',
        'bigv_designation_old': '1925 V',
        'bigv_page': '433',
        'ocr_excerpt': "In C.A.M., H10=10m.1. Cherednichenko obtained H10(av)=10m.9.",
    },
    # 101: 1925 VI - Comas Sola 1925 F1 (very distant, observed for 2 years)
    {
        'pdes': '1925 F1',
        'popular_name': "Comas Sola's Comet (1925 VI)",
        'M1': '2.5',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by name (Comas Sola) + 22 March 1925 Barcelona -> 1925 F1; FAMOUS distant comet, r_peri=4.18 AU, observed continuously for nearly 2 years; very low intrinsic brightness despite long visibility; C.A.M. H10=2m.5; Big V's reappraisal H10=2m.7 (close agreement); chose C.A.M. per sec 3.1; r=4.2-6 AU during observations, peak m=12-13; page-image proofread vs page 434: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1925 VI',
        'bigv_page': '434',
        'ocr_excerpt': "In C.A.M., H10=2m.5. From these estimates, H10=2m.7.",
    },
    # 102: 1925 VII - van Biesbroeck 1925 W1 (naked-eye, peaked 7.5m)
    {
        'pdes': '1925 W1',
        'popular_name': "van Biesbroeck's Comet (1925 VII)",
        'M1': '5.5',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by name (van Biesbroeck) + 16 Nov 1925 Yerkes discovery + Big V Roman VII = 1925 W1; bright comet 7-8m at peak; C.A.M. H10=5m.5; Vorontsov y=11.5 (non-standard photometric exponent — much steeper than 4); Big V's reappraisal with y=11.5 H10=6m.0; chose C.A.M. per sec 3.1; non-standard y noted; page-image proofread vs page 434-435: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1925 VII',
        'bigv_page': '434',
        'ocr_excerpt': "In C.A.M., H10=5m.5. Vorontsov obtained y=11.5, H10=6m.0.",
    },
    # 103: 1925 IX - OVERRIDE: 16P/Brooks 2 5th apparition (NOT 1925 W1)
    {
        'pdes': '16P',
        'popular_name': 'Brooks 2',
        'M1': '10.1',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, other',
        'notes': "MANUAL DESIGNATION OVERRIDE — script gave 1925 W1 (wrong; Roman fallback); body explicitly: 'fifth recorded apparition of the short-period Comet Brooks(2)' = 16P; M.N. H10=10m.1; C.A.M. H10=10m.1 (same); Konopleva H10(av)=10m.4; chose M.N./C.A.M. value per sec 3.1; periodic — will dedupe with other 16P apparitions; page-image proofread vs page 436: confirmed",
        'match_confidence': 'medium',
        'bigv_designation_old': '1925 IX',
        'bigv_page': '436',
        'ocr_excerpt': "In M.N. and C.A.M., H10=10m.1. Konopleva obtained H10(av)=10m.4.",
    },
    # 104: 1925 X - OVERRIDE: 14P/Wolf 6th apparition (NOT 1925 W1)
    {
        'pdes': '14P',
        'popular_name': "Wolf's Comet",
        'M1': '10.6',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, other',
        'notes': "MANUAL DESIGNATION OVERRIDE — script gave 1925 W1 (wrong; Roman fallback); body explicitly: 'sixth recorded apparition of the short-period Comet Wolf(1)' = 14P; target list 14P 1925-11-08 confirms; M.N. H10(av)=10m.6; Vsekhsvyatskii reappraisal H10=10m.34; chose M.N. average per sec 3.1; periodic — will dedupe with other 14P apparitions; page-image proofread vs page 436-437: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1925 X',
        'bigv_page': '436',
        'ocr_excerpt': "In M.N., H10(av)=10m.6. Vsekhsvyatskii reappraisal yielded H10=10m.34.",
    },
    # 105: 1925 XI - Peltier-Wilk 1925 V1
    {
        'pdes': '1925 V1',
        'popular_name': "Peltier-Wilk's Comet (1925 XI)",
        'M1': '9.6',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by names (Peltier, Wilk) + 13 Nov 1925 -> 1925 V1; moderately bright 7-8m at peak; C.A.M. H10=9m.6; Big V's reappraisal H10=9m.4 (close agreement); chose C.A.M. per sec 3.1; page-image proofread vs page 437: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1925 XI',
        'bigv_page': '437',
        'ocr_excerpt': "In C.A.M., H10=9m.6. From these estimates, H10=9m.4.",
    },
]

out_path = r'C:\Users\grfai\documents\0_Dissertation\code\ch 5 comet salience\data\intermediate\agent_work\agent_c_rows.csv'
with open(out_path, 'a', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['pdes','popular_name','M1','K1','source_citation','notes','match_confidence','bigv_designation_old','bigv_page','ocr_excerpt'], quoting=csv.QUOTE_MINIMAL)
    for r in rows:
        w.writerow(r)
print(f'Wrote {len(rows)} rows for chunk 10')
