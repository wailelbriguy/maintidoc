# MaintiDoc — Livrable 1 : cadrage, corpus et architecture

## Équipe
Binôme **ELBRIGUY-RAMZI** : Wail ELBRIGUY et Saad RAMZI.
Module IA générative multimodale — EMSI 2026.

## Objectif du projet
MaintiDoc est un assistant documentaire pour techniciens de maintenance. À partir d'une question et d'une photo, il retrouve dans des manuels, procédures et schémas les informations utiles, répond **en citant ses sources** (document, page, figure ou tableau), consulte l'historique des interventions via un outil MCP et prépare un ticket, **créé seulement après approbation humaine**. C'est une aide documentaire : il ne pilote aucun équipement, ne garantit aucun diagnostic et ne remplace pas un technicien habilité.

Périmètre : deux familles d'équipements fictifs, des **groupes électrogènes** (GE-A-01, GE-B-02) et des **onduleurs** (UPS-A-01, UPS-B-02). Trois groupes d'accès : `techniciens_ge`, `techniciens_ups`, `responsables`.

## Contenu du ZIP
| Élément | Description |
|---|---|
| `L1_MaintiDoc_ELBRIGUY-RAMZI_Rapport.pdf` | Rapport complet (cadrage, corpus, architecture, flux, risques, planning) |
| `L1_MaintiDoc_ELBRIGUY-RAMZI_LienGitHub.txt` | URL du dépôt GitHub |
| `README.md` | Ce fichier |
| `L1_MaintiDoc_ELBRIGUY-RAMZI_Corpus/` | 43 documents (`documents/famille_1`, `documents/famille_2`, `images/`), `inventaire.csv`, `prompts_corpus.md` |

## Structure du dépôt GitHub
```
maintidoc/
├── README.md
├── .gitignore
├── docs/
│   └── diagrammes/      sources et images des schémas (architecture et flux)
├── scripts/corpus/      scripts de génération et de contrôle du corpus
└── corpus/
    ├── inventaire.csv
    ├── prompts_corpus.md
    ├── documents/famille_1/ , famille_2/
    └── images/
```

## À propos du corpus
Les 43 documents sont **synthétiques** (générés avec l'aide de Claude puis contrôlés) ; toutes les valeurs techniques sont fictives. Le corpus contient des cas de test pour la semaine 5 : 2 paires de documents contradictoires, 1 document piégé (injection de prompt), des photos ambiguës et 3 documents scannés. Détails dans `inventaire.csv` et `prompts_corpus.md`.

## Scripts de génération (`scripts/corpus/`)
Les scripts Python produisent les PDF, schémas, images et scans à partir d'un référentiel unique (`master.py`) puis contrôlent la cohérence (`checks.py`, `validate.py`). Les chemins sont écrits en dur (`/home/claude/...`) : les adapter avant de relancer. Dépendances : reportlab, pypdf, matplotlib, pillow, numpy, poppler-utils (`pdftoppm`), tesseract (contrôle OCR).
