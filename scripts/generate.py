"""Genera las dos imágenes del README del perfil: la cabecera y el esquema del caso real.

  python scripts/generate.py      (necesita Pillow y src/panther.jpg)

Cambia los textos de abajo y vuelve a ejecutarlo.
"""
import base64, io
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"
W = 840
BG, BOX, LINE, ACCENT, TEXT, MUTED = "#0f0d17", "#181523", "#3b3158", "#a78bfa", "#f5f3fb", "#a8a2bd"
SANS = '-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif'

HEADLINE = ["Software a medida para negocios", "que quieren dejar de hacerlo a mano."]
SUB = ["Reservas, gestión interna, apps para iPhone y automatización con IA.",
       "De la idea a producción, con una sola persona responsable."]


def svg(h, body, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {h}" '
            f'width="{W}" height="{h}" role="img" aria-label="{escape(label)}"><style>text{{font-family:{SANS}}}</style>'
            f'<rect width="{W}" height="{h}" rx="14" fill="{BG}"/>{body}</svg>\n')


def t(x, y, size, text, fill=TEXT, weight=400, anchor="start"):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{escape(text)}</text>'


def write(name, content):
    OUT.mkdir(exist_ok=True)
    (OUT / name).write_text(content, encoding="utf-8")
    print("wrote", name, f"{len(content) // 1024} KB")


def header():
    from PIL import Image
    im = Image.open(ROOT / "src" / "panther.jpg").convert("RGB").crop((390, 90, 760, 460)).resize((264, 264), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=84, optimize=True)
    data = base64.b64encode(buf.getvalue()).decode()
    h, cx, cy, r = 250, 104, 125, 62
    body = (f'<clipPath id="a"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>'
            f'<image clip-path="url(#a)" x="{cx - r}" y="{cy - r}" width="{2 * r}" height="{2 * r}" xlink:href="data:image/jpeg;base64,{data}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r + 4}" fill="none" stroke="{ACCENT}" stroke-width="2"/>'
            + t(206, 62, 15, "PantherCode", ACCENT, 600)
            + t(206, 104, 30, HEADLINE[0], TEXT, 700) + t(206, 142, 30, HEADLINE[1], TEXT, 700)
            + t(206, 180, 15, SUB[0], MUTED) + t(206, 202, 15, SUB[1], MUTED)
            + f'<circle cx="212" cy="228" r="4.5" fill="{ACCENT}"/>' + t(224, 233, 13.5, "Disponible para nuevos proyectos", TEXT, 600))
    write("cabecera.svg", svg(h, body, "PantherCode. " + " ".join(HEADLINE) + " " + " ".join(SUB) + " Disponible para nuevos proyectos."))


def box(x, y, title, sub, accent=False):
    return (f'<rect x="{x}" y="{y}" width="176" height="66" rx="10" fill="{BOX}" stroke="{ACCENT if accent else LINE}" stroke-width="1.5"/>'
            + t(x + 88, y + 29, 14.5, title, TEXT, 600, "middle") + t(x + 88, y + 49, 12, sub, MUTED, 400, "middle"))


def arrow(x1, y1, x2, y2):
    return f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{ACCENT}" stroke-width="1.6" marker-end="url(#h)" opacity=".9"/>'


def case():
    h = 290
    xs = [24, 229, 434, 640]
    top, mid, bot = 72, 127, 182
    body = (f'<defs><marker id="h" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
            f'<path d="M0 0L10 5L0 10Z" fill="{ACCENT}"/></marker></defs>'
            + t(24, 40, 14, "Todo el software de un grupo de lavaderos de coches, hecho y mantenido por una sola persona", MUTED)
            + box(xs[0], mid, "Sus clientes", "piden hora desde el móvil")
            + box(xs[1], top, "Reservas online", "sin llamadas ni esperas")
            + box(xs[1], bot, "App para iPhone", "nativa, en su bolsillo")
            + box(xs[2], top, "Panel de administración", "el día a día del negocio")
            + box(xs[2], bot, "Cámaras con visión", "vigilan y resumen solas")
            + box(xs[3], mid, "El dueño y su equipo", "todo claro cada mañana", True)
            + arrow(xs[0] + 176, mid + 24, xs[1] - 4, top + 40) + arrow(xs[0] + 176, mid + 42, xs[1] - 4, bot + 26)
            + arrow(xs[1] + 176, top + 33, xs[2] - 4, top + 33) + arrow(xs[1] + 176, bot + 22, xs[2] - 4, top + 52)
            + arrow(xs[2] + 176, top + 40, xs[3] - 4, mid + 24) + arrow(xs[2] + 176, bot + 26, xs[3] - 4, mid + 42)
            + t(24, 268, 13, "Una reserva aparece en el panel al momento, y las cámaras escriben el informe de cada mañana.", MUTED))
    write("caso.svg", svg(h, body, "Esquema del caso real: los clientes reservan online o desde la app de iPhone; las reservas llegan al "
                                   "panel de administración; las cámaras con visión generan un informe diario; el dueño y su equipo lo ven todo cada mañana."))


if __name__ == "__main__":
    header(), case()
