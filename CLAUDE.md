# Pravidlá pre AI agentov v tomto repozitári

Projekt: spoľahlivá databáza investorov (VC, PE, family office, angel investori,
veľkí súkromní investori). Hlavné kritérium je **spoľahlivosť dát**: radšej
chýbajúci údaj ako vymyslený.

## Tvrdé pravidlá pri zbere dát

1. **Každý údaj musí mať zdroj.** Ku každému poľu uveď:
   - `url`: presná adresa stránky, kde je údaj uvedený (nie len doména),
   - `quote`: doslovná citácia zo stránky, ktorá údaj dokladá (bez parafrázovania,
     skopírovaná tak, aby sa dala nájsť na stránke vyhľadaním textu),
   - `accessed`: dátum, kedy si zdroj čítal (YYYY-MM-DD),
   - `published`: dátum publikovania zdroja, ak je uvedený, inak `null`.
2. **Nehádaj.** Ak údaj nevieš doložiť verejným zdrojom, zapíš `null` a do
   `notes` uveď, čo si hľadal. Neodhaduj ticket size, AUM ani sektory z dojmu.
3. **Iba verejné zdroje.** Žiadne platené databázy za paywallom, žiadne
   prihlasovanie, žiadne neoverené agregátory bez pôvodného zdroja (ak agregátor
   cituje pôvodný zdroj, uveď ten pôvodný).
4. **Dôkaz investovania.** Subjekt sa nepovažuje za investora, kým nemá aspoň
   jeden doložený deal (portfóliová firma + dátum + zdroj). Presné pravidlá
   zaradenia sú v `plan/` (po ich spísaní majú prednosť pred touto poznámkou).
5. **Nemeň ručne overené záznamy.** Súbory v `data/verified/` upravuje iba
   človek. Agenti zapisujú do `data/raw/`.
6. **Hlás neistotu.** Ak sú zdroje v rozpore (napr. dva rôzne AUM), uveď oba
   a nevyberaj sám.

## Pracovné pravidlá

- Výstupy pre dáta píš ako JSON/CSV podľa schémy v `data/schema.md`.
- Skripty patria do `scripts/`, musia sa dať spustiť znova a nesmú prepisovať
  ručne overené dáta.
- Texty pre hodnotiteľa (README, plán) píš po slovensky.
- Neskracuj si prácu: ak úlohu nestihneš celú, napíš presne, čo chýba.
