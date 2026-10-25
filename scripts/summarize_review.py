"""Spočíta výsledky ručnej kontroly z results/review.csv.

Jeden riadok CSV = jeden skontrolovaný údaj. Riadok s field = "inclusion"
je rozhodnutie o zaradení investora.

Stĺpce:
    record_id   ID záznamu
    field       názov poľa (napr. website, ticket_size, deal_1) alebo "inclusion"
    priority    povinne / dolezite / doplnkove (pri "inclusion" prázdne)
    ai_value    čo uviedla AI (pri prázdnom poli "null")
    verdict     spravne / nespravne / ciastocne / nepodlozene / neoveritelne / prehliadnute
                - nepodlozene: hodnota môže sedieť, ale citovaný zdroj ju nepodporuje
                - prehliadnute: AI nechala pole prázdne, ale údaj som našiel
    error_type  pri chybe: vymysleny_zdroj / zly_udaj / zamena_firmy / zle_zaradenie / iny
    caught_by   kto chybu zachytil: skript / kontrolny_agent / clovek
    minutes     čas mojej kontroly záznamu (stačí v jednom riadku záznamu)
    notes       poznámka

Spustenie:
    python scripts/summarize_review.py results/review.csv
"""

import csv
import statistics
import sys
from collections import Counter, defaultdict

FILLED = {"spravne", "nespravne", "ciastocne", "nepodlozene", "neoveritelne"}


def share(part, total):
    return f"{part} z {total}" + (f" ({part / total:.0%})" if total else "")


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "results/review.csv"
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        sys.exit(f"{path} je prázdny.")

    inclusion = [r for r in rows if r["field"] == "inclusion"]
    fields = [r for r in rows if r["field"] != "inclusion"]

    print("## Zaradenie")
    correct = sum(r["verdict"] == "spravne" for r in inclusion)
    print(f"Správne rozhodnutie AI o zaradení: {share(correct, len(inclusion))}")

    print("\n## Presnosť vyplnených údajov")
    by_priority = defaultdict(list)
    for r in fields:
        if r["verdict"] in FILLED:
            by_priority[r["priority"] or "neuvedene"].append(r["verdict"])
    for priority, verdicts in sorted(by_priority.items()):
        print(f"{priority}: správne {share(verdicts.count('spravne'), len(verdicts))}, "
              f"nesprávne {verdicts.count('nespravne')}, čiastočne {verdicts.count('ciastocne')}, "
              f"nepodložené {verdicts.count('nepodlozene')}, neoveriteľné {verdicts.count('neoveritelne')}")

    filled = [r for r in fields if r["verdict"] in FILLED]
    supported = sum(r["verdict"] in {"spravne", "ciastocne"} for r in filled)
    print(f"\nÚdaje, ktoré zdroj naozaj podporuje: {share(supported, len(filled))}")

    nulls_checked = [r for r in fields if r["ai_value"].strip().lower() == "null"]
    missed = sum(r["verdict"] == "prehliadnute" for r in nulls_checked)
    print(f"Prázdne polia, pri ktorých som údaj našiel: {share(missed, len(nulls_checked))}")

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


if __name__ == "__main__":
    main()
