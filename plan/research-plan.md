# Plán výskumu: spoľahlivá databáza investorov

| | |
|---|---|
| **Stav** | Návrh v1, čaká na schválenie človekom. Kým nie je schválený, pravidlá Z/V/N sa nesmú používať na zber dát. |
| **Dátum** | 2026-10-25 |
| **Súvisiace** | `CLAUDE.md` (pravidlá pre agentov), `data/schema.md` v0.2 (dátová štruktúra) |
| **Rozsah dokumentu** | Plán a metodika. Neobsahuje žiadne záznamy investorov. |

Značky používané v dokumente:

- **[FAKT]**: tvrdenie so zdrojom (zoznam zdrojov v sekcii 15).
- **[HYPOTÉZA]**: odhad pred pilotom, nie nameraný výsledok. Overí sa v pilote.
- **[ROZHODNUTIE]**: metodická voľba s odôvodnením. Môže sa zmeniť po pilote.
- **[OTVORENÉ]**: rozhodnutie, ktoré treba urobiť pred spustením zberu (sekcia 14).

---

## 0. Manažérske zhrnutie

**Cieľ.** Databáza skutočných investorov do súkromných firiem (VC, PE, family
office, angel investori, veľkí súkromní investori). Pri každom investorovi bude
uvedené, do čoho a v akej výške investuje, aký má kapitál a odkiaľ to vieme.
Najdôležitejšia je presnosť zaradenia: každý záznam musí byť investor
s doloženou investíciou, nie firma, ktorá o sebe tvrdí, že investuje.

**Kto do databázy patrí.** Subjekt, ktorý (Z1) má overenú identitu, (Z2) patrí
do sledovaného typu a geografie a (Z3) má aspoň jednu verejne doloženú
investíciu v posledných 24 mesiacoch. Poradcovia, sprostredkovatelia,
crowdfundingové platformy, SPV na jednu transakciu a neaktívne fondy sa
vyraďujú (V1–V8). Hraničné prípady sa neriešia odhadom, ale označia sa ako
nejasné (N1–N6) a rozhodne o nich človek.

**Pilot.** 40 amerických VC investorov vybraných **náhodne s pevným seedom**
z regulačných podaní SEC (Form ADV a Form D), rozvrstvených podľa veľkosti.
Vzorka teda neobsahuje iba známe fondy z pamäti AI. USA sú vhodné preto, že
existuje verejný register, z ktorého sa dá zostaviť výberový rámec a overiť
identita. Nevýhodou je, že výsledky nemožno priamo preniesť na Európu, family
office ani angel investorov.

**Overovanie.** Každý údaj má URL a doslovnú citáciu. Skript automaticky
overí, či sa citácia na stránke naozaj nachádza. Nezávislý kontrolný agent
potom bez znalosti zdôvodnenia prvého agenta posúdi, či zdroj tvrdenie
podporuje. Nakoniec človek ručne skontroluje všetkých 40 záznamov pole po poli.

**Meranie.** Presnosť zaradenia, presnosť každého poľa, miera vymyslených
zdrojov, úplnosť a miera „falošne prázdnych“ polí, teda údajov, ktoré AI
neuviedla, hoci verejne existujú. Pri n = 40 sa uvádzajú aj 95 % intervaly
spoľahlivosti, pretože bodový odhad sám osebe zavádza.

**Očakávania [HYPOTÉZA].** Identita, krajina a web takmer vždy a správne.
Doložená investícia v okne asi pri 75–85 % zaradených. Ticket size a AUM
verejne len pri menšine investorov (približne 30–50 %). Disponibilný kapitál
takmer nikdy. Databáza bude spoľahlivá v otázke „kto investuje a do čoho“,
ale finančné ukazovatele budú pri mnohých investoroch neúplné. Treba to
otvorene komunikovať a nedopĺňať odhadmi.

**Rozsah.** Podľa ročenky NVCA bolo v USA na konci roka 2025 približne 2 984 VC
firiem [FAKT, overiť v primárnom zdroji]. Globálny počet relevantných
investorov sa odhadne postupom v sekcii 11. Spoľahlivé verejné globálne číslo
neexistuje.

**Náklady.** Namerajú sa v pilote na jeden záznam (tokeny, vyhľadávania, čas
človeka). Na škálovanie sa použije model fixných a variabilných nákladov
(sekcia 12). Pred pilotom predpokladám, že dominantnou položkou bude čas
človeka na kontrolu, nie API [HYPOTÉZA].

**Rozhodnutie po pilote.** Pokračovať, iba ak presnosť zaradenia je aspoň
95 %, žiadny vymyslený zdroj neprejde do `data/verified/` a povinné polia majú
presnosť aspoň 95 % (sekcia 10.4).

**Hlavné obmedzenie.** Termín odovzdania je 2026-10-30. Pilot je navrhnutý na
približne 5 pracovných dní. Ak sa nestihne ručná kontrola všetkých 40
záznamov, zmenší sa vzorka (náhradný postup v sekcii 13), metodika sa nemení.

---

## 1. Cieľ a rozsah

### 1.1 Účel databázy

Databáza má slúžiť ako spoľahlivý zoznam investorov, ktorý sa dá použiť na
oslovovanie investorov (napr. startupmi alebo poradcami pri fundraisingu) bez
toho, aby používateľ musel každý záznam znova overovať. Z toho vyplýva:

- Chybne zaradený subjekt (napr. poradca namiesto investora) je závažnejšia
  chyba než chýbajúci investor. Preto sa optimalizuje **presnosť** pred
  **úplnosťou** [ROZHODNUTIE].
- Každý údaj musí byť dohľadateľný k zdroju, aby si ho používateľ mohol
  overiť sám.

### 1.2 Cieľové skupiny

| Typ (`investor_type`) | V zadaní | V pilote | Poznámka |
|---|---|---|---|
| VC fond / VC firma (`vc`) | áno | **áno** | predmet pilotu |
| PE fond (`pe`) | áno | nie | neskoršia fáza, iné finančné ukazovatele (buyout) |
| Family office (`family_office`) | áno | nie | nízka transparentnosť; v USA nie sú v Form ADV (výnimka pre family office) |
| Angel investor (`angel`) | áno | nie | fyzické osoby, ochrana osobných údajov (sekcia 14, O3) |
| Veľký súkromný investor (`private_investor`) | áno | nie | rovnaké ako pri angel investoroch |
| Corporate VC (`cvc`) | **nie** | nie | samostatná kategória, pozri 1.4 |

### 1.3 Čo je investor a čo nie

Investor je subjekt, ktorý **vlastným alebo spravovaným kapitálom** nadobúda
podiel (alebo nástroj konvertibilný na podiel) v súkromnej spoločnosti a robí
to opakovane ako súčasť svojej činnosti.

Do databázy nepatria: investiční poradcovia bez vlastného kapitálu,
sprostredkovatelia a placement agenti, crowdfundingové a syndikačné platformy
(sprostredkúvajú, ale neinvestujú), správcovia fondov pre fondy (fund
administrators), banky poskytujúce úvery, akcelerátory bez doloženej vlastnej
investície a jednorazové investičné vehikulá (SPV). Pri SPV sa zaradí
investor, ktorý ho riadi, ak spĺňa pravidlá. Konkrétne pravidlá sú v sekcii 2.

### 1.4 Corporate venture capital (CVC)

**Odporúčanie [ROZHODNUTIE]:** CVC evidovať ako **samostatnú kategóriu**
(`investor_type = cvc`, v schéme už existuje), ale **nezaradiť ho do pilotu**
ani do prvej globálnej vlny.

Dôvody:

- Zadanie CVC nemenuje. Jeho zaradenie je rozšírenie rozsahu, nie splnenie
  zadania.
- CVC často investuje z bilancie materskej spoločnosti. Ukazovatele `aum`
  a `fund_size` preto často neexistujú alebo nie sú porovnateľné s VC.
- CVC nie je v amerických podaniach Form ADV, takže by vo výberovom rámci
  pilotu chýbal systematicky. Jeho prítomnosť vo vzorke by bola náhodná.
- Pre startup je však CVC relevantný investor, preto ho neodporúčam vyradiť
  natrvalo.

Dôsledky: vo výberovom rámci pilotu sa CVC vyskytne iba výnimočne (ak má
samostatnú správcovskú spoločnosť registrovanú ako adviser). Taký prípad sa
eviduje ako `cvc` a vo výsledkoch sa vykáže zvlášť. Do metrík pilotu pre VC sa
nezapočíta.

### 1.5 Jednotka záznamu: investičná firma, správca, fond, materská spoločnosť

**[ROZHODNUTIE]** Jeden záznam = **investičná firma**, teda subjekt, ktorý
navonok vystupuje ako investor a rozhoduje o investíciách (napr. „Acme
Ventures“). Ostatné entity sa evidujú v `related_entities` a `fund_size`:

| Entita | Príklad | Kde v schéme |
|---|---|---|
| Investičná firma (značka) | Acme Ventures | samostatný záznam (`name`) |
| Správcovská spoločnosť (adviser, management company) | Acme Ventures Management LLC | `legal_entity`, `related_entities` (`manager`) |
| Jednotlivé fondy | Acme Ventures Fund III, L.P. | `fund_size[]`, `related_entities` (`fund`) |
| General partner | Acme Ventures GP III, LLC | `related_entities` (`other`) |
| Materská spoločnosť | napr. banka alebo holding nad firmou | `related_entities` (`parent`) |

Dôvod: používateľ oslovuje firmu, nie právnickú osobu fondu. Regulačné
podania sú však na úrovni správcu (Form ADV) alebo fondu (Form D). Tieto
entity sa preto musia spájať pod jednu firmu (sekcia 6).

---

## 2. Pravidlá zaradenia, vyradenia a nejasných prípadov

Identifikátory sú stabilné. Pri zmene pravidla sa pridá nové ID, staré sa
nemení ani neprečísluje. V poli `inclusion.rule` sa uvádzajú všetky splnené
pravidlá, napr. `"Z1+Z2+Z3"`, `"V4"` alebo `"N2"`.

### 2.1 Časové okno aktivity

**[ROZHODNUTIE]** Investor je **aktívny**, ak má aspoň jednu doloženú
investíciu s dátumom v intervale:

> **od 2024-10-25 do 2026-10-25 vrátane** (24 mesiacov pred referenčným
> dátumom pilotu)

Referenčný dátum je deň zostavenia výberového rámca. Pri ďalších vlnách zberu
sa okno posúva so zberom a referenčný dátum sa zapíše do záznamu výberu.

Prečo 24 mesiacov:

- Malé VC fondy robia niekoľko nových investícií ročne a nie všetky oznamujú.
  Pri 12 mesiacoch by sa vyradili aj aktívni investori, ktorí len neoznámili
  posledný deal.
- 36 a viac mesiacov by prepustilo fondy, ktoré už iba spravujú portfólio
  a nové investície nerobia. Pre používateľa, ktorý hľadá investora, sú to
  falošne pozitívne záznamy.
