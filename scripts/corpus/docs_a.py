# -*- coding: utf-8 -*-
import os
from lib import *
from master import *

FIG = "/home/claude/figs"
os.makedirs(FIG, exist_ok=True)
LB, LG, LY, LO = "#dbe7f7", "#dff0e0", "#fff2c6", "#fde0c4"


def fig_synoptique_ge(eq, path):
    e = EQ[eq]
    boxes = {
        "res": (2, 30, 16, 12, f"Réservoir\n{e['reservoir']}", LY),
        "mot": (28, 30, 18, 12, "Moteur diesel", LO),
        "alt": (56, 30, 16, 12, "Alternateur", LB),
        "dis": (80, 30, 16, 12, "Disjoncteur\nde sortie", LG),
        "rad": (28, 8, 18, 11, "Radiateur\n(liquide)", LB),
        "bat": (2, 8, 16, 11, f"Batterie\n{e['batterie']}", LY),
        "ctl": (56, 8, 24, 11, "Contrôleur et\npanneau de commande", LG),
    }
    arrows = [("res", "r", "mot", "l", "gazole"), ("mot", "r", "alt", "l", "couple"), ("alt", "r", "dis", "l", e["tension"][:8]),
              ("rad", "t", "mot", "b", "liquide"), ("bat", "t", "res", "b", ""), ("mot", "b", "ctl", "l", "capteurs")]
    blocks_fig(path, boxes, arrows, ylim=48)


def fig_synoptique_ups(eq, path):
    e = EQ[eq]
    boxes = {
        "res": (1, 28, 15, 12, "Réseau\nd'entrée", LY),
        "red": (24, 28, 16, 12, "Redresseur", LB),
        "bus": (47, 28, 14, 12, "Bus\ncontinu", LO),
        "ond": (68, 28, 14, 12, "Onduleur", LB),
        "sor": (88, 28, 11, 12, "Charges", LG),
        "bat": (44, 6, 22, 12, f"Batteries\n{e['batterie'][:18]}", LY),
        "byp": (24, 6, 14, 12, "Bypass", LG),
    }
    arrows = [("res", "r", "red", "l", ""), ("red", "r", "bus", "l", ""), ("bus", "r", "ond", "l", ""), ("ond", "r", "sor", "l", ""),
              ("bat", "t", "bus", "b", "charge/décharge"), ("res", "b", "byp", "l", ""), ("byp", "r", "sor", "b", "")]
    blocks_fig(path, boxes, arrows, ylim=44)


