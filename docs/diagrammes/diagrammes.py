# -*- coding: utf-8 -*-
"""Source des diagrammes MaintiDoc (livrable 1). Exécuter : python diagrammes.py [dossier_de_sortie]"""
import sys, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle

BLUE, GREEN, YELLOW, ORANGE, GREY, PINK = "#dbe7f7", "#dff0e0", "#fff2c6", "#fde0c4", "#ececec", "#f6d5d5"


def anchor(b, side):
    x, y, w, h = b[:4]
    return {"l": (x, y + h / 2), "r": (x + w, y + h / 2), "t": (x + w / 2, y + h), "b": (x + w / 2, y)}[side]


def draw(path, boxes, arrows, markers=(), size=(7.6, 4.2), xlim=140, ylim=72, legend=None):
    fig, ax = plt.subplots(figsize=size)
    ax.set_xlim(0, xlim); ax.set_ylim(0, ylim); ax.axis("off")
    fig.canvas.draw()
    rend = fig.canvas.get_renderer()
    for k, (x, y, w, h, label, col) in boxes.items():
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3,rounding_size=1.4", fc=col, ec="#333", lw=1.1))
        t = ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=6.8, linespacing=1.25)
        fs = 6.8
        while fs > 3.6:
            bb = t.get_window_extent(rend)
            (x0, y0), (x1, y1) = ax.transData.inverted().transform([(bb.x0, bb.y0), (bb.x1, bb.y1)])
            if (x1 - x0) <= w - 1.6 and (y1 - y0) <= h - 1.2:
                break
            fs -= 0.2
            t.set_fontsize(fs)
    for a, sa, b, sb, lab, bi in arrows:
        p1, p2 = anchor(boxes[a], sa), anchor(boxes[b], sb)
        ax.annotate("", xy=p2, xytext=p1, arrowprops=dict(arrowstyle="<|-|>" if bi else "-|>", lw=1.1, color="#222", shrinkA=1, shrinkB=1))
        if lab:
            ax.text((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2 + 1.5, lab, ha="center", fontsize=5.6, color="#7a1f1f",
                    bbox=dict(fc="white", ec="none", pad=0.4))
    for x, y, n in markers:
        ax.add_patch(Circle((x, y), 2.1, fc="#c62828", ec="white", lw=1.0, zorder=5))
        ax.text(x, y, n, color="white", ha="center", va="center", fontsize=6.2, fontweight="bold", zorder=6)
    if legend:
        ax.text(1, 1.0, legend, fontsize=5.8, va="bottom", color="#222", linespacing=1.35)
    fig.savefig(path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def archi(out):
    B = {
        "ui": (2, 34, 20, 15, "Interface web\nStreamlit\n(question + photo)", BLUE),
        "api": (30, 34, 22, 15, "API FastAPI\nauthentification\net autorisation", BLUE),
        "orc": (60, 34, 24, 15, "Orchestrateur\nLangGraph + LangChain\n(état, budgets, pause)", ORANGE),
        "rech": (96, 54, 26, 14, "Recherche documentaire\ntexte + image\nfusion + reranker", GREEN),
        "sto": (130, 54, 20, 14, "Stockage\nPostgreSQL (droits)\nQdrant (index)\nMinIO (fichiers)", GREY),
        "vlm": (96, 34, 26, 15, "Modèle vision-langage\n(poids ouverts)\ndécrit la photo,\nrédige la réponse", GREEN),
        "mcpc": (96, 13, 26, 14, "Client MCP\n(3 appels max.\npar demande)", GREEN),
        "mcps": (130, 13, 20, 14, "Serveur MCP\nmaintenance (démo)\nhistorique, tickets", YELLOW),
        "ver": (60, 10, 24, 15, "Vérificateur\nréférences + format\n(Pydantic)", ORANGE),
        "hum": (2, 10, 20, 15, "Validation humaine\n(approbation\ndu ticket)", PINK),
    }
    A = [("ui", "r", "api", "l", "", True), ("api", "r", "orc", "l", "", True),
         ("orc", "r", "rech", "l", "", False), ("rech", "r", "sto", "l", "", True),
         ("orc", "r", "vlm", "l", "", True), ("orc", "r", "mcpc", "l", "", False),
         ("mcpc", "r", "mcps", "l", "", True), ("orc", "b", "ver", "t", "brouillon", True),
         ("ui", "b", "hum", "t", "contenu exact du ticket", True)]
    M = [(26, 41.5, "1"), (90, 51.2, "2"), (126, 61, "3"), (83, 24, "4"), (21, 24, "5"), (149, 26, "6")]
    leg = ("1 identité et groupes vérifiés   2 filtrage par groupe avant toute recherche   3 droits revérifiés à l'ouverture d'un document ou d'une image\n"
           "4 existence et soutien des citations, format de sortie   5 approbation humaine avant création d'un ticket   6 autorisations revérifiées côté serveur MCP")
    draw(out, B, A, M, size=(6.9, 4.0), xlim=152, ylim=72, legend=leg)


def ingestion(out):
    B = {
        "doc": (2, 30, 18, 14, "Documents\nPDF et photos\n(43 fichiers)", BLUE),
        "sto": (2, 6, 18, 12, "Stockage des\nfichiers originaux\n(MinIO / disque)", GREY),
        "dec": (28, 30, 18, 14, "PDF scanné ?\n(couche texte\nabsente)", YELLOW),
        "ocr": (28, 6, 18, 12, "OCR local\n(à préciser)", ORANGE),
        "ext": (54, 30, 20, 14, "Extraction du texte\net des images\n(PyMuPDF)", GREEN),
        "dec2": (82, 30, 20, 14, "Découpage en passages,\ntableaux, figures", GREEN),
        "met": (110, 30, 22, 14, "Métadonnées +\nembeddings texte\net image", GREEN),
        "inv": (110, 52, 22, 12, "inventaire.csv\n(groupes, version,\néquipement)", YELLOW),
        "idx": (110, 6, 22, 14, "Index de recherche\n(Qdrant) +\nmétadonnées\n(PostgreSQL)", GREY),
    }
    A = [("doc", "r", "dec", "l", "", False), ("doc", "b", "sto", "t", "originaux", False), ("dec", "r", "ext", "l", "non", False),
         ("dec", "b", "ocr", "t", "oui", False), ("ocr", "r", "ext", "b", "texte + position", False), ("ext", "r", "dec2", "l", "", False),
         ("dec2", "r", "met", "l", "", False), ("inv", "b", "met", "t", "", False), ("met", "b", "idx", "t", "", False)]
    draw(out, B, A, size=(6.9, 3.0), xlim=136, ylim=68)


def requete(out):
    B = {
        "s1": (2, 38, 28, 16, "1. Identifier l'utilisateur\net ses groupes", BLUE),
        "s2": (38, 38, 28, 16, "2. Décrire la photo et\nidentifier l'équipement\n(sinon clarification)", GREEN),
        "s3": (74, 38, 28, 16, "3. Rechercher dans les\ndocuments autorisés\n(texte + image + reranker)", GREEN),
        "s4": (110, 38, 28, 16, "4. Consulter l'historique\nvia MCP (si utile)", YELLOW),
        "s5": (110, 8, 28, 16, "5. Rédiger la réponse\navec ses sources", GREEN),
        "s6": (74, 8, 28, 16, "6. Vérifier chaque citation\n(existence + soutien)", ORANGE),
        "s7": (38, 8, 28, 16, "7. Valider le format\nde sortie (Pydantic)", ORANGE),
        "s8": (2, 8, 28, 16, "8. Répondre, ou demander\nune précision, ou\ns'abstenir", BLUE),
    }
    A = [("s1", "r", "s2", "l", "", False), ("s2", "r", "s3", "l", "", False), ("s3", "r", "s4", "l", "", False), ("s4", "b", "s5", "t", "", False),
         ("s5", "l", "s6", "r", "", False), ("s6", "l", "s7", "r", "", False), ("s7", "l", "s8", "r", "", False)]
    M = [(30, 52, "1"), (102, 52, "2"), (138, 52, "6"), (102, 22, "4")]
    draw(out, B, A, M, size=(6.9, 2.9), xlim=142, ylim=60)


def ticket(out):
    B = {
        "t1": (2, 38, 30, 16, "1. Préparer le brouillon\n(équipement, titre, description)\net vérifier get_open_tickets", GREEN),
        "t2": (40, 38, 30, 16, "2. Pause du workflow\n(interruption LangGraph)", ORANGE),
        "t3": (78, 38, 30, 16, "3. Afficher le contenu\nexact à l'utilisateur", BLUE),
        "t4": (116, 38, 30, 16, "4. Approbation explicite\n(toute modification =\nnouvelle approbation)", PINK),
        "t5": (116, 8, 30, 16, "5. Jeton lié à l'utilisateur\net à l'empreinte du contenu", PINK),
        "t6": (78, 8, 30, 16, "6. create_ticket(...,\napproval_token) avec\nclé d'idempotence", YELLOW),
        "t7": (40, 8, 30, 16, "7. Le serveur MCP contrôle\nles droits, le jeton et\nles doublons", YELLOW),
        "t8": (2, 8, 30, 16, "8. Ticket créé,\nidentifiant renvoyé,\névénement journalisé", GREEN),
    }
    A = [("t1", "r", "t2", "l", "", False), ("t2", "r", "t3", "l", "", False), ("t3", "r", "t4", "l", "", False), ("t4", "b", "t5", "t", "", False),
         ("t5", "l", "t6", "r", "", False), ("t6", "l", "t7", "r", "", False), ("t7", "l", "t8", "r", "", False)]
    M = [(146, 52, "5"), (70, 22, "6")]
    draw(out, B, A, M, size=(6.9, 2.8), xlim=148, ylim=60)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(out, exist_ok=True)
    archi(f"{out}/architecture_globale.png"); ingestion(f"{out}/flux_ingestion.png")
    requete(f"{out}/flux_requete.png"); ticket(f"{out}/flux_ticket.png")
    print("diagrammes générés dans", out)
