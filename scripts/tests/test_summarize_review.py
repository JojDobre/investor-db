"""Testy pre scripts/summarize_review.py na syntetických dátach.

Spustenie (z koreňa repozitára):
    python -m unittest discover -s scripts/tests -v

Dáta sú vymyslené a slúžia iba na kontrolu výpočtov, nie sú to výsledky pilotu.
"""

import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "summarize_review.py"
COLUMNS = ["record_id", "field", "priority", "ai_status", "ai_value", "verdict",
           "error_type", "caught_by", "minutes", "notes"]
STANDARD = [("investor_type", "povinne"), ("country", "povinne"), ("website", "povinne"),
            ("registration", "doplnkove"), ("sectors", "dolezite"), ("stages", "dolezite"),
            ("ticket_size", "dolezite"), ("fund_size", "dolezite"), ("aum", "dolezite")]


def row(record, field, priority, value, verdict, status="dolozene", **extra):
    r = dict.fromkeys(COLUMNS, "")
    r.update(record_id=record, field=field, priority=priority, ai_status=status,
             ai_value=value, verdict=verdict, **extra)
    return r


def synthetic():
    """Záznam A: všetky polia. Záznam B: chýba riadok aum a deal."""
    rows = []
    a = {
        "investor_type": ('"vc"', "plna_podpora"),
        "country": ('"CZ"', "plna_podpora"),
        "website": ('"https://a.example"', "nespravne"),
        "registration": ("null", "nekontrolovane"),
        "sectors": ('["fintech"]', "ciastocna_podpora"),
        "stages": ('["seed"]', "neoveritelne"),
        "ticket_size": ("null", "prehliadnute"),
        "fund_size": ("null", "potvrdene_chyba"),
        "aum": ("null", ""),  # bez verdiktu
    }
    for field, priority in STANDARD:
        value, verdict = a[field]
        status = "nedolozene" if value == "null" else "dolozene"
        rows.append(row("A", field, priority, value, verdict, status))
    rows.append(row("A", "deal_1", "povinne", "Firma X 2026-04", "bez_podpory",
                    error_type="vymysleny_zdroj", caught_by="skript"))
    rows.append(row("A", "inclusion", "", "zaradeny Z1+Z2+Z3", "spravne", status="", minutes="12"))

    b = {
        "investor_type": ('"vc"', "plna_podpora"),
        "country": ('"SK"', "plna_podpora"),
        "website": ('"https://b.example"', "plna_podpora"),
        "registration": ("null", "potvrdene_chyba"),
        "sectors": ("null", "prehliadnute"),
        "stages": ('["series A"]', "spravne"),  # neplatný verdikt pre vyplnené pole
        "ticket_size": ("", "plna_podpora"),   # prázdne ai_value = chyba v CSV
        "fund_size": ("null", "potvrdene_chyba"),
    }
    for field, priority in STANDARD[:-1]:  # aum vynechané
        value, verdict = b[field]
        rows.append(row("B", field, priority, value, verdict,
                        "nedolozene" if value == "null" else "dolozene"))
    rows[-1]["ai_status"] = "v_rozpore"  # fund_size B
    rows.append(row("B", "inclusion", "", "zaradeny Z1+Z2+Z3", "nespravne", status="",
                    error_type="zle_zaradenie", caught_by="clovek", minutes="8"))
    return rows


class SummarizeReviewTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        tmp = Path(tempfile.mkdtemp())
        path = tmp / "review.csv"
        with path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=COLUMNS)
            w.writeheader()
            w.writerows(synthetic())
        result = subprocess.run([sys.executable, "-I", str(SCRIPT), str(path)],
                                check=True, capture_output=True, text=True)
        cls.out = result.stdout
        cls.lines = [line.strip() for line in cls.out.splitlines()]

    def assertLine(self, text):
        self.assertIn(text, self.lines, msg="\n" + self.out)

    def test_pocty_riadkov(self):
        # A: 9 polí + deal + inclusion = 11, B: 8 polí + inclusion = 9; spolu 20, 1 bez verdiktu (aum A)
        self.assertLine("Riadkov s verdiktom: 19, bez verdiktu (nepočítané): 1")

    def test_vynechane_polia(self):
        self.assertLine("CHÝBAJÚ RIADKY: B: aum, deal_*")
        self.assertNotIn("CHÝBAJÚ RIADKY: A", self.out)

    def test_neplatne_verdikty(self):
        self.assertLine("CHYBA: 2 riadkov má verdikt, ktorý nepatrí k typu poľa (nepočítané):")
        self.assertIn("B | stages | ai_value='[\"series A\"]' | verdict='spravne'", self.out)
        self.assertIn("B | ticket_size | ai_value='' | verdict='plna_podpora'", self.out)

    def test_zaradenie(self):
        self.assertLine("Správne rozhodnutie AI: 1 z 2 (50.0%), neoveriteľné 0")

    def test_vyplnene_spolu(self):
        # vyplnené: A investor_type, country, website, sectors, stages, deal_1; B investor_type, country, website
        # = 9, neoveriteľné 1 (A stages) => menovateľ 8
        self.assertLine("Spolu: vyplnených 9, z toho posúditeľných 8")
        self.assertLine("úplná podpora:     5 z 8 (62.5%)")
        self.assertLine("čiastočná podpora: 1 z 8 (12.5%)")
        self.assertLine("bez podpory:       1 z 8 (12.5%)")
        self.assertLine("nesprávne:         1 z 8 (12.5%)")
        self.assertLine("neoveriteľné:      1 (mimo menovateľa)")

    def test_vyplnene_povinne(self):
        # povinné vyplnené: A investor_type, country, website, deal_1; B investor_type, country, website = 7
        self.assertLine("povinne: vyplnených 7, z toho posúditeľných 7")
        self.assertLine("úplná podpora:     5 z 7 (71.4%)")

    def test_chybajuce_spolu(self):
        # prázdne s verdiktom: A registration, ticket_size, fund_size; B registration, sectors, fund_size = 6
        # menovateľ = vyplnené (9) + prázdne (6) = 15
        self.assertLine("Spolu: prázdnych 6 z 15 (40.0%) polí (nedoložené 5, v rozpore 1)")
        self.assertLine("údaj neexistuje ani podľa mňa: 3")
        self.assertLine("prehliadnuté (údaj existoval): 2")
        self.assertLine("nekontrolované:                1")

    def test_chybajuce_dolezite(self):
        # dôležité: vyplnené A sectors, A stages; prázdne A ticket, A fund, B sectors, B fund = 6 z 8
        self.assertLine("dolezite: prázdnych 4 z 6 (66.7%) polí (nedoložené 3, v rozpore 1)")

    def test_chyby_a_cas(self):
        self.assertLine("vymysleny_zdroj, zachytil skript: 1")
        self.assertLine("zle_zaradenie, zachytil clovek: 1")
        self.assertLine("záznamov: 2, spolu 20 min, priemer 10.0 min, medián 10.0 min")


if __name__ == "__main__":
    unittest.main()