- 24 mesiacov pokrýva dva ročné cykly a je to bežná hranica „aktívneho
  investora“ v praxi. Toto tvrdenie nemám doložené zdrojom, je to pracovný
  predpoklad.
- Okno sa po pilote vyhodnotí: koľko zaradených investorov by vypadlo pri
  12 mesiacoch a koľko pribudlo pri 36 (metrika M13).

Pravidlá pre dátumy:

- Rozhoduje **dátum investície**. Ak nie je známy, použije sa **dátum
  oznámenia** (`date_kind = announcement`). Oznámenie sa zvyčajne časovo
  približuje investícii, preto je ako dôkaz aktivity prijateľné.
- Ak je známy iba mesiac alebo rok, schéma to nevie zachytiť (nedostatok S2,
  sekcia 14). Do rozhodnutia: `deal_date = null`, presný text zo zdroja
  v citácii, prípad → **N4**.
- Investícia z portfólia na webe bez dátumu nedokladá aktivitu v okne →
  **N6**, pokiaľ sa nenájde iný datovaný zdroj.
- Staršie investície (pred začiatkom okna) sa zaznamenajú v `deals`
  s dátumom. Neprispievajú k Z3, ale slúžia na overenie identity, zamerania
  a na pravidlo V4.
- Získanie kapitálu do nového fondu (napr. Form D) **nie je investícia** do
  firmy. Dokladá fundraising, nie investičnú aktivitu (pozri N2).

### 2.2 Pravidlá zaradenia (všetky musia byť splnené)

| ID | Pravidlo | Minimálny dôkaz |
|---|---|---|
| **Z1** | **Overená identita.** Je jasné, o ktorý subjekt ide, a dá sa odlíšiť od podobne pomenovaných. | Aspoň jedno: oficiálny web investora, alebo záznam v regulačnom či firemnom registri (pre USA záznam Form ADV s číslom CRD alebo podanie Form D s CIK). |
| **Z2** | **Typ a geografia v rozsahu.** Subjekt je investor sledovaného typu (pre pilot `vc`) so sídlom v sledovanej krajine (pre pilot USA). | Typ: vlastné vyjadrenie na webe alebo typ fondu v regulačnom podaní, nie iba zaradenie v adresári (úroveň 3). Sídlo: register alebo web. |
| **Z3** | **Doložená investícia v okne.** Aspoň jedna investícia s dátumom v okne 2.1. | Zdroj úrovne 1 alebo 2, v ktorom je menovaný investor, financovaná firma a ich súvislosť (`CLAUDE.md` sekcia 5). Dôkaz iba z úrovne 3 nestačí → N3. |

Doplňujúce zásady:

- **Investor bez webu** môže splniť Z1 cez register a Z3 cez oznámenie
  financovanej firmy alebo médium. Chýbajúci web sám osebe nie je dôvod na
  vyradenie, ale `website` bude `null` so záznamom v `notes`.
- **Nový fond** existujúcej firmy je súčasť záznamu firmy (`fund_size`),
  nie nový investor. Aktivitu dokladajú investície firmy z ktoréhokoľvek
  jej fondu.
- **Všeobecné tvrdenie nie je aktivita.** Veta „investujeme do seed fázy
  fintech firiem“ dokladá **zameranie** (`stages`, `sectors`), nikdy nie Z3.
  Z3 dokladá iba konkrétna transakcia.

### 2.3 Pravidlá vyradenia (stačí jedno)

| ID | Pravidlo | Príklad |
|---|---|---|
| **V1** | Po vykonaní celého vyhľadávacieho protokolu (sekcia 4.3) sa nenašla **žiadna** doložená investícia, ani mimo okna. | firma má web „investment“, ale žiadne portfólio ani transakciu |
| **V2** | Poskytovateľ služieb, nie investor: poradca, sprostredkovateľ, placement agent, fund administrator, crowdfundingová alebo syndikačná platforma. | platforma, cez ktorú investujú iní |
| **V3** | Akcelerátor alebo inkubátor bez doloženej **vlastnej** investície (iba program, poplatky, granty). | akcelerátor, ktorý len organizuje program |
| **V4** | Neaktívny investor: posledná doložená investícia je staršia ako okno a nie sú dôkazy novšej aktivity, alebo zdroj úrovne 1–2 uvádza ukončenie činnosti. | fond vo fáze správy portfólia, firma oznámila koniec |
| **V5** | Jednorazové vehikulum (SPV) alebo samostatný fond firmy, ktorá je už v databáze alebo bude evidovaná. Záznam sa spojí do záznamu firmy. | „Acme SPV 12, LLC“ |
| **V6** | Duplicita. Subjekt je už v databáze pod iným názvom. Spája sa podľa sekcie 6. | premenovaná firma |
| **V7** | Mimo rozsahu tejto vlny: iný typ (napr. hedge fund, buyout PE v pilote VC) alebo iná krajina sídla. | |
| **V8** | Subjekt zanikol alebo ho nemožno identifikovať a nie je dôvod predpokladať, že ešte existuje (napr. web nefunkčný a žiadna zmienka po začiatku okna). | |

Vyradené záznamy sa **nemažú**. Zostávajú v `data/raw/` s
`inclusion.decision = vyradeny`, aby bolo vidieť, koľko kandidátov vypadlo
a prečo (metrika M14).

### 2.4 Nejasné prípady (rozhodne človek)

| ID | Situácia | Postup |
|---|---|---|
| **N1** | Nejasná identita: nedá sa spoľahlivo spojiť fond, správca a firma, alebo existuje viac podobných subjektov. | Človek rozhodne spojiť, oddeliť, alebo vyradiť podľa V8. |
| **N2** | Nový fond alebo nová firma: doložený fundraising (napr. Form D v okne), ale zatiaľ žiadna investícia. | Nezaradiť do overenej databázy. Eviduje sa ako kandidát na opakovanú kontrolu po 6 mesiacoch. |
| **N3** | Investícia doložená iba zdrojom úrovne 3 (adresár, agregátor). | Pokúsiť sa dohľadať pôvodný zdroj. Ak sa nenájde, nezaradiť. |
| **N4** | Investícia bez presného dátumu, alebo len s mesiacom či rokom. | Ak z citácie jednoznačne vyplýva dátum v okne (napr. „v marci 2026“), človek môže uznať Z3. Inak N4 zostáva. |
| **N5** | Rozpor v type investora alebo vo vzťahu k investícii (napr. zdroje uvádzajú VC aj growth PE, alebo nie je jasné, či investovala firma, alebo jej partner súkromne). | Človek rozhodne typ, prípadne V7. |
| **N6** | Iba portfólio na webe bez dátumov investícií. | Hľadať datované oznámenie investície z portfólia. Ak sa nenájde, N6 zostáva a investor nie je aktívny. |

Agent smie navrhnúť rozhodnutie (`decided_by = agent`), ale do
`data/verified/` sa záznam dostane iba po rozhodnutí človeka.

---

## 3. Pilotná vzorka: americké VC fondy

### 3.1 Kritické posúdenie vhodnosti

**Výhody:**

- **Existuje verejný register.** Správcovia VC fondov podávajú Form ADV ako
  registrovaní poradcovia alebo ako tzv. exempt reporting advisers [FAKT 1, 2].
  Fondy pri získavaní kapitálu podávajú Form D, v ktorom sa uvádza typ fondu
  „Venture Capital Fund“ [FAKT 4]. Výberový rámec sa preto nemusí zostaviť
  z pamäti AI ani z platených databáz.
- **Primárne zdroje pre identitu a veľkosť fondov.** Form ADV obsahuje pre
  každý súkromný fond samostatnú sekciu 7.B.(1) [FAKT 3]. Podľa sekundárnych
  zdrojov obsahuje aj typ fondu a hrubú hodnotu aktív [FAKT 3, overiť].
- **Najväčší a najtransparentnejší VC trh.** Investície sa často oznamujú
  tlačovými správami a v médiách, v angličtine.
- **Kontrola veľkosti populácie.** Ročenka NVCA uvádza počet VC firiem
  [FAKT 7], takže sa dá porovnať veľkosť rámca s nezávislým číslom.

**Nevýhody a obmedzenia:**

- **Reprezentatívnosť.** Výsledky platia pre americké VC. Neplatia pre
  Európu (iné registre, jazyky, nižšia transparentnosť), PE, family office
  ani angel investorov. Pilot meria metodiku na **najľahšom** segmente, preto
  bude presnosť pri iných segmentoch pravdepodobne nižšia.
- **Regulačné podania nie sú úplný zoznam VC.** Chýbajú: CVC investujúce
  z bilancie, family office, angel investori, niektoré malé fondy a správcovia
  využívajúci štátne výnimky. Form D má navyše vlastné medzery v podávaní
  [FAKT 5].
- **Šum v rámci.** Form D s typom „Venture Capital Fund“ podávajú aj SPV na
  jednu transakciu a viaceré fondy jednej firmy. Napríklad tretia strana
  uvádza za Q3 2026 869 nových VC fondov od 642 firiem [FAKT 6, úroveň 3].
  Bez deduplikácie by vzorku tvorili fondy, nie investori.
- **Rozdiel oproti zadaniu.** E-mail spomína „napríklad VC fondy v jednej
  krajine“. USA tomu zodpovedajú, ale pri tisíckach subjektov nie je možné
  overiť celú populáciu. Preto výberová vzorka a odhad, nie úplný zoznam.
- **Technické obmedzenie.** Z cloudového prostredia, v ktorom vznikol tento
  plán, boli `sec.gov` a `nvca.org` nedostupné (proxy 403/DNS). Údaje SEC
  treba stiahnuť z lokálneho počítača alebo upraviť sieťové pravidlá
  prostredia [OTVORENÉ O8].

**Záver [ROZHODNUTIE]:** Americké VC sú vhodné na otestovanie **metodiky**
(pravidlá, dôkazy, overovanie, meranie), pretože existuje verejný výberový
rámec. Nie sú vhodné na odhad presnosti pre celý svet. Výsledky sa tak budú
aj prezentovať.

### 3.2 Výberový rámec

Rámec sa zostaví z dvoch verejných zdrojov SEC a spojí sa na úroveň
investičnej firmy (sekcia 1.5).

| | Form ADV | Form D |
|---|---|---|
| Účel | registrácia a hlásenie poradcov (správcov) | oznámenie o výnimke z registrácie ponuky cenných papierov |
| Úroveň | správca (adviser), fondy v Schedule D 7.B.(1) | jednotlivý fond alebo vehikulum (issuer) |
| Kto podáva | registrovaní poradcovia (RIA) a exempt reporting advisers (ERA), ERA iba vybrané položky [FAKT 2] | emitent, ktorý využíva Reg D (504, 506(b), 506(c)) alebo 4(a)(5) [FAKT 4] |
| Čo dáva | identita (CRD, SEC číslo), sídlo, zoznam fondov, typ fondu, hodnota aktív fondu [overiť] | názov fondu, typ fondu (VC/PE/hedge/iné), súvisiace osoby, výška ponuky, dátum |
| Formát | mesačné súbory (prehľad), štvrťročný archív s detailmi vrátane Schedule D [FAKT 2, overiť] | štvrťročné dátové sady z XML časti formulára [FAKT 4] |
| Obmedzenia | nezachytí CVC, family office, angel investorov, správcov mimo SEC | podanie nemusí byť úplné [FAKT 5]; zachytí fundraising, nie investície; veľa SPV |
| Použitie v pláne | **hlavný rámec** | doplnenie rámca o firmy, ktoré nie sú v ADV, a dôkaz nových fondov (N2) |

