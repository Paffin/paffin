#!/usr/bin/env python3
"""Generates the animated SVG assets used by the profile README (SMIL only, no JS).

Usage:  python3 assets/generate.py [output-dir]    (default: the folder of this script)
Edit the text constants in the functions below and re-run to change the animations.
"""
import os
import sys
from xml.sax.saxutils import escape

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT, exist_ok=True)

SANS = "'Inter','Segoe UI',system-ui,-apple-system,'Helvetica Neue',Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"


def fmt(x):
    return f"{x:.4f}".rstrip("0").rstrip(".")


def write(name, body):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(body)
    print("wrote", name, len(body) // 1024, "KB")


# --------------------------------------------------------------------------- hero
def hero():
    W, H = 960, 300
    taglines = [
        "Kubernetes, CI/CD and private LLMs as one system.",
        "Reproducible. Isolated. Observable. Recoverable.",
        "From an ambiguous problem to a service you can trust.",
    ]
    n = len(taglines)
    cycle = 12
    fade = 0.025

    def tagline(k, text):
        s, e = k / n, (k + 1) / n
        pts = [(0.0, 0, 8)]
        if s > 0:
            pts.append((s, 0, 8))
        pts.append((s + fade, 1, 0))
        pts.append((e - fade, 1, 0))
        pts.append((e, 0, -8))
        if e < 1:
            pts.append((1.0, 0, 8))
        kt = ";".join(fmt(p[0]) for p in pts)
        op = ";".join(str(p[1]) for p in pts)
        tr = ";".join(f"0 {p[2]}" for p in pts)
        return f"""
    <g opacity="{1 if k == 0 else 0}">
      <animate attributeName="opacity" values="{op}" keyTimes="{kt}" dur="{cycle}s" repeatCount="indefinite"/>
      <animateTransform attributeName="transform" type="translate" values="{tr}" keyTimes="{kt}" dur="{cycle}s" repeatCount="indefinite"/>
      <text x="64" y="244" font-family="{MONO}" font-size="16" fill="#cbd5e1"><tspan fill="#38bdf8">› </tspan>{escape(text)}<tspan fill="#38bdf8" fill-opacity="1">▌<animate attributeName="fill-opacity" values="1;0" dur="1s" calcMode="discrete" repeatCount="indefinite"/></tspan></text>
    </g>"""

    nodes = {
        "k8s": (790, 150, 17),
        "ci/cd": (692, 84, 10),
        "llm": (898, 92, 11),
        "mcp": (896, 212, 10),
        "rag": (790, 252, 10),
        "obs": (690, 204, 10),
    }
    edges = [
        ("k8s", "ci/cd"), ("k8s", "llm"), ("k8s", "mcp"), ("k8s", "rag"), ("k8s", "obs"),
        ("ci/cd", "obs"), ("llm", "mcp"), ("rag", "obs"), ("ci/cd", "llm"),
    ]
    edge_svg, packet_svg, node_svg = [], [], []
    for i, (a, b) in enumerate(edges):
        ax, ay, _ = nodes[a]
        bx, by, _ = nodes[b]
        edge_svg.append(
            f'<line x1="{ax}" y1="{ay}" x2="{bx}" y2="{by}" stroke="url(#acc)" stroke-opacity=".38" stroke-width="1.4"/>'
        )
        d = f"M{ax},{ay} L{bx},{by}" if i % 2 == 0 else f"M{bx},{by} L{ax},{ay}"
        dur = 2.6 + (i % 4) * 0.55
        packet_svg.append(
            f'<circle r="3" fill="#fff" filter="url(#soft)"><animateMotion dur="{dur}s" begin="{i * 0.37:.2f}s" repeatCount="indefinite" path="{d}"/></circle>'
        )
    for i, (name, (x, y, r)) in enumerate(nodes.items()):
        ly = y + r + 17
        node_svg.append(f"""
    <g>
      <circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="url(#acc)" stroke-width="1.2">
        <animate attributeName="r" values="{r};{r + 15}" dur="3.4s" begin="{i * 0.55:.2f}s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values=".7;0" dur="3.4s" begin="{i * 0.55:.2f}s" repeatCount="indefinite"/>
      </circle>
      <circle cx="{x}" cy="{y}" r="{r}" fill="#0b1226" stroke="url(#acc)" stroke-width="1.6"/>
      <circle cx="{x}" cy="{y}" r="{max(r // 3, 3)}" fill="url(#acc)"/>
      <text x="{x}" y="{ly}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="#94a3b8" letter-spacing=".5" stroke="#0e1431" stroke-width="4" stroke-linejoin="round" paint-order="stroke">{escape(name)}</text>
    </g>""")

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
  <title id="t">Maxim Kiktev — DevOps Lead · LLM Infrastructure</title>
  <desc id="d">Animated banner: a small infrastructure graph linking Kubernetes, CI/CD, LLM serving, MCP, RAG and observability.</desc>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#090e1d"/><stop offset=".55" stop-color="#0f1636"/><stop offset="1" stop-color="#1a1046"/>
    </linearGradient>
    <linearGradient id="acc" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#38bdf8"/><stop offset=".5" stop-color="#818cf8"/><stop offset="1" stop-color="#c084fc"/>
    </linearGradient>
    <linearGradient id="accName" x1="0" y1="0" x2="1" y2="0" spreadMethod="reflect">
      <stop offset="0" stop-color="#7dd3fc"/><stop offset=".5" stop-color="#a5b4fc"/><stop offset="1" stop-color="#e9b6ff"/>
      <animateTransform attributeName="gradientTransform" type="translate" values="-0.45 0;0.45 0;-0.45 0" dur="9s" repeatCount="indefinite"/>
    </linearGradient>
    <pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse">
      <circle cx="1.5" cy="1.5" r="1" fill="#fff" fill-opacity=".075"/>
    </pattern>
    <clipPath id="card"><rect width="{W}" height="{H}" rx="22"/></clipPath>
    <filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="46"/></filter>
    <filter id="soft" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="1.6"/></filter>
  </defs>

  <g clip-path="url(#card)">
    <rect width="{W}" height="{H}" fill="url(#bg)"/>
    <rect width="{W}" height="{H}" fill="url(#dots)"/>

    <circle cx="170" cy="70" r="150" fill="#38bdf8" fill-opacity=".20" filter="url(#blur)">
      <animate attributeName="cx" values="150;260;150" dur="14s" repeatCount="indefinite"/>
      <animate attributeName="cy" values="60;110;60" dur="11s" repeatCount="indefinite"/>
    </circle>
    <circle cx="820" cy="250" r="170" fill="#a855f7" fill-opacity=".26" filter="url(#blur)">
      <animate attributeName="cx" values="840;740;840" dur="16s" repeatCount="indefinite"/>
      <animate attributeName="cy" values="260;200;260" dur="12s" repeatCount="indefinite"/>
    </circle>

    <!-- infrastructure graph -->
    <g>
      {"".join(edge_svg)}
      {"".join(packet_svg)}
      {"".join(node_svg)}
    </g>

    <!-- copy -->
    <g>
      <animate attributeName="opacity" from="0" to="1" dur=".9s" fill="freeze"/>
      <circle cx="68" cy="58" r="4" fill="#34d399">
        <animate attributeName="opacity" values="1;.25;1" dur="2.2s" repeatCount="indefinite"/>
      </circle>
      <text x="82" y="62" font-family="{MONO}" font-size="12" fill="#7c8aa5" letter-spacing="2.4">PLATFORM ENGINEERING × PRIVATE AI</text>

      <text x="62" y="140" font-family="{SANS}" font-size="64" font-weight="800" letter-spacing="-1.5" fill="url(#accName)">Maxim Kiktev
        <animateTransform attributeName="transform" type="translate" values="0 14;0 0" dur=".9s" calcMode="spline" keySplines=".2 .8 .2 1" keyTimes="0;1" fill="freeze"/>
      </text>
      <text x="64" y="182" font-family="{SANS}" font-size="25" font-weight="500" fill="#e2e8f0">DevOps Lead <tspan fill="#64748b">·</tspan> LLM Infrastructure</text>
      <rect x="64" y="204" width="72" height="3" rx="1.5" fill="url(#acc)">
        <animate attributeName="width" values="0;72" dur="1s" begin=".3s" fill="freeze"/>
      </rect>
    </g>
    {"".join(tagline(k, t) for k, t in enumerate(taglines))}
  </g>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="21.5" fill="none" stroke="url(#acc)" stroke-opacity=".35"/>
</svg>
"""


# ----------------------------------------------------------------------- terminal
def terminal():
    W, H = 780, 322
    CW = 9.0           # one monospace cell, enforced with textLength
    X0 = 30
    P0, PITCH = 86, 26  # first baseline / line pitch
    lines = [
        ("cmd", "whoami"),
        ("out", "maxim-kiktev   # devops lead · llm infrastructure"),
        ("cmd", "cat ~/.principles"),
        ("out", "reproducibility · isolation · observability · security · cost · recovery"),
        ("cmd", "git log --oneline career"),
        ("out", "sysadmin → production ops → devops leadership → private ai platforms"),
        ("cmd", "./ship --to production"),
        ("out", "✔ deployed   ✔ observed   ✔ recoverable"),
        ("cmd", ""),
    ]

    def text_of(kind, s):
        if kind == "cmd":
            return "$ " + s, f'<tspan fill="#3fb950">$ </tspan><tspan fill="#e6edf3">{escape(s)}</tspan>'
        color = "#3fb950" if s.startswith("✔") else "#8b949e"
        return "  " + s, f'<tspan fill="{color}">  {escape(s)}</tspan>'

    t = 0.7
    events = [(0.0, X0, P0 - 14)]
    clips = []
    for i, (kind, s) in enumerate(lines):
        plain, _ = text_of(kind, s)
        n = len(plain)
        y = P0 + i * PITCH
        speed = 0.06 if kind == "cmd" else 0.011
        if kind == "out":
            t += 0.25
        start = t
        if kind == "cmd":
            # the "$ " prompt appears at once, then the command is typed char by char
            times = [start] + [start + 0.25 + (k - 3) * speed for k in range(3, n + 1)]
            widths = [2 * CW] + [k * CW for k in range(3, n + 1)]
        else:
            times = [start + k * speed for k in range(n + 1)]
            widths = [k * CW for k in range(n + 1)]
        clips.append((i, y, n, times, widths))
        for tt, w in zip(times, widths):
            events.append((tt, X0 + w, y - 14))
        t = times[-1] + (0.45 if kind == "cmd" else 0.55)
    hold = 5.5
    T = t + hold

    def anim(attr, vals, times_):
        kt = ";".join(fmt(x / T) for x in times_)
        v = ";".join(fmt(x) for x in vals)
        return f'<animate attributeName="{attr}" values="{v}" keyTimes="{kt}" dur="{fmt(T)}s" calcMode="discrete" repeatCount="indefinite"/>'

    defs_clips, body_lines = [], []
    for (i, y, n, times, widths) in clips:
        kind, s = lines[i]
        _, markup = text_of(kind, s)
        full = n * CW
        # first keyframe at 0 -> hidden, so the loop resets cleanly
        ts = [0.0] + times
        ws = [0] + widths
        # collapse equal timestamps
        dedup = []
        for tt, ww in zip(ts, ws):
            if dedup and abs(dedup[-1][0] - tt) < 1e-6:
                dedup[-1] = (tt, ww)
            else:
                dedup.append((tt, ww))
        ts = [d[0] for d in dedup]
        ws = [d[1] for d in dedup]
        defs_clips.append(
            f'<clipPath id="c{i}"><rect x="{X0}" y="{y - 19}" width="{fmt(full)}" height="26">{anim("width", ws, ts)}</rect></clipPath>'
        )
        if s or kind == "cmd":
            body_lines.append(
                f'<text x="{X0}" y="{y}" font-family="{MONO}" font-size="15" xml:space="preserve" textLength="{fmt(full)}" lengthAdjust="spacing" clip-path="url(#c{i})">{markup}</text>'
            )

    # cursor track
    ev = sorted(events)
    dedup = []
    for tt, x, y in ev:
        if dedup and abs(dedup[-1][0] - tt) < 1e-6:
            dedup[-1] = (tt, x, y)
        else:
            dedup.append((tt, x, y))
    ts = [d[0] for d in dedup]
    cursor = (
        f'<rect x="{X0}" y="{P0 - 14}" width="{fmt(CW)}" height="19" rx="1.5" fill="#58a6ff">'
        f'{anim("x", [d[1] for d in dedup], ts)}{anim("y", [d[2] for d in dedup], ts)}'
        f'<animate attributeName="fill-opacity" values="1;.15" dur="1s" calcMode="discrete" repeatCount="indefinite"/></rect>'
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t">
  <title id="t">Terminal: whoami — Maxim Kiktev, DevOps lead working on LLM infrastructure</title>
  <defs>
    <linearGradient id="bar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1c2230"/><stop offset="1" stop-color="#161b26"/></linearGradient>
    <linearGradient id="acc" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#38bdf8"/><stop offset=".5" stop-color="#818cf8"/><stop offset="1" stop-color="#c084fc"/></linearGradient>
    <clipPath id="win"><rect width="{W}" height="{H}" rx="14"/></clipPath>
    {"".join(defs_clips)}
  </defs>
  <g clip-path="url(#win)">
    <rect width="{W}" height="{H}" fill="#0d1117"/>
    <rect width="{W}" height="44" fill="url(#bar)"/>
    <rect y="43" width="{W}" height="1" fill="#30363d"/>
    <circle cx="26" cy="22" r="6.5" fill="#ff5f56"/><circle cx="48" cy="22" r="6.5" fill="#ffbd2e"/><circle cx="70" cy="22" r="6.5" fill="#27c93f"/>
    <text x="{W / 2}" y="27" text-anchor="middle" font-family="{MONO}" font-size="12.5" fill="#8b949e">maxim@platform: ~</text>
    <rect x="0" y="{H - 3}" width="{W}" height="3" fill="url(#acc)" fill-opacity=".7"/>
    {"".join(body_lines)}
    {cursor}
  </g>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="13.5" fill="none" stroke="#30363d"/>
</svg>
"""


# ----------------------------------------------------------------------- stack
def stack():
    W, H = 960, 150
    PLAT, AI, SEC, SW = "#58a6ff", "#a371f7", "#3fb950", "#f0883e"
    row1 = [(PLAT, x) for x in ["Kubernetes", "Docker", "GitLab CI/CD", "Linux", "NGINX", "HAProxy", "PostgreSQL", "Redis"]] + \
           [(SEC, x) for x in ["Keycloak / SSO", "RBAC", "Secrets management", "Audit logging", "ELK", "Zabbix", "Backup & restore"]]
    row2 = [(AI, x) for x in ["Ollama", "vLLM", "OpenAI-compatible APIs", "MCP", "RAG", "Qdrant", "FAISS", "Agent orchestration"]] + \
           [(SW, x) for x in ["Go", "Python", "Bash", "TypeScript", "React", "FastAPI"]]
    CH, GAP, CPX = 36, 12, 7.1

    def row(items, y, direction, dur_mult=1.0):
        x = 0
        chips = []
        for color, label in items:
            tw = round(len(label) * CPX)
            w = tw + 46
            chips.append(
                f'<g transform="translate({x},0)"><rect width="{w}" height="{CH}" rx="{CH // 2}" fill="#0d1117" stroke="#30363d"/>'
                f'<circle cx="19" cy="{CH // 2}" r="4.5" fill="{color}"/>'
                f'<text x="32" y="{CH // 2 + 4.5}" font-family="{SANS}" font-size="13" font-weight="500" fill="#e6edf3" textLength="{tw}" lengthAdjust="spacingAndGlyphs">{escape(label)}</text></g>'
            )
            x += w + GAP
        total = x
        copies = "".join(chips)
        dur = total / 38 * dur_mult
        frm, to = (0, -total) if direction < 0 else (-total, 0)
        return f"""<g transform="translate(0,{y})"><g>
      <animateTransform attributeName="transform" type="translate" from="{frm} 0" to="{to} 0" dur="{fmt(dur)}s" repeatCount="indefinite"/>
      <g>{copies}</g><g transform="translate({total},0)">{copies}</g><g transform="translate({2 * total},0)">{copies}</g>
    </g></g>"""

    legend = [("platform", PLAT), ("security & ops", SEC), ("ai engineering", AI), ("software", SW)]
    lx, items = 0, []
    for label, color in legend:
        items.append(f'<g transform="translate({lx},0)"><circle cx="0" cy="-4" r="4" fill="{color}"/><text x="11" y="0" font-family="{SANS}" font-size="12" fill="#8b949e">{escape(label)}</text></g>')
        lx += 22 + len(label) * 6.4 + 14
    legend_svg = f'<g transform="translate({fmt((W - lx + 14) / 2)},{H - 14})">{"".join(items)}</g>'

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t">
  <title id="t">Toolbox: Kubernetes, Docker, GitLab CI/CD, Ollama, vLLM, MCP, RAG, Go, Python and more</title>
  <defs>
    <linearGradient id="fade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#000"/><stop offset=".07" stop-color="#fff"/><stop offset=".93" stop-color="#fff"/><stop offset="1" stop-color="#000"/>
    </linearGradient>
    <mask id="m" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H - 30}"><rect width="{W}" height="{H - 30}" fill="url(#fade)"/></mask>
  </defs>
  <g mask="url(#m)">
    {row(row1, 12, -1)}
    {row(row2, 66, +1, 1.12)}
  </g>
  {legend_svg}
</svg>
"""


# --------------------------------------------------------------------- divider
def divider():
    W, H = 960, 28
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="presentation" aria-hidden="true">
  <defs>
    <linearGradient id="line" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#818cf8" stop-opacity="0"/><stop offset=".5" stop-color="#818cf8" stop-opacity=".75"/><stop offset="1" stop-color="#818cf8" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="acc" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#38bdf8"/><stop offset=".5" stop-color="#818cf8"/><stop offset="1" stop-color="#c084fc"/></linearGradient>
    <radialGradient id="pulse"><stop offset="0" stop-color="#a5b4fc"/><stop offset="1" stop-color="#a5b4fc" stop-opacity="0"/></radialGradient>
  </defs>
  <rect x="40" y="13" width="{W - 80}" height="2" rx="1" fill="url(#line)"/>
  <circle r="9" cy="14" fill="url(#pulse)">
    <animate attributeName="cx" values="60;900" dur="7s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.1;.9;1" dur="7s" repeatCount="indefinite"/>
  </circle>
  <g transform="translate({W // 2},14)">
    <rect x="-6" y="-6" width="12" height="12" rx="2" fill="url(#acc)">
      <animateTransform attributeName="transform" type="rotate" values="45;225;405" dur="9s" repeatCount="indefinite"/>
    </rect>
    <circle r="12" fill="none" stroke="#818cf8" stroke-opacity=".5">
      <animate attributeName="r" values="8;16" dur="2.8s" repeatCount="indefinite"/>
      <animate attributeName="stroke-opacity" values=".6;0" dur="2.8s" repeatCount="indefinite"/>
    </circle>
  </g>
</svg>
"""


# ------------------------------------------------------------------------- cta
def cta():
    W, H = 340, 76
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t">
  <title id="t">Discuss a project</title>
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#0284c7"/><stop offset=".5" stop-color="#4f46e5"/><stop offset="1" stop-color="#9333ea"/>
    </linearGradient>
    <linearGradient id="shine" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".38"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="pill"><rect x="8" y="8" width="324" height="60" rx="30"/></clipPath>
    <filter id="glow" x="-20%" y="-60%" width="140%" height="240%"><feGaussianBlur stdDeviation="9"/></filter>
  </defs>
  <rect x="24" y="18" width="292" height="50" rx="25" fill="#6366f1" opacity=".55" filter="url(#glow)">
    <animate attributeName="opacity" values=".35;.65;.35" dur="3.2s" repeatCount="indefinite"/>
  </rect>
  <rect x="8" y="8" width="324" height="60" rx="30" fill="url(#g)"/>
  <g clip-path="url(#pill)">
    <rect y="0" width="80" height="{H}" fill="url(#shine)" transform="skewX(-22)">
      <animate attributeName="x" values="-140;420;420" keyTimes="0;.45;1" dur="4.2s" repeatCount="indefinite"/>
    </rect>
  </g>
  <rect x="8.5" y="8.5" width="323" height="59" rx="29.5" fill="none" stroke="#fff" stroke-opacity=".28"/>
  <text x="170" y="45.5" text-anchor="middle" font-family="{SANS}" font-size="19" font-weight="700" fill="#fff" letter-spacing=".2">Discuss a project
    <tspan font-size="20">→<animate attributeName="dx" values="4;11;4" dur="1.6s" repeatCount="indefinite"/></tspan>
  </text>
</svg>
"""


write("hero.svg", hero())
write("terminal.svg", terminal())
write("stack.svg", stack())
write("divider.svg", divider())
write("cta.svg", cta())
