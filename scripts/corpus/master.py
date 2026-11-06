# -*- coding: utf-8 -*-
"""Source de vérité du corpus MaintiDoc : tous les documents en dérivent."""

GROUPES = {
    "techniciens_ge": "Techniciens groupes électrogènes (GE-A-01, GE-B-02)",
    "techniciens_ups": "Techniciens onduleurs (UPS-A-01, UPS-B-02)",
    "responsables": "Responsables maintenance (accès à tout le corpus, y compris les notes de service)",
}

EQ = {
    "GE-A-01": dict(fam="groupes_electrogenes", court="GE-A", nom="Groupe électrogène diesel GE-A (100 kVA)",
                    puissance="100 kVA / 80 kW", tension="400 V triphasé, 50 Hz",
                    moteur="Diesel 4 cylindres, refroidi par liquide", reservoir="200 L de gazole",
                    huile="15W-40, 12 L", refroid="18 L (mélange eau + antigel 50 %)", batterie="12 V, 100 Ah",
                    serie="GA100-2023-0417", pre="GA", temp_pre=95, temp_stop=105, carb=20, batt_v=11.5,
                    p_huile=2.0, vidange_h=250, filtre_air_h=500, demarreur_s=10, flexion=10),
    "GE-B-02": dict(fam="groupes_electrogenes", court="GE-B", nom="Groupe électrogène diesel GE-B (60 kVA)",
                    puissance="60 kVA / 48 kW", tension="400 V triphasé, 50 Hz",
                    moteur="Diesel 3 cylindres, refroidi par liquide", reservoir="120 L de gazole",
                    huile="15W-40, 9 L", refroid="14 L (mélange eau + antigel 50 %)", batterie="12 V, 80 Ah",
                    serie="GB060-2024-0112", pre="GB", temp_pre=90, temp_stop=100, carb=25, batt_v=11.8,
                    p_huile=1.8, vidange_h=200, filtre_air_h=400, demarreur_s=8, flexion=8),
    "UPS-A-01": dict(fam="onduleurs", court="UPS-A", nom="Onduleur en ligne UPS-A (20 kVA)",
                     puissance="20 kVA / 18 kW", tension="Entrée et sortie 400 V triphasé, 50 Hz",
                     batterie="40 blocs 12 V 9 Ah (bus continu 480 V)", autonomie="10 min à pleine charge",
                     serie="UA020-2023-0236", pre="UA", temp_dissip=70, filtres_mois=6),
    "UPS-B-02": dict(fam="onduleurs", court="UPS-B", nom="Onduleur en ligne UPS-B (10 kVA)",
                     puissance="10 kVA / 9 kW", tension="Entrée et sortie 230 V monophasé, 50 Hz",
                     batterie="20 blocs 12 V 7 Ah (bus continu 240 V)", autonomie="8 min à pleine charge",
                     serie="UB010-2024-0158", pre="UB", temp_dissip=65, filtres_mois=12),
}

# Voyants : ordre = ligne 1 (3 voyants) puis ligne 2 (3 voyants). TEMP et OVLD sont voisins en bas à droite
# sur les quatre panneaux (source volontaire d'ambiguïté visuelle).
LEDS = {
    "GE-A-01": [("OIL", "red", "GA-101"), ("FUEL", "orange", "GA-103"), ("BATT", "orange", "GA-104"),
                ("START", "red", "GA-106"), ("TEMP", "orange", "GA-102"), ("OVLD", "red", "GA-105")],
    "GE-B-02": [("OIL", "red", "GB-201"), ("FUEL", "orange", "GB-203"), ("BATT", "orange", "GB-204"),
                ("START", "red", "GB-206"), ("TEMP", "orange", "GB-202"), ("OVLD", "red", "GB-205")],
    "UPS-A-01": [("ON BATT", "orange", "UA-301"), ("LOW BATT", "red", "UA-302"), ("FAN", "orange", "UA-305"),
                 ("BYPASS", "orange", "UA-306"), ("TEMP", "orange", "UA-304"), ("OVLD", "red", "UA-303")],
    "UPS-B-02": [("ON BATT", "orange", "UB-401"), ("LOW BATT", "red", "UB-402"), ("BATT REPL", "orange", "UB-405"),
                 ("RECT", "red", "UB-406"), ("TEMP", "orange", "UB-404"), ("OVLD", "red", "UB-403")],
}
COULEUR_FR = {"red": "rouge", "orange": "orange", "green": "vert"}

