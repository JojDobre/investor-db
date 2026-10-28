"""Spočíta výsledky ručnej kontroly z results/review.csv.

Jeden riadok CSV = jedno pole jedného záznamu, vrátane prázdnych polí.
Riadok s field = "inclusion" je rozhodnutie o zaradení investora.

Stĺpce:
    record_id   ID záznamu
    field       názov poľa (napr. website, ticket_size, deal_1) alebo "inclusion"
    priority    povinne / dolezite / doplnkove (pri "inclusion" prázdne)
    ai_status   status poľa v návrhu AI: dolozene / neiste / nedolozene / v_rozpore
    ai_value    čo uviedla AI (pri prázdnom poli "null")
    verdict     môj verdikt, podľa typu riadku:
                vyplnené pole (ai_value nie je null):
                  plna_podpora       zdroj hodnotu priamo uvádza a hodnota je správna
                  ciastocna_podpora  časť sedí (napr. suma áno, obdobie alebo mena nie)
                  bez_podpory        citovaný zdroj hodnotu nepodporuje (hodnota môže byť pravdivá)
                  nespravne          hodnota je nepravdivá
                  neoveritelne       neviem rozhodnúť
                prázdne pole (ai_value je null):
                  potvrdene_chyba    údaj som nenašiel ani ja
                  prehliadnute       údaj verejne existuje a AI ho nenašla
                  nekontrolovane     prázdne pole som nehľadal
                inclusion:
                  spravne / nespravne / neoveritelne
    error_type  pri chybe: vymysleny_zdroj / zly_udaj / zamena_firmy / zle_zaradenie / iny
    caught_by   kto chybu zachytil: skript / kontrolny_agent / clovek
    minutes     čas mojej kontroly záznamu (stačí v jednom riadku záznamu)
    notes       poznámka

Spustenie:
    python scripts/summarize_review.py results/review.csv

Riadky s prázdnym verdiktom sa nepočítajú a skript vypíše, koľko ich je.
Neznámy verdikt alebo prázdne ai_value skript nahlási ako chybu a nepočíta ich.
Ak pri zázname chýba riadok niektorého poľa zo schémy, skript to vypíše.
"""

import csv
import statistics
import sys
from collections import Counter, defaultdict

FILLED = ["plna_podpora", "ciastocna_podpora", "bez_podpory", "nespravne", "neoveritelne"]
EMPTY = ["potvrdene_chyba", "prehliadnute", "nekontrolovane"]
INCLUSION = ["spravne", "nespravne", "neoveritelne"]
EXPECTED_FIELDS = ["investor_type", "country", "website", "registration", "sectors",
                   "stages", "ticket_size", "fund_size", "aum", "inclusion"]


def share(part, total):
    return f"{part} z {total}" + (f" ({part / total:.1%})" if total else "")


def is_null(row):
    return row["ai_value"].strip().lower() == "null"


def report_filled(label, rows):
    counts = Counter(r["verdict"] for r in rows)
    evaluable = len(rows) - counts["neoveritelne"]
    print(f"{label}: vyplnených {len(rows)}, z toho posúditeľných {evaluable}")
    print(f"  úplná podpora:     {share(counts['plna_podpora'], evaluable)}")
    print(f"  čiastočná podpora: {share(counts['ciastocna_podpora'], evaluable)}")
    print(f"  bez podpory:       {share(counts['bez_podpory'], evaluable)}")
    print(f"  nesprávne:         {share(counts['nespravne'], evaluable)}")
    print(f"  neoveriteľné:      {counts['neoveritelne']} (mimo menovateľa)")


def report_empty(label, rows, total_fields):
    counts = Counter(r["verdict"] for r in rows)
    by_status = Counter(r.get("ai_status", "") or "neuvedene" for r in rows)
    print(f"{label}: prázdnych {share(len(rows), total_fields)} polí "
          f"(nedoložené {by_status['nedolozene']}, v rozpore {by_status['v_rozpore']})")
    print(f"  údaj neexistuje ani podľa mňa: {counts['potvrdene_chyba']}")
    print(f"  prehliadnuté (údaj existoval): {counts['prehliadnute']}")
    print(f"  nekontrolované:                {counts['nekontrolovane']}")


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "results/review.csv"
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        sys.exit(f"{path} je prázdny.")

    missing = []
    fields_by_record = defaultdict(set)
    for r in rows:
        fields_by_record[r["record_id"]].add(r["field"])
    for record_id, present in sorted(fields_by_record.items()):
        absent = [f for f in EXPECTED_FIELDS if f not in present]
        if not any(f.startswith("deal_") for f in present):
            absent.append("deal_*")
        if absent:
            missing.append((record_id, absent))

    pending = [r for r in rows if not r["verdict"].strip()]
    rows = [r for r in rows if r["verdict"].strip()]
    invalid = []
    inclusion, filled, empty = [], [], []
    for r in rows:
        if r["field"] != "inclusion" and not r["ai_value"].strip():
            target, allowed = None, []
        elif r["field"] == "inclusion":
            target, allowed = inclusion, INCLUSION
        elif is_null(r):
            target, allowed = empty, EMPTY
        else:
            target, allowed = filled, FILLED
        (target if r["verdict"] in allowed else invalid).append(r)

    print(f"Riadkov s verdiktom: {len(rows)}, bez verdiktu (nepočítané): {len(pending)}")
    for record_id, absent in missing:
        print(f"CHÝBAJÚ RIADKY: {record_id}: {', '.join(absent)}")
    if invalid:
        print(f"CHYBA: {len(invalid)} riadkov má verdikt, ktorý nepatrí k typu poľa (nepočítané):")
        for r in invalid:
            print(f"  {r['record_id']} | {r['field']} | ai_value={r['ai_value']!r} | verdict={r['verdict']!r}")

    print("\n## Zaradenie")
    counts = Counter(r["verdict"] for r in inclusion)
    print(f"Správne rozhodnutie AI: {share(counts['spravne'], len(inclusion) - counts['neoveritelne'])}, "
          f"neoveriteľné {counts['neoveritelne']}")

    print("\n## Vyplnené údaje")
    report_filled("Spolu", filled)
    by_priority = defaultdict(list)
    for r in filled:
        by_priority[r["priority"] or "neuvedene"].append(r)
    for priority, items in sorted(by_priority.items()):
        report_filled(priority, items)

    print("\n## Chýbajúce údaje")
    report_empty("Spolu", empty, len(filled) + len(empty))
    by_priority = defaultdict(list)
    totals = Counter(r["priority"] or "neuvedene" for r in filled + empty)
    for r in empty:
        by_priority[r["priority"] or "neuvedene"].append(r)
    for priority, items in sorted(by_priority.items()):
        report_empty(priority, items, totals[priority])

    print("\n## Chyby AI")
    errors = [r for r in rows if r["error_type"]]
    for (etype, caught), n in sorted(Counter((r["error_type"], r["caught_by"] or "?") for r in errors).items()):
        print(f"{etype}, zachytil {caught}: {n}")
    if not errors:
        print("žiadne zaznamenané")

    print("\n## Čas ručnej kontroly")
    minutes = defaultdict(float)
    for r in rows:
        if r["minutes"].strip():
            minutes[r["record_id"]] += float(r["minutes"].replace(",", "."))
    if minutes:
        values = list(minutes.values())
        print(f"záznamov: {len(values)}, spolu {sum(values):.0f} min, "
              f"priemer {statistics.mean(values):.1f} min, medián {statistics.median(values):.1f} min")
    else:
        print("nezaznamenaný")


if __name__ == "__main__":
    main()
