# Plán pilotu: databáza investorov

**Stav:** návrh v2, čaká na schválenie · **Dátum:** 2026-10-25

Pravidlá pre AI agentov sú v `CLAUDE.md`, štruktúra záznamu v
`data/schema.md`. Tento plán ich neopakuje.

## 1. Cieľ

Overiť na malej vzorke, či sa dá s pomocou AI zostaviť zoznam investorov,
v ktorom je **každý záznam skutočný investor** a každý údaj má dohľadateľný
zdroj. Pilot má odpovedať na tri otázky:

1. Ako často AI zaradí subjekt, ktorý v skutočnosti nie je investor?
2. Aký podiel údajov je správny a doložený zdrojom?
3. Koľko času a peňazí stojí jeden overený záznam?

Cieľom nie je hotová databáza, ale overený postup a poctivé čísla.

## 2. Rozsah pilotu

**Segment:** VC fondy so sídlom v Česku a na Slovensku, **25 investorov**.

Prečo tento segment:

- Zdroje sú v jazyku, ktorému rozumiem. Každý údaj viem skontrolovať
  sám, bez prekladu, a tým aj odhaliť chybu AI.
- Trh je malý, takže sa dá porovnať, koľko známych investorov sa do
  zoznamu kandidátov dostalo.
- Je to segment s nižšou transparentnosťou ako USA. Ak postup funguje
  tu, je to dobrý signál. Ak nefunguje, zistím, kde presne zlyháva.

Obmedzenie: výsledky platia pre tento segment. Neplatia pre PE, family
office, angel investorov ani pre iné krajiny.

**Mimo pilotu:** PE, family office, angel investori (fyzické osoby, ochrana
osobných údajov), corporate VC a iné krajiny.

## 3. Kto je investor (pravidlá zaradenia)

Identifikátory sa uvádzajú v poli `inclusion.rule`.

**Zaradiť**, ak platí všetko:

| ID | Pravidlo |
|---|---|
| **Z1** | Identita je jasná: oficiálny web alebo záznam v obchodnom registri. |
| **Z2** | Ide o VC investora so sídlom v CZ alebo SK (podľa webu alebo registra). |
| **Z3** | Má aspoň jednu doloženú investíciu za posledných 24 mesiacov (od 2024-10-25). Dôkaz musí menovať investora aj financovanú firmu, napríklad oznámenie investora, oznámenie firmy alebo článok v médiu. |

**Vyradiť**, ak platí niečo z tohto:

| ID | Pravidlo |
|---|---|
| **V1** | Nenašla sa žiadna doložená investícia. |
| **V2** | Nie je investor, ale poradca, sprostredkovateľ alebo crowdfundingová platforma. |
| **V3** | Neaktívny: všetky doložené investície sú staršie ako 24 mesiacov. |
| **V4** | Duplicita alebo iba ďalší fond firmy, ktorá už v zozname je. |

**Nejasný prípad (rozhodnem ja):**

| ID | Situácia |
|---|---|
| **N1** | Nejasná identita alebo typ investora. |
| **N2** | Investícia je doložená iba portfóliom na webe bez dátumu alebo iba adresárom či agregátorom. |

Prečo 24 mesiacov: kratšie okno by vyradilo menšie fondy, ktoré investujú
málo a nie všetko oznamujú. Dlhšie okno by prepustilo fondy, ktoré už iba
spravujú portfólio. Je to môj pracovný predpoklad, nie odborný štandard.
V pilote si zapíšem, koľko investorov by vypadlo pri 12 mesiacoch, aby sa
dalo posúdiť, či je hranica rozumná.

Všeobecné tvrdenie na webe („investujeme do seed fáz“) dokladá zameranie,
nie investičnú aktivitu. Aktivitu dokladá iba konkrétna investícia.

## 4. Postup

### Krok 1: Zoznam kandidátov
Kandidátov zostavím z verejných zoznamov: členovia českej a slovenskej
asociácie VC/PE (CVCA, SLOVCA), portfóliá verejných fondov fondov a články
s prehľadmi investorov. Či sú tieto zoznamy verejne dostupné a čo
obsahujú, si overím ako prvé. Pri každom kandidátovi si zapíšem, odkiaľ
pochádza.

