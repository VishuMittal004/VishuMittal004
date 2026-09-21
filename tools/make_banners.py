#!/usr/bin/env python3
"""
Generates the SVG artwork used by the profile README.

  python tools/make_banners.py                       # placeholders + headings
  python tools/make_banners.py --header me.jpg       # bake your photo into the header
  python tools/make_banners.py --footer bg.jpg       # bake an image into the footer
  python tools/make_banners.py --header a.jpg --footer b.jpg

Output goes to ./assets. The header/footer keep their green tint and animated waves;
your image sits underneath them. Run it from the repo root.
"""
import argparse, base64, io, os

GREEN = "#059669"
FONT = "'Segoe UI','SF Pro Display','Helvetica Neue',Arial,sans-serif"
MONO = "'Fira Code','SF Mono',Consolas,Menlo,monospace"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")


def embed(path, width):
    """Return a data URI for the image, downscaled/compressed when Pillow is available."""
    ext = os.path.splitext(path)[1].lower()
    try:
        from PIL import Image
        im = Image.open(path).convert("RGB")
        if im.width > width:
            im = im.resize((width, int(im.height * width / im.width)))
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=80, optimize=True)
        return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    except ImportError:
        mime = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}.get(ext, "image/jpeg")
        with open(path, "rb") as f:
            return f"data:{mime};base64," + base64.b64encode(f.read()).decode()


def wave_path(y, amp, period=600, width=2400, bottom=400):
    """A repeating sine-like wave, closed at the bottom so it can be filled."""
    d = f"M0,{y}"
    x = 0
    while x < width:
        d += f" C{x + period * 0.25},{y - amp} {x + period * 0.75},{y + amp} {x + period},{y}"
        x += period
    return d + f" V{bottom} H0 Z"


def banner(kind, image=None):
    """kind = 'header' or 'footer'."""
    if kind == "header":
        w, h = 1200, 280
        clip = "M0,0 H1200 V226 C1050,278 900,184 750,226 C600,268 450,184 300,226 C150,268 60,208 0,232 Z"
        waves = [(200, 22, 600, 16, 0.14), (226, 16, 800, 24, 0.10)]
        label_pos = (44, 44)
        text = f'''
  <g filter="url(#sh)" text-anchor="middle" fill="#fff" font-family="{FONT}">
    <text x="600" y="128" font-size="66" font-weight="800" letter-spacing="1">Vipanshu Mittal</text>
    <text x="600" y="172" font-size="22" font-weight="600" letter-spacing="5" opacity=".95">FULL-STACK  ·  AI  ·  PRODUCT BUILDER</text>
  </g>'''
    else:
        w, h = 1200, 170
        clip = "M0,44 C150,0 300,88 450,44 C600,0 750,88 900,44 C1050,0 1140,64 1200,34 V170 H0 Z"
        waves = [(70, 20, 600, 18, 0.14), (96, 14, 800, 26, 0.10)]
        label_pos = (44, 118)
        text = ""

    img = ""
    placeholder = ""
    if image:
        img = f'<image href="{embed(image, 1600)}" x="0" y="0" width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice"/>'
        tint = 0.68
    else:
        tint = 1
        lx, ly = label_pos
        placeholder = f'''
    <rect x="28" y="{ly - 30 if kind == 'header' else 60}" width="{w - 56}" height="{h - 100 if kind == 'header' else 84}" rx="14" fill="none" stroke="#fff" stroke-opacity=".22" stroke-width="2" stroke-dasharray="10 10"/>
    <text x="{lx}" y="{ly}" font-family="{MONO}" font-size="15" letter-spacing="3" fill="#fff" fill-opacity=".45">IMAGE PLACEHOLDER  ·  {w} x {h}  ·  run tools/make_banners.py --{kind} your-image.jpg</text>'''

    wave_svg = ""
    for i, (y, amp, period, dur, op) in enumerate(waves):
        wave_svg += f'''
    <g opacity="{op}">
      <path fill="#fff" d="{wave_path(y, amp, period, 2 * (w + period), h + 60)}">
        <animateTransform attributeName="transform" type="translate" from="0 0" to="-{period * (1 if i == 0 else 1)} 0" dur="{dur}s" repeatCount="indefinite"/>
      </path>
    </g>'''

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{kind}">
  <defs>
    <clipPath id="shape"><path d="{clip}"/></clipPath>
    <filter id="sh" x="-10%" y="-30%" width="120%" height="180%"><feDropShadow dx="0" dy="3" stdDeviation="5" flood-color="#000" flood-opacity=".35"/></filter>
  </defs>
  <g clip-path="url(#shape)">
    <rect width="{w}" height="{h}" fill="{GREEN}"/>
    {img}
    <rect width="{w}" height="{h}" fill="{GREEN}" fill-opacity="{tint}"/>{placeholder}{wave_svg}
  </g>{text}
