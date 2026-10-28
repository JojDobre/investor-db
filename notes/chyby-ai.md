# Denník chýb AI

Zapisovať priebežne, hneď keď na chybu narazím. Slúži ako podklad pre časť
„Ako som pracoval s AI“ v README.

| Dátum | Krok / súbor | Typ chyby | Čo AI tvrdila | Kto zistil (človek / skript / agent) | Ako sa to zistilo | Oprava / zmena postupu |
|---|---|---|---|---|---|---|
| 2026-10-25 | plan/zdroje-kandidatov.md | nekonzistentný súhrn | Súhrn webového vyhľadávania uviedol, že SLOVCA má „osem riadnych členov“, a hneď vymenoval 12. | agent | porovnanie počtu so zoznamom v tom istom výstupe | do zistení zapísaný vymenovaný zoznam (12) s označením „neoverené“; počet overiť na webe SLOVCA |
| 2026-10-26 | data/raw/cz-credo-ventures.json, `ticket_size` | prehliadnutý údaj | „Web výšku investície neuvádza“ | kontrolný agent | agent našiel na domovskej stránke „$1M - $5M checks.“; overil som v stiahnutom HTML | záznam v `data/raw/` nechávam ako výstup AI kvôli meraniu, oprava pri ručnej kontrole; do pokynu `zber.md` doplniť „prečítaj celú domovskú stránku“ |
| 2026-10-26 | data/raw/cz-credo-ventures.json, investícia Supernova | upravená citácia | citácia „Taiwania Capital , with participation…“ (medzera navyše) | kontrolný agent, potom skript v2 | na stránke je „Taiwania Capital, with“; skript v1 chybu prepustil, lebo pri prevode HTML vkladal medzery na miesto značiek | `check_sources.py`: inline značky sa odstraňujú bez medzery, po úprave skript chybu hlási |
| 2026-10-26 | data/raw/cz-depo-ventures.json, `ticket_size` (dôkaz CVCA) | zlý dátum zdroja | `published: 2023-01-12` | kontrolný agent | v HTML je 12. 1. 2023 označený ako `dateModified`; profil bol publikovaný 23. 1. 2020; overil som | pri ručnej kontrole opraviť; v pokyne rozlišovať dátum publikovania a úpravy |
| 2026-10-26 | data/raw/sk-venture-to-future-fund.json, `fund_size` | nadhodnotený stav | `status: dolozene` pre „vyčlenených 55 mil. EUR“ | kontrolný agent | zdroj neuvádza veľkosť fondu, iba vyčlenené prostriedky; správu o navýšení o 15,3 mil. EUR (28. 5. 2024) AI nečítala; overil som, že správa existuje | pri ručnej kontrole rozhodnúť `nedolozene` alebo `v_rozpore`; interpretáciu neoznačovať ako `dolozene` |
| 2026-10-26 | data/raw/cz-credo-ventures.json, `stages` | interpretácia | hodnota „a neskôr“ z „Pre-seed — Onwards“ | kontrolný agent | hodnota je preklad, nie fáza zo zdroja | pri ručnej kontrole ponechať iba `pre-seed` |

## Typy chýb (dopĺňať)

- vymyslená alebo nefunkčná URL
- citácia, ktorá na stránke nie je
- zastaraný údaj (napr. starý fond, ktorý už neinvestuje)
- nesprávny typ subjektu (poradca/sprostredkovateľ označený ako investor)
- odhad namiesto doloženého údaja