Ak bude kandidátov viac ako 25, vyberiem ich tak, aby vzorka neobsahovala
iba najznámejšie fondy (napr. každý druhý v abecednom poradí). Výber
vysvetlím v `data/raw/candidates.csv`. Vyradení kandidáti v zozname
zostanú, pretože aj počet vyradených je výsledok.

### Krok 2: Zber (AI workflow 1)
Pre každého kandidáta jeden subagent v Claude Code s rovnakým pokynom
(`scripts/prompts/zber.md`). Agent vyplní záznam podľa schémy
s citáciou ku každému údaju, alebo nechá pole prázdne. Uloží ho do
`data/raw/<id>.json` a navrhne zaradenie podľa pravidiel z bodu 3.

Pokyn najprv vyskúšam na 3 kandidátoch, výstup skontrolujem, pokyn
upravím a až potom ho spustím na ostatných. Každú zmenu pokynu si zapíšem.

### Krok 3: Kontrola (AI workflow 2 + skript)
- **Skript** `scripts/check_sources.py` overí pri každom dôkaze, či URL
  funguje a či sa citácia na stránke naozaj nachádza. Tým zachytí
  vymyslené citácie.
- **Kontrolný agent** v novej konverzácii dostane iba tvrdenia a zdroje,
  nie zdôvodnenie prvého agenta. Pri každom tvrdení posúdi, či ho zdroj
  podporuje (áno / čiastočne / nie). Nič nemení, iba hlási.

### Krok 4: Ručná kontrola
Skontrolujem všetkých 25 záznamov. Pri každom údaji najprv otvorím zdroj
a až potom porovnám s hodnotou od AI, aby som sa nenechal ovplyvniť.
Verdikty zapíšem do `results/review.csv`, opravené záznamy uložím do
`data/verified/`. Pri niekoľkých prázdnych poliach skúsim údaj nájsť sám,
aby som vedel, či AI niečo prehliadla.

### Krok 5: Vyhodnotenie
Skript `scripts/summarize_review.py` spočíta výsledky z `review.csv`.
Zhrnutie a poučenia zapíšem do `results/` a do README.

## 5. Ktoré údaje zbierať

| Priorita | Údaje |
|---|---|
| **Povinné** (bez nich sa záznam nezaradí) | názov, web alebo register, typ, krajina, aspoň jedna investícia v okne |
| **Dôležité** (ak sú verejné) | sektory, fázy, výška jednej investície (ticket), veľkosť fondu, kapitál v správe (AUM) |
| **Ak sa nájdu** | disponibilný kapitál, ďalšie investície, súvisiace fondy |

Finančné údaje sú najrizikovejšie. Tri pravidlá, na ktoré si dám pozor:
veľkosť kola nie je výška investície fondu, súčet fondov nie je AUM a výška
investície sa neodhaduje z jedného obchodu (`CLAUDE.md` sekcia 6).
„Celkový investičný kapitál“ zo zadania budem evidovať ako AUM, ak ho
zdroj uvádza. Inak uvediem veľkosť fondu s jasným označením.

## 6. Kontrola kvality

Čo pilot sleduje:

| Čo | Ako sa počíta |
|---|---|
| **Správnosť zaradenia** | koľko zo zaradených investorov som potvrdil ako skutočných investorov |
| **Presnosť údajov** | koľko vyplnených údajov bolo správnych, zvlášť povinné a finančné |
| **Podiel doložených údajov** | koľko údajov má zdroj, ktorý tvrdenie naozaj podporuje |
| **Chyby AI** | počet a typy chýb (vymyslený zdroj, zlý údaj, zámena firmy, zlé zaradenie) a kto ich zachytil: skript, kontrolný agent alebo ja |
| **Čas a náklady** | čas AI a môj čas na jeden záznam, spotreba tokenov podľa Claude Code |

Záznam sa **nepresunie** do `data/verified/`, ak niektorý povinný údaj nie
je doložený, ak niektorá citácia neprešla kontrolou alebo ak ide o nejasný
prípad, o ktorom som ešte nerozhodol.

