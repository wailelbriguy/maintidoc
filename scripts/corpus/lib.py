# -*- coding: utf-8 -*-
import os, random, subprocess, math
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                Table, TableStyle, Image, PageBreak, ListFlowable, ListItem)
from pypdf import PdfReader
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle
from PIL import Image as PILImage, ImageDraw, ImageFont, ImageFilter, ImageChops

FD = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DV", FD + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DV-B", FD + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DV-I", FD + "DejaVuSans-Oblique.ttf"))
pdfmetrics.registerFont(TTFont("DV-BI", FD + "DejaVuSans-BoldOblique.ttf"))
pdfmetrics.registerFontFamily("DV", normal="DV", bold="DV-B", italic="DV-I", boldItalic="DV-BI")

RED, ORANGE, GREEN = "#d32f2f", "#f59a1b", "#3da44d"
BLUE = colors.HexColor("#1f3b66")

S = {
    "p": ParagraphStyle("p", fontName="DV", fontSize=9.3, leading=13.2, spaceAfter=5),
    "h1": ParagraphStyle("h1", fontName="DV-B", fontSize=14.5, leading=18, spaceAfter=8, textColor=BLUE),
    "h2": ParagraphStyle("h2", fontName="DV-B", fontSize=11, leading=14, spaceBefore=6, spaceAfter=4, textColor=BLUE),
    "title": ParagraphStyle("title", fontName="DV-B", fontSize=22, leading=27, spaceAfter=10, textColor=BLUE),
    "sub": ParagraphStyle("sub", fontName="DV", fontSize=12, leading=16, spaceAfter=6, textColor=colors.HexColor("#444444")),
    "cell": ParagraphStyle("cell", fontName="DV", fontSize=8.3, leading=10.8),
    "cellb": ParagraphStyle("cellb", fontName="DV-B", fontSize=8.3, leading=10.8, textColor=colors.white),
    "cap": ParagraphStyle("cap", fontName="DV-I", fontSize=8.3, leading=11, spaceAfter=6, textColor=colors.HexColor("#444444")),
    "note": ParagraphStyle("note", fontName="DV", fontSize=9, leading=12.5),
}
FOOT = "Document synthétique fictif — projet pédagogique MaintiDoc (EMSI 2026) — aucune valeur technique réelle"