Postup zostavenia (skript `scripts/build_frame.py`):

1. Stiahnuť najnovší dostupný štvrťročný archív Form ADV a dátové sady
   Form D za obdobie okna (8 štvrťrokov). Zaznamenať URL, dátum stiahnutia
   a SHA-256 každého súboru do `data/raw/_frame/sources.csv`.
2. **ADV filter:** poradcovia so sídlom v USA, ktorí majú aspoň jeden
   súkromný fond označený ako venture capital fund, alebo ktorí sa
   spoliehajú na výnimku pre poradcov VC fondov. Presný názov polí sa overí
   v dokumentácii dátovej sady pred napísaním filtra.
3. **Form D filter:** podania typu Pooled Investment Fund s typom
   „Venture Capital Fund“ s dátumom v okne. Vyradiť zrejmé SPV podľa vzorov
   názvu („SPV“, „Series“ s číslom pri platformách) a podľa známych
   syndikačných platforiem ako súvisiacich osôb. Zoznam vzorov sa uloží
   do skriptu a do záznamu výberu.
4. **Deduplikácia a spojenie** (podrobne v sekcii 6): fondy z Form D sa
   priradia k správcovi z ADV cez súvisiace osoby, adresu a normalizovaný
   názov. Automaticky iba pri zhode identifikátora alebo presnej zhode
   normalizovaného názvu a adresy. Ostatné párovania sa označia na kontrolu.
5. **Výsledok:** `data/raw/_frame/frame.csv`, jeden riadok = jedna
   kandidátska investičná firma, so stabilným `frame_id` (CRD, ak existuje,
   inak `D-<CIK>`), zdrojom (ADV / D / oboje), veľkostnou triedou a
   identifikátormi.
6. **Doplnenie chýbajúcich subjektov:** porovnať rámec so zoznamom
   členov NVCA, ak je verejne dostupný (neoverené, krok F0). Nie je to výberový zdroj, iba kontrola pokrytia: aký podiel
   členov NVCA rámec obsahuje (metrika M15). Chýbajúce subjekty sa do vzorky
   pilotu **nepridávajú**, aby sa nenarušila náhodnosť. Iba sa vykážu.

### 3.3 Výber 40 kandidátov

**Stratifikácia [ROZHODNUTIE].** Bez stratifikácie by vzorku tvorili najmä
malé fondy, ktorých je najviac. Tak by sa nepreverili veľké firmy s viacerými
fondmi a entitami, ktoré sú najťažšie na deduplikáciu. Vrstvy podľa súčtu
hodnoty aktív fondov z Form ADV:

| Vrstva | Kritérium | Počet vo vzorke |
|---|---|---|
| S1 mikro | < 50 mil. USD | 9 |
| S2 malé | 50–250 mil. USD | 9 |
| S3 stredné | 250 mil. – 1 mld. USD | 9 |
| S4 veľké | > 1 mld. USD | 9 |
| S5 iba Form D | firmy bez záznamu v ADV | 4 |
| **Spolu** | | **40** |

Hranice vrstiev sú pracovný predpoklad. Ak niektorá vrstva v rámci obsahuje
menej ako 30 firiem, hranice sa upravia pred losovaním a úprava sa
zdokumentuje. Rovnomerné rozdelenie (9 v každej vrstve) znamená, že vzorka
**nie je proporcionálna**. Pri výpočte celkovej presnosti za populáciu sa
použijú váhy vrstiev (podiel vrstvy v rámci). Neváhované výsledky sa vykážu
po vrstvách.

**Algoritmus (skript `scripts/sample.py`):**

1. Načítať `frame.csv` a zoradiť podľa `frame_id` (stabilné poradie).
2. Pre každú vrstvu: `random.Random(SEED).sample(zoznam_id_vrstvy, k)`
   v Pythone so seedom **`20261025`** [ROZHODNUTIE].
3. Rovnakým spôsobom vylosovať **rezervu** 3 kandidátov na vrstvu (spolu 15).
   Rezerva sa použije iba vtedy, ak sa kandidát ukáže ako mimo rámca (napr.
   nejde o investičnú firmu, V5/V6/V7 už pri zostavení). Každá výmena sa
   zdokumentuje.
4. Vylosovať **kalibračnú sadu** 5 kandidátov **mimo** vzorky a rezervy.
   Na nej sa ladia pokyny agentov (fáza F3), aby sa pokyny neprispôsobili
   záznamom, na ktorých sa meria presnosť.
5. Uložiť `data/raw/_frame/sample.csv` (`frame_id`, vrstva, poradie,
   rola: vzorka / rezerva / kalibrácia) a `data/raw/_frame/sample-log.md`
   s verziou skriptu (git commit), SHA-256 rámca, seedom a dátumom.

**Reprodukovateľnosť verzus reprezentatívnosť.** Rovnaký rámec, seed a skript
dajú vždy rovnakú vzorku, takže výber je **reprodukovateľný**. Vzorka je
**reprezentatívna iba pre rámec**, teda pre VC firmy viditeľné v podaniach
SEC, nie pre všetkých amerických VC investorov. Rozdiel medzi rámcom
a populáciou sa odhadne cez pokrytie (M15) a porovnanie s číslom NVCA.

### 3.4 Evidencia celého výberového procesu

| Krok | Čo sa eviduje | Kde |
|---|---|---|
| Zdroje rámca | URL, dátum stiahnutia, SHA-256 | `data/raw/_frame/sources.csv` |
| Filtre | presné podmienky a počty pred a po každom filtri | `data/raw/_frame/sample-log.md` |
| Deduplikácia | spojené páry, dôvod, automaticky/ručne | `data/raw/_frame/merges.csv` |
| Losovanie | seed, verzia skriptu, výsledné ID | `sample.csv`, `sample-log.md` |
| Výmeny z rezervy | ktorý kandidát, za ktorého, dôvod | `sample-log.md` |
| Výsledok každého kandidáta | zaradený / vyradený / nejasný + pravidlo | `data/raw/<id>.json` (`inclusion`) |

Vyradení a nejasní kandidáti zostávajú v súboroch a počítajú sa do metrík.
Nevyberajú sa „náhradníci“ za vyradených, pretože podiel vyradených je
sám osebe výsledok (koľko subjektov z registra nie sú skutoční investori).

---

## 4. Metodika vyhľadávania a overovania

### 4.1 Zásady

Platia pravidlá `CLAUDE.md` sekcie 2–6 (zdroje, hierarchia, citácie, zákaz
domýšľania). Tento plán ich neopakuje a dopĺňa iba pracovný postup.

### 4.2 Poradie zdrojov podľa poľa

| Pole | 1. voľba | 2. voľba | Nesmie byť jediný dôkaz |
|---|---|---|---|
| identita, `legal_entity` | Form ADV, Form D, obchodný register štátu | oficiálny web | adresáre (úroveň 3) |
| `investor_type` | web (o nás), typ fondu v ADV/Form D | médium | adresár |
| `country` | register | web | |
| `website` | odkaz z registra alebo zhoda domény s e-mailom/kontaktom | médium | výsledok vyhľadávača bez overenia |
| `sectors`, `stages`, `geography` | web investora (investičná stratégia) | rozhovory, médium | adresár |
| `ticket_size` | web investora | médium s citáciou partnera | odvodenie z jedného dealu (zakázané, `CLAUDE.md` 6) |
| `fund_size` | oznámenie investora o uzavretí fondu, ADV (s definíciou) | médium | Form D „total offering amount“ bez kontextu (je to cieľová ponuka, nie veľkosť fondu) |
| `aum` | ADV (pre RIA regulačné AUM), web investora | médium | súčet veľkostí fondov (zakázané, sekcia 5.3) |
| `deployable_capital` | vyjadrenie investora | médium | výpočet z iných údajov |
| `deals` | oznámenie firmy, oznámenie investora | médium úrovne 2 | agregátor |

### 4.3 Vyhľadávací protokol pre jeden záznam

Pevné poradie, aby sa dalo zmerať, koľko krokov treba, a aby sa nehľadalo
donekonečna:

1. Načítať údaje z rámca (názov, CRD/CIK, adresa, fondy). To sú fakty
   z registra, agent ich preberá, nevymýšľa.
2. Nájsť oficiálny web a overiť, že patrí tomuto subjektu (zhoda názvu,
   adresy alebo mien partnerov s registrom).
3. Prečítať na webe stránky o firme, stratégii, portfóliu, tíme a novinkách.
4. Vyhľadať transakcie v okne (napr. `"<názov>" led seed`, `"<názov>"
   participated Series A`, `"<názov>" invests`) a overiť ich v oznámení
   firmy alebo investora.
5. Vyhľadať veľkosť fondov, AUM a ticket size.
6. Vyhľadať dôkazy neaktivity alebo zmien (zánik, premenovanie, akvizícia).
7. **Zastavovacie pravidlo:** najviac 15 vyhľadávaní a 25 otvorených stránok
   na záznam [ROZHODNUTIE, upraví sa po kalibrácii]. Ak sa údaj nenájde,
   `value = null` a do `notes` sa zapíšu použité dopyty.

### 4.4 Problémové situácie

| Situácia | Postup |
|---|---|
| Nefunkčný odkaz | Jeden opakovaný pokus. Potom archívna kópia (Wayback Machine). Ak existuje, použije sa archívna URL a v `notes` je pôvodná URL. Ak nie, dôkaz sa nepoužije a pole má iný dôkaz, alebo `nedolozene`. |
| Dokument za prihlásením alebo platbou | Nepoužíva sa (`CLAUDE.md` 3). V `notes` sa uvedie, že existuje, ale nie je verejný. |
| PDF alebo tabuľka | Citácia z textu PDF, `locator` = strana alebo tabuľka. Ak PDF nemá textovú vrstvu, údaj sa označí na ručnú kontrolu. |
| Protichodné údaje | `status = v_rozpore`, všetky tvrdenia zostávajú v `evidence` (`CLAUDE.md` 4). Rozpor sa nerieši výberom. |
| Chýbajúci údaj | `value = null`, `status = nedolozene`, v `notes` dopyty a navštívené stránky. |
| Stránka sa zmenila po prečítaní | Kontrolný skript ukladá text stránky a SHA-256 do cache. Pri rozdiele sa rozhoduje podľa uloženej verzie a zmena sa zaznamená. |

### 4.5 Automatická kontrola citácií

Skript `scripts/check_evidence.py` pre každý dôkaz:

1. stiahne URL a zaznamená HTTP stav,
2. extrahuje text (HTML alebo PDF), znormalizuje medzery, úvodzovky a pomlčky,
3. hľadá citáciu presne a potom s toleranciou iba na tieto normalizácie,
4. uloží výsledok do `qa` (`urls_ok`, `quotes_found`, `issues`) a text
   stránky do `data/cache/` (mimo gitu, `.gitignore`) so SHA-256 v zázname.

