# Pravidlá pre AI agentov v tomto repozitári

Projekt: spoľahlivá databáza investorov (VC, PE, family office, angel investori, veľkí súkromní investori). 

Hlavným kritériom je **spoľahlivosť dát**. Radšej chýbajúci údaj ako vymyslený, neoverený alebo nesprávne interpretovaný údaj.

## Záväzné pravidlá projektu
- Pred začatím zberu dát skontroluj `plan/research-plan.md`, ak existuje.
- Dodržuj schválené pravidlá zaradenia, vyradenia a overovania investorov.
- Dátovú štruktúru určuje `data/schema.md`.
- Ak plán chýba alebo sú pravidlá nejednoznačné, upozorni na problém a nevytváraj vlastné pravidlá bez zdokumentovania rozhodnutia.
- Pri rozpore medzi zdrojmi zachovaj dôkazy a zdokumentuj neistotu. Nerozhoduj svojvoľne, ktorý zdroj má pravdu.


## Tvrdé pravidlá pri zbere dát
1. **Každý údaj musí mať zdroj.** Ku každému poľu uveď:
   - `value`: doloženú hodnotu alebo null, ak ju nemožno overiť,
   - `url`: presná adresa stránky, kde je údaj uvedený (nie len doména),
   - `quote`: doslovná citácia zo stránky, ktorá údaj dokladá (bez parafrázovania, skopírovaná tak, aby sa dala nájsť na stránke vyhľadaním textu),
   - `accessed`: dátum, kedy si zdroj čítal (YYYY-MM-DD),
   - `published`: dátum publikovania zdroja, ak je uvedený, inak `null`,
   - `source_type`: typ zdroja, napríklad oficiálny web investora, oznámenie startupu, regulačný dokument alebo dôveryhodné médium.
2. **Nehádaj. Nevymýšľaj.** Ak údaj nevieš doložiť verejným zdrojom:
   - zapíš value na `null`,
   - do `notes` uveď, čo sa nepodarilo overiť a čo bolo hľadané,
   - nevypĺňaj chýbajúcu hodnotu odhadom vydávaným za fakt.
   - Neodhaduj z dojmu investičné sumy, AUM, sektory, investičné fázy ani iné vlastnosti investora.
   - Nezamieňaj neznámy údaj s nulovou hodnotou. Neprítomnosť informácie v zdroji neznamená, že daná vlastnosť neexistuje.
3. **Iba verejné a dôveryhodné zdroje** Nepoužívaj platené databázy ani informácie dostupné iba za paywallom, neobchádzaj prihlasovacie alebo iné prístupové obmedzenia a nepoužívaj neoverené agregátory ako jediný dôkaz. Uprednostňuj primárny zdroj. Ak agregátor uvádza informáciu získanú z pôvodného zdroja, pokús sa overiť a citovať pôvodný zdroj.
   Povolené zdroje:
   - oficiálne weby investorov a ich portfóliá,
   - oficiálne oznámenia investorov a financovaných spoločností,
   - verejné regulačné a firemné dokumenty,
   - dôveryhodné médiá,
   - verejné adresáre, ak možno overiť pôvod ich tvrdení.
4. **Dôkaz investovania.** Subjekt sa nepovažuje za investora, kým nemá aspoň jeden doložený deal (portfóliová firma + dátum + zdroj). Presné pravidlá zaradenia sú v `plan/` (po ich spísaní majú prednosť pred touto poznámkou).
5. **Over existenciu investičnej činnosti.**
   - Subjekt nemožno označiť za overeného investora, kým neexistuje aspoň jeden dôveryhodný verejný dôkaz skutočnej investície
   - Dôkaz musí podľa dostupnosti identifikovať:
        - investora,
        - financovanú spoločnosť alebo transakciu,
        - súvislosť medzi investorom a investíciou,
        - dátum investície alebo oznámenia, ak je dostupný,
        - zdroj, ktorý tieto informácie potvrdzuje.
   - Samotné označenie subjektu ako VC, PE, family office alebo angel investora nestačí.
   - Nezamieňaj investora s poradcom, sprostredkovateľom, akcelerátorom alebo poskytovateľom služieb bez doloženej vlastnej investičnej činnosti.
   - Ak nemožno jednoznačne potvrdiť identitu alebo investíciu, označ prípad ako nejasný alebo navrhni vyradenie podľa pravidiel v plan/research-plan.md.
6. **Rozlišuj finančné ukazovatele.**
   - Nasledujúce pojmy nie sú zameniteľné:
        - ticket_size: typická výška jednej investície.
        - fund_size: veľkosť konkrétneho investičného fondu.
        - AUM: aktíva alebo kapitál v správe.
        - deployable_capital: kapitál dostupný na ďalšie investície.
   - Pri finančných údajoch zaznamenaj menu, dátum alebo obdobie, ktorého sa hodnota týka, a definíciu ukazovateľa, ak je dostupná.
   - Nezamieňaj celkovú hodnotu investičného kola s podielom konkrétneho investora. Neodvodzuj typickú výšku investície z jediného obchodu.
   - Ak zdroje uvádzajú rozdielne hodnoty, zaznamenaj obe aj s príslušnými zdrojmi a dátumami.
7. **Kontroluj duplicity a identitu**
   - Pred pridaním záznamu skontroluj, či už investor nie je v databáze evidovaný pod:
      - rovnakým názvom,
      - alternatívnym názvom,
      - inou doménou,
      - názvom materskej alebo správcovskej spoločnosti.
   - Nespájaj automaticky podobne pomenované subjekty. Over, či ide o tú istú organizáciu, samostatný fond alebo odlišnú právnickú osobu.
   - Ak vzťah medzi subjektmi nie je jasný, zdokumentuj neistotu a nevytváraj duplicitný záznam bez odôvodnenia.
