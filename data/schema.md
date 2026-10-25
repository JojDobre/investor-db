# Dátová schéma záznamu investora (v0.3)

Zjednodušená verzia pre pilot. Cieľ: aby sa záznam dal prečítať a overiť
za pár minút. Pravidlá zaradenia sú v `plan/research-plan.md`, pravidlá
práce so zdrojmi v `CLAUDE.md`.

## Ukladanie

- Jeden investor = jeden súbor `data/raw/<id>.json` (návrh od AI).
- Po ručnej kontrole uložím opravenú verziu do `data/verified/<id>.json`.
- `id`: kód krajiny a názov malými písmenami bez diakritiky, napr.
  `sk-example-ventures`.
- Dátumy `YYYY-MM-DD`. Ak zdroj uvádza iba mesiac, `YYYY-MM`.
- Sumy v mene, ktorú uvádza zdroj, bez prepočtu.

## Dôkaz

Každý údaj má zoznam dôkazov. Jeden dôkaz:

| Pole | Povinné | Popis |
|---|---|---|
| `url` | áno | presná stránka s údajom |
| `quote` | áno | doslovná citácia v pôvodnom jazyku, aby sa dala na stránke nájsť |
| `accessed` | áno | kedy som (alebo agent) stránku čítal |
| `published` | nie | dátum článku alebo oznámenia, ak je uvedený |
| `source_type` | áno | `investor_web`, `company_announcement`, `media`, `register`, `other` |
| `locator` | nie | strana alebo sekcia pri PDF či dlhom dokumente |

`other` je napríklad adresár alebo agregátor. Taký zdroj sám nestačí na
potvrdenie investície (pravidlo N2 v pláne).

## Údaj

Každý faktický údaj má rovnaký tvar:

```json
{ "value": ..., "status": "dolozene", "evidence": [ ... ], "notes": "" }
```

| `status` | Význam | `value` |
|---|---|---|
| `dolozene` | zdroj údaj priamo uvádza | vyplnená |
| `nedolozene` | údaj sa nenašiel | `null`, v `notes` čo som hľadal |
| `v_rozpore` | zdroje uvádzajú rôzne hodnoty | `null`, v `evidence` sú všetky zdroje, v `notes` vysvetlenie |

## Peňažná suma

Používa sa pri `ticket_size`, `fund_size` a `aum`:

```json
{ "min": 200000, "max": 1000000, "currency": "EUR", "as_of": "2026" }
```

Pri jednom čísle je `min` rovné `max`. `as_of` je rok alebo dátum, ku
ktorému suma platí. Pri `fund_size` sa pridá `fund_name`.

## Záznam

| Pole | Typ | Priorita | Popis |
|---|---|---|---|
| `id` | text | | identifikátor |
| `name` | text | povinné | názov investora |
| `investor_type` | údaj | povinné | `vc`, `pe`, `other` |
| `country` | údaj | povinné | `CZ`, `SK`, prípadne iná krajina sídla |
| `website` | údaj | povinné* | oficiálny web |
| `registration` | údaj | povinné* | obchodný register, napr. `"IČO 12345678"` |
| `sectors` | údaj (zoznam) | dôležité | sektory podľa zdroja |
| `stages` | údaj (zoznam) | dôležité | napr. `pre-seed`, `seed`, `series A`, `growth` |
| `ticket_size` | údaj (suma) | dôležité | typická výška **jednej** investície |
| `fund_size` | údaj (suma) | dôležité | veľkosť konkrétneho fondu |
| `aum` | údaj (suma) | dôležité | kapitál v správe, ak ho zdroj uvádza |
| `deals` | zoznam investícií | povinné (aspoň 1 v okne) | pozri nižšie |
| `inclusion` | rozhodnutie | povinné | pozri nižšie |
| `notes` | text | | poznámky k záznamu |
| `updated` | dátum | | posledná zmena |

\* Na overenie identity (pravidlo Z1) stačí web **alebo** register.

### Investícia (`deals`)

| Pole | Popis |
|---|---|
| `company` | financovaná firma |
| `date` | dátum investície alebo oznámenia (`YYYY-MM-DD` alebo `YYYY-MM`) |
| `date_kind` | `investment` alebo `announcement` |
| `evidence` | dôkaz, v ktorom je menovaný investor aj firma |

Výška kola sa neeviduje. Neprezrádza, koľko investoval konkrétny investor,
a ľahko sa zamení s `ticket_size`.

### Rozhodnutie (`inclusion`)