Skript overuje iba to, že **citácia na stránke existuje**. Neoveruje, či
citácia tvrdenie **podporuje**. To robí kontrolný agent a človek (sekcia 8).

---

## 5. Rozsah údajov a ich priorita

### 5.1 Priority polí

| Priorita | Polia | Podmienka pre `data/verified/` |
|---|---|---|
| **Povinné** | `name`, identita (`legal_entity` alebo identifikátor z registra), `investor_type`, `country`, aspoň jeden `deal` v okne, `inclusion` | Musia byť `dolozene` a ručne overené. Inak sa záznam nepresunie. |
| **Dôležité** | `website`, `sectors`, `stages`, `geography`, `ticket_size`, `fund_size`, `aum` | Môžu byť `null`. Ak sú vyplnené, musia byť ručne overené. |
| **Doplnkové** | `deployable_capital`, `alt_names`, `domains`, `related_entities`, `round_amount`, `investor_role`, staršie `deals` | Môžu byť `null`. Ak sú vyplnené, overuje sa ich súlad so zdrojom. |

Doplnkové polia `alt_names`, `domains` a `related_entities` sú
kľúčové pre deduplikáciu. Pre presun do `verified` nie sú povinné, ale pri
ručnej kontrole sa vyplnia, ak sú zrejmé zo zdrojov.

### 5.2 Definície ukazovateľov

| Pole | Čo znamená | Mena a obdobie | Neistota |
|---|---|---|---|
| `investor_type` | prevažujúci typ činnosti podľa vlastného vyjadrenia a regulačného podania | – | pri rozpore N5 |
| `country` | krajina sídla správcu (nie krajina investícií) | – | – |
| `sectors` | sektory podľa formulácie zdroja; mapovanie na jednotnú taxonómiu je otvorené (S4) | `as_of` podľa zdroja | marketingové texty bývajú široké („technológie“) |
| `stages` | fázy podľa enum v schéme, mapované z textu zdroja | – | „early stage“ sa mapuje iba ak je zrejmé, či ide o seed alebo Series A; inak `other` s poznámkou |
| `geography` | kam investor investuje | – | – |
| `ticket_size` | typická výška **jednej** investície investora (prvá investícia, ak to zdroj rozlišuje) | mena zdroja, rok zdroja | nikdy z jedného dealu ani z výšky kola |
| `fund_size` | veľkosť konkrétneho fondu; `definition` rozlišuje **cieľovú**, **uzavretú (záväzky)** a **regulačnú hrubú hodnotu aktív** | mena, `vintage`, `as_of` | hrubá hodnota aktív z ADV ≠ záväzky investorov fondu |
| `aum` | kapitál v správe tak, ako ho uvádza zdroj, s definíciou (regulačné AUM, vlastné vyjadrenie) | mena, `as_of` | rôzne definície → často `v_rozpore` |
| `deployable_capital` | kapitál dostupný na nové investície („dry powder“) podľa vyjadrenia investora | mena, `as_of` | takmer nikdy verejný |
| `deals` | doložená investícia (sekcia 2.1) | `round_amount` = **celé kolo** | podiel investora sa nezisťuje |

### 5.3 Zamedzenie dvojitému započítaniu

- `aum` sa **nikdy** nevypočíta súčtom `fund_size` a súčet sa ani neuloží
  ako hodnota. Ak zdroj AUM neuvádza, `aum = null`.
- Pri agregátoch za databázu (napr. „celkový kapitál VC v USA“) sa
  započíta **iba** `aum` na úrovni firmy. Fondy sa nepripočítavajú, pretože
  sú už v AUM firmy.
- Fond, ktorý je v Form D aj v ADV, je jeden fond. Páruje sa podľa
  identifikátora fondu z ADV a názvu (sekcia 6).
- `round_amount` sa nikdy nesčítava do kapitálu investora.

### 5.4 Celkový investičný kapitál zo zadania

Zadanie požaduje „celkový investičný kapitál“. Odporúčanie a možnosti sú
v sekcii 14 (O1). Do rozhodnutia sa v pilote zbiera `aum` aj `fund_size`
oddelene, takže sa neskôr dá rozhodnúť bez nového zberu.

---

## 6. Deduplikácia a identita

### 6.1 Kľúče na porovnanie

| Kľúč | Zdroj | Sila |
|---|---|---|
| CRD číslo, SEC číslo poradcu | Form ADV | jednoznačný pre správcu |
| CIK | Form D (EDGAR) | jednoznačný pre emitenta (fond), nie pre firmu |
| identifikátor súkromného fondu | ADV 7.B.(1) [FAKT 3] | jednoznačný pre fond v rámci ADV |
| normalizovaná doména | web | silný (pozor na zdieľané domény skupín) |
| normalizovaný názov | všetko | slabý |
| adresa sídla | registre | doplnkový |

Normalizácia názvu: malé písmená, bez interpunkcie, bez právnych foriem
(LLC, L.P., Inc.), bez slov „Management“, „Partners“, „Capital“ až po
porovnaní oboch verzií, bez čísiel fondov (I–XX, 1–20) a slov „Fund“,
„Opportunity“, „Growth“ na konci názvu.

**Nedostatok schémy (S1):** schéma nemá pole pre identifikátory z registrov
(CRD, CIK). Do rozhodnutia sa uvádzajú v `legal_entity.value` a v
`related_entities[].name`. Pre skript je to nespoľahlivé (sekcia 14).

### 6.2 Čo sa rieši automaticky a čo človek

| Prípad | Rozhodnutie |
|---|---|
| Rovnaké CRD alebo rovnaká normalizovaná doména | automatické spojenie, zapíše sa do `merges.csv` |
| Fond z Form D, ktorého súvisiaca osoba alebo adresa zodpovedá správcovi z ADV, a normalizovaný názov sa zhoduje | automatické priradenie fondu k firme |
| Podobný názov bez zhody identifikátora (podobnosť nad prahom) | kandidát na duplicitu (`qa.duplicate_candidates`), **rozhodne človek** |
| Premenovanie (starý a nový názov) | človek; starý názov do `alt_names`, dôkaz premenovania v `notes` |
| Akvizícia jednej firmy druhou | človek; ak nadobúdateľ pokračuje pod vlastnou značkou, spojenie. Inak dva záznamy prepojené cez `related_entities`. |
| Odštiepenie tímu do novej firmy | vždy dva záznamy; nová firma nedostáva históriu investícií starej |
| Viac značiek pod jedným správcom | človek; samostatné záznamy, ak značky investujú samostatne (vlastná stratégia a tím), inak jeden záznam s `alt_names` |

Žiadne automatické spojenie sa nerobí iba na základe podobnosti názvu
(`CLAUDE.md` 7).

---

## 7. Pracovný postup a architektúra

### 7.1 Fázy

Každá fáza má výstup uložený v repozitári. Ďalšia fáza nadväzuje na súbory,
nie na pamäť konverzácie, preto sa dá kedykoľvek pokračovať bez opakovania
predchádzajúcich krokov.

#### F0: Príprava a desk research
- **Cieľ:** schválený plán a prístup k dátam.
- **Kroky:** schváliť plán a otvorené rozhodnutia (sekcia 14); overiť
  v primárnych zdrojoch fakty označené „overiť“; zabezpečiť stiahnutie dát
  SEC (O8).
- **Výstupy:** `plan/research-plan.md` so stavom „schválený“, doplnené
  zdroje v sekcii 15.
- **Hotové, keď:** všetky otvorené rozhodnutia potrebné pre F1–F6 sú
  rozhodnuté a zapísané.
- **Riziká:** fakty z druhej ruky sa ukážu ako nepresné → upraviť plán
  pred F1, nie počas zberu.

#### F1: Výberový rámec
- **Cieľ:** `frame.csv` podľa 3.2.
- **Kroky:** stiahnuť dáta, filtrovať, deduplikovať, zapísať počty.
- **Výstupy:** `data/raw/_frame/{sources.csv, frame.csv, merges.csv}`,
  `scripts/build_frame.py`.
- **Hotové, keď:** skript beží znova s rovnakým výsledkom (rovnaký SHA-256
  rámca), počty po filtroch sú zapísané a porovnané s číslom NVCA.
- **Riziká:** nesprávny názov poľa vo filtri → kontrola náhodných
  10 riadkov rámca ručne voči podaniu.

#### F2: Výber vzorky
- **Cieľ:** 40 kandidátov + rezerva + kalibračná sada podľa 3.3.
- **Výstupy:** `sample.csv`, `sample-log.md`, `scripts/sample.py`.
- **Hotové, keď:** opätovné spustenie dá rovnaké ID.
- **Riziká:** vrstva má príliš málo firiem → úprava hraníc **pred**
  losovaním, zdokumentovaná.

#### F3: Kalibrácia agentov
- **Cieľ:** odladiť pokyny agentov na 5 kalibračných kandidátoch.
- **Kroky:** spustiť A1→A2→S1→A3 na kalibračnej sade; človek skontroluje
  výstupy; upraviť pokyny; zapísať každú zmenu pokynov (v1, v2…) a dôvod.
- **Výstupy:** `scripts/prompts/*.md` (verzované pokyny), záznamy chýb
  v `notes/chyby-ai.md`, kalibračné záznamy v `data/raw/_calibration/`.
- **Hotové, keď:** na kalibračnej sade nie je žiadna vymyslená citácia,
  ktorú by S1 nezachytil, a človek nemá k pokynom ďalšie zásadné výhrady.
  Po tomto bode sa pokyny **zmrazia** pre fázu F4.
- **Riziká:** preladenie na 5 záznamov; preto sa kalibrácia nerobí na
  vzorke.

#### F4: Zber vzorky
- **Cieľ:** 40 záznamov v `data/raw/`.
- **Kroky:** A1 a A2 pre každého kandidáta, s logovaním nákladov (sekcia 12.1).
- **Výstupy:** `data/raw/<id>.json`, `results/cost-log.csv`.
- **Hotové, keď:** každý kandidát má záznam (aj vyradený) a riadok v cost-logu.
- **Riziká:** zmena pokynov počas zberu by znehodnotila meranie → zmena iba
  so zdokumentovaním a opätovným spracovaním dotknutých záznamov.

#### F5: Automatická kontrola a nezávislé overenie
- **Cieľ:** každý záznam má výsledok S1, schémy, deduplikácie a A3.
- **Výstupy:** vyplnené `qa`, `results/verifier-log.csv`.
- **Hotové, keď:** všetky záznamy majú `qa.checked_at` a verdikt A3 pre
  každý dôkaz.
- **Riziká:** A3 opakuje chyby A2 (rovnaký model) → slepé zadanie, sekcia 7.3.

#### F6: Ručná kontrola
- **Cieľ:** ľudský verdikt pre každé vyplnené pole a vybrané prázdne polia
  (sekcia 8).
- **Výstupy:** `results/manual-review.csv`, schválené záznamy
  v `data/verified/`.