def manual_ge(eq):
    e, leds = EQ[eq], LEDS[eq]
    al = ALARMES[eq]
    fs = f"{FIG}/syn_{eq}.png"; fp = f"{FIG}/panel_{eq}.png"
    fig_synoptique_ge(eq, fs)
    panel_fig(fp, leds, ["START", "STOP", "RESET"])
    cod = "codes_alarme_ge_a" if eq == "GE-A-01" else "codes_alarme_ge_b"
    dem = "proc_demarrage_ge_a" if eq == "GE-A-01" else "proc_demarrage_ge_b"
    pages = [
        [("title", f"Manuel d'utilisation<br/>{e['nom']}"), ("sub", f"Équipement {eq} — N° de série {e['serie']}"),
         ("spacer", 6),
         ("table", "Sommaire", ["Section", "Page"],
          [["1. Sécurité", "2"], ["2. Présentation et caractéristiques", "3"], ["3. Synoptique", "4"],
           ["4. Panneau de commande et voyants", "5"], ["5. Démarrage et arrêt", "6"], ["6. Entretien périodique", "7"],
           ["7. Dépannage et alarmes", "8"]], [5, 1]),
         ("note", "Ce manuel est une aide documentaire. Il ne remplace ni les procédures de sécurité du site ni l'intervention d'un technicien habilité.")],
        [("h1", "1. Sécurité"),
         ("p", "Le groupe électrogène produit de la haute tension et comporte des pièces chaudes et en rotation. Respecter les consignes suivantes avant toute intervention :"),
         ("ul", ["Arrêter le groupe, ouvrir le disjoncteur de sortie et consigner l'équipement avant toute opération de maintenance.",
                 "Ne jamais ouvrir le bouchon du radiateur lorsque le moteur est chaud.",
                 "Faire fonctionner le groupe uniquement dans un local ventilé (risque d'intoxication par les gaz d'échappement).",
                 "Ne pas ravitailler pendant que le moteur tourne ; aucune flamme à proximité.",
                 "Porter les équipements de protection individuelle : gants, lunettes, chaussures de sécurité, protection auditive.",
                 "Ne jamais redémarrer le groupe lorsqu'un voyant rouge est actif sans en avoir identifié la cause."]),
         ("note", "Consulter la fiche de sécurité fiche_securite_ge pour le détail des risques liés au carburant et à la batterie.")],
        [("h1", "2. Présentation et caractéristiques"),
         ("p", f"Le {e['nom']} est un groupe de secours destiné à alimenter des charges critiques en cas de coupure du réseau. Il est piloté par un contrôleur qui surveille la pression d'huile, la température, le niveau de carburant, la tension de la batterie et la charge."),
         ("table", "Caractéristiques principales", ["Caractéristique", "Valeur"],
          [["Puissance", e["puissance"]], ["Sortie", e["tension"]], ["Moteur", e["moteur"]], ["Réservoir", e["reservoir"]],
           ["Huile moteur", e["huile"]], ["Circuit de refroidissement", e["refroid"]], ["Batterie de démarrage", e["batterie"]],
           ["N° de série (plaque signalétique)", e["serie"]]], [3, 4])],
        [("h1", "3. Synoptique"),
         ("p", "La figure ci-dessous présente les principaux organes du groupe et leurs liaisons : le moteur entraîne l'alternateur, alimenté en gazole depuis le réservoir et refroidi par le radiateur. Le contrôleur reçoit les mesures des capteurs."),
         ("fig", fs, f"Synoptique du groupe électrogène {eq}", 150)],
        [("h1", "4. Panneau de commande et voyants"),
         ("p", "Le panneau comporte un afficheur, trois boutons (START, STOP, RESET) et six voyants numérotés de (1) à (6), disposés sur deux lignes de trois voyants."),
         ("fig", fp, f"Panneau de commande du {eq} (voyants numérotés)", 120),
         ("table", "Signification des voyants", ["N°", "Voyant", "Couleur", "Code", "Signification"],
          [[i + 1, l, COULEUR_FR[c], code, next(a[1] for a in al if a[0] == code)] for i, (l, c, code) in enumerate(leds)],
          [1, 2, 2, 2, 7])],
        [("h1", "5. Démarrage et arrêt"),
         ("p", f"Le démarrage manuel suit la procédure <b>{dem}</b> : contrôles visuels, vérification des niveaux, démarrage, fonctionnement à vide puis mise en charge progressive. L'arrêt s'effectue après délestage et refroidissement à vide."),
         ("table", "Valeurs de fonctionnement normal", ["Grandeur", "Valeur normale", "Seuil d'alarme"],
          [["Pression d'huile", f"≥ {e['p_huile']:.1f} bar".replace('.', ','), f"{al[0][2]}"],
           ["Température du liquide", f"< {e['temp_pre']} °C", f"pré-alarme à {e['temp_pre']} °C, arrêt à {e['temp_stop']} °C"],
           ["Niveau de carburant", f"> {e['carb']} %", f"alarme sous {e['carb']} %"],
           ["Tension de la batterie", f"≥ {e['batt_v'] + 0.5:.1f} V".replace('.', ','), f"alarme sous {e['batt_v']:.1f} V".replace('.', ',')]],
          [3, 3, 5]),
         ("p", f"Le démarreur est limité à {e['demarreur_s']} secondes par tentative et à 3 tentatives ; au-delà, l'alarme {leds[3][2]} (défaut de démarrage) est déclenchée.")],
        [("h1", "6. Entretien périodique"),
         ("p", "Les intervalles ci-dessous sont exprimés en heures de fonctionnement. Consigner chaque intervention dans le registre de maintenance."),
         ("table", "Intervalles d'entretien", ["Opération", "Intervalle"],
          [["Contrôle du niveau d'huile", "50 h"], ["Vidange d'huile et remplacement du filtre à huile", f"{e['vidange_h']} h"],
           ["Remplacement du filtre à air", f"{e['filtre_air_h']} h"], ["Contrôle du liquide de refroidissement", "100 h"],
           ["Test de la batterie de démarrage", "3 mois"], ["Contrôle de la tension de la courroie du ventilateur", "250 h"]], [5, 2]),
         ("p", "La vidange d'huile et le contrôle du refroidissement suivent respectivement les procédures de vidange et proc_refroidissement_ge.")],
        [("h1", "7. Dépannage et alarmes"),
         ("p", f"En cas d'alarme, relever le voyant allumé et son code, puis consulter le document <b>{cod}</b> (tableau 1.1, page 1) qui donne la signification, le seuil et les causes probables de chaque code."),
         ("ul", ["Voyant rouge : arrêt ou risque d'arrêt. Ne pas redémarrer avant d'avoir identifié la cause.",
                 "Voyant orange : pré-alarme. Planifier une intervention et surveiller l'évolution.",
                 "Si la cause n'est pas identifiée ou si plusieurs voyants sont actifs, contacter un technicien habilité."]),
         ("note", "L'assistant documentaire ne garantit aucun diagnostic. Une ressemblance visuelle entre deux voyants ne suffit pas à conclure : toujours confirmer l'équipement (plaque signalétique).")],
    ]
    return pages


