# Pravidlá pre AI agentov v tomto repozitári

Projekt: spoľahlivá databáza investorov (VC, PE, family office, angel investori,
veľkí súkromní investori).

Hlavným kritériom je **spoľahlivosť dát**. Radšej chýbajúci údaj ako vymyslený,
neoverený alebo nesprávne interpretovaný údaj.

## 1. Záväzné dokumenty

- Pravidlá zaradenia, vyradenia a overovania investorov určuje
  `plan/research-plan.md`. Pred začatím zberu dát si ho prečítaj.
- Dátovú štruktúru určuje `data/schema.md`. Polia a hodnoty mimo schémy nepridávaj.
- Ak plán chýba alebo je pravidlo nejednoznačné, upozorni na to. Nevytváraj
  vlastné pravidlá bez zdokumentovania rozhodnutia.
- Pri rozpore medzi týmto súborom a plánom má prednosť plán.

## 2. Každý údaj musí mať zdroj

Ku každému faktickému poľu uveď dôkaz podľa `data/schema.md`: hodnotu, presnú
URL, doslovnú citáciu, dátum prístupu, dátum publikovania a typ zdroja.

- **Citácia** musí byť doslovná, **v pôvodnom jazyku zdroja**, bez prekladu,
  skracovania alebo úprav, tak aby sa dala na stránke nájsť vyhľadaním textu.
  Ak je údaj v tabuľke, PDF alebo obrázku, uveď v `locator` stranu, tabuľku
  alebo sekciu.
- **URL** musí byť konkrétna podstránka s dôkazom, nie domovská stránka, ak
  podstránka existuje.
- Jeden zdroj možno použiť pre viac polí, iba ak skutočne podporuje každé z nich.
- Ak zdroj požadovaný údaj neobsahuje, neprezentuj ho ako dôkaz tohto údaja.
- Rozlišuj dátum publikovania zdroja, dátum investície a dátum prístupu k zdroju.
- **Nikdy netvrď, že si URL otvoril, obsah prečítal alebo údaj overil, ak sa to
  v skutočnosti nestalo.**

## 3. Povolené zdroje a hodnotenie ich dôveryhodnosti

Používaj iba verejne dostupné zdroje, ktorých pôvod, obsah a relevantnosť možno
overiť. Nepoužívaj platené databázy ani obsah za paywallom a neobchádzaj
prihlasovanie ani iné prístupové obmedzenia.

### 3.1 Hierarchia zdrojov

**Úroveň 1: Primárne zdroje.** Uprednostňuj ich vždy, keď sú dostupné:

- oficiálne weby investorov a ich portfóliá,
- oficiálne oznámenia investorov a financovaných spoločností,
- tlačové správy a oficiálne oznámenia o investičných kolách,
- verejné regulačné dokumenty a firemné registre,
- verejné dokumenty samotných fondov alebo ich správcov.

**Úroveň 2: Sekundárne zdroje s overiteľným pôvodom.** Použi ich, ak primárny
zdroj nie je dostupný alebo neposkytuje potrebné informácie:

- etablované ekonomické a technologické médiá s redakčnou zodpovednosťou,
- odborné médiá zamerané na startupy, rizikový kapitál alebo private equity,
- odborné publikácie, ktoré uvádzajú autora, dátum publikovania a konkrétne
  zdroje svojich tvrdení.

Príklady médií, ktoré možno pri splnení kritérií v 3.2 zvážiť, sú Reuters,
Bloomberg, Financial Times, CNBC, TechCrunch a Sifted. Samotná značka média
však automaticky nepotvrdzuje správnosť každého článku.

**Úroveň 3: Pomocné zdroje na vyhľadávanie kandidátov.** Patria sem verejné
adresáre investorov, agregátory financovania, databázy startupov, profily na
sociálnych sieťach a neoverené zoznamy.

Používaj ich na vyhľadávanie kandidátov alebo dohľadávanie pôvodných zdrojov.
Samy osebe nestačia na potvrdenie investora, investičnej transakcie ani
finančných údajov, pokiaľ ich metodika a pôvod konkrétneho údaja nie sú
nezávisle overiteľné.

### 3.2 Kritériá dôveryhodnosti

Pred použitím sekundárneho zdroja skontroluj:

1. **Identifikovateľný pôvod:** Je jasné, kto obsah publikoval a na akej stránke?
2. **Autorstvo a zodpovednosť:** Je uvedený autor, redakcia alebo organizácia
   zodpovedná za obsah?