# code -> (libellé, seuil/condition, causes probables, action documentaire)
ALARMES = {
    "GE-A-01": [
        ("GA-101", "Pression d'huile basse", "< 1,0 bar : arrêt immédiat", "niveau d'huile bas, filtre colmaté, pompe à huile", "Arrêter le groupe ; ne pas redémarrer sans contrôle (voir proc_vidange_ge_a_v2)"),
        ("GA-102", "Température du liquide de refroidissement élevée", "Pré-alarme à 95 °C ; arrêt automatique à 105 °C", "niveau de liquide bas, radiateur encrassé, courroie du ventilateur détendue", "Voir proc_refroidissement_ge"),
        ("GA-103", "Niveau de carburant bas", "< 20 % du réservoir (200 L)", "consommation prolongée, jauge défectueuse", "Ravitailler (voir fiche_securite_ge)"),
        ("GA-104", "Tension de la batterie de démarrage basse", "< 11,5 V", "batterie usée, chargeur défaillant, bornes oxydées", "Contrôler la batterie (voir proc_maintenance_prev_ge)"),
        ("GA-105", "Surcharge", "> 110 % de la charge nominale pendant 60 s", "charge excessive, court-circuit aval", "Délester la charge ; contrôler le tableau aval"),
        ("GA-106", "Défaut de démarrage", "3 tentatives de démarrage sans succès", "carburant absent, batterie faible, électrovanne", "Voir proc_demarrage_ge_a"),
    ],
    "GE-B-02": [
        ("GB-201", "Pression d'huile basse", "< 0,8 bar : arrêt immédiat", "niveau d'huile bas, filtre colmaté", "Arrêter le groupe ; contrôler l'huile"),
        ("GB-202", "Température du liquide de refroidissement élevée", "Pré-alarme à 90 °C ; arrêt automatique à 100 °C", "niveau de liquide bas, radiateur encrassé, courroie détendue", "Voir proc_refroidissement_ge"),
        ("GB-203", "Niveau de carburant bas", "< 25 % du réservoir (120 L)", "consommation prolongée, jauge défectueuse", "Ravitailler (voir fiche_securite_ge)"),
        ("GB-204", "Tension de la batterie de démarrage basse", "< 11,8 V", "batterie usée, chargeur défaillant", "Contrôler la batterie"),
        ("GB-205", "Surcharge", "> 105 % de la charge nominale pendant 60 s", "charge excessive, court-circuit aval", "Délester la charge"),
        ("GB-206", "Défaut de démarrage", "3 tentatives de démarrage sans succès", "carburant absent, batterie faible", "Voir proc_demarrage_ge_b"),
    ],
    "UPS-A-01": [
        ("UA-301", "Fonctionnement sur batterie", "Perte ou dégradation du réseau d'entrée", "coupure réseau, test de batterie en cours", "Normal pendant un test (voir proc_test_batterie_ups_a_v2)"),
        ("UA-302", "Batterie faible", "Autonomie restante < 3 min", "décharge prolongée, batteries vieillissantes", "Préparer l'arrêt propre des charges"),
        ("UA-303", "Surcharge", "> 105 % de la charge nominale", "charge excessive côté sortie", "Délester ; transfert possible vers bypass"),
        ("UA-304", "Température interne élevée", "Dissipateur > 70 °C", "ventilateur défaillant, filtres encrassés, local trop chaud", "Voir proc_nettoyage_ventilation_ups"),
        ("UA-305", "Défaut de ventilateur", "Vitesse de rotation hors tolérance", "ventilateur bloqué ou usé", "Voir proc_nettoyage_ventilation_ups"),
        ("UA-306", "Bypass actif", "Charges alimentées directement par le réseau", "transfert manuel ou automatique", "Voir proc_bypass_ups_a"),
    ],
    "UPS-B-02": [
        ("UB-401", "Fonctionnement sur batterie", "Perte ou dégradation du réseau d'entrée", "coupure réseau", "Surveiller l'autonomie restante"),
        ("UB-402", "Batterie faible", "Autonomie restante < 2 min", "décharge prolongée", "Préparer l'arrêt propre des charges"),
        ("UB-403", "Surcharge", "> 100 % de la charge nominale", "charge excessive côté sortie", "Délester la sortie"),
        ("UB-404", "Température interne élevée", "Dissipateur > 65 °C", "ventilation obstruée, local trop chaud", "Voir proc_nettoyage_ventilation_ups"),
        ("UB-405", "Remplacement des batteries requis", "Test automatique en échec ou batteries âgées de plus de 4 ans", "vieillissement des blocs", "Voir proc_remplacement_batterie_ups_b"),
        ("UB-406", "Défaut du redresseur", "Tension du bus continu hors tolérance", "composant de puissance défaillant", "Contacter un technicien habilité (hors périmètre documentaire)"),
    ],
}