def manual_ups(eq):
    e, leds, al = EQ[eq], LEDS[eq], ALARMES[eq]
    fs = f"{FIG}/syn_{eq}.png"; fp = f"{FIG}/panel_{eq}.png"
    fig_synoptique_ups(eq, fs)
    panel_fig(fp, leds, ["ON/OFF", "TEST", "RESET"])
    cod = "codes_alarme_ups_a" if eq == "UPS-A-01" else "codes_alarme_ups_b"
    dem = "proc_bypass_ups_a" if eq == "UPS-A-01" else "proc_demarrage_ups_b"
    pages = [
        [("title", f"Manuel d'utilisation<br/>{e['nom']}"), ("sub", f"Équipement {eq} — N° de série {e['serie']}"),
         ("spacer", 6),
         ("table", "Sommaire", ["Section", "Page"],
          [["1. Sécurité", "2"], ["2. Présentation et caractéristiques", "3"], ["3. Synoptique", "4"],
           ["4. Panneau de commande et voyants", "5"], ["5. Modes de fonctionnement", "6"], ["6. Entretien périodique", "7"],
           ["7. Dépannage et alarmes", "8"]], [5, 1]),
         ("note", "Ce manuel est une aide documentaire. Il ne remplace ni les procédures de sécurité du site ni l'intervention d'un technicien habilité.")],
        [("h1", "1. Sécurité"),
         ("p", "L'onduleur contient des batteries et un bus continu qui restent sous tension même lorsque l'appareil est hors tension réseau."),
         ("ul", ["Ne jamais ouvrir le capot sans avoir mis l'onduleur hors tension et attendu la décharge des condensateurs.",
                 "Les batteries présentent un risque de court-circuit : utiliser des outils isolés et retirer bijoux et montres.",
                 "Ne pas obstruer les grilles de ventilation ; respecter un dégagement de 30 cm autour de l'appareil.",
                 "Ne pas exposer les batteries à une source de chaleur ; ventiler le local.",
                 "Toute intervention interne est réservée à un technicien habilité."]),
         ("note", "Consulter la fiche de sécurité fiche_securite_ups pour les risques liés aux batteries.")],
        [("h1", "2. Présentation et caractéristiques"),
         ("p", f"Le {e['nom']} est un onduleur à double conversion destiné à protéger des charges critiques contre les coupures et les perturbations du réseau. Il fournit une tension de sortie stable, en continu."),
         ("table", "Caractéristiques principales", ["Caractéristique", "Valeur"],
          [["Puissance", e["puissance"]], ["Tension", e["tension"]], ["Batteries", e["batterie"]],
           ["Autonomie", e["autonomie"]], ["Seuil de température du dissipateur", f"{e['temp_dissip']} °C"],
           ["Remplacement des filtres", f"tous les {e['filtres_mois']} mois"], ["N° de série (plaque signalétique)", e["serie"]]], [3, 4])],
        [("h1", "3. Synoptique"),
         ("p", "En fonctionnement normal, le redresseur alimente le bus continu qui charge les batteries et alimente l'onduleur. En cas de coupure réseau, les batteries prennent le relais sans interruption."),
         ("fig", fs, f"Synoptique de l'onduleur {eq}", 150)],
        [("h1", "4. Panneau de commande et voyants"),
         ("p", "Le panneau comporte un afficheur, trois boutons (ON/OFF, TEST, RESET) et six voyants numérotés de (1) à (6), disposés sur deux lignes de trois voyants."),
         ("fig", fp, f"Panneau de commande de l'{eq} (voyants numérotés)", 120),
         ("table", "Signification des voyants", ["N°", "Voyant", "Couleur", "Code", "Signification"],
          [[i + 1, l, COULEUR_FR[c], code, next(a[1] for a in al if a[0] == code)] for i, (l, c, code) in enumerate(leds)],
          [1, 2, 2, 2, 7])],
        [("h1", "5. Modes de fonctionnement"),
         ("table", "Modes de fonctionnement", ["Mode", "Description", "Voyant associé"],
          [["Normal", "Charges alimentées par l'onduleur, batteries maintenues en charge", "aucun"],
           ["Sur batterie", "Perte du réseau d'entrée : les batteries alimentent les charges", leds[0][2] + " (" + leds[0][0] + ")"],
           ["Bypass", "Charges alimentées directement par le réseau (maintenance ou surcharge)", next((l[2] + " (" + l[0] + ")") for l in leds if l[0] in ("BYPASS",)) if eq == "UPS-A-01" else "non disponible sur ce modèle"]],
          [2, 6, 3]),
         ("p", f"Voir aussi : <b>{dem}</b>. L'autonomie réelle dépend de la charge et de l'état des batteries ; elle diminue avec le vieillissement des blocs.")],
        [("h1", "6. Entretien périodique"),
         ("table", "Intervalles d'entretien", ["Opération", "Intervalle"],
          [["Nettoyage des grilles de ventilation", "3 mois"], ["Remplacement des filtres", f"{e['filtres_mois']} mois"],
           ["Test de décharge des batteries", "12 mois"], ["Remplacement des batteries", "4 ans environ"]], [5, 2]),
         ("p", "Le nettoyage et les filtres suivent la procédure proc_nettoyage_ventilation_ups. Le test des batteries et leur remplacement suivent les procédures dédiées.")],
        [("h1", "7. Dépannage et alarmes"),
         ("p", f"En cas d'alarme, relever le voyant allumé et son code, puis consulter le document <b>{cod}</b> (tableau 1.1, page 1) pour la signification, le seuil et les causes probables."),
         ("ul", ["Voyant rouge : risque de perte de protection des charges ; agir sans délai.",
                 "Voyant orange : dégradation ou information ; planifier une intervention.",
                 "Si plusieurs voyants sont actifs ou si la cause n'est pas identifiée, contacter un technicien habilité."]),
         ("note", "L'assistant documentaire ne garantit aucun diagnostic. Une ressemblance visuelle entre deux voyants ne suffit pas à conclure : toujours confirmer l'équipement (plaque signalétique).")],
    ]
    return pages


