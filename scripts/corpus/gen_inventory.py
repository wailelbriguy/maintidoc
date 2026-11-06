# -*- coding: utf-8 -*-
import json, csv
C = "/home/claude/L1_MaintiDoc_ELBRIGUY-RAMZI/L1_MaintiDoc_ELBRIGUY-RAMZI_Corpus"
reg = json.load(open("/home/claude/work/registry.json"))
COLS = ["document_id","fichier","titre","famille_equipement","equipement_id","type_document","version","nb_pages","langue","format",
        "elements_visuels","provenance","licence","genere_par_ia","outil_ia","verifie_par","corrections","groupe_acces","usage_test","remarques"]
CORR = {
 "photo_panneau_ge_a": "teinte orange (rendue jaune au premier essai) corrigée ; recadrage corrigé pour supprimer un fragment de voyant voisin",
 "photo_panneau_ups_a": "teinte orange corrigée ; recadrage corrigé pour supprimer un fragment de voyant voisin",
 "photo_panneau_ge_b": "teinte orange (rendue jaune au premier essai) corrigée",
 "photo_panneau_ups_b": "teinte orange corrigée ; chevauchement des libellés ON BATT / LOW BATT / BATT REPL corrigé",
 "schema_bypass_ups_a": "libellé débordant de sa boîte corrigé",
 "proc_maintenance_prev_ge": "tension minimale de batterie du GE-B-02 corrigée (12,2 V puis 12,3 V) pour concorder avec manuel_ge_b p.6",
 "proc_test_batterie_ups_a_v1": "charge maximale du test ajoutée (50 %) : la durée de 10 min égalait l'autonomie à pleine charge",
 "proc_test_batterie_ups_a_v2": "charge maximale du test ajoutée (50 %) par cohérence avec l'autonomie de 10 min à pleine charge",
}
rows = []
for r in reg:
    rem = r["remarques"]
    if r["format"] == "pdf_scanne":
        rem = (rem + " ; " if rem else "") + "pages rasterisées avec bruit et rotation ; OCR requis"
    if r["type_document"] == "photo":
        rem = (rem + " ; " if rem else "") + "image synthétique générée par script (non photographique)"
    fam1 = r["fichier"].startswith("documents/famille_1") or (r["fichier"].startswith("images") and r["famille_equipement"] == "groupes_electrogenes")
    rows.append({
        "document_id": r["document_id"], "fichier": r["fichier"], "titre": r["titre"], "famille_equipement": r["famille_equipement"],
        "equipement_id": r["equipement_id"], "type_document": r["type_document"], "version": r["version"], "nb_pages": r["nb_pages"],
        "langue": r["langue"], "format": r["format"], "elements_visuels": r["elements_visuels"], "provenance": "synthetique", "licence": "synthetique",
        "genere_par_ia": "oui", "outil_ia": f"Claude (prompt {r['prompt']})", "verifie_par": "Saad" if fam1 else "Wail",
        "corrections": CORR.get(r["document_id"], "aucune"), "groupe_acces": r["groupe_acces"], "usage_test": r["usage_test"], "remarques": rem})
with open(f"{C}/inventaire.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=COLS, delimiter=",", quoting=csv.QUOTE_MINIMAL); w.writeheader(); w.writerows(rows)
print(len(rows), "lignes")
