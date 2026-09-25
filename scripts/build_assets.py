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
  <text x="340" y="292" font-family="{SANS}" font-size="20" fill="{t['muted']}">Elche, Spain  ·  Systems and networks student  ·  Full stack at a law firm</text>"""
    write("hero", theme, svg(1280, 360, "Cristóbal Tormo, full stack developer", inner))


def terminal(theme):
    t = THEMES[theme]
    fs = 18
    cw = 10.85
    lh = 31
    x0 = 52
    y0 = 108
    script = [
        ("cmd", "whoami"),
        ("out", "Cristóbal Tormo, full stack developer from Elche, Spain"),
        ("cmd", "cat now.txt"),
        ("out", "> runs the whole digital side of a law firm"),
        ("out", "> studies systems and networks (2025 to 2027)"),
        ("out", "> keeps a homelab full of apps alive, on purpose"),
        ("cmd", "gitsync --version"),
        ("out", "gitsync v1.0.0  (mine, open source, Apache-2.0)"),
    ]
    parts = []
    clips = []
    now = 0.8
    for i, (kind, text) in enumerate(script):
        y = y0 + i * lh
        if kind == "cmd":
            n = len(text)
            step = 0.07
            vals = ";".join(f"{(k * cw):.1f}" for k in range(n + 1))
            keys = ";".join(f"{k / n:.4f}" for k in range(n + 1))
            width = n * cw + 4
            if STATIC:
                rect = f'<rect x="{x0 + 2 * cw}" y="{y - fs}" width="{width:.1f}" height="{lh}"/>'
            else:
                rect = (
                    f'<rect x="{x0 + 2 * cw}" y="{y - fs}" width="0" height="{lh}">'
                    f'<animate attributeName="width" values="{vals}" keyTimes="{keys}" calcMode="discrete" '
                    f'dur="{n * step:.2f}s" begin="{now:.2f}s" fill="freeze"/></rect>'
                )
            clips.append(f'<clipPath id="c{i}">{rect}</clipPath>')
            prompt_op = "1" if STATIC else "0"
            pset = "" if STATIC else f'<set attributeName="opacity" to="1" begin="{now:.2f}s" fill="freeze"/>'
            parts.append(
                f'<g><text x="{x0}" y="{y}" font-family="{MONO}" font-size="{fs}" fill="{t["accent"]}" opacity="{prompt_op}">$ {pset}</text>'
                f'<text x="{x0 + 2 * cw}" y="{y}" font-family="{MONO}" font-size="{fs}" fill="{t["text"]}" clip-path="url(#c{i})">{esc(text)}</text></g>'
            )
            now += n * step + 0.45
        else:
            op = "1" if STATIC else "0"
            sset = "" if STATIC else f'<set attributeName="opacity" to="1" begin="{now:.2f}s" fill="freeze"/>'
            parts.append(
                f'<text x="{x0}" y="{y}" font-family="{MONO}" font-size="{fs}" fill="{t["muted"]}" opacity="{op}">{esc(text)}{sset}</text>'
            )
            now += 0.35
    yc = y0 + len(script) * lh
    blink = "" if STATIC else f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.1s" begin="{now:.2f}s" repeatCount="indefinite"/>'
    cursor_op = "1" if STATIC else "0"
    cursor_set = "" if STATIC else f'<set attributeName="opacity" to="1" begin="{now:.2f}s" fill="freeze"/>'
    parts.append(
        f'<text x="{x0}" y="{yc}" font-family="{MONO}" font-size="{fs}" fill="{t["accent"]}" opacity="{cursor_op}">${cursor_set}</text>'
        f'<rect x="{x0 + 2 * cw}" y="{yc - fs + 1}" width="10" height="{fs + 3}" fill="{t["text"]}" opacity="{cursor_op}">{cursor_set}{blink}</rect>'
    )
    h = yc + 46
    inner = f"""  <defs>{''.join(clips)}</defs>
  <rect x="1" y="1" width="{900 - 2}" height="{h - 2}" rx="14" fill="{t['panel']}" stroke="{t['border']}" stroke-width="2"/>
  <path d="M1 44 H899" stroke="{t['border']}" stroke-width="2"/>
  <circle cx="32" cy="23" r="6.5" fill="#ed6a5e"/><circle cx="54" cy="23" r="6.5" fill="#f4bf4f"/><circle cx="76" cy="23" r="6.5" fill="#61c554"/>
  <text x="450" y="28" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{t['muted']}">cristobal@homelab: ~</text>
  {''.join(parts)}"""
    write("terminal", theme, svg(900, h, "Terminal introducing Cristóbal Tormo", inner))


def cards(theme):
    t = THEMES[theme]
    data = [
        ("git-sync", "Open source", ["Mirrors your Git server to GitHub", "within seconds. One small Go binary", "for Linux, macOS and Windows."], "Go  ·  Docker  ·  Webhooks"),
        ("Tickets", "Full stack", ["Multi-user ticket portal with API,", "two-factor auth and push alerts.", "Real-time updates over Socket.IO."], "Next.js  ·  PostgreSQL  ·  Prisma"),
        ("Discord bot", "Bot", ["65+ slash commands, a web dashboard", "and AI-assisted moderation for a", "full community server."], "Discord.js  ·  Express  ·  MongoDB"),
        ("WhatsApp monitor", "Real time", ["Spots deleted and edited messages", "as they happen. Installable PWA", "with push notifications."], "Socket.IO  ·  Baileys  ·  MongoDB"),
        ("Self-hosted mail", "Infra", ["Own mail server with DKIM, SPF,", "DMARC and MTA-STS, relayed by a", "VPS over WireGuard past port 25."], "Mailcow  ·  Postfix  ·  WireGuard"),
        ("Law firm platform", "Client work", ["Public site and admin panel for a", "law firm, with its own mail server", "and an SEO-driven blog workflow."], "Astro  ·  Node.js  ·  Postfix"),
    ]
    cw, ch, gap = 310, 196, 20
    W = 3 * cw + 2 * gap + 4
    H = 2 * ch + gap + 4
    out = []
    for i, (title, badge, lines, tags) in enumerate(data):
        x = 2 + (i % 3) * (cw + gap)
        y = 2 + (i // 3) * (ch + gap)
        bw = len(badge) * 7.4 + 20
        accent_bar = ""
        body = "".join(
            f'<text x="{x + 24}" y="{y + 100 + k * 22}" font-family="{SANS}" font-size="14.5" fill="{t["muted"]}">{esc(l)}</text>'
            for k, l in enumerate(lines)
        )
        out.append(
            f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="12" fill="{t["panel"]}" stroke="{t["border"]}" stroke-width="1.5"/>'
            f"{accent_bar}"
            f'<text x="{x + 24}" y="{y + 45}" font-family="{SANS}" font-size="20" font-weight="650" fill="{t["text"]}">{esc(title)}</text>'
            f'<rect x="{x + 24}" y="{y + 56}" width="{bw:.0f}" height="20" rx="10" fill="none" stroke="{t["accent"]}" stroke-width="1.2"/>'
            f'<text x="{x + 24 + bw / 2:.1f}" y="{y + 70}" text-anchor="middle" font-family="{SANS}" font-size="11.5" font-weight="600" fill="{t["accent"]}">{esc(badge)}</text>'
            f"{body}"
            f'<text x="{x + 24}" y="{y + ch - 20}" font-family="{MONO}" font-size="12" fill="{t["muted"]}">{esc(tags)}</text>'
        )
    write("projects", theme, svg(W, H, "Selected projects", "\n  ".join(out)))


def homelab(theme):
    t = THEMES[theme]

    def node(x, y, w, h, title, sub, accent=False):
        stroke = t["accent"] if accent else t["border"]
        return (
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{t["panel"]}" stroke="{stroke}" stroke-width="1.6"/>'
            f'<text x="{x + w / 2}" y="{y + h / 2 - 2}" text-anchor="middle" font-family="{SANS}" font-size="16" font-weight="650" fill="{t["text"]}">{esc(title)}</text>'
            f'<text x="{x + w / 2}" y="{y + h / 2 + 18}" text-anchor="middle" font-family="{SANS}" font-size="12" fill="{t["muted"]}">{esc(sub)}</text>'
        )

    flow = "" if STATIC else '<animate attributeName="stroke-dashoffset" from="0" to="-28" dur="1.4s" repeatCount="indefinite"/>'

    def line(d, label=None, lx=0, ly=0):
        s = f'<path d="{d}" fill="none" stroke="{t["accent"]}" stroke-width="2" stroke-dasharray="6 8" stroke-linecap="round" marker-end="url(#arr)">{flow}</path>'
        if label:
            s += f'<text x="{lx}" y="{ly}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{t["muted"]}">{esc(label)}</text>'
        return s

    chips = [
        "cv", "tickets", "balbot", "msg",
        "git", "vault", "adguard", "home assistant",
        "wireguard", "planka", "failover",
        "mail",
    ]
    cx0, cy0, cw, chh, g = 404, 96, 126, 38, 12
    chip_svg = []
    for i, name in enumerate(chips):
        hot = name == "mail"
        slot = 12 if hot else i
        x = cx0 + (slot % 4) * (cw + g)
        y = cy0 + (slot // 4) * (chh + g)
        stroke = t["accent"] if hot else t["border"]
        chip_svg.append(
            f'<rect x="{x}" y="{y}" width="{cw}" height="{chh}" rx="8" fill="{t["bg"]}" stroke="{stroke}" stroke-width="1.4"/>'
            f'<text x="{x + cw / 2}" y="{y + 24}" text-anchor="middle" font-family="{MONO}" font-size="13.5" fill="{t["text"]}">{esc(name)}</text>'
        )
    mx = cx0 + 1 * (cw + g)
    my = cy0 + 3 * (chh + g)
    chip_svg.append(
        f'<rect x="{mx}" y="{my}" width="{cw}" height="{chh}" rx="8" fill="none" stroke="{t["border"]}" stroke-width="1.4" stroke-dasharray="4 4"/>'
        f'<text x="{mx + cw / 2}" y="{my + 24}" text-anchor="middle" font-family="{MONO}" font-size="13.5" fill="{t["muted"]}">+ more</text>'
    )
    inner = f"""  <defs><marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{t['accent']}"/></marker></defs>
  <rect x="380" y="30" width="590" height="400" rx="16" fill="{t['panel']}" stroke="{t['border']}" stroke-width="1.6"/>
  <text x="404" y="66" font-family="{SANS}" font-size="17" font-weight="650" fill="{t['text']}">Proxmox VE</text>
  <text x="516" y="66" font-family="{SANS}" font-size="14" fill="{t['muted']}">one isolated LXC container per project</text>
  {''.join(chip_svg)}
  <line x1="404" y1="332" x2="946" y2="332" stroke="{t['border']}" stroke-width="1.2"/>
  <text x="404" y="364" font-family="{MONO}" font-size="13" fill="{t['muted']}">nightly backups to a USB disk  ·  UPS with clean shutdown  ·  1 mini PC</text>
  <text x="404" y="392" font-family="{MONO}" font-size="13" fill="{t['muted']}">DNS by AdGuard Home  ·  secrets in Vaultwarden  ·  Git on Forgejo</text>
  {node(30, 60, 150, 62, "Internet", "visitors and mail")}
  {node(30, 205, 150, 70, "Cloudflare", "tunnel + access", True)}
  {node(30, 335, 150, 70, "VPS relay", "SMTP + HAProxy", True)}
  {line("M105 124 V 203")}
  {line("M182 240 H 378", "tunnel", 280, 228)}
  {line("M182 370 H 300 V 261 H 402", "WireGuard", 240, 358)}"""
    write("homelab", theme, svg(1000, 460, "Homelab architecture", inner))


def stack(theme):
    t = THEMES[theme]
    rows = [
        ("Frontend", [("react", "React"), ("nextdotjs", "Next.js"), ("astro", "Astro"), ("typescript", "TypeScript"), ("tailwindcss", "Tailwind"), ("vite", "Vite")]),
        ("Backend", [("nodedotjs", "Node.js"), ("express", "Express"), ("fastify", "Fastify"), ("go", "Go"), ("python", "Python"), ("socketdotio", "Socket.IO")]),
        ("Data", [("postgresql", "PostgreSQL"), ("mongodb", "MongoDB"), ("sqlite", "SQLite"), ("redis", "Redis"), ("prisma", "Prisma")]),
        ("Infrastructure", [("proxmox", "Proxmox"), ("linux", "Linux"), ("docker", "Docker"), ("caddy", "Caddy"), ("cloudflare", "Cloudflare"), ("wireguard", "WireGuard")]),
        ("Tooling", [("git", "Git"), ("forgejo", "Forgejo"), ("github", "GitHub"), ("githubactions", "Actions"), ("claude", "Claude Code"), ("vaultwarden", "Vaultwarden")]),
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
        terminal(th)
        cards(th)
        homelab(th)
        stack(th)
        pill("pill-web", "Website", "cristobaltormo.com", th)
        pill("pill-linkedin-cristobaltormo", "LinkedIn", "cristobaltormo", th)
        pill("pill-mail", "Email", "info@cristobaltormo.com", th)
    print("ok", OUT)