3. **Dátum:** Je známy dátum publikovania alebo aktualizácie a je zdroj
   primerane aktuálny pre dané tvrdenie?
4. **Konkrétnosť:** Uvádza zdroj konkrétneho investora, financovanú spoločnosť,
   transakciu alebo finančný údaj?
5. **Doložiteľnosť:** Odkazuje na pôvodné oznámenie, dokument alebo inú
   overiteľnú evidenciu, prípadne uvádza jasný základ svojho tvrdenia?
6. **Nezávislé potvrdenie:** Možno dôležité tvrdenie potvrdiť ďalším
   nezávislým zdrojom?

Ak zdroj nespĺňa základné kritériá pôvodu, konkrétnosti a doložiteľnosti,
nepoužívaj ho ako dôkaz.

### 3.3 Pravidlá použitia

- Primárny zdroj má prednosť pred sekundárnym, ak oba priamo a jednoznačne
  potvrdzujú rovnaké tvrdenie.
- Ak primárny zdroj nie je dostupný, možno použiť kvalitný sekundárny zdroj,
  ale jeho typ a obmedzenia musia byť zaznamenané.
- Ak agregátor preberá informáciu z pôvodného zdroja, dohľadaj a cituj pôvodný
  zdroj.
- Pri významných finančných údajoch, sporných tvrdeniach alebo nejednoznačnej
  identite vyhľadaj nezávislé potvrdenie, ak je dostupné.
- Dva články preberajúce rovnakú tlačovú správu sa nepovažujú za dva nezávislé
  dôkazy.
- Ak dôveryhodnosť alebo relevantnosť zdroja nemožno posúdiť, označ údaj ako
  neoverený a vysvetli dôvod v `notes`.
- Nikdy nevymýšľaj hodnotenie dôveryhodnosti ani netvrď, že nezávislé
  potvrdenie existuje, ak si ho nenašiel.

## 4. Nehádaj, nevymýšľaj, priznaj neistotu

- Ak údaj nevieš doložiť verejným zdrojom, zapíš `value: null` a v `notes`
  uveď, čo bolo hľadané a čo sa nepodarilo overiť.
- Neodhaduj z dojmu investičné sumy, AUM, sektory, investičné fázy ani iné
  vlastnosti investora. Odhad nevydávaj za fakt.
- Nezamieňaj neznámy údaj s nulovou hodnotou. Neprítomnosť informácie
  v zdroji neznamená, že daná vlastnosť neexistuje.
- **Rozpor medzi zdrojmi:** zachovaj všetky tvrdenia s ich citáciami a dátumami
  a označ pole ako `v_rozpore`. Nerozhoduj sám, ktorý zdroj má pravdu,
  a rozpor nerieš odhadom.

## 5. Dôkaz investičnej činnosti

- Subjekt nemožno označiť za investora, kým nemá aspoň jeden dôveryhodný
  verejný dôkaz skutočnej investície. Samotné označenie subjektu ako VC, PE,
  family office alebo angel investora nestačí.
- Dôkaz investície **musí** obsahovať:
  - investora,
  - financovanú spoločnosť alebo transakciu,
  - zdroj, z ktorého je zrejmá súvislosť medzi investorom a investíciou.
- Dátum investície alebo oznámenia uveď vždy, keď je dostupný. Dôkaz bez
  dátumu nestačí na preukázanie **aktuálnej** činnosti.
- Za aktívneho investora sa subjekt považuje, iba ak má doloženú investíciu
  v časovom okne, ktoré určuje `plan/research-plan.md`. Staršie investície
  zaznamenaj, ale subjekt bez aktuálnej investície neoznačuj ako aktívny.
- Nezamieňaj investora s poradcom, sprostredkovateľom, akcelerátorom alebo
  poskytovateľom služieb bez doloženej vlastnej investičnej činnosti.
- Ak nemožno jednoznačne potvrdiť identitu alebo investíciu, označ prípad ako
  nejasný alebo navrhni vyradenie podľa pravidiel v pláne.

## 6. Finančné ukazovatele

Nasledujúce pojmy nie sú zameniteľné:

- `ticket_size`: typická výška jednej investície,
- `fund_size`: veľkosť konkrétneho investičného fondu,
- `aum`: aktíva alebo kapitál v správe,
- `deployable_capital`: kapitál dostupný na ďalšie investície.

Pravidlá:

