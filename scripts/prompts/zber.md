# Pokyn pre zber (AI workflow 1) – v2

Zmeny oproti v1 (po teste na 3 investoroch, 2026-10-26): body 4–6.

Použitie: jeden subagent na jedného kandidáta z `data/raw/candidates.csv`.
Pred spustením nahraď `<KANDIDÁT>` a `<DÁTUM_KONTROLY>`.

---

Vytvor záznam investora **<KANDIDÁT>** podľa `data/schema.md` a ulož ho do
`data/raw/<id>.json`. Dodrž `CLAUDE.md` a pravidlá Z/V/N z
`plan/research-plan.md`. Časové okno: 24 mesiacov pred <DÁTUM_KONTROLY>.

Postup:
1. Nájdi oficiálny web. Zo stránky kontakt alebo o nás zapíš krajinu sídla
   a IČO, ak sú uvedené.
2. Typ, fázy, sektory a ticket ber z webu investora. Profil v asociácii
   (CVCA, SLOVCA) je `source_type: other` a sám nestačí.
3. Investíciu v okne hľadaj v sekcii noviniek investora, potom v oznámení
   financovanej firmy alebo v médiu. Zdroj musí menovať investora aj firmu.
4. Pri investícii zapíš oddelene dátum oznámenia kola (`announced`)
   a dátum uzavretia (`closed`), ak ho zdroj výslovne uvádza. Dátum
   článku (`published`) nie je dátum uzavretia.
5. Ak je hodnota tvoj výklad zdroja (preklad, zaradenie do fázy,
   „vyčlenené prostriedky“ ako veľkosť fondu), použi stav `neiste`, nie `dolozene`.
6. Prečítaj celú stránku zdroja vrátane päty a zoznamov s odrážkami,
   než napíšeš, že údaj na nej nie je.
7. Citácie kopíruj zo stránky doslovne. Ak si stránku neotvoril, nepoužívaj ju.
8. Čo nenájdeš, nechaj `null` a do `notes` napíš, kde si hľadal.
9. Navrhni `inclusion` s `decided_by: agent`.

Na konci vypíš: zoznam otvorených URL, polia, ktoré zostali prázdne,
a všetko, čím si si nebol istý.
