# Dátová schéma záznamu investora

Verzia schémy: **0.2** (zmeny oproti verzii 0.1: finančné ukazovatele rozdelené
na `ticket_size`, `fund_size`, `aum` a `deployable_capital`, pridaný typ
a úroveň zdroja, stav poľa, viacero dôkazov na pole a evidencia rozporov).

Pravidlá zaradenia a časové okno aktivity určuje `plan/research-plan.md`.
Pravidlá práce so zdrojmi sú v `CLAUDE.md`, sekcie 2 až 4.

## Ukladanie

- Jeden investor = jeden súbor `data/raw/<id>.json` (neoverené návrhy od AI).
- Po ručnej kontrole človek uloží schválenú verziu do `data/verified/<id>.json`.
- `id` je malými písmenami, bez diakritiky, slová oddelené pomlčkou, s kódom
  krajiny: `cz-example-ventures`.
- Kódovanie UTF-8, dátumy vo formáte `YYYY-MM-DD`, meny podľa ISO 4217
  (`EUR`, `CZK`, `USD`), krajiny podľa ISO 3166-1 alpha-2 (`CZ`, `SK`).

## Stavebné prvky

### Dôkaz (`Evidence`)

Jeden zdroj, ktorý dokladá jedno tvrdenie.

| Pole | Typ | Povinné | Popis |
|---|---|---|---|
| `claimed_value` | podľa poľa | áno | hodnota, ktorú tvrdí práve tento zdroj |
| `url` | string | áno | presná podstránka s dôkazom |
| `quote` | string | áno | doslovná citácia v pôvodnom jazyku, bez úprav |
| `quote_lang` | string | áno | jazyk citácie (`cs`, `sk`, `en`, ...) |
| `locator` | string / null | nie | strana, tabuľka alebo sekcia pri PDF, tabuľke či obrázku |
| `accessed` | date | áno | dátum, kedy bol zdroj skutočne otvorený a prečítaný |
| `published` | date / null | áno | dátum publikovania alebo aktualizácie zdroja, ak je uvedený |
| `source_type` | enum | áno | typ zdroja, pozri nižšie |
| `source_level` | 1 / 2 / 3 | áno | úroveň podľa `CLAUDE.md` 3.1 |
| `independent_of` | string / null | nie | URL pôvodnej tlačovej správy, ak zdroj iba preberá jej obsah (takýto dôkaz sa nepočíta ako nezávislý) |

**`source_type`** (v zátvorke úroveň):

| Hodnota | Popis | Úroveň |
|---|---|---|
| `investor_website` | oficiálny web investora | 1 |
| `investor_portfolio` | portfólio na webe investora | 1 |
| `investor_announcement` | oznámenie alebo tlačová správa investora | 1 |
| `company_announcement` | oznámenie financovanej spoločnosti | 1 |
| `regulatory_filing` | regulačný dokument (napr. register ČNB, NBS, SEC) | 1 |
| `company_register` | obchodný register a zbierka listín | 1 |
| `fund_document` | verejný dokument fondu alebo jeho správcu (výročná správa, factsheet) | 1 |
| `media` | ekonomické alebo technologické médium s redakčnou zodpovednosťou | 2 |
| `specialized_media` | odborné médium o startupoch, VC alebo PE | 2 |
| `publication` | odborná publikácia s autorom, dátumom a zdrojmi (napr. správa asociácie) | 2 |
| `directory` | verejný adresár investorov | 3 |
| `aggregator` | agregátor financovania alebo databáza startupov | 3 |
| `social` | profil na sociálnej sieti | 3 |
| `other` | iné, dôvod uviesť v `notes` poľa | 3 |

### Pole s dôkazmi (`Field`)

Každé faktické pole záznamu má tento tvar:

| Pole | Typ | Popis |
|---|---|---|
| `value` | podľa poľa / null | prijatá hodnota; `null`, ak nie je doložená alebo je v rozpore |
| `status` | enum | `dolozene`, `nedolozene`, `v_rozpore` |
| `evidence` | Evidence[] | všetky nájdené dôkazy, aj protichodné |
| `notes` | string | čo sa hľadalo, obmedzenia zdroja, dôvod rozporu |

Pravidlá pre `status`:

- `dolozene`: aspoň jeden dôkaz úrovne 1 alebo 2 podporuje `value` a žiadny
  dôveryhodný dôkaz mu neprotirečí. Dôkazy úrovne 3 samy nestačia.
- `nedolozene`: `value` je `null`, `evidence` môže byť prázdne; v `notes` je,
  čo sa hľadalo.
- `v_rozpore`: zdroje uvádzajú rôzne hodnoty; `value` je `null`, všetky
  tvrdenia zostávajú v `evidence` s vlastným `claimed_value`.

### Peňažná suma (`Money`)

Používa sa ako `value` finančných polí.

| Pole | Typ | Popis |
|---|---|---|
| `amount` | number / null | presná suma, ak ju zdroj uvádza ako jedno číslo |
| `min` | number / null | dolná hranica rozpätia |
| `max` | number / null | horná hranica rozpätia |
| `currency` | string | mena podľa zdroja, bez prepočtu |
| `as_of` | date / string / null | dátum alebo obdobie, ku ktorému sa suma vzťahuje |
| `definition` | string / null | ako zdroj ukazovateľ definuje, ak to uvádza |