- **Hotové, keď:** všetkých 40 záznamov má verdikt.
- **Riziká:** únava a „kotvenie“ na odpovedi AI → postup v 8.2.

#### F7: Metriky a náklady
- **Výstupy:** `scripts/metrics.py`, `results/accuracy.md`,
  `results/cost.md`.
- **Hotové, keď:** metriky z 10.2 sú vypočítané skriptom z CSV, nie ručne.

#### F8: Vyhodnotenie a globálny odhad
- **Výstupy:** `results/global-estimate.md`, rozhodnutie podľa 10.4,
  doplnené README.
- **Hotové, keď:** README uvádza, čo je hotové, čo chýba a prečo.

### 7.2 Roly agentov a skriptov

| Rola | Typ | Cieľ | Vstup | Výstup | Povolené zdroje | Obmedzenia |
|---|---|---|---|---|---|---|
| **R0 Rámec** | skript | zostaviť rámec a vzorku | dáta SEC | `frame.csv`, `sample.csv` | iba stiahnuté súbory SEC | žiadne LLM, deterministické |
| **A1 Identita** | agent | nájsť oficiálny web a potvrdiť identitu | riadok rámca | `name`, `alt_names`, `domains`, `website`, `legal_entity`, `country` s dôkazmi | web, registre | nevypĺňa finančné polia ani zameranie |
| **A2 Extrakcia** | agent | vyplniť ostatné polia a dealy | výstup A1 | návrh záznamu v `data/raw/` | `CLAUDE.md` 3 | protokol 4.3, limit vyhľadávaní, navrhuje `inclusion` |
| **S1 Dôkazy** | skript | URL a citácie existujú | záznam | `qa` | iba URL zo záznamu | nehodnotí význam |
| **S2 Schéma** | skript | súlad so schémou | záznam | `qa.schema_valid`, `issues` | – | – |
| **S3 Duplicity** | skript | kandidáti na duplicity | všetky záznamy | `qa.duplicate_candidates` | – | nikdy nespája podľa podobnosti názvu |
| **A3 Kontrolór** | agent, nový kontext | posúdiť, či zdroj tvrdenie podporuje, a hľadať protidôkazy | iba trojice (pole, hodnota, URL + citácia), **bez** `notes` a zdôvodnenia A2 | verdikt pre každý dôkaz: podporuje / čiastočne / nepodporuje / nedostupné; zoznam protidôkazov | URL zo záznamu + vlastné vyhľadávanie protidôkazov (zánik, iný typ) | nesmie meniť záznam, iba hlásiť |
| **A4 Duplicity** | agent | posúdiť páry od S3 | dva záznamy | návrh: rovnaký / iný / nejasný + dôkaz | registre, web | návrh, rozhoduje človek |
| **Človek** | – | rozhodovať | všetko | `data/verified/`, `manual-review.csv` | – | – |

Rozhodnutia, ktoré **zostávajú výhradne na človeku:**

- schválenie plánu a zmeny pravidiel Z/V/N,
- rozhodnutie pri všetkých prípadoch N1–N6,
- spojenie alebo oddelenie entít mimo automatických pravidiel v 6.2,
- presun záznamu do `data/verified/`,
- vyriešenie rozporu medzi A2 a A3,
- rozhodnutie o pokračovaní projektu (10.4).

### 7.3 Nezávislosť kontroly a nezhody

- A3 beží v **novom kontexte** a nedostane zdôvodnenie ani poznámky A2,
  iba tvrdenia a zdroje. Musí každý zdroj otvoriť sám a posúdiť, či citácia
  tvrdenie podporuje **v kontexte stránky** (napr. citácia nie je o inej
  firme s podobným názvom).
- A3 dostane navyše úlohu hľadať **protidôkazy** k povinným poliam: zánik
  firmy, iný typ investora, investícia pripísaná inému subjektu.
- Ak je k dispozícii, A3 beží na **inom modeli** ako A2. Pri rovnakom modeli
  je nezávislosť iba čiastočná a uvedie sa to v obmedzeniach [OTVORENÉ O6].

Pravidlá pre nezhody:

| Situácia | Výsledok |
|---|---|
| S1 nenašiel citáciu | dôkaz neplatný; ak to bol jediný dôkaz povinného poľa → ručná kontrola |
| A3: „nepodporuje“ alebo „čiastočne“ pri povinnom poli | celý záznam → ručná kontrola s prioritou |
| A3: „nepodporuje“ pri inom poli | pole → ručná kontrola |
| A3 našiel protidôkaz | záznam → ručná kontrola, A3 pripojí zdroj protidôkazu |
| A2 navrhol N1–N6 | vždy ručná kontrola |
| A2 a A3 súhlasia | záznam prejde ručnou kontrolou v štandardnom poradí; v pilote sa kontroluje **všetko** |

Nezhody sa nerozhodujú hlasovaním ani ďalším agentom. Rozhoduje človek.

### 7.4 Pomocné skripty

| Skript | Účel | Spustenie |
|---|---|---|
| `scripts/build_frame.py` | výberový rámec z dát SEC | `python scripts/build_frame.py --adv <súbor> --formd <priečinok>` |
| `scripts/sample.py` | losovanie vzorky | `python scripts/sample.py --seed 20261025` |
| `scripts/check_evidence.py` | S1: URL a citácie | `python scripts/check_evidence.py data/raw/` |
| `scripts/validate_schema.py` | S2: súlad so schémou (JSON Schema odvodená z `data/schema.md`) | `python scripts/validate_schema.py data/raw/` |
| `scripts/find_duplicates.py` | S3: kandidáti na duplicity | `python scripts/find_duplicates.py data/raw/ data/verified/` |
| `scripts/metrics.py` | metriky presnosti a nákladov | `python scripts/metrics.py` |
| `scripts/export_csv.py` | CSV export z JSON (ak sa schváli, O4) | `python scripts/export_csv.py` |

Všetky skripty sú idempotentné, `data/verified/` iba čítajú a chyby
zapisujú do výstupu, nepreskakujú ich potichu (`CLAUDE.md` 8).

---

## 8. Kontrola kvality a ručné overovanie

### 8.1 Technická validita verzus správnosť

| Úroveň | Čo potvrdzuje | Čo **nepotvrdzuje** |
|---|---|---|
| Platný JSON a schéma (S2) | štruktúru | nič o pravdivosti |
| Dostupná URL (S1) | stránka existuje | že patrí správnemu subjektu |
| Citácia nájdená (S1) | text na stránke je | že podporuje tvrdenie, je aktuálny a o správnom subjekte |
| Verdikt A3 | druhý pohľad na podporu tvrdenia | správnosť (môže sa mýliť rovnako ako A2) |
| Ručné overenie | správnosť podľa človeka | úplnosť (človek tiež nenájde všetko) |

Vo výsledkoch sa tieto úrovne nikdy nesčítajú do jedného čísla
(`CLAUDE.md` 11).

### 8.2 Postup ručnej kontroly

V pilote sa kontroluje **100 % záznamov vzorky** (40).

1. Poradie: najprv záznamy, ktoré označili S1/A3, potom ostatné v poradí
   zo `sample.csv`.
2. Pri každom poli **najprv otvoriť zdroj a prečítať kontext**, až potom
   porovnať s hodnotou AI. Tým sa znižuje kotvenie na odpovedi AI.
3. Pre každé vyplnené pole verdikt:
   - `spravne`: hodnota zodpovedá zdroju a zdroj je relevantný a aktuálny,
   - `nespravne`: hodnota nezodpovedá zdroju alebo realite,
   - `ciastocne`: napr. správny rozsah, nesprávna mena alebo obdobie,
   - `nepodlozene`: hodnota môže byť pravdivá, ale citovaný zdroj ju
     nepodporuje (chyba dôkazu, nie hodnoty),
   - `neoveritelne`: človek nevie rozhodnúť ani po kontrole.
4. **Kontrola prázdnych polí:** pri každom zázname sa pre `website`,
   `stages`, `ticket_size`, `fund_size` a `aum`, ktoré AI nechala `null`,
   hľadá najviac 5 minút. Ak sa údaj nájde, ide o **falošne prázdne** pole
   (metrika M6). Takto sa odlíši „chýba, lebo neexistuje“ od „chýba, lebo
   AI nenašla“.
5. Kontrola aktuálnosti: pri finančných údajoch, či `as_of` nie je starší
   ako 3 roky. Ak je, verdikt `ciastocne` s poznámkou.
6. Kontrola priradenia: či dôkaz patrí k správnemu poľu (napr. veľkosť
   kola zapísaná ako `ticket_size` je `nespravne`).
7. Zaznamenať čas kontroly záznamu v minútach.

Záznam v `results/manual-review.csv`:
`record_id, field, ai_value, ai_status, verdict, corrected_value,
evidence_url, minutes, reviewer, date, notes`.

### 8.3 Evidencia chýb, opráv a neistoty

- Každý verdikt iný ako `spravne` sa zapíše do `manual-review.csv`.
  Typické alebo poučné chyby sa zapíšu aj do `notes/chyby-ai.md`
  so stĺpcom „Kto zistil“.
- Opravená hodnota sa zapíše iba do `data/verified/<id>.json`.
  Pôvodný návrh AI v `data/raw/` zostáva nezmenený, aby sa dalo merať.
- Neistota zostáva v zázname (`v_rozpore`, `notes`). Pri ručnej kontrole sa
  neodstraňuje iba preto, aby záznam vyzeral čistejšie.

### 8.4 Kedy sa záznam **nesmie** presunúť do `data/verified/`

1. Niektoré povinné pole (5.1) nie je `dolozene` alebo má verdikt iný ako
   `spravne`.
2. Rozhodnutie je `vyradeny` alebo `nejasny` (vyradené záznamy sa
   evidujú iba v `data/raw/`).
3. Niektorý dôkaz v zázname má S1 výsledok „citácia nenájdená“ a nebol
   opravený alebo odstránený.
4. Existuje nevyriešený kandidát na duplicitu.
5. Existuje protidôkaz od A3, ktorý človek nevyhodnotil.
6. Záznam neprešiel validáciou schémy.
7. Aktivita je doložená iba zdrojom úrovne 3 alebo bez dátumu (N3, N4, N6).

---

## 9. Odhad očakávanej spoľahlivosti pred pilotom

Všetky čísla v tejto tabuľke sú **[HYPOTÉZA] pred pilotom, nie namerané
výsledky.** Vychádzajú z úvahy o dostupnosti zdrojov, nie z dát. Po pilote sa
vedľa nich doplnia namerané hodnoty s intervalom spoľahlivosti.

