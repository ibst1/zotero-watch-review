"""A stand-in for Zotero's web API with a small made-up library, for trying the app without touching a real one.

    python tests/mock_zotero.py            -> http://localhost:8765/?api=http://localhost:8765  (any key works)

Serves the app's files too. GET /_state shows the items as they are now; GET /_bump/<key> changes an item's
version, as a sync from another computer would (the app's next change to it then meets a conflict).
"""

import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent.parent
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
USER = "1"
LONG = ("Wilms tumour is the most common renal cancer of childhood. " * 14).strip()

collections = [
    {"key": "TOPF", "name": "F – Forskning", "parentCollection": False},
    {"key": "WATF", "name": "Bevakning", "parentCollection": "TOPF"},
    {"key": "GEN1", "name": "Genetik", "parentCollection": "TOPF"},
    {"key": "WILM", "name": "Wilms tumör", "parentCollection": "GEN1"},
    {"key": "METH", "name": "Metylering", "parentCollection": "TOPF"},
    {"key": "TOPT", "name": "T – Tro, tanke & teologi", "parentCollection": False},
    {"key": "WATT", "name": "Bevakning", "parentCollection": "TOPT"},
    {"key": "APOL", "name": "Apologetik", "parentCollection": "TOPT"},
    {"key": "TREV", "name": "To review", "parentCollection": False},  # for the "Simple" setup
]


def article(key, title, authors, journal, date, coll, abstract="", kind="journalArticle", doi=""):
    return {"key": key, "version": 10, "itemType": kind, "title": title, "date": date,
            "creators": [{"creatorType": "author", "firstName": "A.", "lastName": a} for a in authors],
            "publicationTitle": journal, "abstractNote": abstract, "DOI": doi, "url": f"https://doi.org/{doi}" if doi else "",
            "collections": [coll], "tags": [{"tag": "bevakning"}], "dateAdded": f"{date}T08:00:00Z"}


items = {i["key"]: i for i in [
    article("IT01", "Modeling Wilms Tumor Development in Kidney Organoids", ["Gong", "Li", "Wang", "Chen"],
            "Cancer Research", "2026-10-10", "WATF", LONG, doi="10.1038/s41586-020-2649-2"),  # a real open-access DOI
    article("IT02", "Methylation-defined tumour subtypes in paediatric renal cancer", ["Oberhammer", "Pfister"],
            "Acta Neuropathologica", "2026-10-11", "WATF", "Short abstract.", doi="10.1007/s00401-026-0002"),
    article("IT03", "Textbook Outcome in Pediatric Oncology Surgery", ["Ghandour"], "medRxiv", "2026-10-12", "WATF",
            kind="preprint"),
    article("IT04", "Unexpected patterns, irrelevance, and scientific explanation", ["Southgate", "Robinson"],
            "Zygon", "2026-10-09", "WATT", "On fine-tuning and explanation."),
    article("IT05", "Finding Ourselves After Darwin", ["Rosenberg"], "", "2026-10-13", "WATT", kind="book"),
]}
for extra in (dict(article("IT06", "A plain item to review", ["Svensson"], "BMJ", "2026-09-01", "TREV"), tags=[]),
              dict(article("IT07", "Another item, in two collections", ["Berg"], "Lancet", "2026-09-02", "TREV"),
                   tags=[], collections=["TREV", "APOL"])):
    items[extra["key"]] = extra
library = {i["key"]: i for i in [
    dict(article("LIB1", "Clonal evolution of Wilms tumour", ["Gong", "Andersson"], "Nature", "2024-01-01", "TOPF"),
         tags=[]),
    dict(article("LIB2", "Methylation-defined tumour subtypes in paediatric renal cancer", ["Oberhammer"],
                 "bioRxiv", "2025-06-01", "TOPF", kind="preprint"), tags=[]),
]}
for i in items.values():
    if i["itemType"] == "book":
        i.pop("publicationTitle")
        i["publisher"] = "Baker Academic"
notes = {k: {"key": f"N{k}", "itemType": "note", "parentItem": k, "tags": [{"tag": "claude-bevakning"}],
             "note": f"<h1>Bevakning: varför</h1>\n<p>Relevant for the project on {items[k]['title'][:30]}.</p>\n"
                     f"<p><strong>Projekt:</strong> Wilms tumour evolution</p>\n<p><em>Relevans: {'medel' if k in ('IT04', 'IT01') else 'hög'}.</em></p>"} for k in items}
project_list = {"key": "PLST", "version": 5, "itemType": "note", "tags": [{"tag": "partitur-projekt"}],
                "note": "<h1>Partitur: aktiva projekt</h1>\n<ul>\n<li>F – 2601. Wilms tumour evolution</li>\n"
                        "<li>F – 2605. Metylering i barntumörer</li>\n<li>T – 2610. Artikel - Försyn, slump och mutation</li>\n"
                        "<li>M – Riktlinjer sarkom</li>\n</ul>"}
own_notes = {}  # notes made in the app
library_version = [100]