class DocBuilder:
    def __init__(self, path, doc_id, title, version):
        self.path, self.doc_id, self.title, self.version = path, doc_id, title, version
        self.visuals = []

    def _footer(self, canv, doc):
        canv.saveState()
        canv.setFont("DV", 7.2)
        canv.setFillColor(colors.HexColor("#666666"))
        canv.drawString(18 * mm, 10 * mm, f"{self.doc_id} — {self.version}")
        canv.drawRightString(A4[0] - 18 * mm, 10 * mm, f"Page {doc.page}")
        canv.drawCentredString(A4[0] / 2, 6 * mm, FOOT)
        canv.setStrokeColor(colors.HexColor("#bbbbbb"))
        canv.line(18 * mm, 13.5 * mm, A4[0] - 18 * mm, 13.5 * mm)
        canv.setFont("DV-B", 7.5)
        canv.setFillColor(BLUE)
        canv.drawString(18 * mm, A4[1] - 11 * mm, self.title[:95])
        canv.restoreState()

    def build(self, pages):
        doc = BaseDocTemplate(self.path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
                              topMargin=18 * mm, bottomMargin=19 * mm, title=self.title,
                              author="Équipe MaintiDoc (synthétique)")
        frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
        doc.addPageTemplates([PageTemplate(id="t", frames=[frame], onPage=self._footer)])
        story = []
        W = doc.width
        for pno, blocks in enumerate(pages, start=1):
            fn = tn = 0
            for b in blocks:
                k = b[0]
                if k in ("h1", "h2", "p", "title", "sub"):
                    story.append(Paragraph(b[1], S[k]))
                elif k == "spacer":
                    story.append(Spacer(1, b[1] * mm))
                elif k == "note":
                    t = Table([[Paragraph(b[1], S["note"])]], colWidths=[W])
                    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fff3cd")),
                                           ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#d9a400")),
                                           ("LEFTPADDING", (0, 0), (-1, -1), 6), ("TOPPADDING", (0, 0), (-1, -1), 5),
                                           ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
                    story += [t, Spacer(1, 5)]
                elif k in ("ul", "ol"):
                    items = [ListItem(Paragraph(x, S["p"]), leftIndent=14) for x in b[1]]
                    story.append(ListFlowable(items, bulletType="bullet" if k == "ul" else "1",
                                              start="•" if k == "ul" else 1, bulletFontName="DV", bulletFontSize=8.5,
                                              leftIndent=14))
                    story.append(Spacer(1, 4))
                elif k == "table":
                    _, caption, header, rows, cw = b
                    tn += 1
                    lab = f"tableau {pno}.{tn}"
                    self.visuals.append((lab, pno, f"tableau_{pno}_{tn}"))
                    story.append(Paragraph(f"<b>Tableau {pno}.{tn}</b> — {caption}", S["cap"]))
                    data = [[Paragraph(h, S["cellb"]) for h in header]]
                    for r in rows:
                        data.append([Paragraph(str(c), S["cell"]) for c in r])
                    tot = sum(cw)
                    t = Table(data, colWidths=[W * c / tot for c in cw], repeatRows=1)
                    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), BLUE),
                                           ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
                                           ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f1f4f9")]),
                                           ("VALIGN", (0, 0), (-1, -1), "TOP"),
                                           ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
                    story += [t, Spacer(1, 7)]
                elif k == "fig":
                    _, png, caption, wmm = b
                    fn += 1
                    lab = f"fig {pno}.{fn}"
                    self.visuals.append((lab, pno, f"figure_{pno}_{fn}"))
                    from PIL import Image as _I
                    iw, ih = _I.open(png).size
                    w = wmm * mm
                    story.append(Image(png, width=w, height=w * ih / iw))
                    story.append(Paragraph(f"<b>Figure {pno}.{fn}</b> — {caption}", S["cap"]))
            if pno < len(pages):
                story.append(PageBreak())
        doc.build(story)
        n = len(PdfReader(self.path).pages)
        if n != len(pages):
            raise RuntimeError(f"{self.doc_id}: {n} pages générées au lieu de {len(pages)} (débordement)")
        # vérification : chaque libellé visuel apparaît bien sur sa page
        for lab, pno, _ in self.visuals:
            if lab.startswith("tableau"):
                key = "Tableau " + lab.split()[1]
            else:
                key = "Figure " + lab.split()[1]
            txt = PdfReader(self.path).pages[pno - 1].extract_text() or ""
            if key not in txt:
                raise RuntimeError(f"{self.doc_id}: '{key}' absent de la page {pno}")
        return n

    def visuals_str(self):
        if not self.visuals:
            return "aucun"
        return " ; ".join(f"{l} p.{p}" for l, p, _ in self.visuals)


# ---------- figures ----------
def _anchor(b, side):
    x, y, w, h = b[:4]
    return {"l": (x, y + h / 2), "r": (x + w, y + h / 2), "t": (x + w / 2, y + h), "b": (x + w / 2, y)}[side]