</svg>
'''


def heading(caption, title, width=800, height=104):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-label="{title}">
  <defs>
    <linearGradient id="t" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#6EE7B7"/><stop offset=".5" stop-color="#10B981"/><stop offset="1" stop-color="#34D399"/>
    </linearGradient>
    <linearGradient id="l" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#10B981" stop-opacity="0"/><stop offset="1" stop-color="#10B981"/>
    </linearGradient>
    <linearGradient id="r" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#10B981"/><stop offset="1" stop-color="#10B981" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <text x="{width/2}" y="24" text-anchor="middle" font-family="{MONO}" font-size="13" letter-spacing="6" fill="#10B981" fill-opacity=".9">{caption}</text>
  <text x="{width/2}" y="70" text-anchor="middle" font-family="{FONT}" font-size="40" font-weight="800" letter-spacing="9" fill="url(#t)">{title}</text>
  <rect x="{width/2 - 210}" y="88" width="180" height="2" fill="url(#l)"/>
  <rect x="{width/2 + 30}" y="88" width="180" height="2" fill="url(#r)"/>
  <rect x="{width/2 - 5}" y="84" width="10" height="10" fill="#10B981" transform="rotate(45 {width/2} 89)"/>
</svg>
'''


def wordmark(width=800, height=150):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-label="ULTRON">
  <defs>
    <linearGradient id="t" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#6EE7B7"/><stop offset=".5" stop-color="#10B981"/><stop offset="1" stop-color="#059669"/>
    </linearGradient>
    <filter id="g" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="9"/></filter>
  </defs>
  <text x="{width/2}" y="92" text-anchor="middle" font-family="{FONT}" font-size="84" font-weight="900" letter-spacing="26" fill="#10B981" opacity=".35" filter="url(#g)">ULTRON</text>
  <text x="{width/2}" y="92" text-anchor="middle" font-family="{FONT}" font-size="84" font-weight="900" letter-spacing="26" fill="url(#t)">ULTRON</text>
  <text x="{width/2}" y="130" text-anchor="middle" font-family="{MONO}" font-size="14" letter-spacing="7" fill="#10B981" fill-opacity=".85">AI OPERATING ASSISTANT</text>
</svg>
'''


HEADINGS = {
    "h-about": ("01 / ABOUT", "WHO I AM"),
    "h-building": ("02 / IN PROGRESS", "CURRENTLY BUILDING"),
    "h-stack": ("03 / STACK", "TECH ARSENAL"),
    "h-projects": ("04 / WORK", "FEATURED PROJECTS"),
    "h-analytics": ("05 / ACTIVITY", "GITHUB ANALYTICS"),
}


def write(name, content):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote assets/" + name)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--header", help="image to use behind the header")
    ap.add_argument("--footer", help="image to use behind the footer")
    a = ap.parse_args()
    write("header.svg", banner("header", a.header))
    write("footer.svg", banner("footer", a.footer))
    for name, (cap, title) in HEADINGS.items():
        write(name + ".svg", heading(cap, title))
    write("ultron.svg", wordmark())