| Pole | Očakávaná vyplnenosť | Očakávaná presnosť vyplnených | Zdôvodnenie |
|---|---|---|---|
| identita | ~100 % | ≥ 98 % | vychádza z registra |
| `country` | ~100 % | ≥ 98 % | register |
| `website` | 90–95 % | ≥ 95 % | väčšina VC má web; riziko zámeny s podobnou doménou |
| `investor_type` | ~100 % | 90–95 % | register uvádza typ fondu, ale hranica VC / growth / PE je nejasná |
| deal v okne (Z3) | 75–85 % zaradených | ≥ 90 % po S1 | menšie fondy oznamujú menej; riziko zámeny investora s podobným názvom |
| `stages` | 70–85 % | 80–90 % | vlastné vyjadrenie na webe, často vágne |
| `sectors` | 80–90 % | 80–90 % | rovnako; problém granularity |
| `geography` | 60–80 % | 85–90 % | často uvedené iba nepriamo |
| `ticket_size` | 30–45 % | ~80 % | mnohé fondy rozsah neuvádzajú; riziko zámeny s veľkosťou kola |
| `fund_size` | 55–70 % | ~85 % | oznámenia o uzavretí fondov sú bežné; rozdiel cieľ / uzavretie / regulačná hodnota |
| `aum` | 30–50 % | ~75 % | ERA nemusia uvádzať regulačné AUM; rôzne definície a dátumy |
| `deployable_capital` | < 10 % | neodhadnuteľné | zriedka verejné |
| presnosť zaradenia | – | ≥ 95 % | prísne pravidlá Z, nejasné prípady idú človeku |
| vymyslené citácie v návrhu AI | 2–10 % dôkazov | – | známa slabina LLM; S1 ich má zachytiť |

Vyhodnotenie: pre každý riadok sa vypočíta metrika M3 (presnosť poľa)
a M5 (vyplnenosť) z ručnej kontroly a porovná sa s hypotézou. Hypotéza sa
považuje za potvrdenú, ak interval spoľahlivosti nameranej hodnoty prekrýva
hypotetický rozsah.

---

## 10. Meranie presnosti a úspešnosti

### 10.1 Vzorkovanie

- **Pilot:** úplná ručná kontrola všetkých 40 záznamov (census vzorky).
- **Pri škálovaní:** náhodná kontrolná vzorka z každej dávky
  (predbežne 10 %, minimálne 30 záznamov na dávku), stratifikovaná podľa
  krajiny a typu, s pevným seedom.
- Pri n = 40 sa pre každý podiel uvedie **95 % Wilsonov interval**. Príklad:
  38 správnych zo 40 (95 %) má interval približne 83–99 %. Preto sa
  z pilotu nedá tvrdiť presnosť „95 %“ bez intervalu.

### 10.2 Metriky

V tabuľke „vyplnené pole“ znamená pole s `value ≠ null` v návrhu AI.

| ID | Metrika | Definícia | Menovateľ |
|---|---|---|---|
| **M1** | Presnosť zaradenia | záznamy, ktoré AI navrhla zaradiť **a** človek potvrdil | záznamy, ktoré AI navrhla zaradiť |
| **M2** | Správnosť vyradenia | vyradenia, s ktorými človek súhlasí | záznamy, ktoré AI navrhla vyradiť |
| **M3** | Presnosť poľa | vyplnené polia s verdiktom `spravne` | vyplnené polia daného typu, okrem `neoveritelne` |
| **M4** | Podiel polí s dôkazom | vyplnené polia s aspoň jedným dôkazom, ktorý prešiel S1 | vyplnené polia |
| **M5** | Vyplnenosť (úplnosť) | polia s `value ≠ null` | zaradené záznamy × pole |
| **M6** | Falošne prázdne polia | `null` polia, pri ktorých človek našiel údaj do 5 minút | kontrolované `null` polia |
| **M7** | Miera chybných tvrdení | vyplnené polia s verdiktom `nespravne` | vyplnené polia |
| **M8** | Miera vymyslených zdrojov | dôkazy s neexistujúcou URL alebo citáciou, ktorá na stránke nie je | všetky dôkazy |
| **M9** | Záchyt vymyslených zdrojov | vymyslené dôkazy (M8), ktoré zachytil S1 alebo A3 | vymyslené dôkazy zistené kýmkoľvek |
| **M10** | Miera nepodložených tvrdení | verdikt `nepodlozene` | vyplnené polia |
| **M11** | Miera neoveriteľných | verdikt `neoveritelne` | vyplnené polia |
| **M12** | Miera duplicít | záznamy, ktoré sa ukázali ako duplicita iného | všetky záznamy vzorky |
| **M13** | Citlivosť na okno | zaradení, ktorí by vypadli pri 12 mesiacoch / pribudli pri 36 | zaradení |
| **M14** | Podiel vyradených z rámca | vyradení podľa V1–V8, rozpísané podľa pravidla | kandidáti vzorky |
| **M15** | Pokrytie rámca | členovia NVCA nájdení v rámci | členovia NVCA so sídlom v USA |
| **M16** | Podiel ručne opravených záznamov | záznamy s aspoň jedným verdiktom iným ako `spravne` | zaradené záznamy |
| **M17** | Zhoda A3 s človekom | dôkazy, kde verdikt A3 zodpovedá verdiktu človeka | dôkazy s oboma verdiktmi |

Rozlíšenie chýbajúceho a nesprávneho údaja: `null` nikdy nie je chyba
presnosti (M3, M7), ale znižuje vyplnenosť (M5). Ak údaj existoval, zvyšuje
falošne prázdne polia (M6). Tak sa dá oddeliť opatrnosť od chybovosti.

Validácia schémy (S2) sa medzi metrikami kvality **neuvádza**. Je to
podmienka spracovania, nie dôkaz správnosti.

### 10.3 Výpočet

`scripts/metrics.py` načíta `data/raw/`, `results/manual-review.csv`
a `results/verifier-log.csv` a vypíše tabuľky do `results/accuracy.md`:
bodový odhad, interval, počet, a to celkovo (váhovane podľa vrstiev)
aj za každú vrstvu. Žiadna metrika sa nepočíta ručne.

### 10.4 Akceptačné prahy a rozhodnutie po pilote

| Metrika | Prah | Odôvodnenie |
|---|---|---|
| M1 presnosť zaradenia | ≥ 95 % (bodovo) a žiadny prípad V2 zaradený ako investor | hlavná požiadavka zadania: „každý záznam musí byť skutočný investor“ |
| M3 povinné polia | ≥ 95 % | sú podmienkou zaradenia |
| M3 dôležité polia | ≥ 85 % pre každé pole zvlášť | chybný údaj o tickete alebo kapitáli zavádza používateľa |
| M9 záchyt vymyslených zdrojov | 100 % (žiadny nesmie prejsť do `verified`) | jediný vymyslený zdroj podkopáva dôveru v celú databázu |
| M6 falošne prázdne | ≤ 20 % | inak je metodika príliš opatrná a databáza zbytočne prázdna |
| čas ručnej kontroly | medián ≤ 15 min na záznam | pri vyššom čase nie je globálne škálovanie realistické (sekcia 12) |

Rozhodnutie:

- **Pokračovať** (ďalšia krajina alebo typ): všetky prahy splnené.
- **Upraviť metodiku a zopakovať pilot na novej vzorke:** M1 a povinné
  polia splnené, ale niektoré dôležité pole pod prahom alebo príliš veľa
  falošne prázdnych polí. Dôsledok: zmeniť zdroje alebo pokyny pre dané
  pole, prípadne pole prehlásiť za „nepovinné, nízka dostupnosť“.
- **Zastaviť rozširovanie a prehodnotiť prístup:** M1 < 90 %, alebo
  vymyslený zdroj prešiel do `verified`, alebo medián ručnej kontroly
  > 30 min. Plne automatizovaný zber pri požadovanej spoľahlivosti
  nefunguje a treba zmeniť model (napr. menej polí, viac ručnej práce).
- Medzi 90 a 95 % pri M1: rozhodne človek podľa typov chýb.

Prahy sú zvolené pred pilotom a po pilote sa nesmú meniť tak, aby sa
výsledky „zmestili“. Zmena prahu sa zdôvodní a výsledok sa vykáže voči
pôvodnému aj novému prahu.

---

## 11. Rozšírenie na globálnu databázu

### 11.1 Postup rozširovania

1. **Po krajinách, nie naraz.** Ďalšia vlna: jedna krajina s dobrým
   registrom (napr. Spojené kráľovstvo: register FCA a Companies House)
   a jedna s nízkou transparentnosťou (napr. Česko alebo Slovensko).
   Každá vlna má malý vlastný pilot (20–30 záznamov) a meranie podľa
   sekcie 10, pretože presnosť sa medzi krajinami nedá preniesť.
2. **Po typoch.** PE ako ďalší typ (podobné zdroje ako VC); family office
   a angel investori až po vyriešení ochrany osobných údajov (O3)
   a s vlastnými pravidlami zaradenia, pretože pri nich chýba register.
3. **Výberový rámec pre každú krajinu** sa zostaví z najlepších dostupných
   verejných zdrojov: registre správcov fondov (v EÚ registre AIFM
   a EuVECA podľa národných dohľadov a ESMA), členské zoznamy národných
   asociácií (napr. Invest Europe, BVCA), portfóliá verejných fondov
   fondov (napr. EIF). Pri každom zdroji sa zapíše jeho pokrytie
   a obmedzenia rovnako ako v 3.2. Ich dostupnosť a obsah som v tomto
   pláne neoveroval.

### 11.2 Rozdiely medzi krajinami

| Oblasť | Dôsledok pre metodiku |
|---|---|
| Registre | Kde register správcov chýba, Z1 sa opiera o firemný register a web; vyššia miera N1. |
| Jazyk | Citácie v pôvodnom jazyku (`CLAUDE.md` 2); ručná kontrola vyžaduje znalosť jazyka alebo dvojité overenie. |
| Právne formy | Mapovanie právnych foriem na typy investorov (napr. SICAV, investiční fond s.r.o.) do tabuľky pre každú krajinu. |
| Transparentnosť financií | Pri mnohých krajinách očakávať nižšiu vyplnenosť `aum` a `ticket_size`; neznižovať prah presnosti, iba akceptovať nižšiu vyplnenosť. |
| Zvyky oznamovania dealov | Menej tlačových správ → nižšia vyplnenosť Z3 → viac N6 a V1. Je potrebné zvážiť dlhšie okno pre danú krajinu, ale iba ako zdokumentovanú výnimku. |

### 11.3 Odhad počtu investorov

Evidujú sa tri **rozdielne** čísla, ktoré sa nesmú zamieňať:

| Číslo | Význam | Odkiaľ |
|---|---|---|
| **objavení** | kandidáti vo výberových rámcoch | počet riadkov rámcov |
| **odhadovaný celkový počet** | aktívni investori v populácii | rámec × miera zaradenia z pilotu (1 − M14) ÷ pokrytie rámca (M15), s intervalom |
| **overení** | záznamy v `data/verified/` | počet súborov |

Východiská pre USA, VC [FAKT, z druhej ruky, overiť v primárnom zdroji]:

- NVCA 2026 Yearbook: 2 984 VC firiem v roku 2025, pokles z 3 054 [FAKT 7].
- NVCA 2024 Yearbook: 3 417 VC firiem na konci roka 2023, AUM 1,21 bil. USD
  [FAKT 8]. Rozdiel oproti 3 054 naznačuje zmenu metodiky medzi ročníkmi.
  Čísla z rôznych ročníkov preto **neporovnávať** ako trend.