INTERVENTIONS = {
    "GE-A-01": [
        ("INT-GA-0001", "2026-01-12", "GA-103", "Niveau de carburant sous 20 %", "Ravitaillement en gazole, jauge contrôlée", "fiche_securite_ge p.1", "clos"),
        ("INT-GA-0002", "2026-03-04", "GA-102", "Pré-alarme température à 95 °C en charge", "Nettoyage du radiateur à la soufflette basse pression", "proc_refroidissement_ge p.2", "clos"),
        ("INT-GA-0003", "2026-05-20", "GA-104", "Tension de batterie à 11,2 V au démarrage", "Remplacement de la batterie de démarrage 12 V 100 Ah", "proc_maintenance_prev_ge p.2", "clos"),
        ("INT-GA-0004", "2026-08-17", "GA-102", "Nouvelle pré-alarme température (récurrence)", "Courroie du ventilateur retendue ; surveillance renforcée", "proc_refroidissement_ge p.2", "ticket TK-GA-0007 ouvert"),
    ],
    "GE-B-02": [
        ("INT-GB-0001", "2026-02-09", "GB-203", "Niveau de carburant sous 25 %", "Ravitaillement en gazole", "fiche_securite_ge p.1", "clos"),
        ("INT-GB-0002", "2026-04-22", "GB-204", "Tension de batterie à 11,6 V", "Nettoyage des bornes, charge de la batterie", "proc_maintenance_prev_ge p.2", "clos"),
        ("INT-GB-0003", "2026-07-03", "GB-206", "Défaut de démarrage après arrêt prolongé", "Purge du circuit de carburant, nouveau démarrage réussi", "proc_demarrage_ge_b p.2", "clos"),
        ("INT-GB-0004", "2026-09-28", "GB-202", "Pré-alarme température à 90 °C", "Appoint de liquide de refroidissement", "proc_refroidissement_ge p.2", "clos"),
    ],
    "UPS-A-01": [
        ("INT-UA-0001", "2026-01-30", "UA-301", "Passage sur batterie lors d'une coupure réseau de 4 min", "Aucune action (fonctionnement normal)", "manuel_ups_a p.6", "clos"),
        ("INT-UA-0002", "2026-04-14", "UA-305", "Défaut de ventilateur n°2", "Remplacement du ventilateur n°2, nettoyage des filtres", "proc_nettoyage_ventilation_ups p.2", "clos"),
        ("INT-UA-0003", "2026-06-25", "UA-304", "Température du dissipateur à 72 °C", "Filtres encrassés remplacés", "proc_nettoyage_ventilation_ups p.2", "clos"),
        ("INT-UA-0004", "2026-09-10", "UA-306", "Bypass actif après transfert manuel pour maintenance", "Retour en mode normal après intervention", "proc_bypass_ups_a p.2", "ticket TK-UA-0003 ouvert"),
    ],
    "UPS-B-02": [
        ("INT-UB-0001", "2026-02-18", "UB-401", "Coupure réseau de 2 min", "Aucune action (fonctionnement normal)", "manuel_ups_b p.6", "clos"),
        ("INT-UB-0002", "2026-05-05", "UB-404", "Température du dissipateur à 66 °C", "Nettoyage des grilles de ventilation", "proc_nettoyage_ventilation_ups p.2", "clos"),
        ("INT-UB-0003", "2026-08-12", "UB-405", "Test automatique de batterie en échec", "Remplacement programmé des 20 blocs", "proc_remplacement_batterie_ups_b p.2", "ticket TK-UB-0005 ouvert"),
        ("INT-UB-0004", "2026-10-02", "UB-402", "Batterie faible lors d'une coupure de 6 min", "Contrôle des batteries, remplacement confirmé", "proc_remplacement_batterie_ups_b p.2", "ticket TK-UB-0005 ouvert"),
    ],
}

# pages stables dans les manuels (utilisées pour les renvois croisés)
PAGE_VOYANTS = 5
PAGE_MODES = 6