8. **Nemeň ručne overené záznamy.** Súbory v `data/verified/` upravuje iba človek. Agenti zapisujú do `data/raw/`.
9. **Hlás neistotu.** Ak sú zdroje v rozpore (napr. dva rôzne AUM), uveď oba a nevyberaj sám.

## Pravidlá pre zdroje:
- Každé pole musí mať vlastný relevantný dôkaz. Jeden zdroj možno použiť pre viac polí iba vtedy, ak skutočne podporuje každé z nich.
- Citácie musia zodpovedať skutočnému obsahu stránky. Nesmú byť parafrázované ani vymyslené.
- Nepoužívaj iba domovskú stránku, ak existuje konkrétna podstránka s dôkazom.
- Nikdy netvrď, že si URL otvoril, obsah prečítal alebo údaj overil, ak sa to v skutočnosti nestalo.
- Rozlišuj dátum publikovania, dátum investície a dátum prístupu k zdroju.
- Ak zdroj neposkytuje požadovaný údaj, neprezentuj ho ako dôkaz tohto údaja.

## Pracovné pravidlá
- Výstupy pre dáta píš ako JSON/CSV podľa schémy v `data/schema.md`.
- `data/raw/` obsahuje neoverené údaje a návrhy vytvorené AI agentmi.
- `data/verified/` obsahuje záznamy schválené po ľudskej kontrole.
- **Nikdy neupravuj ani neprepisuj súbory** v `data/verified/`. Nové alebo opravené návrhy zapisuj do `data/raw/`.
- Skripty patria do `scripts/`, musia sa dať spustiť znova a nesmú prepisovať ručne overené dáta.
- Texty pre hodnotiteľa (README, plán) píš po slovensky.
- Neskracuj si prácu: ak úlohu nestihneš celú, napíš presne, čo chýba.
- Pred zápisom skontroluj súlad so schémou a existujúce duplicity.
- Zachovávaj pôvod údajov a ich zdroje.
- Pred zápisom skontroluj súlad so schémou a existujúce duplicity.

10. **Kontrola kvality.** Automatické kontroly nenahrádzajú ľudské overenie faktických tvrdení. Pred označením záznamu za pripravený na ručné overenie skontroluj:
    - Identitu a typ investora.
    - Existenciu dôkazu investičnej činnosti.
    - Relevantnosť a dostupnosť zdrojových URL.
    - Súlad citácií so skutočným obsahom zdrojov.
    - Správnosť hodnôt a dátumov.
    - Rozlíšenie finančných ukazovateľov.
    - Možné duplicity a rozpory.
    - Súlad so schémou.

11. **Dokumentovanie chýb AI**
    - Ak zistíš chybu AI, zaznamenaj ju do notes/chyby-ai.md. Záznam má podľa dostupnosti obsahovať:
        - dátum zistenia,
        - súbor alebo záznam, ktorého sa chyba týka,
        - typ chyby,
        - nesprávne tvrdenie,
        - výsledok overenia,
        - zdroj alebo dôkaz opravy,
        - prijaté nápravné opatrenie.
    - Sleduj najmä vymyslené URL, neexistujúce alebo nesprávne citácie, zastarané údaje, zámenu identity, nesprávny typ investora a nepodložené finančné odhady.
   
12. **Skripty a reprodukovateľnosť**
   - Skripty patria do scripts/.
   - Skripty musia mať jasný účel a zdokumentovaný spôsob spustenia.
   - Opakované spustenie nesmie vytvárať neodôvodnené duplicity.
   - Skripty nesmú meniť ani prepisovať ručne overené dáta.
   - Pri chybách alebo nedostupných zdrojoch zaznamenaj problém namiesto tichého preskočenia.
   - Rozlišuj automatické výsledky od ručne overených výsledkov.

13. **Presnosť a odhady**
   - Nevydávaj plánované hodnoty za namerané výsledky.
   - Presnosť vypočítaj až po zdokumentovanom overení vzorky.
   - Uveď počet skontrolovaných, správnych, nesprávnych a nerozhodnuteľných prípadov.
   - Rozlišuj správnosť zaradenia investora od správnosti jednotlivých údajov.
   - Globálny rozsah databázy a náklady na rozšírenie uvádzaj ako odhady s vysvetlenými predpokladmi, zdrojmi a obmedzeniami.
   - Výsledky pilotnej vzorky neprezentuj ako dôkaz presnosti pre všetky typy investorov alebo celý svet.

14. **Dokumentácia a komunikácia**
   - Texty určené hodnotiteľovi, najmä README a plán, píš po slovensky.
   - Dôležité rozhodnutia a ich zdôvodnenia zaznamenaj v príslušných dokumentoch.
   - V README jasne uveď, čo je hotové, čo je rozpracované a čo chýba.
   - Ak úlohu nedokončíš celú, presne uveď, ktoré časti zostávajú nedokončené.
   - Po práci s Claude Code exportuj konverzáciu podľa pokynov v ai-log/README.md.

## Základný princíp
Každý zaradený investor musí mať overiteľnú identitu a dôkaz investičnej činnosti. Každé faktické tvrdenie musí mať relevantný zdroj. Každá neistota musí byť priznaná a každý nameraný výsledok musí byť reprodukovateľný.