- Fundraising 2025: 67 mld. USD v 585 fondoch (tlačová správa NVCA)
  [FAKT 9]. Rôzne zdroje uvádzajú 575 až 626 fondov.

Pre ostatné krajiny a typy sa v F0 a pri každej vlne zbiera rovnaká trojica
čísel z verejných zdrojov (asociácie, registre). **Globálne číslo zatiaľ
neuvádzam.** Nenašiel som verejný zdroj, ktorý by spoľahlivo počítal
investorov všetkých typov vo svete. Číslo bez zdroja by porušilo pravidlá
projektu. Odhad sa zostaví zdola nahor po krajinách a spresní sa každou vlnou:

- najprv krajiny s najväčším objemom VC/PE (tie dávajú väčšinu populácie),
- pri krajinách bez dát extrapolácia podľa pomeru k objemu investícií,
  s explicitne širokým intervalom a označením [HYPOTÉZA],
- family office a angel investori ako samostatné, výrazne neistejšie čísla.

Zdroje neistoty: rôzne definície „VC firmy“, neúplné registre,
neaktívne subjekty v rámcoch, dvojité započítanie firiem pôsobiacich vo
viacerých krajinách (jedna firma = jeden záznam podľa sídla správcu).

---

## 12. Časový plán a náklady

### 12.1 Meranie nákladov v pilote

Pre každé volanie agenta sa zapíše riadok do `results/cost-log.csv`:

`record_id, phase, role, attempt, model, input_tokens, output_tokens,
cache_read_tokens, cache_write_tokens, model_calls, web_searches,
web_fetches, wall_seconds, outcome (ok / failed / retried), notes`

a pre ručnú prácu do `results/manual-review.csv` (minúty na záznam) a
počet opráv.

Ako získať čísla [OTVORENÉ O5]:

- **Varianta A (odporúčaná):** agenti A1–A3 bežia cez Claude API zo
  skriptu. Odpoveď API obsahuje presnú spotrebu tokenov a počet použití
  serverových nástrojov (vyhľadávanie). Čísla sú presné a priamo
  použiteľné na odhad.
- **Varianta B:** agenti bežia ako subagenti v Claude Code. Spotreba sa
  zapisuje z prehľadu, ktorý Claude Code po úlohe ukáže. Je to menej presné
  a predplatné Claude Code nie je rovnaké ako cena API. Na odhad nákladov
  sa tokeny prepočítajú cenníkom API.

Výpočet v `scripts/metrics.py`: priemer **aj medián** na záznam za každú
rolu a celkovo, oddelene pre zaradené a vyradené záznamy (vyradenie býva
lacnejšie, ale stále stojí peniaze) a pre neúspešné pokusy.

### 12.2 Model nákladov

```
Náklady(N) = F + N × (v_api + v_hľadanie + v_človek) + údržba(N, rok)

v_api      = tokeny_vstup × cena_vstup + tokeny_výstup × cena_výstup  (pre každú rolu)
v_hľadanie = počet_vyhľadávaní × cena_vyhľadávania
v_človek   = minúty_kontroly / 60 × hodinová_sadzba × podiel_kontrolovaných
údržba     = N × frekvencia_rekontroly × (v_api + v_hľadanie) × podiel_zmenených
F          = vývoj skriptov, pokynov, rámcov pre každú krajinu (hodiny človeka)
```

- **Fixné (F):** vývoj skriptov (jednorazovo), rámec pre každú krajinu
  (jednorazovo na krajinu), kalibrácia pokynov pre každú krajinu a typ.
- **Variabilné (v):** merané v pilote, teda priemer a medián z cost-logu.
- **Údržba:** opätovná kontrola aktivity (Z3) a finančných údajov,
  predbežne raz za 6 mesiacov [ROZHODNUTIE]. Náklady na kontrolu jedného
  záznamu sa namerajú opakovaním zberu na 10 záznamoch po pilote. Pred
  pilotom sa odhadujú na 30–50 % prvotného zberu [HYPOTÉZA].

Ceny Claude API zo stránky Anthropic [FAKT 10], USD za milión tokenov:

| Model | Vstup | Výstup | Batch (−50 %) vstup / výstup |
|---|---|---|---|
| Claude Opus 5.5 | 4 | 20 | 2 / 10 |
| Claude Sonnet 5.5 | 2 | 10 | 1 / 5 |
| Claude Haiku 5.5 (do 100 tis. tokenov promptu) | 0,10 | 0,50 | 0,05 / 0,25 |

Webové vyhľadávanie: 10 USD za 1 000 vyhľadávaní; načítanie stránky (web
fetch) bez príplatku, platia sa iba tokeny [FAKT 10].

**Ilustračný výpočet [HYPOTÉZA], nie odhad:** ak by jeden záznam
spotreboval 150 tis. vstupných a 15 tis. výstupných tokenov na Sonnet 5.5
a 20 vyhľadávaní, náklady API by boli približne 0,30 + 0,15 + 0,20 =
0,65 USD. Kontrolór A3 by pridal podobnú sumu. Ručná kontrola 10 minút pri
sadzbe 20 € za hodinu stojí približne 3,3 €. Ak sa tieto predpoklady čo
i len zhruba potvrdia, **dominantnou položkou bude čas človeka**,
a preto sa rozhoduje hlavne o podiele ručne kontrolovaných záznamov.

### 12.3 Scenáre

| Scenár | Ručná kontrola | Čo umožňuje | Riziko |
|---|---|---|---|
| **S-A Automatický** | iba náhodná vzorka 5–10 % na meranie | lacné pokrytie veľkého počtu investorov | presnosť iba odhadnutá, chybné záznamy v databáze zostanú |
| **S-B Hybridný (odporúčaný)** | 100 % povinných polí + záznamy označené S1/A3 + náhodná vzorka ostatných polí | spoľahlivé zaradenie pri primeraných nákladoch | dôležité polia s nižšou istotou, musí sa to v dátach označiť |
| **S-C Úplná kontrola** | 100 % všetkých polí | najvyššia spoľahlivosť | náklady rastú lineárne s časom človeka |

Platené zdroje (napr. komerčné databázy investorov) sa v tomto projekte
nepoužívajú (požiadavka zadania). Ak by sa neskôr zvažovali, iba ako zdroj
kandidátov, nikdy ako dôkaz, a podľa ich licenčných podmienok. Hosting nie
je pre databázu v podobe súborov v repozitári potrebný. Ak by vznikla
webová aplikácia, ide o samostatný fixný náklad mimo tohto plánu.

Podmienky používania zdrojov: SEC vyžaduje pri automatizovanom sťahovaní
identifikáciu v User-Agent a obmedzuje počet požiadaviek. Konkrétne limity
treba overiť na sec.gov pred napísaním skriptu. Weby investorov sa čítajú
iba v rozsahu potrebnom na dôkaz, bez hromadného sťahovania.

### 12.4 Časový plán

| Etapa | Obsah | Odhad času [HYPOTÉZA] |
|---|---|---|
| Pilot (do 2026-10-30) | F0–F8 pre 40 záznamov | ~5 dní: F0–F2 1 deň, F3 0,5 dňa, F4–F5 1 deň, F6 1,5 dňa (40 × 10–15 min ≈ 7–10 hodín), F7–F8 1 deň |
| Vyhodnotenie a úprava metodiky | po pilote | 2–3 dni |
| Druhá vlna (2 krajiny, 20–30 záznamov každá) | nové rámce a piloty | 1–2 týždne |
| Škálovanie | podľa nameraných nákladov a scenára | vypočíta sa z modelu 12.2 |
| Údržba | rekontrola každých 6 mesiacov | vypočíta sa z modelu 12.2 |

---

## 13. Riziká a obmedzenia

| Riziko | Dopad | Opatrenie |
|---|---|---|
| **Halucinácie AI** (vymyslené URL, citácie, dealy) | chybné záznamy, strata dôvery | povinná doslovná citácia, S1 kontrola citácií, nezávislý A3, 100 % ručná kontrola v pilote, metriky M8 a M9 |
| **Zámena identity** (podobné názvy, iná firma) | dealy pripísané nesprávnemu investorovi | identita z registra (A1 pred A2), A3 kontroluje kontext stránky, deduplikácia podľa ID |
| **Neaktuálne údaje** | neaktívni investori a staré sumy | časové okno, `as_of` pri financiách, rekontrola každých 6 mesiacov |
| **Nízka transparentnosť** | prázdne polia | `null` namiesto odhadu, vykazovať vyplnenosť (M5), nekompenzovať odhadmi |
| **Duplicity** | nadhodnotený počet, rozporné záznamy | jednotka záznamu (1.5), kľúče (6.1), ľudské rozhodnutie pri nejasných |
| **Zaujatosť výberu** | presnosť platí iba pre ľahké prípady | výber z registra s náhodným losovaním a stratifikáciou; jasne uviesť, že USA VC sú najľahší segment |
| **Kotvenie človeka na odpovedi AI** | nadhodnotená presnosť | najprv zdroj, potom hodnota AI (8.2); kontrola prázdnych polí |
| **Preladenie pokynov** | vzorka sa javí lepšia, ako je metodika | kalibrácia na samostatnej sade, zmrazenie pokynov pred F4 |
| **Malá vzorka** | nepresný odhad presnosti | intervaly spoľahlivosti, žiadne tvrdenia bez intervalu |
| **Nedostupnosť zdrojov SEC z prostredia** | blokuje F1 | stiahnuť lokálne alebo upraviť sieťové pravidlá (O8) |
| **Časová tieseň (2026-10-30)** | nedokončená ručná kontrola | náhradný postup: zmenšiť vzorku na prvých 6 z každej vrstvy S1–S4 a 2 z S5 (spolu 26) podľa poradia v `sample.csv`. Výber zostane náhodný, metodika sa nemení a zmenšenie sa uvedie v README. |
| **Zmena webov počas projektu** | dôkaz prestane platiť | uložená kópia textu a SHA-256 (4.5), archívne kópie |

### 13.1 Ochrana osobných údajov

V pilote sa fyzické osoby ako investori nezbierajú. Mená partnerov VC firiem
sa používajú iba na overenie identity firmy a do záznamu sa neukladajú.
Pri angel a súkromných investoroch v ďalších fázach pozri O3.

### 13.2 Limity verejných zdrojov

Z verejných zdrojov sa **spoľahlivo** nedá zistiť: skutočná výška
investície jedného investora v kole (zvyčajne sa oznamuje iba celé kolo),
disponibilný kapitál, aktuálne AUM pri menších správcoch, aktivita
investorov, ktorí investície neoznamujú (family office, mnohí angel
investori), a investície, ktoré sa nikdy neoznámili. Databáza preto
**podhodnocuje** aktivitu nenápadných investorov. Ich neprítomnosť
neznamená, že neinvestujú.

---

## 14. Otvorené rozhodnutia a nedostatky pravidiel

### 14.1 Otvorené rozhodnutia (pred spustením zberu)