def wrap(data):
    return {"key": data["key"], "version": data.get("version", 1), "data": data}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        sys.stderr.write("%s %s\n" % (self.command, self.path))

    def send(self, status, body=None, headers=None):
        raw = b"" if body is None else json.dumps(body, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Expose-Headers", "Total-Results, Last-Modified-Version, Retry-After")
        if body is not None:
            self.send_header("Content-Type", "application/json; charset=utf-8")
        for k, v in (headers or {}).items():
            self.send_header(k, str(v))
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

    def page(self, rows, q):
        start, limit = int(q.get("start", ["0"])[0]), int(q.get("limit", ["25"])[0])
        self.send(200, rows[start:start + limit], {"Total-Results": len(rows)})

    def do_GET(self):
        url = urlparse(self.path)
        q, parts = parse_qs(url.query), [p for p in url.path.split("/") if p]
        if parts[:1] == ["keys"]:
            return self.send(200, {"userID": int(USER), "access": {"user": {"library": True, "write": True}}})
        if parts == ["_state"]:
            return self.send(200, items)
        if parts[:1] == ["_bump"]:
            items[parts[1]]["version"] += 1
            return self.send(200, {"version": items[parts[1]]["version"]})
        if parts[:2] == ["users", USER]:
            rest = parts[2:]
            if rest == ["collections"]:
                return self.page([wrap(c) for c in collections], q)
            if len(rest) == 4 and rest[0] == "collections" and rest[2:] == ["items", "top"]:
                tag = q.get("tag", [None])[0]
                rows = [i for i in items.values() if rest[1] in i["collections"] and not i.get("deleted")
                        and (tag is None or any(t["tag"] == tag for t in i["tags"]))]
                return self.page([wrap(i) for i in sorted(rows, key=lambda i: i["dateAdded"])], q)
            if len(rest) == 3 and rest[0] == "items" and rest[2] == "children":
                kids = ([notes[rest[1]]] if rest[1] in notes else []) + [n for n in own_notes.values()
                                                                         if n["parentItem"] == rest[1]]
                return self.send(200, [wrap(n) for n in kids])
            if rest == ["items", "top"] and "q" in q:
                words = q["q"][0].lower().split()
                rows = [i for i in list(items.values()) + list(library.values())
                        if all(w in (i["title"] + " " + " ".join(c["lastName"] for c in i["creators"])).lower()
                               for w in words)]
                return self.page([wrap(i) for i in rows], q)
            if rest == ["items"] and q.get("tag", [""])[0] == "partitur-projekt":
                return self.send(200, [wrap(project_list)])
            if len(rest) == 2 and rest[0] == "items":
                return self.send(200, wrap(items[rest[1]]))
            return self.send(404, {"error": "unknown"})
        # the app's own files
        name = url.path.lstrip("/") or "index.html"
        path = (ROOT / name).resolve()
        if ROOT not in path.parents or not path.is_file():
            return self.send(404, {"error": "no such file"})
        raw = path.read_bytes()
        types = {".html": "text/html; charset=utf-8", ".js": "text/javascript", ".svg": "image/svg+xml",
                 ".png": "image/png", ".webmanifest": "application/manifest+json"}
        self.send_response(200)
        self.send_header("Content-Type", types.get(path.suffix, "application/octet-stream"))
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_POST(self):
        parts = [p for p in urlparse(self.path).path.split("/") if p]
        if parts != ["users", USER, "items"]:
            return self.send(404, {"error": "unknown"})
        made = {}
        for n, obj in enumerate(json.loads(self.rfile.read(int(self.headers["Content-Length"])))):
            library_version[0] += 1
            key = f"NOTE{len(own_notes) + 1}"
            own_notes[key] = dict(obj, key=key, version=library_version[0])
            made[str(n)] = {"key": key, "version": library_version[0], "data": own_notes[key]}
        self.send(200, {"successful": made, "success": {k: v["key"] for k, v in made.items()}, "failed": {}})

    def do_DELETE(self):
        parts = [p for p in urlparse(self.path).path.split("/") if p]
        key = parts[-1]
        if key not in own_notes:
            return self.send(404, {"error": "unknown"})
        if int(self.headers.get("If-Unmodified-Since-Version", "-1")) != own_notes[key]["version"]:
            return self.send(412)
        del own_notes[key]
        self.send(204)

    def do_PATCH(self):
        parts = [p for p in urlparse(self.path).path.split("/") if p]
        if not (parts[:3] == ["users", USER, "items"] and len(parts) == 4 and parts[3] in items):
            return self.send(404, {"error": "unknown"})
        item = items[parts[3]]
        if int(self.headers.get("If-Unmodified-Since-Version", "-1")) != item["version"]:
            return self.send(412)
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        for k, v in body.items():
            if k == "deleted" and not v:
                item.pop("deleted", None)
            else:
                item[k] = v
        library_version[0] += 1
        item["version"] = library_version[0]
        self.send(204, None, {"Last-Modified-Version": item["version"]})


if __name__ == "__main__":
    print(f"http://localhost:{PORT}/?api=http://localhost:{PORT}")
    ThreadingHTTPServer(("localhost", PORT), Handler).serve_forever()