Pri 25 záznamoch sú čísla orientačné. Jedna chyba posunie presnosť
o 4 percentuálne body. Výsledky preto uvediem ako počty („23 z 25“), nie
iba ako percentá.

## 7. Vyhodnotenie pilotu

Pilot považujem za úspešný, ak:

- žiadny zaradený subjekt nie je poradca ani platforma a aspoň 24 z 25
  zaradených sú skutoční aktívni investori,
- žiadny vymyslený zdroj sa nedostane do `data/verified/`,
- povinné údaje sú takmer bez chýb.

Pri finančných údajoch čakám nízku vyplnenosť, pretože malé fondy ich
často nezverejňujú. To nie je neúspech, ak nie sú vymyslené.

Ak pilot neuspeje, nebudem meniť hranice, aby výsledky vyšli lepšie.
Popíšem, kde postup zlyhal a čo by som zmenil.

## 8. Odhad rozsahu a nákladov na celý svet

**Rozsah.** Z 25 záznamov v jednom segmente sa nedá spoľahlivo určiť, koľko
investorov je vo svete. Krajiny sa líšia dostupnosťou zdrojov a typy
investorov (najmä family office a angel investori) sa verejne prezentujú
oveľa menej ako VC. Uvediem preto iba:

- čo som z verejných zdrojov našiel pre CZ/SK,
- aké verejné čísla existujú pre väčšie trhy (napr. počty VC firiem
  v ročenkách asociácií), so zdrojom,
- prečo je počet pre family office a angel investorov z verejných
  zdrojov len veľmi hrubý.

**Náklady.** Z pilotu uvediem skutočne namerané hodnoty: tokeny a čas AI
na jeden záznam a môj čas na kontrolu. Odhad pre väčší rozsah bude
jednoduchý výpočet (počet záznamov × náklad na záznam) s jasne uvedenými
predpokladmi. Predpokladám, že najdrahšia položka bude čas ručnej
kontroly, nie AI. Pilot ukáže, či je to pravda.

## 9. Riziká

| Riziko | Čo s tým |
|---|---|
| AI si vymyslí zdroj alebo citáciu | skript overí citácie, ručná kontrola všetkých záznamov |
| AI zamení firmu s podobným názvom | kontrolujem, či zdroj hovorí o tej istej firme (web, mená, adresa) |
| Staré údaje | pri finančných údajoch zapisujem, ku ktorému dátumu platia |
| Vzorka obsahuje iba známe fondy | kandidáti z viacerých zdrojov, výber vysvetlený |
| Nestihnem to do 30. 10. | radšej menej záznamov poriadne skontrolovaných ako 25 neskontrolovaných; zmenšenie uvediem v README |
| Weby nie sú dostupné z cloudového prostredia | zber spúšťam lokálne v Claude Code (z cloudu boli niektoré weby zablokované) |

## 10. Možné budúce rozšírenia

Vedome ich v pilote nerobím. Uvádzam ich iba ako smer, nie ako plán:

- **Iné trhy a zdroje:** v USA sa dá zoznam kandidátov zostaviť
  z verejných podaní SEC (Form ADV, Form D). Bolo by to systematickejšie
  ako zoznamy asociácií, ale vyžaduje to pochopenie týchto registrov.
- **Náhodný výber z väčšieho zoznamu** so zapísaným postupom, aby sa
  výsledky dali zovšeobecniť na celý trh.
- **Viac metrík a intervaly spoľahlivosti** pri väčšej vzorke.
- **Ďalšie typy investorov** (PE, family office, angel) s vlastnými
  pravidlami a riešením ochrany osobných údajov.
- **Pravidelná aktualizácia** záznamov, pretože investori prestávajú byť
  aktívni.

## 11. Otvorené otázky

1. Segment CZ/SK VC namiesto USA: potvrdiť.
2. Sú členské zoznamy CVCA a SLOVCA verejné a použiteľné? Overiť v kroku 1.
3. Zjednodušiť `data/schema.md` pre pilot? Verzia 0.2 obsahuje polia, ktoré
   pilot nevyužije (napr. úrovne zdrojov, nezávislosť dôkazov).