| ID | Otázka | Odporúčanie | Zdôvodnenie a dôsledky |
|---|---|---|---|
| **O1** | Čo je „celkový investičný kapitál“ zo zadania? | Hlavný ukazovateľ = `aum` s definíciou zo zdroja. `fund_size` evidovať zvlášť. V prezentácii pri chýbajúcom `aum` zobraziť veľkosť najnovšieho fondu s označením „veľkosť fondu, nie AUM“, nikdy súčet. | Možnosť „súčet fondov“ je zavádzajúca: staršie fondy sú už rozinvestované a čiastočne vrátené, súčet nadhodnocuje kapitál a porušuje 5.3. Možnosť „iba `aum`“ je presná, ale veľa záznamov bude prázdnych. Odporúčanie zachová presnosť aj užitočnosť. |
| **O2** | Časové okno 24 mesiacov | schváliť podľa 2.1 | kratšie okno vyradí aktívnych, dlhšie zaradí neaktívnych; overí sa metrikou M13 |
| **O3** | Ochrana osobných údajov pri angel a súkromných investoroch | Mimo pilotu. Neskôr zbierať iba profesionálne zverejnené údaje (meno, verejný investorský profil, doložené investície). Žiadne súkromné kontakty ani adresy. Pred zberom v EÚ posúdiť právny základ (oprávnený záujem podľa GDPR) a zabezpečiť právo na námietku a výmaz. Pri osobách bez verejného investorského profilu nezbierať vôbec. | Zber o fyzických osobách v EÚ podlieha GDPR aj z verejných zdrojov. Dôsledok: schéma potrebuje rozlíšenie fyzickej osoby a proces na výmaz; nižšie pokrytie angel investorov. Odporúčam konzultáciu s právnikom pred touto fázou. |
| **O4** | CSV export | Áno, ako **odvodený** výstup skriptu `export_csv.py`. Zdrojom pravdy zostáva JSON. CSV: jeden riadok na investora, pre každé pole `value`, `status` a URL prvého dôkazu; dealy v samostatnom CSV. | Hodnotiteľ a bežný používateľ pracujú skôr s tabuľkou; ručná úprava CSV by však oddelila dáta od dôkazov. Dôsledok: CSV sa nikdy neupravuje ručne. |
| **O5** | Ako spúšťať agentov a merať náklady | Varianta A (skript cez API), ak je k dispozícii API kľúč; inak B | A dáva presné náklady na globálny odhad, B je jednoduchší na spustenie |
| **O6** | Iný model pre A3 | Áno, ak je dostupný (napr. A2 na Sonnet 5.5, A3 na Opus 5.5) | zvyšuje nezávislosť kontroly; zvyšuje náklady A3 |
| **O7** | Hranice veľkostných vrstiev | podľa 3.3, upraviť pred losovaním podľa rozloženia rámca | zabráni prázdnym vrstvám |
| **O8** | Prístup k dátam SEC | Stiahnuť dáta lokálne a commitnúť do `data/raw/_frame/` (ak to veľkosť dovolí, inak iba hash a postup), alebo povoliť `sec.gov` v sieťových pravidlách cloudového prostredia. | Bez toho nemožno začať F1. |
| **O9** | CVC | samostatná kategória, mimo pilotu (1.4) | |
| **O10** | Hodinová sadzba pre výpočet nákladov človeka | určiť jednu sadzbu a uviesť ju v `results/cost.md` | bez nej nie je výsledný odhad porovnateľný |

### 14.2 Nedostatky a rozpory v existujúcich pravidlách

Neriešim ich zmenou schémy. Navrhujem ich rozhodnúť pred F1.

| ID | Kde | Problém | Návrh |
|---|---|---|---|
| **S1** | `data/schema.md` | Chýbajú polia pre identifikátory z registrov (CRD, CIK, SEC číslo, IČO). `CLAUDE.md` 1 zakazuje pridávať polia mimo schémy, takže sa musia ukladať do textu `legal_entity`. | Pridať pole `identifiers` (zoznam `{scheme, value, evidence}`). |
| **S2** | `data/schema.md`, `Deal.deal_date` | Neumožňuje čiastočný dátum (iba mesiac alebo rok), ktorý je v oznámeniach bežný. | Povoliť formát `YYYY-MM` a `YYYY` s poľom `date_precision`. |
| **S3** | `data/schema.md` | Nie je kde evidovať fundraising (Form D) oddelene od investícií. Pre N2 je to potrebné. | Pole `fundraising_events` alebo zaznamenať v `fund_size` s definíciou „ponuka podľa Form D“. |
| **S4** | `data/schema.md`, `sectors` | Voľný text „podľa formulácie zdroja“ sťažuje meranie presnosti a agregáciu. | Pridať mapovanie na jednotnú taxonómiu (pôvodný text ostane v citácii). |
| **S5** | `data/schema.md`, `QA` | Ručné overenie nie je v zázname evidované (kto a kedy). Ukladá sa iba v `results/manual-review.csv`. | Ponechať, ale v `data/verified/` pridať `review: {reviewer, date}`, prípadne to nechať na CSV a odkazovať naň. |
| **S6** | `data/schema.md`, príklad | Príklad v `ticket_size` uvádza `definition: "první investice"` po česky, ale `definition` nie je citácia. Nie je jasné, v akom jazyku písať popisné polia. | Popisné polia (`definition`, `notes`) písať po slovensky, citácie v pôvodnom jazyku. |
| **S7** | `CLAUDE.md` 1 | Plán má prednosť pred `CLAUDE.md`, ale plán napísala AI. | Doplniť, že prednosť má iba **schválená** verzia plánu (stav v hlavičke). |
| **S8** | `CLAUDE.md` 8 | `data/cache/` (kópie stránok) nie je v pravidlách spomenutý. | Doplniť: cache je mimo gitu a nie je dôkaz, iba kópia na kontrolu. |
| **S9** | `CLAUDE.md` 10 | Agenti majú zapisovať chyby do `notes/chyby-ai.md`, ale pri paralelnom behu viacerých agentov hrozí konflikt zápisov. | Agenti zapisujú do `qa.issues`, do denníka zapisuje skript alebo človek. |

---

## 15. Zdroje

Zdroje boli vyhľadané 2026-10-25. Stránky `sec.gov` a `nvca.org` boli
z prostredia, v ktorom vznikol plán, **nedostupné**. Tvrdenia z nich sú
prevzaté z výsledkov vyhľadávania (úryvkov) alebo zo sekundárnych zdrojov.
Pred F1 ich treba otvoriť priamo a citáty overiť (krok F0). Ide o zdroje pre
odhady, nie pre záznamy investorov.

| # | Tvrdenie v pláne | Zdroj | Ako získané | Relevantnosť |
|---|---|---|---|---|
| 1 | Exempt reporting advisers sú poradcovia, ktorí využívajú výnimku pre poradcov VC fondov (203(l)) alebo pre súkromné fondy (203(m)). | SEC, final rule IA-3222 (2011): https://www.sec.gov/files/rules/final/2011/ia-3222.pdf; SEC topical guide k pravidlám 203(l)-1 a 203(m)-1: https://www.sec.gov/about/divisions-offices/division-investment-management/topical-reference-guide/secg-rules-203-l-1-203-m-1-ia40 | vyhľadávanie | základ výberového rámca z ADV |
| 2 | ERA vypĺňajú iba položky 1, 2, 3, 6, 7, 10 a 11 Form ADV; mesačné súbory sú prehľad, štvrťročný archív obsahuje viac detailov vrátane Schedule D. | SEC, Information About Registered Investment Advisers and Exempt Reporting Advisers: https://www.sec.gov/data-research/sec-markets-data/information-about-registered-investment-advisers-exempt-reporting-advisers; SEC FAQ k Form ADV a IARD: https://www.sec.gov/about/divisions-offices/division-investment-management/electronic-filing-investment-advisers-iard/frequently-asked-questions-form-adv-iard | vyhľadávanie | čo rámec z ADV obsahuje a čo nie |
| 3 | Sekcia 7.B.(1) Schedule D sa vypĺňa pre každý súkromný fond a fond má stabilné identifikačné číslo. Typ fondu a hrubá hodnota aktív: podľa sekundárnych zdrojov, **overiť** vo formulári. | SEC, Form ADV Instructions: https://www.sec.gov/files/formadv-instructions.pdf; Form ADV Part 1A: https://www.sec.gov/files/formadv-part1a_1.pdf | vyhľadávanie | filter VC fondov, veľkostné vrstvy, deduplikácia fondov |
| 4 | Form D dátové sady: štruktúrované dáta z XML časti oznámení podľa Rule 504, 506(b), 506(c) a 4(a)(5), štvrťročne. Pri Pooled Investment Fund sa volí typ: Hedge Fund, Private Equity Fund, Venture Capital Fund, Other. | SEC DERA, Form D Data Sets: https://www.sec.gov/dera/data/form-d; SEC, Form D: https://www.sec.gov/files/formd.pdf | vyhľadávanie | doplnkový rámec, N2 |
| 5 | Štúdia DERA (2017) odhadla, že môžu chýbať podania až pri 10 % ponúk spĺňajúcich podmienky 506(b). | uvedené vo výsledku vyhľadávania k Form D dátam DERA; primárny dokument štúdie **nenájdený** | vyhľadávanie | obmedzenie úplnosti rámca |
| 6 | Za Q3 2026 869 nových VC fondov od 642 firiem (prvé Form D, typ VC, bez dodatkov). | ZInvestorHunting: https://zinvestorhunting.com/guides/new-venture-funds-last-quarter (úroveň 3) | vyhľadávanie | ilustrácia šumu (viac fondov na firmu, SPV); nie je dôkaz |
| 7 | V roku 2025 2 984 VC firiem, pokles z 3 054, prvý pokles. | NVCA 2026 Yearbook: https://nvca.org/wp-content/uploads/2026/04/NVCA-2026-Yearbook-4.9.26.pdf (nedostupné), citované podľa 1752vc: https://www.1752.vc/learn/what-is-venture-capital a https://dollarcommerce.substack.com/p/venture-capital-is-shrinking-heres | sekundárne zdroje | kontrola veľkosti populácie USA VC |
| 8 | Na konci roka 2023 3 417 VC firiem, AUM 1,21 bil. USD. | NVCA, tlačová správa k 2024 Yearbook: https://nvca.org/?p=120789 | úryvok z vyhľadávania | historické porovnanie, rozdielna metodika |
| 9 | Fundraising 2025: 67 mld. USD v 585 fondoch; 15 352 dealov. | NVCA, tlačová správa k 2026 Yearbook (cez Morningstar/PR Newswire): https://www.prnewswire.com/news-releases/nvca-releases-2026-yearbook-charts-a-venture-industry-in-transition-302740013.html | vyhľadávanie | kontext; počty fondov sa medzi zdrojmi líšia |
| 10 | Ceny Claude API, batch −50 %, web search 10 USD / 1 000 vyhľadávaní, web fetch bez príplatku. | Anthropic, Pricing: https://platform.claude.com/docs/en/about-claude/pricing | stránka otvorená 2026-10-25 | model nákladov |