def codes_alarme(eq):
    e, leds, al = EQ[eq], LEDS[eq], ALARMES[eq]
    led_of = {code: (l, c) for l, c, code in leds}
    return [
        [("h1", f"Codes d'alarme — {eq}"),
         ("p", f"Ce document recense les alarmes du {e['nom']} (équipement {eq}). Chaque code correspond à un voyant du panneau de commande."),
         ("table", "Codes d'alarme et voyants", ["Code", "Voyant", "Couleur", "Signification"],
          [[code, led_of[code][0], COULEUR_FR[led_of[code][1]], lib] for code, lib, *_ in al], [2, 2, 2, 8]),
         ("note", "Rouge : arrêt ou risque d'arrêt, ne pas redémarrer sans identifier la cause. Orange : pré-alarme, planifier une intervention.")],
        [("h1", "Seuils, causes probables et renvois"),
         ("table", "Seuils de déclenchement et actions documentaires", ["Code", "Seuil / condition", "Causes probables", "Action documentaire"],
          [[code, seuil, causes, action] for code, lib, seuil, causes, action in al], [2, 4, 5, 5]),
         ("p", "Les causes probables sont indicatives : seule une inspection par un technicien habilité permet de confirmer un diagnostic.")],
    ]


def schema_doc(eq, kind):
    e = EQ[eq]
    p = f"{FIG}/sch_{kind}.png"
    if kind == "synoptique_ge_a":
        fig_synoptique_ge(eq, p)
        titre, cap, rows = f"Schéma synoptique du {eq}", f"Synoptique du groupe {eq}", [
            ["Réservoir", f"{e['reservoir']} ; alarme niveau bas sous {e['carb']} % ({e['pre']}-103)"],
            ["Moteur diesel", e["moteur"]], ["Alternateur", e["puissance"]], ["Radiateur", f"liquide {e['refroid']}"],
            ["Contrôleur", "Surveillance pression d'huile, température, carburant, batterie, charge"]]
    elif kind == "electrique_ge_b":
        boxes = {"alt": (3, 28, 16, 12, "Alternateur\n60 kVA", LB), "dis": (28, 28, 18, 12, "Disjoncteur\nprincipal", LG),
                 "tab": (55, 28, 18, 12, "Tableau de\ndistribution", LY), "chg": (82, 28, 16, 12, "Charges\ncritiques", LG),
                 "ctl": (28, 6, 22, 11, "Contrôleur\n(mesures U, I, Hz)", LG), "bat": (58, 6, 20, 11, "Batterie 12 V 80 Ah", LY)}
        blocks_fig(p, boxes, [("alt", "r", "dis", "l", "400 V"), ("dis", "r", "tab", "l", ""), ("tab", "r", "chg", "l", ""),
                              ("alt", "b", "ctl", "l", "mesures"), ("bat", "l", "ctl", "r", "12 V")], ylim=46)
        titre, cap = f"Schéma électrique simplifié du {eq}", f"Schéma électrique simplifié du groupe {eq}"
        rows = [["Alternateur", "60 kVA / 48 kW, 400 V triphasé"], ["Disjoncteur principal", "Protection de sortie ; alarme surcharge GB-205 à 105 %"],
                ["Contrôleur", "Mesure tension, courant, fréquence"], ["Batterie", e["batterie"]]]
    elif kind == "refroidissement_ge_a":
        boxes = {"mot": (38, 28, 20, 12, "Moteur\n(chemise d'eau)", LO), "rad": (4, 28, 20, 12, "Radiateur", LB),
                 "vent": (4, 6, 20, 11, "Ventilateur\n(courroie)", LG), "vase": (72, 28, 22, 12, "Vase\nd'expansion", LY),
                 "pompe": (38, 6, 20, 11, "Pompe à eau", LB)}
        blocks_fig(p, boxes, [("mot", "l", "rad", "r", "retour"), ("pompe", "t", "mot", "b", ""), ("mot", "r", "vase", "l", "trop-plein"),
                              ("vent", "t", "rad", "b", "air")], ylim=46)
        titre, cap = f"Circuit de refroidissement du {eq}", f"Circuit de refroidissement du groupe {eq}"
        rows = [["Capacité", e["refroid"]], ["Pré-alarme température", f"{e['temp_pre']} °C (GA-102)"],
                ["Arrêt automatique", f"{e['temp_stop']} °C"], ["Courroie du ventilateur", f"flèche de {e['flexion']} mm sous 10 N"]]
    elif kind == "synoptique_ups_a":
        fig_synoptique_ups(eq, p)
        titre, cap = f"Schéma synoptique de l'{eq}", f"Synoptique de l'onduleur {eq}"
        rows = [["Redresseur", "Alimente le bus continu"], ["Batteries", e["batterie"]], ["Onduleur", e["puissance"]], ["Bypass", "Alimentation directe des charges par le réseau"]]
    elif kind == "cablage_ups_b":
        boxes = {"res": (2, 28, 16, 12, "Réseau\n230 V", LY), "dis": (26, 28, 16, 12, "Disjoncteur\nd'entrée", LG),
                 "ond": (50, 28, 18, 12, "UPS-B-02\n10 kVA", LB), "sor": (78, 28, 18, 12, "Sortie\n230 V", LG),
                 "bat": (50, 6, 22, 11, "Coffret batteries\n20 × 12 V 7 Ah", LY)}
        blocks_fig(p, boxes, [("res", "r", "dis", "l", ""), ("dis", "r", "ond", "l", ""), ("ond", "r", "sor", "l", ""), ("bat", "t", "ond", "b", "240 V DC")], ylim=46)
        titre, cap = f"Schéma de câblage de l'{eq}", f"Câblage de l'onduleur {eq}"
        rows = [["Entrée", "230 V monophasé, disjoncteur dédié"], ["Batteries", e["batterie"]], ["Sortie", "230 V monophasé, 9 kW"]]
    elif kind == "bypass_ups_a":
        boxes = {"res": (2, 28, 14, 12, "Réseau", LY), "ond": (30, 36, 26, 12, "Chaîne onduleur\n(redresseur + onduleur)", LB),
                 "byp": (34, 8, 20, 12, "Ligne de bypass", LG), "sor": (80, 24, 16, 12, "Charges", LG), "int": (58, 24, 16, 12, "Commutateur\nde transfert", LO)}
        blocks_fig(p, boxes, [("res", "r", "ond", "l", ""), ("res", "r", "byp", "l", ""), ("ond", "r", "int", "t", ""), ("byp", "r", "int", "b", ""), ("int", "r", "sor", "l", "")], ylim=50)
        titre, cap = f"Schéma du bypass de l'{eq}", f"Chemins de transfert normal et bypass de l'onduleur {eq}"
        rows = [["Mode normal", "Charges alimentées par la chaîne onduleur"], ["Mode bypass", "Charges alimentées par la ligne de bypass ; voyant UA-306 allumé"],
                ["Commutateur", "Transfert manuel ou automatique (surcharge > 105 %, code UA-303)"]]
    return [[("h1", titre), ("p", "Schéma de principe à usage documentaire (non à l'échelle)."), ("fig", p, cap, 160)],
            [("h1", "Légende et références"), ("table", "Légende du schéma", ["Élément", "Description"], rows, [3, 7]),
             ("p", f"Équipement concerné : <b>{eq}</b>. Voir le manuel de l'équipement pour les consignes de sécurité.")]]


