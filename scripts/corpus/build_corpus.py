# -*- coding: utf-8 -*-
import os, json, shutil, sys
sys.path.insert(0, "/home/claude/work")
from docs_b import *

ROOT = "/home/claude/L1_MaintiDoc_ELBRIGUY-RAMZI"
CORPUS = f"{ROOT}/L1_MaintiDoc_ELBRIGUY-RAMZI_Corpus"
if os.path.exists(ROOT):
    shutil.rmtree(ROOT)
for d in ("documents/famille_1", "documents/famille_2", "images"):
    os.makedirs(f"{CORPUS}/{d}", exist_ok=True)

G1, G2 = "techniciens_ge ; responsables", "techniciens_ups ; responsables"
GE, UPS = "groupes_electrogenes", "onduleurs"
A, B = "GE-A-01", "GE-B-02"
UA, UB = "UPS-A-01", "UPS-B-02"
# (id, dossier, titre, famille, equips, type, version, langue, builder, groupe, usage, prompt, scan, remarques)
DOCS = [
    ("manuel_ge_a", 1, "Manuel d'utilisation groupe électrogène GE-A", GE, A, "manuel", "v1.2 (2025-03)", "fr", lambda: manual_ge(A), G1, "normal", "P02", False, "voyants décrits p.5 ; intervalles p.7"),
    ("manuel_ge_b", 1, "Manuel d'utilisation groupe électrogène GE-B", GE, B, "manuel", "v1.0 (2025-06)", "fr", lambda: manual_ge(B), G1, "normal", "P02", False, "seuils différents du GE-A (température 90 °C)"),
    ("codes_alarme_ge_a", 1, "Codes d'alarme du GE-A-01", GE, A, "codes_alarme", "v1.0 (2025-03)", "fr", lambda: codes_alarme(A), G1, "normal", "P04", False, "tableau 1.1 p.1"),
    ("codes_alarme_ge_b", 1, "Codes d'alarme du GE-B-02", GE, B, "codes_alarme", "v1.0 (2025-06)", "fr", lambda: codes_alarme(B), G1, "normal", "P04", False, "seuils différents du GE-A"),
    ("proc_demarrage_ge_a", 1, "Procédure de démarrage du GE-A-01", GE, A, "procedure", "v1.1 (2025-02)", "fr", lambda: p_demarrage_ge(A), G1, "normal", "P05", False, ""),
    ("proc_arret_ge_a", 1, "Procédure d'arrêt du GE-A-01", GE, A, "procedure", "v1.0 (2025-02)", "fr", p_arret_ge_a, G1, "normal", "P05", False, ""),
    ("proc_demarrage_ge_b", 1, "Procédure de démarrage du GE-B-02", GE, B, "procedure", "v1.0 (2025-04)", "fr", lambda: p_demarrage_ge(B), G1, "normal", "P05", False, "valeurs différentes du GE-A-01"),
    ("proc_vidange_ge_a_v1", 1, "Procédure de vidange du GE-A-01 (v1)", GE, A, "procedure", "v1 (2023-06)", "fr", lambda: p_vidange(1), G1, "contradictoire", "P07", True, "couple du bouchon 40 N·m ; contredit proc_vidange_ge_a_v2 (45 N·m)"),
    ("proc_vidange_ge_a_v2", 1, "Procédure de vidange du GE-A-01 (v2)", GE, A, "procedure", "v2 (2025-09)", "fr", lambda: p_vidange(2), G1, "contradictoire", "P07", False, "couple du bouchon 45 N·m ; contredit proc_vidange_ge_a_v1 (40 N·m)"),
    ("proc_refroidissement_ge", 1, "Contrôle du circuit de refroidissement des GE", GE, f"{A} ; {B}", "procedure", "v1.0 (2025-05)", "fr", p_refroidissement, G1, "ambigu", "P05", False, "seuils de température différents selon l'équipement"),
    ("proc_maintenance_prev_ge", 1, "Maintenance préventive trimestrielle des GE", GE, f"{A} ; {B}", "procedure", "v1.0 (2024-09)", "fr", p_maintenance_prev, G1, "normal", "P05", True, "document scanné"),
    ("fiche_securite_ge", 1, "Fiche de sécurité des groupes électrogènes", GE, f"{A} ; {B}", "fiche_securite", "v1.0 (2025-01)", "fr", lambda: fiche_securite("ge"), G1, "normal", "P09", False, ""),
    ("schema_synoptique_ge_a", 1, "Schéma synoptique du GE-A-01", GE, A, "schema", "v1.0 (2025-01)", "fr", lambda: schema_doc(A, "synoptique_ge_a"), G1, "normal", "P10", False, ""),
    ("schema_electrique_ge_b", 1, "Schéma électrique simplifié du GE-B-02", GE, B, "schema", "v1.0 (2025-01)", "fr", lambda: schema_doc(B, "electrique_ge_b"), G1, "normal", "P10", False, ""),
    ("schema_refroidissement_ge_a", 1, "Circuit de refroidissement du GE-A-01", GE, A, "schema", "v1.0 (2025-01)", "fr", lambda: schema_doc(A, "refroidissement_ge_a"), G1, "normal", "P10", False, ""),
    ("historique_ge_a", 1, "Historique des interventions du GE-A-01", GE, A, "historique", "2026-10", "fr", lambda: historique(A), G1, "normal", "P11", False, "récurrence de GA-102 ; ticket TK-GA-0007"),
    ("historique_ge_b", 1, "Historique des interventions du GE-B-02", GE, B, "historique", "2026-10", "fr", lambda: historique(B), G1, "normal", "P11", False, ""),
    ("note_service_ge_piegee", 1, "Note de service NS-2025-14 (refroidissement GE)", GE, f"{A} ; {B}", "procedure", "v1 (2025-11)", "fr", note_piegee, "responsables", "injection", "P12", False, "contient une instruction malveillante p.2 (document piégé)"),
    ("datasheet_ge_a_en", 1, "Datasheet GE-A diesel generator set", GE, A, "manuel", "v1.0 (2025-03)", "en", datasheet_en, G1, "normal", "P13", False, "document en anglais"),
    ("manuel_ups_a", 2, "Manuel d'utilisation onduleur UPS-A", UPS, UA, "manuel", "v1.1 (2025-02)", "fr", lambda: manual_ups(UA), G2, "normal", "P03", False, "modes de fonctionnement p.6"),
    ("manuel_ups_b", 2, "Manuel d'utilisation onduleur UPS-B", UPS, UB, "manuel", "v1.0 (2025-05)", "fr", lambda: manual_ups(UB), G2, "normal", "P03", False, "pas de bypass sur ce modèle"),
    ("codes_alarme_ups_a", 2, "Codes d'alarme de l'UPS-A-01", UPS, UA, "codes_alarme", "v1.0 (2025-02)", "fr", lambda: codes_alarme(UA), G2, "normal", "P04", False, "tableau 1.1 p.1"),
    ("codes_alarme_ups_b", 2, "Codes d'alarme de l'UPS-B-02", UPS, UB, "codes_alarme", "v1.0 (2025-05)", "fr", lambda: codes_alarme(UB), G2, "normal", "P04", False, ""),
    ("proc_test_batterie_ups_a_v1", 2, "Test de décharge des batteries UPS-A-01 (v1)", UPS, UA, "procedure", "v1 (2023-06)", "fr", lambda: p_test_batterie(1), G2, "contradictoire", "P08", False, "durée du test 10 min ; contredit v2 (5 min)"),
    ("proc_test_batterie_ups_a_v2", 2, "Test de décharge des batteries UPS-A-01 (v2)", UPS, UA, "procedure", "v2 (2025-04)", "fr", lambda: p_test_batterie(2), G2, "contradictoire", "P08", False, "durée du test 5 min ; contredit v1 (10 min)"),
    ("proc_bypass_ups_a", 2, "Transfert vers le bypass de l'UPS-A-01", UPS, UA, "procedure", "v1.0 (2025-06)", "fr", p_bypass, G2, "normal", "P06", False, ""),
    ("proc_remplacement_batterie_ups_b", 2, "Remplacement des batteries de l'UPS-B-02", UPS, UB, "procedure", "v1.0 (2024-11)", "fr", p_remplacement_batt, G2, "normal", "P06", True, "document scanné"),
    ("proc_demarrage_ups_b", 2, "Procédure de démarrage de l'UPS-B-02", UPS, UB, "procedure", "v1.0 (2025-03)", "fr", p_demarrage_ups_b, G2, "normal", "P06", False, ""),
    ("proc_nettoyage_ventilation_ups", 2, "Nettoyage de la ventilation des onduleurs", UPS, f"{UA} ; {UB}", "procedure", "v1.0 (2025-05)", "fr", p_nettoyage, G2, "ambigu", "P06", False, "seuils de température différents selon l'équipement"),
    ("fiche_securite_ups", 2, "Fiche de sécurité des onduleurs", UPS, f"{UA} ; {UB}", "fiche_securite", "v1.0 (2025-01)", "fr", lambda: fiche_securite("ups"), G2, "normal", "P09", False, ""),
    ("schema_synoptique_ups_a", 2, "Schéma synoptique de l'UPS-A-01", UPS, UA, "schema", "v1.0 (2025-01)", "fr", lambda: schema_doc(UA, "synoptique_ups_a"), G2, "normal", "P10", False, ""),
    ("schema_cablage_ups_b", 2, "Schéma de câblage de l'UPS-B-02", UPS, UB, "schema", "v1.0 (2025-01)", "fr", lambda: schema_doc(UB, "cablage_ups_b"), G2, "normal", "P10", False, ""),
    ("schema_bypass_ups_a", 2, "Schéma du bypass de l'UPS-A-01", UPS, UA, "schema", "v1.0 (2025-01)", "fr", lambda: schema_doc(UA, "bypass_ups_a"), G2, "normal", "P10", False, ""),
    ("historique_ups_a", 2, "Historique des interventions de l'UPS-A-01", UPS, UA, "historique", "2026-10", "fr", lambda: historique(UA), G2, "normal", "P11", False, "ticket TK-UA-0003 ouvert"),
    ("historique_ups_b", 2, "Historique des interventions de l'UPS-B-02", UPS, UB, "historique", "2026-10", "fr", lambda: historique(UB), G2, "normal", "P11", False, "ticket TK-UB-0005 ouvert"),
    ("note_service_ups_batteries", 2, "Note de service NS-2026-03 (batteries onduleurs)", UPS, f"{UA} ; {UB}", "procedure", "v1 (2026-02)", "fr", note_ups, "responsables", "normal", "P12", False, "document réservé aux responsables (test de contrôle d'accès)"),
    ("quickguide_ups_b_en", 2, "Quick guide UPS-B online UPS", UPS, UB, "manuel", "v1.0 (2025-05)", "en", quickguide_en, G2, "normal", "P13", False, "document en anglais"),
]

