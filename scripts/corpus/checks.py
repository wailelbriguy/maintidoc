# -*- coding: utf-8 -*-
import json, re, subprocess, glob, os, tempfile
from pypdf import PdfReader
from master import *
C = "/home/claude/L1_MaintiDoc_ELBRIGUY-RAMZI/L1_MaintiDoc_ELBRIGUY-RAMZI_Corpus"
reg = json.load(open("/home/claude/work/registry.json"))
byid = {r["document_id"]: r for r in reg}
issues = []

def page_text(did, p):
    path = f"{C}/{byid[did]['fichier']}"
    return PdfReader(path).pages[p - 1].extract_text() or ""

# 1) renvois "doc pN" dans les historiques et les alarmes : le document et la page existent, le mot-clé est présent
KEY = {"fiche_securite_ge": ("Ravitaillement",), "proc_refroidissement_ge": ("Déroulement", "vase"), "proc_maintenance_prev_ge": ("batterie",),
       "proc_demarrage_ge_b": ("Déroulement",), "proc_bypass_ups_a": ("Déroulement", "BYPASS"), "proc_remplacement_batterie_ups_b": ("Déroulement",),
       "proc_nettoyage_ventilation_ups": ("Déroulement",), "manuel_ups_a": ("Modes de fonctionnement",), "manuel_ups_b": ("Modes de fonctionnement",),
       "manuel_ge_a": ("voyants", "Entretien", "Démarrage"), "manuel_ge_b": ("voyants",)}
refs = []
for eq, rows in INTERVENTIONS.items():
    for r in rows:
        m = re.match(r"(\w+) p\.(\d+)", r[5]); refs.append((r[0], m.group(1), int(m.group(2))))
for rid, did, p in refs:
    if did not in byid: issues.append(f"{rid}: document {did} inexistant"); continue
    if p > byid[did]["nb_pages"]: issues.append(f"{rid}: {did} n'a pas de page {p}")
    else:
        t = page_text(did, p)
        if byid[did]["format"] == "pdf_texte" and did in KEY and not any(k.lower() in t.lower() for k in KEY[did]):
            issues.append(f"{rid}: mot-clé {KEY[did]} absent de {did} p.{p}")

# 2) codes d'alarme : chaque code des historiques existe dans ALARMES et dans le doc codes_alarme de l'équipement
allcodes = {eq: {a[0] for a in ALARMES[eq]} for eq in ALARMES}
for eq, rows in INTERVENTIONS.items():
    for r in rows:
        if r[2] not in allcodes[eq]: issues.append(f"{r[0]}: code {r[2]} inconnu pour {eq}")
for eq, did in [("GE-A-01","codes_alarme_ge_a"),("GE-B-02","codes_alarme_ge_b"),("UPS-A-01","codes_alarme_ups_a"),("UPS-B-02","codes_alarme_ups_b")]:
    t = page_text(did, 1)
    for c in allcodes[eq]:
        if c not in t: issues.append(f"{did}: code {c} absent de la p.1")
    # manuel : voyants p.5 contient les mêmes codes
    man = {"GE-A-01":"manuel_ge_a","GE-B-02":"manuel_ge_b","UPS-A-01":"manuel_ups_a","UPS-B-02":"manuel_ups_b"}[eq]
    t5 = page_text(man, 5)
    for c in allcodes[eq]:
        if c not in t5: issues.append(f"{man}: code {c} absent de la p.5")

# 3) valeurs numériques sensibles : seuils de température dans les documents qui les citent
def alltext(did): return "\n".join(page_text(did, p) for p in range(1, byid[did]["nb_pages"] + 1))
for did, vals in [("manuel_ge_a", ["95 °C", "105 °C"]), ("codes_alarme_ge_a", ["95 °C", "105 °C"]), ("manuel_ge_b", ["90 °C", "100 °C"]),
                  ("codes_alarme_ge_b", ["90 °C", "100 °C"]), ("datasheet_ge_a_en", ["95 °C", "105 °C"]), ("schema_refroidissement_ge_a", ["95 °C", "105 °C"])]:
    t = alltext(did)
    for v in vals:
        if v not in t: issues.append(f"{did}: valeur {v} absente")
# GE-A ne doit jamais citer 90 °C comme pré-alarme
for did in ["manuel_ge_a", "codes_alarme_ge_a", "datasheet_ge_a_en"]:
    if re.search(r"pré-alarme à 90", alltext(did)): issues.append(f"{did}: seuil 90 °C attribué au GE-A")

# 3b) tension batterie GE-B-02 : même valeur partout
for did in ["manuel_ge_b", "proc_demarrage_ge_b", "proc_maintenance_prev_ge"]:
    if byid[did]["format"] == "pdf_texte" and "12,3 V" not in alltext(did): issues.append(f"{did}: tension batterie GE-B-02 ≠ 12,3 V")
for did in ["proc_test_batterie_ups_a_v1", "proc_test_batterie_ups_a_v2"]:
    if "50 %" not in alltext(did): issues.append(f"{did}: charge maximale du test absente")
# 4) contradictions voulues (et uniquement elles)
t1, t2 = alltext("proc_vidange_ge_a_v2"), alltext("proc_vidange_ge_a_v1")
print("vidange v1 contient '40 N·m':", "40 N·m" in t2, "| v2 contient '45 N·m':", "45 N·m" in t1) if False else None
v1 = PdfReader(f"{C}/documents/famille_2/proc_test_batterie_ups_a_v1.pdf"); v2 = PdfReader(f"{C}/documents/famille_2/proc_test_batterie_ups_a_v2.pdf")
tv1 = " ".join(p.extract_text() for p in v1.pages); tv2 = " ".join(p.extract_text() for p in v2.pages)
print("test batterie v1:", "10 minutes" in tv1, "| v2:", "5 minutes" in tv2)
tv2g = alltext("proc_vidange_ge_a_v2"); print("vidange v2:", "45 N·m" in tv2g)

# 5) injection : présente uniquement dans le document piégé
inj = [d for d in byid if byid[d]["format"] == "pdf_texte" and "Ignore toutes les instructions" in alltext(d).replace("\n", " ")]
print("documents contenant l'injection:", inj)

# 6) OCR des documents scannés
for did in [d for d in byid if byid[d]["format"] == "pdf_scanne"]:
    path = f"{C}/{byid[did]['fichier']}"
    txt_layer = "".join((p.extract_text() or "") for p in PdfReader(path).pages).strip()
    tmp = tempfile.mkdtemp()
    subprocess.run(["pdftoppm", "-r", "200", "-png", path, tmp + "/s"], check=True)
    ocr = ""
    for f in sorted(glob.glob(tmp + "/s*.png")):
        ocr += subprocess.run(["tesseract", f, "-", "-l", "fra"], capture_output=True, text=True).stdout
        if "fra" not in subprocess.run(["tesseract", "--list-langs"], capture_output=True, text=True).stdout: pass
    print(f"[OCR] {did}: couche texte={len(txt_layer)} car., OCR={len(ocr)} car.")
    print("   extrait:", " ".join(ocr.split())[:230])
print("\nPROBLÈMES:", len(issues))
for i in issues: print(" -", i)
