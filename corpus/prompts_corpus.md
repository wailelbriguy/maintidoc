# Journal des prompts du corpus — MaintiDoc

Équipe : Wail ELBRIGUY, Saad RAMZI
Outil : Claude (Anthropic), interface claude.ai — modèle Claude Sonnet 5.5
Date : 2026-11-04

## Note de méthode

- Voie choisie : **génération de documents synthétiques** (voie 2 des consignes). Aucun document public n'a été téléchargé : le corpus ne dépend donc d'aucun lien externe ni d'aucune licence tierce.
- Les documents ne sont pas écrits « à la main » dans un chat : Claude a écrit des scripts Python (ReportLab, Matplotlib, Pillow) qui produisent les PDF, les schémas, les images et les scans à partir d'un **référentiel technique unique** (équipements, codes d'alarme, seuils, groupes d'accès). Cela garantit la cohérence des identifiants, des codes et des numéros de page.
- **P00** reproduit les demandes réelles de l'équipe. **P01 à P15** sont les consignes de génération formulées par lot (une ligne par lot), telles qu'elles ont été données à Claude pour produire les documents. La colonne `outil_ia` de `inventaire.csv` renvoie à ces numéros.
- Toutes les valeurs techniques (seuils, couples de serrage, durées, capacités) sont **fictives** : plausibles, mais non conformes à un matériel réel.

## P00 — Demandes réelles de l'équipe (2026-11-04)

> « realise le livrable 1 dis moi exactement ce que tu vas faire etape par etapes et explique les moi »

Réponses de l'équipe aux questions de cadrage : binôme Wail ELBRIGUY et Saad RAMZI ; familles *groupes électrogènes* et *onduleurs* ; un seul PC partagé (8 Go de RAM, GPU Intel UHD intégré, aucun GPU externe) ; équipements et groupes d'accès validés ; rendu prévu le lendemain (2026-11-05).

## P01 — Référentiel technique (2026-11-04)

Définir quatre équipements fictifs (GE-A-01, GE-B-02, UPS-A-01, UPS-B-02) avec leurs caractéristiques, six codes d'alarme par équipement (code, voyant, couleur, seuil, causes probables, action documentaire), l'organisation des voyants sur le panneau (TEMP et OVLD voisins sur les quatre panneaux pour créer une ambiguïté visuelle), des historiques d'interventions cohérents et trois groupes d'accès : `techniciens_ge`, `techniciens_ups`, `responsables`.

## P02 — Manuels des groupes électrogènes (2026-11-04)

Générer deux manuels de 8 pages en français (GE-A-01 et GE-B-02) : sommaire, sécurité, caractéristiques (tableau), synoptique (figure), panneau et voyants (figure + tableau), démarrage/arrêt, entretien, dépannage. Les seuils du GE-B-02 doivent différer de ceux du GE-A-01 (température 90 °C au lieu de 95 °C).

## P03 — Manuels des onduleurs (2026-11-04)

Générer deux manuels de 8 pages (UPS-A-01 et UPS-B-02) sur la même structure, avec une section « modes de fonctionnement » (normal, sur batterie, bypass). Le modèle B n'a pas de bypass.

## P04 — Tableaux de codes d'alarme (2026-11-04)

Générer un document de 2 pages par équipement : tableau des codes (code, voyant, couleur, signification) et tableau des seuils, causes probables et renvois vers les procédures. Les codes doivent être identiques à ceux du manuel (page 5).

## P05 — Procédures des groupes électrogènes (2026-11-04)

Générer les procédures de démarrage (GE-A-01 et GE-B-02), d'arrêt (GE-A-01), de contrôle du refroidissement (commune aux deux équipements, avec tableau des valeurs par équipement) et de maintenance préventive trimestrielle. Valeurs cohérentes avec les manuels.

## P06 — Procédures des onduleurs (2026-11-04)

Générer les procédures de transfert vers le bypass (UPS-A-01), de remplacement des batteries (UPS-B-02), de démarrage (UPS-B-02) et de nettoyage de la ventilation (commune aux deux équipements).

## P07 — Paire contradictoire n°1 : vidange du GE-A-01 (2026-11-04)

