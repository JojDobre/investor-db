# Dátová schéma (návrh, upraví sa v pláne)

Jeden investor = jeden JSON objekt. Každé faktické pole je objekt s hodnotou
a zdrojom:

```json
{
  "value": "...",
  "url": "https://...",
  "quote": "doslovná citácia zo zdroja",
  "accessed": "2026-10-22",
  "published": "2026-03-15"
}
```

Ak údaj nie je doložený: `"value": null` a dôvod v `notes`.

## Polia

| Pole | Popis |
|---|---|
| `id` | interný identifikátor |
| `name` | názov investora |
| `type` | VC / PE / family office / angel / súkromný investor / iné |
| `country` | krajina sídla |
| `website` | oficiálny web |
| `sectors` | sektory, do ktorých investuje |
| `stages` | štádiá (pre-seed, seed, Series A, ..., buyout) |
| `ticket_size` | bežná výška investície (min–max, mena) |
| `total_capital` | celkový investičný kapitál / AUM (mena, k dátumu) |
| `evidence_deals` | zoznam doložených investícií: firma, dátum, zdroj |
| `status` | zaradený / vyradený / nejasný + pravidlo, podľa ktorého |
| `confidence` | vysoká / stredná / nízka |
| `notes` | poznámky, rozpory medzi zdrojmi |
