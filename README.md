# Spoľahlivá databáza investorov

Riešenie praktickej úlohy (Zadanie A) do výberového konania na pozíciu
Junior AI Developer v Clientelo.

> **Stav:** rozpracované. Hotové: príprava repozitára, pravidlá pre AI
> (`CLAUDE.md`), schéma v0.3, plán pilotu v2 (čaká na schválenie), skripty na kontrolu citácií a súhrn ručnej kontroly.
> Zber dát ešte nezačal.

## Obsah repozitára

| Cesta | Obsah |
|---|---|
| `plan/` | Plán: pravidlá zaradenia/vyradenia, overovanie, odhad rozsahu a spoľahlivosti |
| `data/schema.md` | Dátová schéma záznamu investora |
| `data/raw/` | Surové výstupy AI agentov (neoverené) |
| `data/verified/` | Ručne overená vzorka so zdrojom pri každom údaji |
| `scripts/` | Skripty (zber, automatická kontrola zdrojov, meranie presnosti) |
| `results/` | Výsledok merania presnosti a odhad nákladov |
| `notes/chyby-ai.md` | Priebežný denník chýb, ktoré AI urobila |
| `ai-log/` | Export konverzácií s Claude Code (`/export`) |
| `CLAUDE.md` | Pravidlá, ktoré dostávajú všetci AI agenti |

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
