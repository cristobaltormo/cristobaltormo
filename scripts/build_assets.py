import os
import re
import sys
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.environ.get("OUT", os.path.join(ROOT, "assets"))
STATIC = os.environ.get("STATIC") == "1"
os.makedirs(OUT, exist_ok=True)

SANS = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

THEMES = {
    "light": dict(bg="#ffffff", panel="#f6f8fa", border="#d0d7de", text="#1f2328", muted="#59636e", accent="#2563eb", glow="0.10"),
    "dark": dict(bg="#0d1117", panel="#161b22", border="#30363d", text="#e6edf3", muted="#8b949e", accent="#4f8cff", glow="0.16"),
}


def esc(s):
    return escape(s)


def write(name, theme, body):
    with open(os.path.join(OUT, f"{name}-{theme}.svg"), "w", encoding="utf-8") as f:
        f.write(body)


def svg(w, h, label, inner):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'role="img" aria-label="{esc(label)}">\n{inner}\n</svg>\n'
    )


def symbol_paths():
    src = open(os.path.join(ROOT, "assets", "symbol.svg"), encoding="utf-8").read()
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', src).group(1).split()]
    paths = re.findall(r'<path[^>]*\bd="([^"]+)"', src)
    return vb, paths


def icon_path(name):
    src = open(os.path.join(ROOT, "assets", "icons", f"{name}.svg"), encoding="utf-8").read()
    return re.search(r'<path d="([^"]+)"', src).group(1)


def hero(theme):
    t = THEMES[theme]
    vb, paths = symbol_paths()
    target = 150
    s = target / vb[3]
    sym = "".join(f'<path d="{d}" fill="{t["text"]}"/>' for d in paths)
    roles = [
        "full stack developer",
        "self-hosting everything",
        "Node.js, TypeScript and Go",
        "learning systems and networks",
    ]
    char_w = 15.6
    x0 = 340
    y = 226
    dur = 4 * 3.2
    items = []
    for i, role in enumerate(roles):
        begin = i * 3.2
        anim = ""
        op = "1" if (STATIC and i == 0) else "0"
        if not STATIC:
            anim = (
                f'<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.03;0.22;0.25;1" '
                f'dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'
            )
        cx = x0 + 2 * char_w + len(role) * char_w + 6
        cursor = f'<rect x="{cx:.1f}" y="{y - 24}" width="11" height="28" fill="{t["accent"]}"/>'
        items.append(
            f'<g opacity="{op}">{anim}'
            f'<text x="{x0}" y="{y}" font-family="{MONO}" font-size="26" fill="{t["muted"]}">$ </text>'
            f'<text x="{x0 + 2 * char_w}" y="{y}" font-family="{MONO}" font-size="26" fill="{t["accent"]}">{esc(role)}</text>'
            f"{cursor}</g>"
        )
    inner = f"""  <defs>
    <pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.2" fill="{t['border']}"/></pattern>
    <linearGradient id="fade" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.55" stop-color="#fff" stop-opacity="0.15"/><stop offset="1" stop-color="#fff" stop-opacity="1"/></linearGradient>
    <mask id="m"><rect width="1280" height="360" fill="url(#fade)"/></mask>
    <radialGradient id="glow" cx="0.82" cy="0.1" r="0.7"><stop offset="0" stop-color="{t['accent']}" stop-opacity="{t['glow']}"/><stop offset="1" stop-color="{t['accent']}" stop-opacity="0"/></radialGradient>
  </defs>
  <rect width="1280" height="360" fill="{t['bg']}"/>
  <rect width="1280" height="360" fill="url(#glow)"/>
  <rect width="1280" height="360" fill="url(#dots)" mask="url(#m)"/>
  <g transform="translate(110 105) scale({s:.4f}) translate({-vb[0]} {-vb[1]})">{sym}</g>
  <line x1="290" y1="95" x2="290" y2="255" stroke="{t['border']}" stroke-width="2"/>
  <text x="338" y="162" font-family="{SANS}" font-size="72" font-weight="700" letter-spacing="-2" fill="{t['text']}">Cristóbal Tormo</text>
  {''.join(items)}
  <text x="340" y="292" font-family="{SANS}" font-size="20" fill="{t['muted']}">Full stack developer  ·  Systems and networks student</text>"""
    write("hero", theme, svg(1280, 360, "Cristóbal Tormo, full stack developer", inner))


