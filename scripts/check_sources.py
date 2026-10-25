"""Overí, či zdroje v záznamoch existujú a či sa citácie na stránkach naozaj nachádzajú.

Prejde všetky JSON súbory v zadanom priečinku, nájde v nich každý dôkaz
(objekt s kľúčmi "url" a "quote"), stiahne stránku a hľadá v nej citáciu.
Záznamy nemení. Výsledok zapíše do CSV.

Spustenie:
    python scripts/check_sources.py data/raw/ --out results/source-check.csv

Skript overuje iba to, že citácia na stránke JE. Neoveruje, či citácia
tvrdenie PODPORUJE. To robí kontrolný agent a človek.
"""

import argparse
import csv
import html
import json
import re
import sys
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path

USER_AGENT = "investor-db-pilot/0.1 (kontrola citácií)"
TIMEOUT = 20


def normalize(text):
    """Zjednotí medzery, úvodzovky a pomlčky, aby drobné rozdiely v zápise nespôsobili falošnú chybu."""
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"[‘’‚‛′]", "'", text)
    text = re.sub(r"[“”„‟″«»]", '"', text)
    text = re.sub(r"[‐-―−]", "-", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()


def html_to_text(raw):
    raw = re.sub(r"(?is)<(script|style|noscript).*?</\1>", " ", raw)
    raw = re.sub(r"(?s)<[^>]+>", " ", raw)
    return html.unescape(raw)


def fetch(url):
    """Vráti (stav, text, poznámka). Stav je HTTP kód alebo 'chyba'."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            content_type = resp.headers.get("Content-Type", "")
            body = resp.read()
            status = resp.status
    except urllib.error.HTTPError as e:
        return e.code, "", f"HTTP {e.code}"
    except Exception as e:  # sieť, DNS, timeout, SSL
        return "chyba", "", f"{type(e).__name__}: {e}"

    if "pdf" in content_type.lower() or url.lower().endswith(".pdf"):
        return status, "", "PDF: citáciu skontrolovať ručne"
    charset = "utf-8"
    m = re.search(r"charset=([\w-]+)", content_type)
    if m:
        charset = m.group(1)
    return status, html_to_text(body.decode(charset, errors="replace")), ""


def find_evidence(node, path=""):
    """Rekurzívne nájde všetky dôkazy v zázname a vráti (cesta k poľu, dôkaz)."""
    if isinstance(node, dict):
        if "url" in node and "quote" in node:
            yield path, node
        for key, value in node.items():
            yield from find_evidence(value, f"{path}.{key}" if path else key)
    elif isinstance(node, list):
        for i, item in enumerate(node):
            yield from find_evidence(item, f"{path}[{i}]")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("folder", help="priečinok so záznamami, napr. data/raw/")
    parser.add_argument("--out", default="results/source-check.csv")
    args = parser.parse_args()

    files = sorted(Path(args.folder).glob("*.json"))
    if not files:
        sys.exit(f"V {args.folder} nie sú žiadne JSON súbory.")

    cache = {}
    rows = []
    for file in files:
        try:
            record = json.loads(file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            rows.append({"record": file.stem, "field": "", "url": "", "status": "",
                         "result": "neplatny_json", "note": str(e)})
            continue

        for field, ev in find_evidence(record):
            url, quote = ev.get("url") or "", ev.get("quote") or ""
            if not url or not quote:
                result, status, note = "chyba_url_alebo_citacia", "", "prázdna URL alebo citácia"
            else:
                if url not in cache:
                    cache[url] = fetch(url)
                status, text, note = cache[url]
                if not text:
                    result = "rucne" if note.startswith("PDF") else "nedostupne"
                elif normalize(quote) in normalize(text):
                    result = "najdene"
                else:
                    result = "nenajdene"
            rows.append({"record": file.stem, "field": field, "url": url,
                         "status": status, "result": result, "note": note})

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["record", "field", "url", "status", "result", "note"])
        writer.writeheader()
        writer.writerows(rows)

    counts = {}
    for row in rows:
        counts[row["result"]] = counts.get(row["result"], 0) + 1
    print(f"Záznamov: {len(files)}, dôkazov: {len(rows)}")
    for result, n in sorted(counts.items()):
        print(f"  {result}: {n}")
    print(f"Výsledok: {out}")
    problems = [r for r in rows if r["result"] != "najdene"]
    if problems:
        print("\nNa kontrolu:")
        for r in problems:
            print(f"  {r['record']} | {r['field']} | {r['result']} | {r['url']} {r['note']}")


if __name__ == "__main__":
    main()
