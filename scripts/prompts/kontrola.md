# Pokyn pre kontrolu (AI workflow 2) – v1

Použitie: nová konverzácia, bez prístupu k zdôvodneniu agenta zo zberu.
Agent dostane iba súbor `data/raw/<id>.json`.

---

Skontroluj záznam `data/raw/<id>.json`. Nič v ňom nemeň.

Pri každom dôkaze otvor URL a posúď, či citácia **v kontexte stránky**
podporuje hodnotu poľa:

- `ano`: zdroj hodnotu priamo uvádza a týka sa tohto investora,
- `ciastocne`: napríklad sedí suma, ale nie obdobie alebo mena,
- `nie`: zdroj hodnotu nepodporuje alebo hovorí o inom subjekte,
- `nedostupne`: stránku sa nepodarilo otvoriť.

Ďalej skontroluj:
- či dátum investície spadá do okna a nie je zamenený s dátumom článku,
- či ide o investora, nie o poradcu, platformu alebo klub,
- či `ticket_size` nie je v skutočnosti veľkosť kola a `aum` súčet fondov.

Výstup: tabuľka `pole | url | verdikt | dôvod` a zoznam podozrení.
Ak niečo nevieš posúdiť, napíš to; nehádaj.
