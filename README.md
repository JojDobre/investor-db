# Spoľahlivá databáza investorov

Riešenie praktickej úlohy (Zadanie A) do výberového konania na pozíciu
Junior AI Developer v Clientelo.

> **Stav:** rozpracované. Hotové: príprava repozitára, pravidlá pre AI
> (`CLAUDE.md`), schéma v0.4, plán pilotu v2 (čaká na schválenie), skripty na kontrolu citácií a súhrn ručnej kontroly s testami.
> Rozpracované: zoznam kandidátov z CVCA a SLOVCA, test workflowu na 3 investoroch (návrhy AI v `data/raw/`, ručná kontrola čaká).
> Zatiaľ chýba: ručná kontrola, overené záznamy v `data/verified/`, výsledky presnosti, exporty v `ai-log/`.

## Obsah repozitára

| Cesta | Obsah |
|---|---|
| `plan/` | Plán: pravidlá zaradenia/vyradenia, overovanie, odhad rozsahu a spoľahlivosti |
| `data/schema.md` | Dátová schéma záznamu investora |
| `data/raw/` | Surové výstupy AI agentov (neoverené) a zoznam kandidátov `candidates.csv` |
| `data/verified/` | Ručne overené záznamy (zatiaľ prázdne) |
| `scripts/` | `scripts/check_sources.py` (URL a výskyt citácií), `scripts/summarize_review.py` (súhrn ručnej kontroly), `scripts/prompts/` (pokyny pre AI), `scripts/tests/` (testy: `python -m unittest discover -s scripts/tests`) |
| `results/` | `source-check.csv` (výsledok skriptu), `review.csv` (ručná kontrola, zatiaľ bez verdiktov), `kontrola-zaznamov-2026-10-26.md` (podklad pre ručnú kontrolu); výsledky presnosti a náklady zatiaľ nie sú |
| `notes/chyby-ai.md` | Priebežný denník chýb, ktoré AI urobila |
| `ai-log/` | Export konverzácií s Claude Code (`/export`), zatiaľ prázdne |
| `CLAUDE.md` | Pravidlá, ktoré dostávajú všetci AI agenti |

## Ako spustiť

Potrebný je iba Python 3 (otestované na 3.13) a pre jeden test príkaz
`openssl`. Externé knižnice sa nepoužívajú. Príkazy sa spúšťajú z koreňa
repozitára.

```bash
# testy (24, bez internetu)
python3 -m unittest discover -s scripts/tests -v

# kontrola URL a citácií v návrhoch AI
python3 scripts/check_sources.py data/raw/ --out results/source-check.csv
# ak niektorý web neposiela úplný reťazec certifikátov (napr. cvca.cz):
SSL_CERT_FILE=<ca-súbor-s-doplnenými-medzicertifikátmi> python3 scripts/check_sources.py data/raw/ --out results/source-check.csv

# súhrn ručnej kontroly
python3 scripts/summarize_review.py results/review.csv
```

## 1. Plán

Návrh: [`plan/research-plan.md`](plan/research-plan.md) (v2, čaká na schválenie).

_TODO: zhrnutie po schválení._

## 2. Vzorka

_TODO: krajina, počet záznamov, odkaz na dáta._

## 3. Meranie presnosti

_TODO: metodika a výsledky._

## 4. Odhad nákladov na rozšírenie na celý svet

_TODO_

## 5. Ako som pracoval s AI

_TODO: pokyny pre agentov, spôsob kontroly výstupov, kde sa AI pomýlila
(podklady v `notes/chyby-ai.md` a `ai-log/`)._

## 6. Rozhodnutia a ich zdôvodnenie

_TODO: nejasnosti v zadaní a ako som ich rozhodol._

## 7. Čo v riešení chýba

_TODO_
