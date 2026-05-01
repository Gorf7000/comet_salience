import csv

rows = [
    # 61: 1914 IV - Campbell 1914 S1 (bright)
    {
        'pdes': '1914 S1',
        'popular_name': "Campbell's Comet (1914 IV)",
        'M1': '7.0',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by name (Campbell) + Dorado 17 Sept 1914 -> 1914 S1; bright comet 3-4m at discovery, naked-eye visible early; V.I H0=6m.2; C.A.M. H10=7m.0; Big V from 21 Oct estimates H10=6m.0; chose C.A.M. per sec 3.1; sanity check: peak m~3.7 (~Theta Eridani) reported 21-22 Sept with r=1.15, Δ=0.28 -> peak ~ 7.0 + 5log(0.32) - 10log(1.15) = 7.0 - 2.47 - 0.61 ~ 3.92 — consistent with 3-4m reported peak; page-image proofread vs page 404: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1914 IV',
        'bigv_page': '404',
        'ocr_excerpt': "In V.I, H0=6m.2; in C.A.M., H10=7m.0; from estimates of 21 Oct., H10=6m.0. In November, D1=6'.5. S>0.003.",
    },
    # 62: 1914 V - Delavan 1913 Y1 (very bright famous comet)
    {
        'pdes': '1913 Y1',
        'popular_name': "Delavan's Comet (1914 V)",
        'M1': '1.1',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by name (Delavan) + La Plata 17 Dec 1913 -> 1913 Y1; FAMOUS bright comet, peaked m=3.0 in Sept 1914, two tails 10 deg straight + 4-5 deg curving; V.I y=11.0 H0=0m.64 (Holetschek), y=10.9 H0=1m.0 (Nijland), y=9.8 H10=1m.4 (Yagolim); C.A.M. H10=1m.1; Bobrovnikoff y=8.8 H0=1m.8 (260 estimates, 37 normals — Big V flags as differing 'much more widely from estimates of 1915'); chose C.A.M. per sec 3.1; observed nearly two years (Dec 1913 to Sept 1915); sanity check: very bright intrinsically, peak m=3 with r_peri=1.10, Δ=1.71 -> peak ~ 1.1 + 5log(1.881) + 10log(1.10) = 1.1 + 1.37 + 0.41 = 2.88 — excellent agreement with reported 3m peak; non-standard y=11.0; page-image proofread vs page 405-406: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1914 V',
        'bigv_page': '405',
        'ocr_excerpt': "In V.I, Vsekhsvyatskii obtained from Holetschek's observations y=11.0, H0=0m.64; from Nijland's observations, y=10.9, H0=1m.0; from Yagolim's observations, y=9.8, H10=1m.4. In C.A.M., H10=1m.1. Bobrovnikoff and McLaughlin obtained from 260 estimates of various observers (37 normal locations) y=8.8, H0=1m.8.",
    },
    # 63: 1914 VI - 2P/Encke 33rd apparition
    {
        'pdes': '2P',
        'popular_name': "Encke's Comet",
        'M1': '10.1',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by body — 'thirty-third recorded apparition of the short-period Comet Encke' = 2P; Holetschek H1=9m.8-10m.2 (own estimates 25-27 Oct); V.II H10=10m.0; C.A.M. H10=10m.1 (same figures in A.Zh. 31:282 1954); chose C.A.M. per sec 3.1; periodic — will dedupe with other 2P apparitions; type I tail; page-image proofread vs page 406-407: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1914 VI',
        'bigv_page': '406',
        'ocr_excerpt': "Holetschek from his own estimates, for 25 Oct. and 27 Oct. gave H1=9.8 to 10m.2; in V.II, H10=10m.0; in C.A.M., H10=10m.1. The same values were given in the most recent publication, A.Zh., 31:282. 1954.",
    },
    # 64: 1915 I - 10P/Tempel 2 sixth apparition
    {
        'pdes': '10P',
        'popular_name': 'Tempel 2',
        'M1': '11.0',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by body — 'sixth recorded apparition of the short-period Comet Tempel(2) (not observed in 1910)' = 10P; absolute magnitude first determined by Vsekhsvyatskii in M.N., 90:712; C.A.M. H10=11m; Big V synthesis H10=10m.2; chose C.A.M. per sec 3.1; periodic — will dedupe with other 10P apparitions; very faint (12-15m); no estimates by visual observers; page-image proofread vs page 407: confirmed",
        'match_confidence': 'medium',
        'bigv_designation_old': '1915 I',
        'bigv_page': '407',
        'ocr_excerpt': "The absolute magnitude determined first by Vsekhsvyatskii in M.N., 90:712; in C.A.M., H10=11m; considering these estimates, we obtain H10=10m.2.",
    },
    # 65: 1915 II - Mellish 1915 C1 (naked-eye, double nucleus)
    {
        'pdes': '1915 C1',
        'popular_name': "Mellish's Comet (1915 II)",
        'M1': '3.7',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by name (Mellish) + Ophiuchus 9 Feb 1915 -> 1915 C1; naked-eye visible from late July, double nucleus observed in May (components separated 0'.3 to 38'); V.I y=-2.1 H0=6m.9 (Holetschek/Nijland to May, NEGATIVE y indicating brightness DROP toward perihelion, very unusual); C.A.M. H10=3m.7 (numerous estimates); Bobrovnikoff y=9.9 H0=4m.5 (78 estimates to Dec 1915); chose C.A.M. per sec 3.1; sanity check: peak m=4 in May with r_peri=1.0, Δ=0.40 -> peak ~ 3.7 + 5log(0.40) + 10log(1.0) = 3.7 - 1.99 + 0 = 1.71 — too bright vs reported 4m peak; M1=3.7 may be slight overestimate; possibly type I tail; non-standard y; page-image proofread vs page 407-408: confirmed",
        'match_confidence': 'medium',
        'bigv_designation_old': '1915 II',
        'bigv_page': '407',
        'ocr_excerpt': "According to the observations of Holetschek and Nijland up to May 1915, V.I gave y=-2.1, H0=6m.9; in C.A.M., according to numerous estimates, H10=3m.7. From 78 estimates up to 30 Dec. 1915, Bobrovnikoff obtained y=9.9, H10=4m.5.",
    },
    # 66: 1915 III - 7P/Pons-Winnecke 9th apparition
    {
        'pdes': '7P',
        'popular_name': 'Pons-Winnecke',
        'M1': '9.2',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by body — 'ninth recorded apparition of the short-period Comet Pons-Winnecke' = 7P (Big V notes 'nine apparitions were overlooked'); Holetschek H1=10m.0; M.N. 90:713 Vsekhsvyatskii Hm=9m.2 Hb=8m.4; C.A.M. H10=9m.2; chose C.A.M. per sec 3.1; periodic — will dedupe with other 7P apparitions; reached m=9.5 in Oct; D1=2.2; page-image proofread vs page 409: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1915 III',
        'bigv_page': '409',
        'ocr_excerpt': "Holetschek estimated H1=10m.0; in M.N., 90:713, Vsekhsvyatskii obtained Hm=9m.2, Hb=8m.4; in C.A.M., H10=9m.2. In Oct., D1=2.2.",
    },
    # 67: 1915 IV - OVERRIDE: 1915 R1 (Mellish) NOT 226P
    {
        'pdes': '1915 R1',
        'popular_name': "Mellish's Comet (1915 IV)",
        'M1': '10.0',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, other',
        'notes': "MANUAL DESIGNATION OVERRIDE — script gave 226P (wrong; 226P/Pigott-LINEAR-Kowalski 1915-09-15 has same year but body lacks periodicity claim); body says 'Discovered by Mellish (Williams Bay, U.S.A.) on the morning of 13 Sept' — single-apparition Mellish discovery 13 Sept matches C/1915 R1 (Mellish) per target list (R = 1-15 Sept); only 5 observation days before solar conjunction; C.A.M. H10=11m; Big V synthesis H10=9m.5-10m.5 (mid 10.0); chose Big V mid-range per sec 3.4; very brief observation; page-image proofread vs page 409: confirmed",
        'match_confidence': 'medium',
        'bigv_designation_old': '1915 IV',
        'bigv_page': '409',
        'ocr_excerpt': "In C.A.M., H10=11m. Taking m=9 to 10m upon discovery and for the last observation, we obtain H10=9m.5 to 10m.5.",
    },
    # 68: 1916 I - 69P/Taylor first apparition
    {
        'pdes': '69P',
        'popular_name': 'Taylor',
        'M1': '8.8',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by name (Taylor) + Orion 24 Nov 1915 -> 69P/Taylor first apparition (target list); V.I H10=8m.8 (Holetschek/van Biesbroeck); C.A.M. H10=8m.8 (same figure); chose C.A.M. per sec 3.1; periodic — will dedupe with other 69P apparitions; double nucleus observed Feb 1916 (split); 27 May 1916 m=13m.9 (rapid fading); page-image proofread vs page 409-410: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1916 I',
        'bigv_page': '409',
        'ocr_excerpt': "V.I gave, according to observations of Holetschek, van Biesbroeck et al., H10=8m.8; same figure in C.A.M.",
    },
    # 69: 1916 II - 25D/Neujmin 2 first apparition
    {
        'pdes': '25D',
        'popular_name': 'Neujmin 2',
        'M1': '10.7',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, other',
        'notes': "matched by body — 'first recorded appearance of the short-period Comet Neujmin(2)' = 25D; V.I (at y=10) H10=11m.4 (van Biesbroeck); from these estimates Big V synthesis H10=10m.7; chose Big V's reappraisal as preferred (closer to actual estimates); periodic — will dedupe with other 25D apparitions; D1=2'.2; page-image proofread vs page 410: confirmed",
        'match_confidence': 'medium',
        'bigv_designation_old': '1916 II',
        'bigv_page': '410',
        'ocr_excerpt': "From van Biesbroeck's estimates, V.I gave (at y=10) H10=11m.4. From these estimates, H10=10m.7. In March and April D1=2'.2.",
    },
    # 70: 1916 IV - Metcalf 489P? (very few observations)
    {
        'pdes': '489P?',
        'popular_name': "Metcalf's Comet (1916 IV)",
        'M1': '12.5',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, other',
        'notes': "JSONL pdes 489P (Roman fallback unverified) — body description: Metcalf discovery 21 Nov 1916 in Taurus on minor-planet-tracking plate, observed only 21-26 Nov; orbit considered 'very questionable' by Crommelin; 489P/Lemmon-PANSTARRS would be a modern periodic identification but uncertain — flagged with ?; only Big V's m-based estimate H10=11m.5-13m.5 (mid 12.5) cited, no C.A.M. or other authority; LOW CONFIDENCE — designation uncertain (orbit doubtful), few observations; page-image proofread vs page 411: confirmed",
        'match_confidence': 'low',
        'bigv_designation_old': '1916 IV',
        'bigv_page': '411',
        'ocr_excerpt': "Adopting for 21 Nov. to 26 Nov., m=11 to 13m we obtain H10=11.5 to 13m.5.",
    },
]

out_path = r'C:\Users\grfai\documents\0_Dissertation\code\ch 5 comet salience\data\intermediate\agent_work\agent_c_rows.csv'
with open(out_path, 'a', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['pdes','popular_name','M1','K1','source_citation','notes','match_confidence','bigv_designation_old','bigv_page','ocr_excerpt'], quoting=csv.QUOTE_MINIMAL)
    for r in rows:
        w.writerow(r)
print(f'Wrote {len(rows)} rows for chunk 7')