def blocks_fig(path, boxes, arrows, figsize=(7.4, 3.5), ylim=50):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(0, 100); ax.set_ylim(0, ylim); ax.axis("off")
    for key, (x, y, w, h, label, col) in boxes.items():
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3,rounding_size=1.2", fc=col, ec="#333", lw=1.1))
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=7.6)
    for a, sa, b, sb, lab in arrows:
        p1, p2 = _anchor(boxes[a], sa), _anchor(boxes[b], sb)
        ax.annotate("", xy=p2, xytext=p1, arrowprops=dict(arrowstyle="-|>", lw=1.3, color="#222"))
        if lab:
            ax.text((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2 + 1.6, lab, ha="center", fontsize=6.8, color="#8a1c1c",
                    bbox=dict(fc="white", ec="none", pad=0.6))
    fig.savefig(path, dpi=170, bbox_inches="tight", facecolor="white")
    plt.close(fig)


COL = {"red": RED, "orange": ORANGE, "green": GREEN}


def panel_fig(path, leds, buttons):
    """leds: liste de 6 (label, couleur, code) ordonnée ligne 1 puis ligne 2."""
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    ax.set_xlim(0, 100); ax.set_ylim(0, 55); ax.axis("off")
    ax.add_patch(FancyBboxPatch((2, 2), 96, 51, boxstyle="round,pad=0.2,rounding_size=2", fc="#3b3f44", ec="black", lw=1.5))
    ax.add_patch(Rectangle((8, 36), 40, 13, fc="#10261c", ec="#999"))
    ax.text(28, 42.5, "AFFICHEUR", color="#7fe0a0", ha="center", va="center", fontsize=7)
    for i, (lab, col, code) in enumerate(leds):
        r, c = divmod(i, 3)
        cx, cy = 58 + c * 14, 42 - r * 17
        ax.add_patch(Circle((cx, cy), 3.0, fc=COL[col], ec="white", lw=1))
        ax.text(cx, cy - 6, lab, color="white", ha="center", fontsize=6.4)
        ax.text(cx, cy + 4.4, f"({i + 1})", color="#dddddd", ha="center", fontsize=6.2)
    for i, bl in enumerate(buttons):
        bx = 10 + i * 17
        ax.add_patch(Rectangle((bx, 8), 14, 8, fc="#cfd3d8", ec="black"))
        ax.text(bx + 7, 12, bl, ha="center", va="center", fontsize=6.6)
    fig.savefig(path, dpi=170, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ---------- photos synthétiques ----------
def _font(sz, bold=True):
    return ImageFont.truetype(FD + ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"), sz)


def draw_panel(leds, lit, model_label=None, stripe="#c9a227"):
    W, H = 1400, 1000
    img = PILImage.new("RGB", (W, H), (150, 148, 140))
    d = ImageDraw.Draw(img)
    for y in range(H):
        g = int(150 - 30 * y / H)
        d.line([(0, y), (W, y)], fill=(g, g - 2, g - 8))
    d.rounded_rectangle((120, 90, 1280, 910), 40, fill=(58, 62, 68), outline=(20, 20, 22), width=8)
    for bx, by in [(160, 130), (1240, 130), (160, 870), (1240, 870)]:
        d.ellipse((bx - 14, by - 14, bx + 14, by + 14), fill=(120, 120, 124), outline=(30, 30, 30), width=3)
    d.rectangle((120, 90, 1280, 130), fill=stripe)
    d.rectangle((200, 190, 640, 420), fill=(14, 32, 24), outline=(150, 150, 150), width=5)
    d.text((420, 305), "—  —  —", font=_font(46), fill=(40, 90, 60), anchor="mm")
    glow = PILImage.new("RGB", (W, H), (0, 0, 0))
    gd = ImageDraw.Draw(glow)
    pos = []
    for i, (lab, col, _) in enumerate(leds):
        r, c = divmod(i, 3)
        cx, cy = 780 + c * 160, 300 + r * 240
        base = {"red": (210, 40, 40), "orange": (245, 130, 15), "green": (61, 164, 77)}[col]
        pos.append((lab, cx, cy, base, lab == lit))
        if lab == lit:
            gd.ellipse((cx - 60, cy - 60, cx + 60, cy + 60), fill=tuple(int(v * 0.55) for v in base))
    glow = glow.filter(ImageFilter.GaussianBlur(34))
    img = ImageChops.add(img, glow)
    d = ImageDraw.Draw(img)
    for lab, cx, cy, base, on in pos:
        fill = base if on else tuple(int(v * 0.28) for v in base)
        d.ellipse((cx - 42, cy - 42, cx + 42, cy + 42), fill=fill, outline=(220, 220, 220), width=5)
        d.text((cx, cy + 78), lab, font=_font(22 if len(lab) > 5 else 30), fill=(235, 235, 235), anchor="mm")
    for i, bl in enumerate(["START", "STOP", "RESET"]):
        bx = 220 + i * 190
        d.rounded_rectangle((bx, 700, bx + 160, 780), 12, fill=(205, 208, 212), outline=(20, 20, 20), width=4)
        d.text((bx + 80, 740), bl, font=_font(28), fill=(20, 20, 20), anchor="mm")
    if model_label:
        d.rectangle((900, 800, 1230, 860), fill=(215, 215, 215))
        d.text((1065, 830), model_label, font=_font(30), fill=(30, 30, 30), anchor="mm")
    return img


def draw_plate(lines, tint=(176, 180, 186)):
    W, H = 1200, 800
    img = PILImage.new("RGB", (W, H), (96, 90, 82))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((120, 120, 1080, 680), 24, fill=tint, outline=(60, 60, 60), width=8)
    for bx, by in [(165, 165), (1035, 165), (165, 635), (1035, 635)]:
        d.ellipse((bx - 14, by - 14, bx + 14, by + 14), fill=(110, 110, 114), outline=(40, 40, 40), width=3)
    y = 190
    for i, (k, v) in enumerate(lines):
        d.text((190, y), k, font=_font(34, i == 0), fill=(40, 40, 44))
        d.text((600, y), v, font=_font(34, i == 0), fill=(25, 25, 30))
        y += 62
    return img


def photoize(img, seed, crop=None, angle=2.0):
    random.seed(seed)
    if crop:
        img = img.crop(crop)
    w, h = img.size
    img = img.rotate(angle, resample=PILImage.BICUBIC, expand=False, fillcolor=(100, 98, 92))
    # léger flou + bruit + vignettage
    img = img.filter(ImageFilter.GaussianBlur(1.1))
    import numpy as np
    a = np.asarray(img).astype("float32")
    rng = np.random.default_rng(seed)
    a += rng.normal(0, 6.5, a.shape)
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    a *= (1 - 0.28 * np.clip(r - 0.4, 0, 1))[..., None]
    a = np.clip(a, 0, 255).astype("uint8")
    return PILImage.fromarray(a)


def scan_pdf(src_pdf, dst_pdf, seed=1, dpi=130):
    """Rasterise un PDF texte et dégrade les pages pour simuler un scan (aucune couche texte)."""
    import numpy as np, tempfile, glob, shutil
    tmp = tempfile.mkdtemp()
    subprocess.run(["pdftoppm", "-r", str(dpi), "-png", src_pdf, os.path.join(tmp, "p")], check=True)
    pages = []
    rng = np.random.default_rng(seed)
    for i, f in enumerate(sorted(glob.glob(os.path.join(tmp, "p*.png")))):
        im = PILImage.open(f).convert("L")
        ang = float(rng.uniform(-0.9, 0.9))
        im = im.rotate(ang, resample=PILImage.BICUBIC, expand=False, fillcolor=255)
        im = im.filter(ImageFilter.GaussianBlur(0.9))
        a = np.asarray(im).astype("float32")
        a = 235 + (a - 255) * 0.82 + 8 * (a / 255.0 - 1) * 0  # papier légèrement grisé, contraste réduit
        a += rng.normal(0, 7, a.shape)
        h, w = a.shape
        yy, xx = np.mgrid[0:h, 0:w]
        a *= (1 - 0.10 * (xx / w) ** 3)  # ombre sur un bord
        # quelques taches
        for _ in range(8):
            cx, cy, rr = rng.integers(0, w), rng.integers(0, h), int(rng.integers(6, 22))
            m = ((xx - cx) ** 2 + (yy - cy) ** 2) < rr ** 2
            a[m] *= 0.93
        pages.append(PILImage.fromarray(np.clip(a, 0, 255).astype("uint8")).convert("RGB"))
    pages[0].save(dst_pdf, save_all=True, append_images=pages[1:], resolution=dpi, quality=72)
    shutil.rmtree(tmp)
