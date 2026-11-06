# -*- coding: utf-8 -*-
import csv, os, re, collections
from pypdf import PdfReader
C = "/home/claude/L1_MaintiDoc_ELBRIGUY-RAMZI/L1_MaintiDoc_ELBRIGUY-RAMZI_Corpus"
raw = open(f"{C}/inventaire.csv", "rb").read()
raw.decode("utf-8")  # UTF-8 valide
rows = list(csv.DictReader(open(f"{C}/inventaire.csv", encoding="utf-8")))
ok = True
def bad(m):
    global ok; ok = False; print("ERREUR:", m)
COLS = 20
if len(csv.reader(open(f"{C}/inventaire.csv", encoding="utf-8")).__next__()) != COLS: bad("nb colonnes")
ids = [r["document_id"] for r in rows]
if len(ids) != len(set(ids)): bad("doublons d'identifiants")
for i in ids:
    if not re.fullmatch(r"[a-z0-9_]+", i): bad(f"id invalide {i}")
# 1:1 fichiers <-> lignes
on_disk = set()
for root, _, fs in os.walk(C):
    for f in fs:
        rel = os.path.relpath(os.path.join(root, f), C)
        if rel.startswith("documents/") or rel.startswith("images/"): on_disk.add(rel)
inv = {r["fichier"] for r in rows}
if on_disk != inv: bad(f"écart fichiers/inventaire: {on_disk ^ inv}")
for r in rows:
    base = os.path.splitext(os.path.basename(r["fichier"]))[0]
    if base != r["document_id"]: bad(f"nom de fichier ≠ document_id: {r['fichier']}")
    if r["fichier"].endswith(".pdf"):
        n = len(PdfReader(f"{C}/{r['fichier']}").pages)
        if n != int(r["nb_pages"]): bad(f"nb_pages {r['document_id']}: {n} ≠ {r['nb_pages']}")
    if r["type_document"] not in {"manuel","procedure","fiche_securite","schema","codes_alarme","photo","historique"}: bad(f"type {r['document_id']}")
    if r["langue"] not in {"fr","en"}: bad("langue")
    if r["format"] not in {"pdf_texte","pdf_scanne","image"}: bad("format")
    if r["usage_test"] not in {"normal","contradictoire","injection","ambigu"}: bad("usage_test")
    if r["famille_equipement"] not in {"groupes_electrogenes","onduleurs"}: bad("famille")
    for g in r["groupe_acces"].split(" ; "):
        if g not in {"techniciens_ge","techniciens_ups","responsables"}: bad(f"groupe {g}")
    for e in r["equipement_id"].split(" ; "):
        if e not in {"GE-A-01","GE-B-02","UPS-A-01","UPS-B-02"}: bad(f"equipement {e}")
    for k, v in r.items():
        if k not in ("outil_ia","remarques") and v.strip() == "": bad(f"vide {r['document_id']}.{k}")
cnt = collections.Counter(r["format"] for r in rows)
vis = [r for r in rows if r["elements_visuels"] != "aucun"]
print("documents:", len(rows), "| par format:", dict(cnt))
print("par famille:", dict(collections.Counter(r["famille_equipement"] for r in rows)))
print("par type:", dict(collections.Counter(r["type_document"] for r in rows)))
print("avec éléments visuels:", len(vis), "| scannés:", cnt["pdf_scanne"], "| usage_test:", dict(collections.Counter(r["usage_test"] for r in rows)))
print("en anglais:", [r["document_id"] for r in rows if r["langue"] == "en"])
print("accès:", dict(collections.Counter(r["groupe_acces"] for r in rows)))
assert 30 <= len(rows) <= 50, "volume"
assert len(vis) >= 10 and cnt["pdf_scanne"] >= 2
assert sum(r["usage_test"] == "contradictoire" for r in rows) >= 2 and sum(r["usage_test"] == "injection" for r in rows) == 1
tot = sum(os.path.getsize(os.path.join(rt, f)) for rt, _, fs in os.walk(C) for f in fs)
print("taille du corpus: %.1f Mo" % (tot / 1e6))
print("VALIDATION", "OK" if ok else "ÉCHEC")
