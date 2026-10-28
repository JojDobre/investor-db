# Kontrola záznamov pred ručnou kontrolou (2026-10-26)

**Toto nie je výsledok ručnej kontroly.** Ide o zhrnutie automatickej
kontroly (`scripts/check_sources.py`), kontrolného agenta
(`scripts/prompts/kontrola.md`) a mojej kontroly jeho nálezov v
stiahnutých stránkach. Záznamy v `data/raw/` zostávajú nezmenené, ako ich
navrhla AI. Žiadny záznam nie je overený. Návrhy pre `data/verified/`
vzniknú až po ručnej kontrole zapísanej v `results/review.csv`.

Záznamy sú vo formáte schémy v0.3 (`date` + `date_kind`). Prevod na v0.4
je opísaný v `data/schema.md`.

SHA-256 záznamov v čase tejto kontroly (na overenie, že sa nemenili):

| Súbor | SHA-256 |
|---|---|
| `data/raw/cz-credo-ventures.json` | `cfaff790f9dfdc23dfef3ef4a5b5e83ee64e8720ef1b5b4baa736614404a28fb` |
| `data/raw/cz-depo-ventures.json` | `21afa06967a6389af08005ddd5158a67607ec7910b04788358b7af50d46ce215` |
| `data/raw/sk-venture-to-future-fund.json` | `f7017e75cae3eb8236313fa1d4d0011b63c9977c90addeb44ab7d5531edb9493` |

## Zistenia podľa polí

Stĺpec „Návrh na ručnú kontrolu“ hovorí, na čo sa zamerať. Nie je to
rozhodnutie.

### DEPO Ventures (`cz-depo-ventures`)

| Pole | Stav v návrhu AI | Zistenie | Návrh na ručnú kontrolu |
|---|---|---|---|
| investor_type, country, website, registration, sectors, stages | `dolozene` | citácie nájdené, agent: podporuje | potvrdiť |
| ticket_size | `v_rozpore` | dôkaz CVCA má `published: 2023-01-12`, čo je dátum úpravy; publikované 2020-01-23 | opraviť dátum; rozhodnúť, či starý profil (`other`) vôbec počítať ako rozpor |
| fund_size, aum | `nedolozene` | v poznámkach správne odlíšené „investovaný kapitál“ a starý profil CVCA | potvrdiť `nedolozene` |
| deal Tapaya | `date: 2026-04`, `announcement` | článok Vestbee publikovaný 2026-04-29; web DEPO bez dátumu; zdroje sa líšia v úlohe (led / co-led). Mechanický prevod dá `announced: 2026-04`, čo je menej presné, ako dovoľuje zdroj | v0.4: `announced: 2026-04-29` (dátum článku, uviesť v poznámke), `closed: null` |
| inclusion | `zaradeny`, agent | Z1–Z3 podľa agenta aj mňa splnené | rozhodne človek |

### Credo Ventures (`cz-credo-ventures`)

| Pole | Stav v návrhu AI | Zistenie | Návrh na ručnú kontrolu |
|---|---|---|---|
| investor_type | `dolozene` | citácia hovorí „fund“, nie VC. Na domovskej stránke som slovo „venture“ ani „VC“ nenašiel, iba v názve „Credo Ventures“; je tam „● Leading Pre-Seed rounds.“ a „5 Funds“ | **`neiste`**: typ VC je výklad. Rozhodne človek (N1); fond, ktorý vedie pre-seed kolá startupov, zodpovedá definícii VC, ale zdroj to priamo nehovorí |
| country, website | `dolozene` | citácie nájdené; web má aj kanceláriu v Krakove | potvrdiť; sídlo v registri neoverené |
| stages | `dolozene`, hodnota `pre-seed`, `a neskôr` | „a neskôr“ je preklad „Onwards“, nie fáza zo zdroja | hodnota AI je **`neiste`**; pre overený záznam navrhujem `["pre-seed"]` so stavom `dolozene` (citácia „Pre-seed — Onwards.“, v poznámke „Onwards“ bez konkrétnych fáz) |
| ticket_size | `nedolozene` | **chyba AI:** domovská stránka uvádza „$1M - $5M checks.“ | doplniť ako `prehliadnute` |
| registration, sectors, fund_size, aum | `nedolozene` | nekontrolované | pri ručnej kontrole hľadať najviac 5 minút |
| deal Supernova | `date: 2025-09-30`, `announcement` | **chyba AI v citácii:** medzera pred čiarkou; upravený skript ju hlási ako `nenajdene` | opraviť citáciu; v0.4: `announced: 2025-09-30` (dátum článku), `closed: null` |
| inclusion | `zaradeny`, agent | Z1–Z3 splnené aj po oprave citácie | rozhodne človek |

### Venture to Future Fund (`sk-venture-to-future-fund`)

| Pole | Stav v návrhu AI | Zistenie | Návrh na ručnú kontrolu |
|---|---|---|---|
| investor_type, country, website, registration, stages, ticket_size | `dolozene` | citácie nájdené, agent: podporuje | potvrdiť |
| fund_size | `dolozene` | „vyčlenených 55 mil. EUR“ je výklad, nie veľkosť fondu. Správa o navýšení (28. 5. 2024, prečítaná 2026-10-26) uvádza „navýšenie kapitálu o 15,3 milióna eur“ a predĺženie investičného obdobia, celkovú veľkosť fondu ani to, či je navýšenie v 55 mil. EUR zahrnuté, neuvádza | **`neiste`**: zdroj existuje, ale hodnota je výklad (schéma v0.4) |
| sectors, aum | `nedolozene` | web konkrétne sektory ani AUM neuvádza | potvrdiť |
| deal NETGRIF | `date: 2024-11-12`, `announcement` | „dnes oznámila“ v texte s dátumom 12. novembra 2024 | v0.4: `announced: 2024-11-12`, `closed: null` |
| deal Patron GO | `date: 2024-08-12` | mimo okna, iba história | ponechať ako históriu |
| inclusion | `zaradeny`, agent | hraničné: jediné oznámenie v okne, 17 dní po jeho začiatku | rozhodne človek |

## Čo sa z tejto kontroly nedá vyvodiť

- Presnosť zberu. Tá sa počíta až z dokončenej ručnej kontroly.
- Že polia bez nálezu sú správne. Kontrolný agent videl celé záznamy
  vrátane poznámok AI, preto jeho kontrola nebola úplne nezávislá.
