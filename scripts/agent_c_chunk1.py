import csv

rows = [
    # 1: 1901 I — bright southern comet, asymmetric
    {
        'pdes': '1901 G1',
        'popular_name': "Viscara's Comet (Great Southern 1901)",
        'M1': '4.0',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, other',
        'notes': "matched by name (Viscara) + bright southern comet 12 April 1901; V.II H10=5m.9 (Nijland/Aitken/Innes); pre-peri H10=4m.0 from estimates beg of May (chosen as brighter per sec 3.3); post-peri June m=10-11 -> H10=7m.2; ASYMMETRIC; sanity check: bright morning naked-eye comet, magnitude 1-2 reported, peak intrinsic 1m.0 (5.3 May); page-image proofread vs page 351-352: confirmed",
        'match_confidence': 'low',
        'bigv_designation_old': '1901 I',
        'bigv_page': '351',
        'ocr_excerpt': "V II gave, according to the estimates of Nijland, Aitken, Innes et al., H10=5m.9. From the estimates for the beginning of May, H10=4m.0. In June, m=10 to 11m; hence H10=7m.2.",
    },
    # 2: 1901 II — 2P Encke
    {
        'pdes': '2P',
        'popular_name': "Encke's Comet",
        'M1': '9.1',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by body — 'twenty ninth recorded apparition of Comet Encke' = 2P; Holetschek H1=7m.6-8m.5 (mid 8.05); nucleus 9m.1-10m; C.A.M. H10=9m.1; chose C.A.M. per sec 3.1; periodic — will dedupe with other 2P apparitions; page-image proofread vs page 353: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1901 II',
        'bigv_page': '353',
        'ocr_excerpt': "Holetschek, making use of his own estimates and those of other observers, obtained H1=7m.6 to 8m.5; nucleus 9m.1 to 10m. In C.A.M., H10=9m.1.",
    },
    # 3: 1902 I — Brooks
    {
        'pdes': '1902 G1',
        'popular_name': "Brooks's Comet (1902 I)",
        'M1': '11.7',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, other',
        'notes': "matched by name (Brooks) + Pegasus 14 April 1902 -> 1902 G1; only V.I H10=11m.7 cited (h0=12m.2 nucleus); D1=1'.5; S=0.004; brief telescopic comet; faint object (7-8m at discovery, faded after perihelion); page-image proofread vs page 353: confirmed (V.I treated as 'other' since not specifically C.A.M./Holetschek/E-II/E-I)",
        'match_confidence': 'medium',
        'bigv_designation_old': '1902 I',
        'bigv_page': '353',
        'ocr_excerpt': "From V.I, H10=11m.7; h10=12m.2. D1=1'.5; S=0.004.",
    },
    # 4: 1902 II — 26P Grigg-Skjellerup first apparition
    {
        'pdes': '26P',
        'popular_name': 'Grigg-Skjellerup',
        'M1': '9.0',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, other',
        'notes': "matched by body — 'first recorded apparition of the short-period Comet Grigg-Skjellerup' = 26P; V.II H10=9m; Big V synthesis 'estimating m=8 to 10m for 22 Aug.-29 Aug., we obtain H10=9 to 10m' (mid 9.5); chose V.II=9m as primary value (range 9-10 also cited but body lists 9 first); D1=1'.6; periodic — will dedupe; page-image proofread vs page 354: confirmed",
        'match_confidence': 'medium',
        'bigv_designation_old': '1902 II',
        'bigv_page': '354',
        'ocr_excerpt': "In V.II, H10=9m. Estimating m=8 to 10m for 22 Aug. to 29 Aug., we obtain H10=9 to 10m. D1=1'.6.",
    },
    # 5: 1902 III — Perrine 1902 R1
    {
        'pdes': '1902 R1',
        'popular_name': "Perrine's Comet (1902 III)",
        'M1': '6.0',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by name (Perrine) + Perseus 1 Sept 1902 -> 1902 R1; V.I y=11.5 H0=6m.0 (Holetschek); same source y=9.2 H0=5m.7 (Nijland/Graff/Wirtz); C.A.M. H10=6m.0; Bobrovnikoff y=6.6 H0=6m.8 noted as too low by Big V; chose C.A.M. per sec 3.1; reached naked-eye 4.2-4.1 in Oct; non-standard photometric law y=11.5 (NOT y=4); page-image proofread vs page 354-355: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1902 III',
        'bigv_page': '354',
        'ocr_excerpt': "In V.I, according to Holetschek's observations, y=11.5; H0=6m.0. The same source gave, according to the estimates of Nijland, Graff, Wirtz et al., y=9.2; H0=5m.7; in C.A.M., H10=6m.0.",
    },
    # 6: 1903 I — OVERRIDE: this is 1903 A1 Giacobini, NOT 11P
    {
        'pdes': '1903 A1',
        'popular_name': "Giacobini's Comet (1903 I)",
        'M1': '8.6',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "MANUAL DESIGNATION OVERRIDE — script gave 11P (wrong; 11P/Tempel-Swift 1903 apparition was 113P/Spitaler in target list with peri 1903-12-15, but this entry's peri is 1903-03-16 from r,delta); body identifies as Giacobini's Pisces discovery 15 Jan 1903 = 1903 A1 (Giacobini) per target list peri 1903-03-16; V.I H0=8m.2 y=6.8; C.A.M. H10=8m.6; Big V synthesis from m=4m on 16 March -> H10=7m.7; post-peri y=17.5 (very rapid fading); chose C.A.M. per sec 3.1; non-standard y values; page-image proofread vs page 355-356: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1903 I',
        'bigv_page': '355',
        'ocr_excerpt': "From V.I, H0=8m.2, y=6.8. In C.A.M., H10=8m.6. Taking m=4m on 16 March, we obtain H10=7m.7; the decrease in brightness after the perihelion passage corresponds to y=17.5.",
    },
    # 7: 1903 II — OVERRIDE: this is 1902 X1 (Giacobini Dec 1902 discovery), NOT 1903 A1
    {
        'pdes': '1902 X1',
        'popular_name': "Giacobini's Comet (1903 II)",
        'M1': '5.0',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "MANUAL DESIGNATION OVERRIDE — script gave 1903 A1 (wrong; that's 1903 I, the previous entry); body identifies as Giacobini's 2 Dec 1902 Monoceros discovery, distant comet (r=2.97 to 2.94) -> 1902 X1 (Giacobini) per target list peri 1903-03-23; first determination of H10 in V.I; C.A.M. H10=5m.0 (nucleus 6m.5); D1=2'.8 to 3'.0 in Jan-Feb, 7' in April; chose C.A.M. per sec 3.1; faint distant object (11-12m); page-image proofread vs page 356-357: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1903 II',
        'bigv_page': '356',
        'ocr_excerpt': "The first determination of the absolute magnitude H10 was given in V.I. In C.A.M., H10=5m.0. Nucleus 6m.5. Jan. and Feb., D1=2'.8 to 3'.0; in April, 7'.",
    },
    # 8: 1903 III — Grigg 1903 H1
    {
        'pdes': '1903 H1',
        'popular_name': "Grigg's Comet (1903 III)",
        'M1': '9.1',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, other',
        'notes': "matched by name (Grigg) + Eridanus 17 April 1903 -> 1903 H1 (Grigg); V.II based on m=13m.5 'obvious underestimate' so flagged erroneous (V1 pattern); from estimates above (8-9m at discovery, 12-13m at last) Big V synthesis H10=8m.6 to 9m.6 (mid 9.1); chose Big V's preferred synthesis since V.II flagged underestimate; observed only in southern hemisphere; ERRONEOUS V.II flagged; page-image proofread vs page 357: confirmed",
        'match_confidence': 'medium',
        'bigv_designation_old': '1903 III',
        'bigv_page': '357',
        'ocr_excerpt': "In V.II estimated on the assumption that m=13m.5 (obvious underestimate). From the estimates above we obtain H10=8m.6 to 9m.6.",
    },
    # 9: 1903 IV — Borrelly 1903 M1
    {
        'pdes': '1903 M1',
        'popular_name': "Borrelly's Comet (1903 IV)",
        'M1': '6.3',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by name (Borrelly) + Aquarius 21 June 1903 -> 1903 M1 (Borrelly); V.I h10=10m.0 (nucleus); Yagolim y=4.2 H10=5m.9; C.A.M. H10=6m.3; Bobrovnikoff y=5.95 H0=6m.50 (Big V notes radically disagree with observations); chose C.A.M. per sec 3.1; reached naked-eye peak m=2m.8 on 18 July; sanity check: bright bare-eye comet observed by Schwab 2-3m; consistent with M1=6.3 K=10 fit; page-image proofread vs page 357-358: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1903 IV',
        'bigv_page': '357',
        'ocr_excerpt': "V.I gave according to Holetschek's observations h10=10m.0; from Yagolim, Izv. Russ. Astr. Org., y=4.2. H10=5m.9; in C.A.M., H10=6m.3.",
    },
    # 10: 1903 V — 16P/Brooks 2 third apparition
    {
        'pdes': '16P',
        'popular_name': 'Brooks 2',
        'M1': '9.5',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by body — 'third recorded apparition of the short period Comet Brooks (2)' = 16P; Holetschek H1=10m.2-11m.6 (mid 10.9); C.A.M. H10=9m.5; Konopleva H10(av)=10m.3; chose C.A.M. per sec 3.1; periodic — will dedupe with other 16P apparitions; brightness fluctuations noted; page-image proofread vs page 359: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1903 V',
        'bigv_page': '359',
        'ocr_excerpt': "Holetschek, from the estimates of Barnard and Aitken, found H1=10m.2 to 11m.6. In Aug., D1=3'.5; in Dec., 1'.0. In C.A.M., H10=9m.5. V.P. Konopleva, Publ. Kiev Obs. 5. 1953, obtained H10(av)=10m.3.",
    },
]

out_path = r'C:\Users\grfai\documents\0_Dissertation\code\ch 5 comet salience\data\intermediate\agent_work\agent_c_rows.csv'
with open(out_path, 'a', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['pdes','popular_name','M1','K1','source_citation','notes','match_confidence','bigv_designation_old','bigv_page','ocr_excerpt'], quoting=csv.QUOTE_MINIMAL)
    for r in rows:
        w.writerow(r)
print(f'Wrote {len(rows)} rows for chunk 1')