| Pole | Popis |
|---|---|
| `decision` | `zaradeny`, `vyradeny`, `nejasny` |
| `rule` | pravidlá z plánu, napr. `"Z1+Z2+Z3"`, `"V2"`, `"N1"` |
| `reason` | krátke zdôvodnenie |
| `decided_by` | `agent` (návrh v `data/raw/`) alebo `human` (v `data/verified/`) |

## Príklad

Ilustračný záznam. Názvy, URL a hodnoty sú **vymyslené**, slúžia iba na
ukážku formátu.

```json
{
  "id": "sk-example-ventures",
  "name": "Example Ventures",
  "investor_type": {
    "value": "vc",
    "status": "dolozene",
    "evidence": [{
      "url": "https://example.com/o-nas",
      "quote": "Sme fond rizikového kapitálu zameraný na rané fázy.",
      "accessed": "2026-10-25",
      "published": null,
      "source_type": "investor_web"
    }],
    "notes": ""
  },
  "country": {
    "value": "SK",
    "status": "dolozene",
    "evidence": [{
      "url": "https://example.com/kontakt",
      "quote": "Example Ventures, Hlavná 1, 811 01 Bratislava",
      "accessed": "2026-10-25",
      "published": null,
      "source_type": "investor_web"
    }],
    "notes": ""
  },
  "website": {
    "value": "https://example.com",
    "status": "dolozene",
    "evidence": [{
      "url": "https://example.com/kontakt",
      "quote": "Example Ventures, Hlavná 1, 811 01 Bratislava",
      "accessed": "2026-10-25",
      "published": null,
      "source_type": "investor_web"
    }],
    "notes": ""
  },
  "registration": { "value": null, "status": "nedolozene", "evidence": [],
                    "notes": "Web IČO neuvádza, register som zatiaľ nehľadal." },
  "sectors": { "value": ["fintech", "zdravotníctvo"], "status": "dolozene",
    "evidence": [{
      "url": "https://example.com/o-nas",
      "quote": "Investujeme najmä do fintechu a zdravotníctva.",
      "accessed": "2026-10-25", "published": null, "source_type": "investor_web"
    }], "notes": "" },
  "stages": { "value": ["seed"], "status": "dolozene",
    "evidence": [{
      "url": "https://example.com/o-nas",
      "quote": "Sme fond rizikového kapitálu zameraný na rané fázy.",
      "accessed": "2026-10-25", "published": null, "source_type": "investor_web"
    }], "notes": "Zdroj hovorí o „raných fázach“, ako seed som to označil ja." },
  "ticket_size": {
    "value": { "min": 200000, "max": 1000000, "currency": "EUR", "as_of": "2026" },
    "status": "dolozene",
    "evidence": [{
      "url": "https://example.com/o-nas",
      "quote": "Prvá investícia zvyčajne 200 tis. až 1 mil. EUR",
      "accessed": "2026-10-25", "published": null, "source_type": "investor_web"
    }],
    "notes": ""
  },
  "fund_size": { "value": null, "status": "nedolozene", "evidence": [],
                 "notes": "Hľadané: web (o nás, novinky), správy o uzavretí fondu." },
  "aum": {
    "value": null,
    "status": "v_rozpore",
    "evidence": [
      { "url": "https://example.com/novinky/fond-ii",
        "quote": "spravujeme 50 miliónov eur",
        "accessed": "2026-10-25", "published": "2024-05-02", "source_type": "investor_web" },
      { "url": "https://media.example.org/clanok/123",
        "quote": "fond s 80 miliónmi eur v správe",
        "accessed": "2026-10-25", "published": "2026-02-10", "source_type": "media" }
    ],
    "notes": "Rôzne hodnoty z rôznych rokov. Nerozhodol som, ktorá platí."
  },
  "deals": [{
    "company": "Example Startup s.r.o.",
    "date": "2026-03",
    "date_kind": "announcement",
    "evidence": [{
      "url": "https://startup.example.net/blog/seed",
      "quote": "Kolo viedol fond Example Ventures",
      "accessed": "2026-10-25", "published": "2026-03-15", "source_type": "company_announcement"
    }]
  }],
  "inclusion": {
    "decision": "zaradeny",
    "rule": "Z1+Z2+Z3",
    "reason": "Oficiálny web, sídlo v Bratislave, investícia oznámená 03/2026.",
    "decided_by": "agent"
  },
  "notes": "",
  "updated": "2026-10-25"
}
```

## Čo schéma vedome nerieši

- Vzťahy medzi správcovskou spoločnosťou, fondmi a materskou firmou. Pri
  25 investoroch ich zapíšem do `notes`.
- Disponibilný kapitál. Verejne sa takmer nevyskytuje.
- Výsledky automatických kontrol. Tie zapisuje skript do
  `results/source-check.csv`, nie do záznamu.
