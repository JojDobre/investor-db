"""Testy pre scripts/check_sources.py.

Spustenie (z koreňa repozitára):
    python -m unittest discover -s scripts/tests -v

Testy bežia proti lokálnemu HTTP a HTTPS serveru na 127.0.0.1, nepotrebujú
internet. HTTPS test používa dočasný samopodpísaný certifikát (vyžaduje
príkaz openssl) a overuje, že skript certifikát bez dôvery ODMIETNE.
"""

import csv
import http.server
import json
import os
import shutil
import socket
import ssl
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "check_sources.py"

PAGES = {
    "/clanok.html": (
        "text/html; charset=utf-8",
        "<html><head><script>var x = 'Kolo viedol fond Iný';</script></head><body>"
        "<p>Kolo viedol fond Example&nbsp;Ventures   spolu s ďalšími.</p>"
        "<p>The round was led by Taiwania <a href='#'>Capital</a>, with participation from Credo.</p>"
        "<p>Prvý odsek</p><p>Druhý odsek</p>"
        "<p>„Typografické úvodzovky“ a pomlčka – tu.</p>"
        "</body></html>",
    ),
    "/dokument.pdf": ("application/pdf", "%PDF-1.4 fake"),
}


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        page = PAGES.get(self.path)
        if page is None:
            self.send_error(404)
            return
        content_type, body = page
        data = body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):
        pass


def start_server(context=None):
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    if context:
        server.socket = context.wrap_socket(server.socket, server_side=True)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def evidence(url, quote):
    return {"url": url, "quote": quote, "accessed": "2026-10-26", "published": None,
            "source_type": "other"}


class CheckSourcesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp())
        cls.http = start_server()
        cls.base = f"http://127.0.0.1:{cls.http.server_address[1]}"

    @classmethod
    def tearDownClass(cls):
        cls.http.shutdown()
        cls.http.server_close()
        shutil.rmtree(cls.tmp)

    def run_check(self, records, env_extra=None):
        folder = Path(tempfile.mkdtemp(dir=self.tmp))
        for name, content in records.items():
            text = content if isinstance(content, str) else json.dumps(content, ensure_ascii=False)
            (folder / f"{name}.json").write_text(text, encoding="utf-8")
        out = folder / "out.csv"
        env = dict(os.environ, NO_PROXY="127.0.0.1,localhost", no_proxy="127.0.0.1,localhost")
        env.update(env_extra or {})
        subprocess.run([sys.executable, "-I", str(SCRIPT), str(folder), "--out", str(out)],
                       check=True, capture_output=True, text=True, env=env)
        with out.open(encoding="utf-8") as f:
            return {row["field"]: row for row in csv.DictReader(f)}

    def one(self, url, quote, **kw):
        rows = self.run_check({"r": {"x": {"evidence": [evidence(url, quote)]}}}, **kw)
        return rows["x.evidence[0]"]

    def test_presna_citacia(self):
        self.assertEqual(self.one(self.base + "/clanok.html", "spolu s ďalšími.")["result"], "najdene")

    def test_medzery_a_nbsp_sa_zjednotia(self):
        row = self.one(self.base + "/clanok.html", "Kolo viedol fond Example Ventures spolu")
        self.assertEqual(row["result"], "najdene")

    def test_typograficke_znaky_sa_zjednotia(self):
        row = self.one(self.base + "/clanok.html", '"Typografické úvodzovky" a pomlčka - tu.')
        self.assertEqual(row["result"], "najdene")

    def test_pozmenena_citacia(self):
        row = self.one(self.base + "/clanok.html", "Kolo viedol fond Example Ventures sám.")
        self.assertEqual(row["result"], "nenajdene")

    def test_text_zo_skriptu_sa_nepocita(self):
        self.assertEqual(self.one(self.base + "/clanok.html", "Kolo viedol fond Iný")["result"], "nenajdene")

    def test_inline_znacka_bez_medzery(self):
        row = self.one(self.base + "/clanok.html", "led by Taiwania Capital, with participation")
        self.assertEqual(row["result"], "najdene")

    def test_vlozena_medzera_pred_ciarkou(self):
        row = self.one(self.base + "/clanok.html", "led by Taiwania Capital , with participation")
        self.assertEqual(row["result"], "nenajdene")

    def test_blokove_znacky_oddeluju_slova(self):
        self.assertEqual(self.one(self.base + "/clanok.html", "Prvý odsek Druhý odsek")["result"], "najdene")

    def test_neexistujuca_url(self):
        row = self.one(self.base + "/neexistuje.html", "čokoľvek")
        self.assertEqual((row["result"], row["status"]), ("nedostupne", "404"))

    def test_nedostupny_zdroj(self):
        row = self.one(f"http://127.0.0.1:{free_port()}/x.html", "čokoľvek")
        self.assertEqual((row["result"], row["status"]), ("nedostupne", "chyba"))

    def test_pdf_ide_na_rucnu_kontrolu(self):
        row = self.one(self.base + "/dokument.pdf", "čokoľvek")
        self.assertEqual(row["result"], "rucne")

    def test_prazdna_citacia(self):
        self.assertEqual(self.one(self.base + "/clanok.html", "")["result"], "chyba_url_alebo_citacia")

    def test_neplatny_json(self):
        rows = self.run_check({"zly": "{nie je json"})
        self.assertEqual(rows[""]["result"], "neplatny_json")

    @unittest.skipUnless(shutil.which("openssl"), "chýba openssl")
    def test_tls_overenie_zostava_zapnute(self):
        cert, key = self.tmp / "cert.pem", self.tmp / "key.pem"
        subprocess.run(["openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes", "-days", "1",
                        "-subj", "/CN=127.0.0.1", "-addext", "subjectAltName=IP:127.0.0.1",
                        "-keyout", str(key), "-out", str(cert)], check=True, capture_output=True)
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(cert, key)
        server = start_server(context)
        try:
            url = f"https://127.0.0.1:{server.server_address[1]}/clanok.html"
            row = self.one(url, "spolu s ďalšími.")
            self.assertEqual(row["result"], "nedostupne")
            self.assertIn("CERTIFICATE_VERIFY_FAILED", row["note"])
            # S výslovne dôveryhodným certifikátom (SSL_CERT_FILE) stránka prejde.
            row = self.one(url, "spolu s ďalšími.", env_extra={"SSL_CERT_FILE": str(cert)})
            self.assertEqual(row["result"], "najdene")
        finally:
            server.shutdown()
            server.server_close()

    def test_skript_nevypina_tls(self):
        source = SCRIPT.read_text(encoding="utf-8")
        for forbidden in ("CERT_NONE", "_create_unverified_context", "check_hostname = False", "verify=False"):
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()