def fiche_securite(famille):
    if famille == "ge":
        return [
            [("h1", "Fiche de sécurité — groupes électrogènes GE-A-01 et GE-B-02"),
             ("h2", "Ravitaillement en carburant"),
             ("ul", ["Arrêter le moteur et attendre son refroidissement avant tout ravitaillement.",
                     "Ravitailler uniquement avec du gazole propre ; essuyer immédiatement tout déversement.",
                     "Interdiction de fumer et aucune flamme à moins de 5 mètres.",
                     "Le niveau d'alarme carburant bas est de 20 % pour le GE-A-01 et de 25 % pour le GE-B-02."]),
             ("h2", "Batterie de démarrage"),
             ("ul", ["Débrancher d'abord la borne négative, rebrancher en dernier.",
                     "Risque d'étincelle et de projection d'acide : lunettes et gants obligatoires."])],
            [("h1", "Équipements de protection et conduite à tenir"),
             ("table", "Risques, protections et conduite à tenir", ["Risque", "Protection", "Conduite à tenir"],
              [["Brûlure (collecteur, radiateur)", "Gants, vêtements couvrants", "Attendre le refroidissement ; ne jamais ouvrir le bouchon à chaud"],
               ["Électrique (400 V)", "Consignation, gants isolants", "Ouvrir le disjoncteur de sortie ; vérifier l'absence de tension"],
               ["Bruit", "Protection auditive", "Porter un casque près du groupe en marche"],
               ["Gaz d'échappement", "Ventilation du local", "Évacuer le local en cas d'odeur anormale"],
               ["Incendie", "Extincteur à portée", "Alerter et évacuer ; ne pas combattre un feu de carburant à l'eau"]], [3, 3, 5])]]
    return [
        [("h1", "Fiche de sécurité — onduleurs UPS-A-01 et UPS-B-02"),
         ("h2", "Batteries"),
         ("ul", ["Les batteries restent sous tension même onduleur arrêté : bus continu de 480 V (UPS-A-01) ou 240 V (UPS-B-02).",
                 "Utiliser des outils isolés ; retirer bijoux et montre avant d'intervenir.",
                 "Ne jamais court-circuiter les bornes ; couvrir les bornes dégagées."]),
         ("h2", "Ventilation et température"),
         ("ul", ["Ne pas obstruer les grilles ; dégagement de 30 cm autour de l'appareil.",
                 "Seuil d'alarme température : 70 °C (UPS-A-01) et 65 °C (UPS-B-02) au dissipateur."])],
        [("h1", "Équipements de protection et conduite à tenir"),
         ("table", "Risques, protections et conduite à tenir", ["Risque", "Protection", "Conduite à tenir"],
          [["Électrique (bus continu)", "Gants isolants, outils isolés", "Mettre hors tension, attendre la décharge, vérifier l'absence de tension"],
           ["Acide / hydrogène (batteries)", "Lunettes, gants, ventilation", "Aérer le local ; ne pas approcher de flamme"],
           ["Poids des blocs batteries", "Chaussures de sécurité", "Manutention à deux pour les blocs lourds"],
           ["Départ de feu", "Extincteur CO2 à portée", "Alerter et évacuer"]], [3, 3, 5])]]


def historique(eq):
    rows = INTERVENTIONS[eq]
    tk = [r for r in rows if "ticket" in r[6]]
    p2 = [("h1", "Tickets ouverts et observations"),
          ("table", "Tickets ouverts", ["Ticket", "Équipement", "Statut", "Origine"],
           [[r[6].split()[1], eq, "ouvert", r[0]] for r in tk] or [["aucun", eq, "-", "-"]], [3, 3, 2, 3]),
          ("p", f"Équipement {eq} : {len(rows)} interventions consignées entre {rows[0][1]} et {rows[-1][1]}. Les données sont fictives."),
          ("p", "Observation : consulter ces informations via le service de maintenance (MCP) ; les tickets ci-dessus sont des données de démonstration.")]
    return [[("h1", f"Historique des interventions — {eq}"),
             ("p", f"Registre des interventions de {EQ[eq]['nom']}. Les codes d'alarme renvoient au document de codes d'alarme de l'équipement."),
             ("table", "Interventions", ["Réf.", "Date", "Code", "Constat", "Action menée", "Source", "Statut"],
              [list(r) for r in rows], [2.2, 2, 1.6, 4, 4.4, 3.4, 2.4])], p2]