Vypĺňa sa buď `amount`, alebo `min` a `max`. Hodnoty sú v celých jednotkách
meny (10 mil. EUR = `10000000`).

## Záznam investora

| Pole | Typ | Popis |
|---|---|---|
| `schema_version` | string | `"0.2"` |
| `id` | string | identifikátor podľa pravidiel vyššie |
| `name` | string | hlavný názov investora |
| `alt_names` | string[] | iné názvy, skratky, staré názvy (kvôli duplicitám) |
| `domains` | string[] | všetky známe domény (kvôli duplicitám) |
| `legal_entity` | Field\<string\> | právnická osoba a IČO / registračné číslo |
| `investor_type` | Field\<enum\> | `vc`, `pe`, `family_office`, `angel`, `private_investor`, `cvc`, `other` |
| `country` | Field\<string\> | krajina sídla (ISO kód) |
| `website` | Field\<string\> | oficiálny web |
| `related_entities` | RelatedEntity[] | správcovská/materská spoločnosť, jednotlivé fondy |
| `sectors` | Field\<string[]\> | sektory, do ktorých investuje, podľa formulácie zdroja |
| `stages` | Field\<string[]\> | `pre_seed`, `seed`, `series_a`, `series_b_plus`, `growth`, `buyout`, `other` |
| `geography` | Field\<string[]\> | krajiny alebo regióny, kam investuje |
| `ticket_size` | Field\<Money\> | typická výška jednej investície |
| `fund_size` | FundSize[] | veľkosť jednotlivých fondov |
| `aum` | Field\<Money\> | kapitál v správe |
| `deployable_capital` | Field\<Money\> | kapitál dostupný na ďalšie investície |
| `deals` | Deal[] | doložené investície |
| `last_deal_date` | date / null | dátum najnovšej doloženej investície (odvodené z `deals`) |
| `inclusion` | Inclusion | rozhodnutie o zaradení |
| `qa` | QA | výsledky automatických kontrol |
| `created` | date | kedy záznam vznikol |
| `updated` | date | posledná zmena |
| `notes` | string | poznámky k záznamu ako celku |

### `RelatedEntity`

| Pole | Typ | Popis |
|---|---|---|
| `name` | string | názov súvisiaceho subjektu |
| `relation` | enum | `manager`, `parent`, `fund`, `subsidiary`, `other` |
| `record_id` | string / null | `id` záznamu, ak je subjekt v databáze samostatne |
| `evidence` | Evidence[] | dôkaz vzťahu |

### `FundSize`

| Pole | Typ | Popis |
|---|---|---|
| `fund_name` | string | názov fondu |
| `vintage` | number / null | rok vzniku alebo prvého uzavretia |
| `size` | Field\<Money\> | veľkosť fondu; `definition` rozlišuje cieľovú a uzavretú veľkosť |

### `Deal`

| Pole | Typ | Popis |
|---|---|---|
| `company` | string | financovaná spoločnosť |
| `company_website` | string / null | web spoločnosti |
| `round` | string / null | typ kola podľa zdroja (seed, Series A, ...) |
| `deal_date` | date / null | dátum investície alebo jej oznámenia |
| `date_kind` | enum | `investment` (dátum investície) alebo `announcement` (dátum oznámenia) |
| `round_amount` | Money / null | **celková** veľkosť kola, nie podiel investora |
| `investor_role` | enum | `lead`, `co_investor`, `unknown` |
| `evidence` | Evidence[] | dôkaz; musí byť zrejmá súvislosť investora s investíciou |

Dôkaz investície musí obsahovať investora, financovanú spoločnosť a zdroj,
z ktorého je zrejmá ich súvislosť (`CLAUDE.md` sekcia 5).

### `Inclusion`

| Pole | Typ | Popis |
|---|---|---|
| `decision` | enum | `zaradeny`, `vyradeny`, `nejasny` |
| `rule` | string | pravidlo z `plan/research-plan.md`, podľa ktorého sa rozhodlo |
| `reason` | string | zdôvodnenie konkrétneho prípadu |
| `active` | boolean / null | má doloženú investíciu v časovom okne plánu |
| `decided_by` | enum | `agent` (návrh v `data/raw/`) alebo `human` (v `data/verified/`) |

### `QA`

Iba výsledky **automatických** kontrol. Ručné overenie sa eviduje prenesením
záznamu do `data/verified/` a vo výsledkoch merania presnosti.

| Pole | Typ | Popis |
|---|---|---|
| `checked_at` | date / null | kedy kontrola bežala |
| `urls_ok` | boolean / null | všetky URL sú dostupné |
| `quotes_found` | boolean / null | všetky citácie sa našli na stránkach |
| `schema_valid` | boolean / null | záznam zodpovedá schéme |
| `duplicate_candidates` | string[] | `id` možných duplicít |
| `issues` | string[] | zoznam zistených problémov |

## Príklad