def cards(theme):
    t = THEMES[theme]
    data = [
        ("git-sync", "Mirror your Git server to GitHub, live.", "Apache-2.0",
         ["Forgejo, Gitea, GitLab, Gogs and more", "One small Go binary, or Docker", "Linux, macOS and Windows"],
         "Go  ·  Docker  ·  Webhooks"),
        ("typedeck", "Turn any USB keyboard into a macro keyboard.", "MIT",
         ["Arduino Leonardo and a USB Host Shield", "macOS, Linux and Windows", "Live editor and OBS control"],
         "Go  ·  Arduino  ·  HID"),
    ]
    w, h = 480, 232
    for name, tagline, lic, bullets, tags in data:
        bw = len(lic) * 7.4 + 20
        rows = "".join(
            f'<circle cx="34" cy="{122 + k * 26 - 5}" r="2.5" fill="{t["accent"]}"/>'
            f'<text x="48" y="{122 + k * 26}" font-family="{SANS}" font-size="14.5" fill="{t["muted"]}">{esc(b)}</text>'
            for k, b in enumerate(bullets)
        )
        inner = (
            f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="{t["panel"]}" stroke="{t["border"]}" stroke-width="1.5"/>'
            f'<text x="28" y="50" font-family="{SANS}" font-size="24" font-weight="700" fill="{t["text"]}">{esc(name)}</text>'
            f'<rect x="{w - 28 - bw:.0f}" y="31" width="{bw:.0f}" height="22" rx="11" fill="none" stroke="{t["accent"]}" stroke-width="1.2"/>'
            f'<text x="{w - 28 - bw / 2:.1f}" y="46" text-anchor="middle" font-family="{SANS}" font-size="12" font-weight="600" fill="{t["accent"]}">{esc(lic)}</text>'
            f'<text x="28" y="82" font-family="{SANS}" font-size="15.5" fill="{t["text"]}">{esc(tagline)}</text>'
            f'<line x1="28" y1="96" x2="{w - 28}" y2="96" stroke="{t["border"]}" stroke-width="1"/>'
            f"{rows}"
            f'<text x="28" y="{h - 22}" font-family="{MONO}" font-size="12.5" fill="{t["muted"]}">{esc(tags)}</text>'
        )
        write(f"project-{name}", theme, svg(w, h, name, inner))

def stack(theme):
    t = THEMES[theme]
    rows = [
        ("Frontend", [("react", "React"), ("nextdotjs", "Next.js"), ("astro", "Astro"), ("typescript", "TypeScript"), ("tailwindcss", "Tailwind"), ("vite", "Vite")]),
        ("Backend", [("nodedotjs", "Node.js"), ("express", "Express"), ("fastify", "Fastify"), ("go", "Go"), ("python", "Python"), ("socketdotio", "Socket.IO")]),
        ("Data", [("postgresql", "PostgreSQL"), ("mongodb", "MongoDB"), ("sqlite", "SQLite"), ("redis", "Redis"), ("prisma", "Prisma")]),
        ("Infrastructure", [("proxmox", "Proxmox"), ("linux", "Linux"), ("docker", "Docker"), ("cloudflare", "Cloudflare")]),
    ]
    tw, th, pitch, rowh = 100, 78, 112, 96
    x_tiles = 190
    out = []
    for r, (label, items) in enumerate(rows):
        y = 8 + r * rowh
        out.append(f'<text x="8" y="{y + 44}" font-family="{SANS}" font-size="15" font-weight="650" fill="{t["text"]}">{esc(label)}</text>')
        if r:
            out.append(f'<line x1="8" y1="{y - 9}" x2="{x_tiles + 6 * pitch - 12}" y2="{y - 9}" stroke="{t["border"]}" stroke-width="1"/>')
        for c, (ic, name) in enumerate(items):
            x = x_tiles + c * pitch
            out.append(
                f'<rect x="{x}" y="{y}" width="{tw}" height="{th}" rx="12" fill="{t["panel"]}" stroke="{t["border"]}" stroke-width="1.3"/>'
                f'<svg x="{x + tw / 2 - 15}" y="{y + 14}" width="30" height="30" viewBox="0 0 24 24"><path d="{icon_path(ic)}" fill="{t["text"]}"/></svg>'
                f'<text x="{x + tw / 2}" y="{y + 66}" text-anchor="middle" font-family="{SANS}" font-size="12.5" fill="{t["muted"]}">{esc(name)}</text>'
            )
    W = x_tiles + 6 * pitch
    H = 8 + len(rows) * rowh
    write("stack", theme, svg(W, H, "Technology stack", "\n  ".join(out)))


def pill(name, label, detail, theme):
    t = THEMES[theme]
    w = int(24 + len(label) * 9.2 + 14 + len(detail) * 8.2 + 26 + 22)
    inner = (
        f'<rect x="1" y="1" width="{w - 2}" height="46" rx="23" fill="{t["panel"]}" stroke="{t["border"]}" stroke-width="1.6"/>'
        f'<text x="24" y="30" font-family="{SANS}" font-size="15" font-weight="650" fill="{t["text"]}">{esc(label)}</text>'
        f'<text x="{24 + len(label) * 9.2 + 12:.1f}" y="30" font-family="{MONO}" font-size="13" fill="{t["muted"]}">{esc(detail)}</text>'
        f'<path d="M{w - 34} 24 H{w - 20} M{w - 26} 18 L{w - 20} 24 L{w - 26} 30" fill="none" stroke="{t["accent"]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
    )
    write(name, theme, svg(w, 48, label, inner))


if __name__ == "__main__":
    for th in THEMES:
        hero(th)
        cards(th)
        stack(th)
        pill("pill-web", "Website", "cristobaltormo.com", th)
        pill("pill-linkedin-cristobaltormo", "LinkedIn", "cristobaltormo", th)
        pill("pill-mail", "Email", "info@cristobaltormo.com", th)
    print("ok", OUT)