- Pri každom finančnom údaji zaznamenaj menu, dátum alebo obdobie, ktorého sa
  hodnota týka, a definíciu ukazovateľa, ak ju zdroj uvádza.
- Nezamieňaj celkovú hodnotu investičného kola s podielom konkrétneho investora.
- Neodvodzuj typickú výšku investície z jediného obchodu.
- Neprepočítavaj meny. Hodnotu zapíš v mene, v ktorej ju uvádza zdroj.

## 7. Duplicity a identita

- Pred pridaním záznamu skontroluj, či investor už nie je evidovaný pod
  rovnakým alebo alternatívnym názvom, inou doménou alebo názvom materskej či
  správcovskej spoločnosti.
- Nespájaj automaticky podobne pomenované subjekty. Over, či ide o tú istú
  organizáciu, samostatný fond alebo odlišnú právnickú osobu.
- Ak vzťah medzi subjektmi nie je jasný, zdokumentuj neistotu a nevytváraj
  duplicitný záznam bez odôvodnenia.

## 8. Práca so súbormi a skriptami

- `data/raw/` obsahuje neoverené údaje a návrhy od AI agentov. Sem zapisuj
  všetky nové aj opravené záznamy.
- `data/verified/` obsahuje záznamy schválené po ľudskej kontrole. **Tieto
  súbory nikdy neupravuj ani neprepisuj**, a to ani skriptom.
- Pred zápisom skontroluj súlad so schémou a možné duplicity.
- Skripty patria do `scripts/`. Musia mať jasný účel, zdokumentovaný spôsob
  spustenia a opakované spustenie nesmie vytvárať duplicity.
- Ak skript narazí na chybu alebo nedostupný zdroj, zaznamenaj problém, nepreskakuj
  ho potichu.
- Vždy rozlišuj automatické výsledky od ručne overených.

## 9. Kontrola kvality

Automatické kontroly nenahrádzajú ľudské overenie faktických tvrdení. Pred
označením záznamu za pripravený na ručné overenie skontroluj:

- identitu a typ investora,
- existenciu dôkazu investičnej činnosti,
- relevantnosť a dostupnosť zdrojových URL,
- súlad citácií so skutočným obsahom zdrojov,
- správnosť hodnôt a dátumov,
- rozlíšenie finančných ukazovateľov,
- možné duplicity a rozpory,
- súlad so schémou.

## 10. Denník chýb AI

- Do `notes/chyby-ai.md` zapisuj iba chyby, ktoré si **preukázateľne zistil**
  (napr. automatickou kontrolou citácií alebo URL), a vyplň stĺpec „Kto
  zistil“. Chyby zistené človekom zapisuje človek.
- Záznam má podľa dostupnosti obsahovať dátum, dotknutý súbor alebo záznam,
  typ chyby, nesprávne tvrdenie, výsledok overenia, dôkaz opravy a prijaté
  opatrenie.
- Sleduj najmä vymyslené URL, neexistujúce alebo nesprávne citácie, zastarané
  údaje, zámenu identity, nesprávny typ investora a nepodložené finančné odhady.

## 11. Presnosť a odhady

- Nevydávaj plánované hodnoty za namerané výsledky.
- Presnosť vypočítaj až po zdokumentovanom ručnom overení vzorky.
- Uveď počet skontrolovaných, správnych, nesprávnych a nerozhodnuteľných prípadov.
- Rozlišuj správnosť zaradenia investora od správnosti jednotlivých údajov.
- Globálny rozsah databázy a náklady na rozšírenie uvádzaj ako odhady
  s vysvetlenými predpokladmi, zdrojmi a obmedzeniami.
- Výsledky pilotnej vzorky neprezentuj ako dôkaz presnosti pre všetky typy
  investorov alebo celý svet.

## 12. Dokumentácia

- Texty pre hodnotiteľa (README, plán) píš po slovensky.
- Dôležité rozhodnutia a ich zdôvodnenia zaznamenaj v príslušných dokumentoch.
- V README jasne uveď, čo je hotové, čo je rozpracované a čo chýba. Neskracuj
  si prácu potichu: ak úlohu nestihneš celú, presne uveď, čo zostáva.
- Po práci s Claude Code exportuj konverzáciu podľa `ai-log/README.md`.

## Základný princíp

Každý zaradený investor musí mať overiteľnú identitu a dôkaz investičnej
činnosti. Každé faktické tvrdenie musí mať relevantný zdroj. Každá neistota
musí byť priznaná a každý nameraný výsledok musí byť reprodukovateľný.