registry = []
for (did, fol, titre, fam, eqs, typ, ver, lang, fn, grp, usage, pr, scan, rem) in DOCS:
    out = f"{CORPUS}/documents/famille_{fol}/{did}.pdf"
    tmp = out if not scan else f"/home/claude/figs/{did}_text.pdf"
    db = DocBuilder(tmp, did, titre, ver)
    n = db.build(fn())
    if scan:
        scan_pdf(tmp, out, seed=len(did))
    registry.append(dict(document_id=did, fichier=f"documents/famille_{fol}/{did}.pdf", titre=titre, famille_equipement=fam,
                         equipement_id=eqs, type_document=typ, version=ver, nb_pages=n, langue=lang,
                         format="pdf_scanne" if scan else "pdf_texte", elements_visuels=db.visuals_str(),
                         groupe_acces=grp, usage_test=usage, prompt=pr, remarques=rem, visuals=db.visuals))
    print("OK", did, n, "p", "(scanné)" if scan else "")

# ---------- photos ----------
IMG = f"{CORPUS}/images"
photos = [
    ("photo_panneau_ge_a", "Photo du panneau de commande du GE-A-01 (gros plan)", A, "ambigu", "voyant TEMP orange allumé",
     lambda: photoize(draw_panel(LEDS[A], "TEMP", None, "#c9a227").crop((866, 440, 1206, 660)).resize((1020, 660), PILImage.LANCZOS), 11, angle=1.5),
     "gros plan sans plaque visible ; identique visuellement à photo_panneau_ups_a"),
    ("photo_panneau_ups_a", "Photo du panneau de commande de l'UPS-A-01 (gros plan)", UA, "ambigu", "voyant TEMP orange allumé",
     lambda: photoize(draw_panel(LEDS[UA], "TEMP", None, "#2b6cb0").crop((866, 440, 1206, 660)).resize((1020, 660), PILImage.LANCZOS), 12, angle=-1.2),
     "gros plan sans plaque visible ; identique visuellement à photo_panneau_ge_a"),
    ("photo_panneau_ge_b", "Photo du panneau de commande du GE-B-02", B, "normal", "voyant FUEL orange allumé ; étiquette modèle visible",
     lambda: photoize(draw_panel(LEDS[B], "FUEL", "GE-B 60", "#c9a227"), 13, angle=1.8), "voyant carburant bas (GB-203)"),
    ("photo_panneau_ups_b", "Photo du panneau de commande de l'UPS-B-02", UB, "normal", "voyant BATT REPL orange allumé ; étiquette modèle visible",
     lambda: photoize(draw_panel(LEDS[UB], "BATT REPL", "UPS-B 10", "#2b6cb0"), 14, angle=-1.6), "remplacement des batteries requis (UB-405)"),
    ("photo_plaque_ge_a", "Photo de la plaque signalétique du GE-A-01", A, "normal", "plaque : modèle et numéro de série lisibles",
     lambda: photoize(draw_plate([("PLAQUE SIGNALÉTIQUE", ""), ("Modèle", "GE-A 100 kVA"), ("Équipement", A), ("N° de série", EQ[A]["serie"]),
                                  ("Puissance", "100 kVA / 80 kW"), ("Tension", "400 V - 50 Hz"), ("Année", "2023")]), 15, angle=1.0), "permet de confirmer l'équipement"),
    ("photo_plaque_ups_b", "Photo de la plaque signalétique de l'UPS-B-02", UB, "normal", "plaque : modèle et numéro de série lisibles",
     lambda: photoize(draw_plate([("PLAQUE SIGNALÉTIQUE", ""), ("Modèle", "UPS-B 10 kVA"), ("Équipement", UB), ("N° de série", EQ[UB]["serie"]),
                                  ("Puissance", "10 kVA / 9 kW"), ("Tension", "230 V - 50 Hz"), ("Année", "2024")], tint=(168, 176, 188)), 16, angle=-1.0), "permet de confirmer l'équipement"),
]
for did, titre, eq, usage, vis, fn, rem in photos:
    im = fn()
    im.save(f"{IMG}/{did}.jpg", quality=88)
    registry.append(dict(document_id=did, fichier=f"images/{did}.jpg", titre=titre, famille_equipement=EQ[eq]["fam"], equipement_id=eq,
                         type_document="photo", version="2026-10", nb_pages=1, langue="fr", format="image", elements_visuels=vis,
                         groupe_acces=G1 if EQ[eq]["fam"] == GE else G2, usage_test=usage, prompt="P14", remarques=rem, visuals=[]))
    print("OK photo", did)

json.dump(registry, open("/home/claude/work/registry.json", "w"), ensure_ascii=False, indent=1)
print("TOTAL", len(registry))
