import csv

rows = [
    # 31: 1908 I - 2P/Encke 31st apparition
    {
        'pdes': '2P',
        'popular_name': "Encke's Comet",
        'M1': '10.8',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by body — 'thirty-first recorded apparition of the short-period Comet Encke-Backlund' = 2P; Holetschek H1=10m.6 (m=8 at beginning of June); C.A.M. H10=10m.8; chose C.A.M. per sec 3.1; periodic — will dedupe with other 2P apparitions; faint apparition; page-image proofread vs page 374-375: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1908 I',
        'bigv_page': '374',
        'ocr_excerpt': "Holetschek took m=8m at the beginning of June and obtained H1=10m.6; in C.A.M., H10=10m.8.",
    },
    # 32: 1908 II - OVERRIDE: 11P/Tempel-Swift NOT 64P
    {
        'pdes': '11P',
        'popular_name': 'Tempel-Swift-LINEAR',
        'M1': '12.8',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, other',
        'notes': "MANUAL DESIGNATION OVERRIDE — script gave 64P (wrong); body explicitly: 'fourth (and apparently the last) recorded apparition of Comet Tempel(3)-Swift' = 11P/Tempel-Swift-LINEAR; target list 11P peri 1908-10-05 matches body's 29 Sept Javelle discovery; Holetschek H1=14m.5-16m.5 (mid 15.5); C.A.M. H10=15m.1; Big V synthesis from Oct estimates m=12-13m gives H10=12m.8 (preferred — brighter, brightest period as required for periodics per sec 3.6); periodic — will dedupe with other 11P apparitions; very faint; page-image proofread vs page 375: confirmed",
        'match_confidence': 'medium',
        'bigv_designation_old': '1908 II',
        'bigv_page': '375',
        'ocr_excerpt': "Holetschek obtained from the estimates above H1=14m.5 to 16m.5; in C.A.M., H10=15m.1; in October, we obtain m=12 to 13m, hence H10=12m.8.",
    },
    # 33: 1908 III - Morehouse 1908 R1 (FAMOUS COMET)
    {
        'pdes': '1908 R1',
        'popular_name': "Morehouse's Comet (1908 III)",
        'M1': '4.2',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by name (Morehouse) + Des Moines 1 Sept 1908 -> 1908 R1; one of the remarkable comets of the 20th century; Orlov from observations of Holetschek/Nijland/Wirtz: y=8.8, H0=4m.3, h0=4m.2; C.A.M. H10=4m.2; Bobrovnikoff y=12.5 H0=4m.0 and y=12.9 H0=3m.94 (110 estimates); chose C.A.M. per sec 3.1; sanity check: famous remarkable comet, intrinsic brightness 9->6->5m, naked-eye prominent for months, complex tail with type I; M1=4.2 with r_peri~0.94, Δ_min~1.06 -> peak ~ 4.2 + 5log(1.0) - 10log(0.94) = 4.2 + 0 + 0.27 ~ 4.5 — consistent with reported 5m peak; non-standard y=8.8 to 12.9; page-image proofread vs page 375-377: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1908 III',
        'bigv_page': '375',
        'ocr_excerpt': "Photometric parameter obtained for the first time by S.V. Orlov... From the observations of Holetschek, Nijland, Wirtz, et al., we obtain y=8.8, H0=4m.3, h0=4m.2. In C.A.M., H10=4m.2. Bobrovnikoff obtained from 110 estimates y=12.5, H0=4m.0 and y=12.9, H0=3m.94.",
    },
    # 34: 1909 II - OVERRIDE: 7P/Pons-Winnecke (NOT 18D)
    {
        'pdes': '7P',
        'popular_name': 'Pons-Winnecke',
        'M1': '9.7',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "MANUAL DESIGNATION OVERRIDE — script gave 18D (wrong); body explicitly: 'eighth recorded apparition of the short-period Comet Pons-Winnecke' = 7P/Pons-Winnecke; target list 7P peri 1909-10-09 matches body's 31 Oct Porro discovery (post-peri); Holetschek H1=8m.8-8m.9 (from Perrine estimates); V.I y=0.1 H0=9m.7; C.A.M. H10=9m.7; nucleus 10-11m.9; D1=2'.8; chose C.A.M. per sec 3.1; periodic — will dedupe with other 7P apparitions; non-standard y=0.1 (essentially flat); page-image proofread vs page 378: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1909 II',
        'bigv_page': '378',
        'ocr_excerpt': "From Perrine's estimates, Holetschek found H1=8m.8 to 8m.9; from the same estimates, V.I found y=0.1, H0=9m.7; in C.A.M., H0=9m.7; nucleus 10 to 11m.9; D1=2'.8.",
    },
    # 35: 1909 III - 18D/Perrine-Mrkos second apparition (correct designation, but body confirms Perrine 2nd, not first)
    {
        'pdes': '18D',
        'popular_name': 'Perrine-Mrkos',
        'M1': '13.3',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, other',
        'notes': "matched by body — 'second recorded apparition of the short-period Comet Perrine (was not detected in 1902)' = 18D/Perrine-Mrkos; Holetschek H1=14m.6-16m.3 'an apparent underestimate'; V.I h10=14m.3 (van Biesbroeck — nucleus); Big V says 'For the intrinsic brightness we adopt an H10-value smaller by 1m' i.e., 13m.3 — chose Big V's preferred synthesis since Holetschek flagged as underestimate (V1 pattern); periodic — will dedupe with other 18D apparitions; ERRONEOUS Holetschek flagged; page-image proofread vs page 379: confirmed",
        'match_confidence': 'low',
        'bigv_designation_old': '1909 III',
        'bigv_page': '379',
        'ocr_excerpt': "Taking on 2 Aug. m=15m; in September, 14m; 11 Oct., 13m; 20 Nov., 14m, Holetschek obtained H1=14.6 to 16m.3, an apparent underestimate. V.I obtained, according to van Biesbroeck's estimates, h10=14m.3. For the intrinsic brightness we adopt an H10-value smaller by 1m, which is in good agreement with Wolf's observations in September.",
    },
    # 36: 1909 IV - OVERRIDE: 33P/Daniel first apparition (NOT 7P)
    {
        'pdes': '33P',
        'popular_name': 'Daniel',
        'M1': '9.5',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "MANUAL DESIGNATION OVERRIDE — script gave 7P (wrong; 7P is entry 1909 II); body explicitly: 'first recorded apparition of the short period Comet Daniel' = 33P/Daniel; target list 33P peri 1909-11-29 matches body's 6 Dec Daniel discovery; Dubiago y=13.9; V.I y=21 H0=6m.7 (van Biesbroeck); C.A.M. H10=9m.5; chose C.A.M. per sec 3.1; periodic — will dedupe with other 33P apparitions; very high y=21 (unusual); page-image proofread vs page 379-380: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1909 IV',
        'bigv_page': '379',
        'ocr_excerpt': "From A. Dubiago, Erganz. Heft., 4(8), y=13.9; in V.I, from van Biesbroeck et al., y=21, H0=6m.7; in C.A.M., H10=9m.5.",
    },
    # 37: 1910 I - Great January Daylight Comet 1910 A1 (FAMOUS, external check)
    {
        'pdes': '1910 A1',
        'popular_name': 'Great January Comet 1910 (Daylight Comet)',
        'M1': '5.4',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by body — 'Brilliant comet first spotted on 12 Jan. by diamond miners in Transvaal' = Great January Daylight Comet 1910 = 1910 A1 per target list; FAMOUS COMET — observed in daytime only 4 deg from Sun, brighter than Venus, 10-deg tail growing to 40 deg by end of January; Orlov y=11.5 H0=5m.4 h0=6m.3 (van Biesbroeck and others); C.A.M. H10=5m.4; chose C.A.M. per sec 3.1; D1=4'; Smax=0.50; sanity check (external lit): peak m=-5 reported in literature; with M1=5.4, r_peri=0.13, Δ=1.42: m = 5.4 + 5log(1.42) + 10log(0.13) = 5.4 + 0.76 - 8.86 = -2.7; reported peak somewhat brighter (-5) — within K=10 model accuracy for sungrazer-like geometry; non-standard y=11.5; page-image proofread vs page 380-382: confirmed (note: PDF OCR garbled C.A.M. value, page image confirms 5m.4)",
        'match_confidence': 'high',
        'bigv_designation_old': '1910 I',
        'bigv_page': '380',
        'ocr_excerpt': "S.V. Orlov, A.N., 189:4, obtained, from van Biesbroeck and several other observers, y=11.5, H0=5m.4, h0=6m.3; in C.A.M., H10=5m.4. D=4'. Smax=0.50.",
    },
    # 38: 1910 III - Metcalf 1910 P1
    {
        'pdes': '1910 P1',
        'popular_name': "Metcalf's Comet (1910 III)",
        'M1': '5.4',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by name (Metcalf) + Hercules 8 Aug 1910 -> 1910 P1; V.I y=7.1 H0=6m.7 (van Biesbroeck); C.A.M. H10=5m.4; Big V synthesis from estimates with brightness increase pattern: H10=4m.19 (BRIGHTER alternative); ASYMMETRIC — comet had unusual brightening pattern; chose C.A.M. per sec 3.1 (Big V's 4.19 synthesis available as alternate but C.A.M. is preferred); D1=3'.6 in Aug-Sept; non-standard y=7.1; page-image proofread vs page 384-385: confirmed",
        'match_confidence': 'medium',
        'bigv_designation_old': '1910 III',
        'bigv_page': '384',
        'ocr_excerpt': "V.I gave, according to van Biesbroeck, y=7.1, H0=6m.7; in C.A.M., H10=5m.4. Proceeding from estimates that correspond to the increase in brightness... we obtain H10=4m.19.",
    },
    # 39: 1910 IV - 6P/d'Arrest 7th apparition
    {
        'pdes': '6P',
        'popular_name': "d'Arrest's Comet",
        'M1': '10.1',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by body — 'seventh recorded apparition of the short-period Comet d'Arrest' = 6P; Holetschek H1=10m.3 to 13m (from Algerian estimates); C.A.M. H10=10m.1; D1=2'.2-2'.4; chose C.A.M. per sec 3.1; periodic — will dedupe with other 6P apparitions; faint apparition (14m at discovery); page-image proofread vs page 385: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1910 IV',
        'bigv_page': '385',
        'ocr_excerpt': "Holetschek obtained, from the Algerian estimates, H1=10.3 to 13m; in C.A.M., H10=10m.1. D1=2.2 to 2'.4.",
    },
    # 40: 1910 V - 4P/Faye 9th apparition
    {
        'pdes': '4P',
        'popular_name': "Faye's Comet",
        'M1': '9.6',
        'K1': '10.0',
        'source_citation': 'Vsekhsvyatskij 1958, C.A.M.',
        'notes': "matched by body — 'ninth recorded apparition of the short-period Comet Faye' = 4P; Holetschek H1=9m.6-11m.0 (from Dec 1910 estimates); C.A.M. H10=9m.6; Cherednichenko H10(av)=9m.1, H10(max)=7m.6, H10(min)=10m.7; chose C.A.M. per sec 3.1; periodic — will dedupe with other 4P apparitions; D1=1'.2; Smax=0.003; page-image proofread vs page 386: confirmed",
        'match_confidence': 'high',
        'bigv_designation_old': '1910 V',
        'bigv_page': '386',
        'ocr_excerpt': "Holetschek, from estimates for December 1910, found H1=9m.6 to 11m.0; in C.A.M., H10=9m.6. Cherednichenko, Publ. Kiev Obs. 5:102. 1953, obtained H10(av)=9m.1; H10(max)=7m.6; H10(min)=10m.7. D1=1'.2. Smax=0.003.",
    },
]

out_path = r'C:\Users\grfai\documents\0_Dissertation\code\ch 5 comet salience\data\intermediate\agent_work\agent_c_rows.csv'
with open(out_path, 'a', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['pdes','popular_name','M1','K1','source_citation','notes','match_confidence','bigv_designation_old','bigv_page','ocr_excerpt'], quoting=csv.QUOTE_MINIMAL)
    for r in rows:
        w.writerow(r)
print(f'Wrote {len(rows)} rows for chunk 4')