Ilustračný záznam. Názvy, URL a hodnoty sú **vymyslené** a slúžia iba na
ukážku formátu.

```json
{
  "schema_version": "0.2",
  "id": "cz-example-ventures",
  "name": "Example Ventures",
  "alt_names": ["Example Ventures Fund I"],
  "domains": ["example.com"],
  "legal_entity": {
    "value": "Example Ventures s.r.o., IČO 00000000",
    "status": "dolozene",
    "evidence": [{
      "claimed_value": "Example Ventures s.r.o., IČO 00000000",
      "url": "https://example.com/register/00000000",
      "quote": "Example Ventures s.r.o., IČO: 00000000",
      "quote_lang": "cs",
      "locator": null,
      "accessed": "2026-10-25",
      "published": null,
      "source_type": "company_register",
      "source_level": 1,
      "independent_of": null
    }],
    "notes": ""
  },
  "investor_type": {
    "value": "vc",
    "status": "dolozene",
    "evidence": [{
      "claimed_value": "vc",
      "url": "https://example.com/about",
      "quote": "Jsme fond rizikového kapitálu zaměřený na rané fáze.",
      "quote_lang": "cs",
      "locator": null,
      "accessed": "2026-10-25",
      "published": null,
      "source_type": "investor_website",
      "source_level": 1,
      "independent_of": null
    }],
    "notes": ""
  },
  "ticket_size": {
    "value": { "amount": null, "min": 200000, "max": 1000000, "currency": "EUR",
               "as_of": "2026", "definition": "první investice" },
    "status": "dolozene",
    "evidence": [{
      "claimed_value": { "min": 200000, "max": 1000000, "currency": "EUR" },
      "url": "https://example.com/about",
      "quote": "První investice obvykle 200 tis. až 1 mil. EUR",
      "quote_lang": "cs",
      "locator": null,
      "accessed": "2026-10-25",
      "published": null,
      "source_type": "investor_website",
      "source_level": 1,
      "independent_of": null
    }],
    "notes": ""
  },
  "aum": {
    "value": null,
    "status": "v_rozpore",
    "evidence": [
      { "claimed_value": { "amount": 50000000, "currency": "EUR", "as_of": "2024" },
        "url": "https://example.com/news/fund-close",
        "quote": "spravujeme 50 milionů eur",
        "quote_lang": "cs", "locator": null,
        "accessed": "2026-10-25", "published": "2024-05-02",
        "source_type": "investor_announcement", "source_level": 1,
        "independent_of": null },
      { "claimed_value": { "amount": 80000000, "currency": "EUR", "as_of": "2026" },
        "url": "https://media.example.org/clanek/123",
        "quote": "fond s 80 miliony eur v správě",
        "quote_lang": "cs", "locator": null,
        "accessed": "2026-10-25", "published": "2026-02-10",
        "source_type": "media", "source_level": 2,
        "independent_of": null }
    ],
    "notes": "Rozdielne hodnoty a obdobia; mohlo dôjsť k navýšeniu kapitálu, nerozhodnuté."
  },
  "deals": [{
    "company": "Example Startup a.s.",
    "company_website": "https://startup.example.net",
    "round": "seed",
    "deal_date": "2026-03-15",
    "date_kind": "announcement",
    "round_amount": { "amount": 1500000, "min": null, "max": null,
                      "currency": "EUR", "as_of": "2026-03-15", "definition": "celé kolo" },
    "investor_role": "lead",
    "evidence": [{
      "claimed_value": "Example Ventures viedol seed kolo Example Startup",
      "url": "https://startup.example.net/blog/seed",
      "quote": "Kolo vedl fond Example Ventures",
      "quote_lang": "cs", "locator": null,
      "accessed": "2026-10-25", "published": "2026-03-15",
      "source_type": "company_announcement", "source_level": 1,
      "independent_of": null
    }]
  }],
  "last_deal_date": "2026-03-15",
  "inclusion": {
    "decision": "zaradeny",
    "rule": "R1 (doložená investícia v časovom okne)",
    "reason": "Doložený lead v seed kole 03/2026.",
    "active": true,
    "decided_by": "agent"
  },
  "qa": {
    "checked_at": null, "urls_ok": null, "quotes_found": null,
    "schema_valid": null, "duplicate_candidates": [], "issues": []
  },
  "created": "2026-10-25",
  "updated": "2026-10-25",
  "notes": ""
}
```

Polia, ktoré v príklade chýbajú (`country`, `website`, `sectors`, `stages`,
`geography`, `fund_size`, `deployable_capital`, `related_entities`), majú
v skutočnom zázname rovnaký tvar ako ostatné polia, prípadne `"value": null`
a `"status": "nedolozene"`.

## Otvorené otázky (rozhodnú sa v pláne)

- Ktoré pole zodpovedá „celkovému investičnému kapitálu“ zo zadania:
  `aum`, súčet `fund_size`, alebo oboje s vysvetlením?
- Ako zaznamenať angel investorov a súkromné osoby (ochrana osobných údajov,
  `legal_entity` nemusí existovať).
- Či sa pre CSV export zjednodušia vnorené polia (napr. iba `value` a prvá URL).
