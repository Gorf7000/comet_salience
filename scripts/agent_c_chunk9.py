import csv

rows = [
    # 81: 1920 II - OVERRIDE: 10P/Tempel 2 seventh apparition (NOT 21P)
    {
        'pdes': '10P',
        'popular_name': 'Tempel 2',
        'M1': '10.0',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, other',
        'notes': "MANUAL DESIGNATION OVERRIDE — script gave 21P (wrong); body explicitly: 'seventh recorded apparition of the short-period Comet Tempel(2)' = 10P; target list 10P peri 1920-06-10 matches body's 25 May Kudara discovery; V.II H10=10m.0 (van Biesbroeck and others); M.N. 90:712 Hm=10m.1 Hb=9m.5 Hs=11m.5; chose V.II 10.0 as primary; periodic — will dedupe with other 10P apparitions; D1=1'.6; page-image proofread vs page 420: confirmed",
        'match_confidence': 'medium',
        'bigv_designation_old': '1920 II',
        'bigv_page': '420',
        'ocr_excerpt': "In V.II, from observations of van Biesbroeck and others, H10=10m.0; in M.N., 90:712, Hm=10m.1, Hb=9m.5, Hs=11m.5; D1=1'.6; S>0.0004.",
    },
    # 82: 1920 III - OVERRIDE: 1920 X1 (Skjellerup) (NOT 11P)
    {
        'pdes': '1920 X1',
        'popular_name': "Skjellerup's Comet (1920 III)",
        'M1': '11.9',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, other',
        'notes': "MANUAL DESIGNATION OVERRIDE — script gave 11P (wrong; 'Taylor' name match is for the 8 Dec discoverer not eponymous comet); body says discovered by Taylor 8 Dec 1920 and Skjellerup 13 Dec 1920 near alpha Hydrae -> C/1920 X1 (Skjellerup) per target list peri 1920-12-11; faint comet; E-I H10=11m.0 'apparently too large a value'; Big V's reappraisal H10=11m.9; chose Big V synthesis (E-I flagged as overestimate, taking Big V's preferred value per pattern); page-image proofread vs page 420: confirmed",
        'match_confidence': 'low',
        'bigv_designation_old': '1920 III',
        'bigv_page': '420',
        'ocr_excerpt': "E-I gave, according to the first estimates, H10=11m.0, apparently too large a value. Proceeding from the estimates above, we obtain H10=11m.9.",
    },
    # 83: 1921 I - Dubyago 1921 H1
    {
        'pdes': '1921 H1',
        'popular_name': "Dubyago's Comet (1921 I)",
        'M1': '10.5',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, E-I',
        'notes': "matched by body — Dubyago 24 April 1921 Auriga/Lynx discovery -> 1921 H1 (Dubyago) per target list; only E-I H10=10m.5 cited; brief observation period (April-June); decrease in brightness reported; chose E-I as the only authority value; D=0'.7; page-image proofread vs page 421: confirmed",
        'match_confidence': 'medium',
        'bigv_designation_old': '1921 I',
        'bigv_page': '421',
        'ocr_excerpt': "In E-I, H10=10m.5. A decrease in brightness reported in May and June. D=0'.7.",
    },
    # 84: 1921 II - Reid 1921 E1 (bright naked-eye)
    {
        'pdes': '1921 E1',
        'popular_name': "Reid-Dubiago's Comet (1921 II)",
        'M1': '6.7',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, other',
        'notes': "matched by name (Reid) + Capetown 13 March 1921 -> 1921 E1; bright naked-eye comet, peaked m=4-5 in early May; V.I y=17 H0=5m.9 (Holetschek), y=7.3 H0=7m.0 (van Biesbroeck), y=20 H0=6m.3 (Orlov); Big V's average synthesis y=9.6 H10=6m.7 h0=8m.3; Bobrovnikoff y=13.8 H0=6m.9 (97 estimates, close to Big V); chose Big V's synthesis 6m.7 as primary; sanity check: peak m=4-5 (van Biesbroeck) with r_peri=1.0, Δ=0.63 -> peak ~ 6.7 + 5log(0.63) - 10log(1.0) = 6.7 - 1.00 + 0 = 5.70 — consistent with 5m peak; type I + type III tails; non-standard y; page-image proofread vs page 421-422: confirmed",
        'match_confidence': 'medium',
        'bigv_designation_old': '1921 II',
        'bigv_page': '421',
        'ocr_excerpt': "V.I gave, according to Holetschek's observations, y=17, H0=5m.9; according to van Biesbroeck, y=7.3, H0=7m.0; the eight estimates of S.V. Orlov gave y=20, H0=6m.3. The average of these figures and the observations of Dziewulski, Hellerich and Wirtz is y=9.6, H10=6m.7, h0=8m.3; Bobrovnikoff... obtained y=13.8, H0=6m.9.",
    },
    # 85: 1921 IV - 2P/Encke 35th apparition
    {
        'pdes': '2P',
        'popular_name': "Encke's Comet",
        'M1': '10.8',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, E-I',
        'notes': "matched by body — 'thirty-fifth observed apparition of the short-period Comet Encke' = 2P; observed only in southern hemisphere (Cape, Johannesburg, Santiago); E-I H10=10m.8; Big V's reappraisal from estimates H10=11m.2 to 11m.5; chose E-I 10m.8 (brighter, primary authority); periodic — will dedupe with other 2P apparitions; faint apparition (8.5-12m); page-image proofread vs page 423: confirmed",
        'match_confidence': 'medium',
        'bigv_designation_old': '1921 IV',
        'bigv_page': '423',
        'ocr_excerpt': "In E-I, H10=10m.8; proceeding from these estimates, H10=11m.2 to 11m.5.",
    },
    # 86: 1921 VI - Reid 1922 B1
    {
        'pdes': '1922 B1',
        'popular_name': "Reid's Comet (1921 VI)",
        'M1': '6.3',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, E-I',
        'notes': "matched by name (Reid) + Antlia 20 Jan 1922 -> 1922 B1; only E-I H10=6m.3 cited; bright comet 9-10m at discovery (3 months post-perihelion); only observed in southern hemisphere; revolution period 1400 years (long-period); page-image proofread vs page 424: confirmed",
        'match_confidence': 'medium',
        'bigv_designation_old': '1921 VI',
        'bigv_page': '424',
        'ocr_excerpt': "In E-I, H10=6m.3.",
    },
    # 87: 1922 I - 26P/Grigg-Skjellerup second apparition
    {
        'pdes': '26P',
        'popular_name': 'Grigg-Skjellerup',
        'M1': '12.5',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by body — 'second recorded apparition of the short-period Comet Grigg-Skjellerup (1902 II)' = 26P; A.Zh. 7:215 H10=13m; C.A.M. H10=12 to 13m (took mid 12.5); Big V from 20-25 May m=10m -> H10=13m.1; from 20-25 July m=15m -> H10=15m (rapid post-peri fading); ASYMMETRIC; chose C.A.M. midpoint per sec 3.4 range-only; periodic — will dedupe with other 26P apparitions; close approach to Earth (Δ=0.27); page-image proofread vs page 424: confirmed",
        'match_confidence': 'medium',
        'bigv_designation_old': '1922 I',
        'bigv_page': '424',
        'ocr_excerpt': "In A.Zh., 7:215, H10=13m; in C.A.M., H10=12 to 13m. Taking m=10m on 20 May to 25 May, we obtain H10=13m.1; taking m=15m on 20 July and 25 July, we obtain H10=15m, indicating a rapid decrease in brightness with the increasing distance from the perihelion.",
    },
    # 88: 1922 II - Baade 1922 U1
    {
        'pdes': '1922 U1',
        'popular_name': "Baade's Comet (1922 II)",
        'M1': '5.5',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by name (Baade) + Cygnus 19 Oct 1922 -> 1922 U1; distant comet (r=2.26-5.19 AU); C.A.M. H10=5m.5; Big V's reappraisal H10=5m.3 ('yields m=15m.9 for 26 Feb 1923 in good agreement with van Biesbroeck'); chose C.A.M. per sec 3.1; observed for over 15 months, photographed up to Jan 1924 with anomalous 17' tail at P=283 deg; page-image proofread vs page 425: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1922 II',
        'bigv_page': '425',
        'ocr_excerpt': "In C.A.M., H10=5m.5. From these estimates, we obtain H10=5m.3, which yields m=15m.9 for 26 Feb. 1923 in good agreement with van Biesbroeck's estimates.",
    },
    # 89: 1923 I - Skjellerup-Reid 1922 W1 (asymmetric)
    {
        'pdes': '1922 W1',
        'popular_name': "Skjellerup-Reid's Comet (1923 I)",
        'M1': '7.5',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, E-I',
        'notes': "matched by name (Skjellerup, Reid) + 26 Nov 1922 Capetown discovery -> 1922 W1; bright at discovery 7-8m; E-I H10=7m.5 from first estimates; Big V's reappraisal using Schaumasse 11m gives H10=10m.5 (post-peri fainter); ASYMMETRIC — comet faded rapidly approaching and after perihelion; chose E-I 7m.5 (brighter, pre-peri) per sec 3.3; page-image proofread vs page 425-426: confirmed",
        'match_confidence': 'low',
        'bigv_designation_old': '1923 I',
        'bigv_page': '425',
        'ocr_excerpt': "E-I gave, according to the first estimates, H10=7m.5, which yields m=9m.5 for 24 Feb. Apparently the comet rapidly grew faint with approach to the perihelion and remained faint after the perihelion passage. Adopting Schaumasse's estimate, we obtain H10=10m.5.",
    },
    # 90: 1923 II - 6P/d'Arrest 8th apparition
    {
        'pdes': '6P',
        'popular_name': "d'Arrest's Comet",
        'M1': '9.8',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, other',
        'notes': "matched by body — 'eighth recorded apparition of the short-period Comet d'Arrest' = 6P; Vsekhsvyatskii M.N. 90:712 H10=9m.8 for period of increasing brightness (pre-peri); Big V synthesis from Sept estimates and Dec 1923/Jan 1924 obs gives H10=10m.0 to 13m.9 (avg 11m.4) — post-peri fading; ASYMMETRIC brightness flare after perihelion; chose M.N. 9m.8 brighter pre-peri value per sec 3.3 and sec 3.6 brightest preference for periodics; periodic — will dedupe with other 6P apparitions; page-image proofread vs page 426: confirmed",
        'match_confidence': 'medium',
        'bigv_designation_old': '1923 II',
        'bigv_page': '426',
        'ocr_excerpt': "Apparently a brightness flare after the perihelion passage. For the period of increasing brightness Vsekhsvyatskii, M.N., 90:712, gave H10=9m.8. Making use of September estimates, and also of observations in December 1923 and January 1924, we obtain H10=10.0 to 13m.9 (11m.4 on the average).",
    },
]

out_path = r'C:\Users\grfai\documents\0_Dissertation\code\ch 5 comet salience\data\intermediate\agent_work\agent_c_rows.csv'
with open(out_path, 'a', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['pdes','popular_name','M1','K1','source_citation','notes','match_confidence','bigv_designation_old','bigv_page','ocr_excerpt'], quoting=csv.QUOTE_MINIMAL)
    for r in rows:
        w.writerow(r)
print(f'Wrote {len(rows)} rows for chunk 9')