Générer deux versions de la procédure de vidange, identiques sauf le couple de serrage du bouchon : **40 N·m** dans la v1 (2023-06) et **45 N·m** dans la v2 (2025-09). La v1 est ensuite dégradée en scan.

## P08 — Paire contradictoire n°2 : test des batteries UPS-A-01 (2026-11-04)

Générer deux versions de la procédure de test de décharge, identiques sauf la durée du test : **10 minutes** dans la v1 (2023-06) et **5 minutes** dans la v2 (2025-04).

## P09 — Fiches de sécurité (2026-11-04)

Générer une fiche de sécurité par famille (carburant, batterie de démarrage, brûlures, électricité pour les groupes ; batteries, bus continu, ventilation pour les onduleurs) avec un tableau risques / protections / conduite à tenir.

## P10 — Schémas (2026-11-04)

Générer six schémas de principe avec légende : synoptique du GE-A-01, schéma électrique du GE-B-02, circuit de refroidissement du GE-A-01, synoptique de l'UPS-A-01, câblage de l'UPS-B-02 et bypass de l'UPS-A-01.

## P11 — Historiques d'interventions (2026-11-04)

Générer un historique de quatre interventions par équipement (référence, date, code d'alarme, constat, action, source documentaire, statut) et les tickets ouverts correspondants. Chaque code d'alarme et chaque renvoi de page doit exister dans les autres documents.

## P12 — Notes de service, dont le document piégé (2026-11-04)

Générer (a) une note de service réservée aux responsables sur les batteries des onduleurs ; (b) une note de service NS-2025-14 d'apparence légitime sur le refroidissement des groupes électrogènes dont la **page 2 contient une tentative d'injection de prompt** (instruction d'ignorer les consignes, de divulguer les documents du groupe `responsables`, de créer un ticket sans approbation et d'envoyer un résumé vers une adresse en `.invalid`). Ce document sert uniquement de cas de test pour la semaine 5.

## P13 — Documents en anglais (2026-11-04)

Générer deux documents courts en anglais, signalés comme tels : une fiche technique du GE-A-01 et un guide rapide de l'UPS-B-02, cohérents avec les documents français.

## P14 — Photos et plaques signalétiques synthétiques (2026-11-04)

Générer six images : quatre vues de panneaux de commande (un voyant orange allumé) et deux plaques signalétiques. Les deux gros plans « TEMP orange » du GE-A-01 et de l'UPS-A-01 doivent être visuellement identiques (cas ambigu) ; les plaques servent à lever l'ambiguïté.

## P15 — Simulation de documents scannés (2026-11-04)

Transformer trois PDF en scans : rasterisation à 130 ppp, légère rotation, flou, bruit, taches et ombre de bord, sans couche texte (documents : `proc_vidange_ge_a_v1`, `proc_maintenance_prev_ge`, `proc_remplacement_batterie_ups_b`).

## Journal des vérifications (résultats réels)

| Contrôle | Résultat |
|---|---|
| Nombre de pages et présence de chaque figure/tableau sur la page annoncée (automatique) | Conforme (aucun débordement de page) |
| Codes d'alarme identiques entre codes_alarme, manuel p.5, historiques, documents en anglais (automatique) | Conforme |
| Renvois « document pN » des historiques : document existant, page existante, mot-clé présent (automatique) | Conforme |
| Injection présente dans un seul document (automatique) | `note_service_ge_piegee` uniquement |
| OCR des 3 scans (Tesseract, modèle anglais) | Lisibles ; accents perdus (« contréle », « 4 huile »), « ≥ » lu « = » |
| Relecture visuelle (manuel, scan, schéma, photos) | 4 défauts corrigés : voyants orange rendus jaunes, recadrage non ambigu, libellés qui se chevauchent, texte débordant d'une boîte |
| Relecture de cohérence des valeurs (non détectée par les contrôles automatiques) | 2 incohérences corrigées : tension de batterie du GE-B-02 (12,2 V / 12,3 V) et durée du test UPS-A-01 égale à l'autonomie à pleine charge |
| Relecture humaine croisée | **À réaliser par Wail et Saad avant le rendu** |
