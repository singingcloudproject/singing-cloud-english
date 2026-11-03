"""
The singing cloud mascot for the hero, drawn as a layered SVG so the mouth can move.
Used by build.py. The animation itself is in assets/script.js ("singing cloud" section).
Same cloud as on Singing Cloud Studio; here the floor shadow is softer for the light, warm background.

Layers (back to front): glossy body → soft shading → highlights → mouth (inside, tongue, inner shadow, lip).
Mouth shape is set by three numbers: W (half width), H (how far it opens), T (top-lip curve; negative = rounder).
"""

# The cloud body is made of overlapping round "puffs" (cx, cy, r) in a 400 × 290 drawing area,
# traced to match the puffy shape of logo.png, plus an oval base to join them.
PUFFS = [(80, 192, 76), (116, 112, 60), (222, 100, 94), (324, 128, 66), (330, 202, 70)]
BASE = (200, 232, 150, 50)  # an oval that joins the puffs underneath: cx, cy, rx, ry


def cloud_shapes():
    out = "".join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in PUFFS)
    cx, cy, rx, ry = BASE
    out += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}"/>'
    return out + '<ellipse cx="205" cy="175" rx="150" ry="95"/>'  # solid core: no gaps between the puffs'


MOUTH_CX, MOUTH_CY = 208, 104
REST = (118, 108, 20)  # the still pose (also used for "reduce motion"), like the logo


def mouth_path(w, h, t, cx=MOUTH_CX, cy=MOUTH_CY):
    return (f"M{cx - w:.1f} {cy}C{cx - w * .55:.1f} {cy + t:.1f} {cx + w * .55:.1f} {cy + t:.1f} {cx + w:.1f} {cy}"
            f"C{cx + w:.1f} {cy + h * 1.33:.1f} {cx - w:.1f} {cy + h * 1.33:.1f} {cx - w:.1f} {cy}Z")


def tongue_transform(w, h, cx=MOUTH_CX, cy=MOUTH_CY):
    return f"translate({cx} {cy + h * .8:.1f}) scale({w * .46:.2f} {max(h, 1) * .4:.2f})"


TONGUE = "M-1 0C-1-.55-.45-.8 0-.45C.45-.8 1-.55 1 0C1 .6 .5 .8 0 .8C-.5 .8-1 .6-1 0Z"


def mascot_svg(label):
    m = mouth_path(*REST)
    return f"""<svg class="mascot" viewBox="-30 -40 460 370" role="img" aria-label="{label}">
  <defs>
    <radialGradient id="sc-body" gradientUnits="userSpaceOnUse" cx="150" cy="58" r="330">
      <stop offset="0" stop-color="#e2f7ff"/><stop offset=".32" stop-color="#a9def9"/>
      <stop offset=".7" stop-color="#6db8f0"/><stop offset="1" stop-color="#3d8ee0"/>
    </radialGradient>
    <linearGradient id="sc-shade" gradientUnits="userSpaceOnUse" x1="0" y1="120" x2="0" y2="290">
      <stop offset=".5" stop-color="#1c5cb8" stop-opacity="0"/><stop offset="1" stop-color="#1f62ba" stop-opacity=".32"/>
    </linearGradient>
    <radialGradient id="sc-spec"><stop offset="0" stop-color="#fff" stop-opacity=".95"/><stop offset=".55" stop-color="#fff" stop-opacity=".35"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
    <radialGradient id="sc-bounce" cy="0"><stop offset="0" stop-color="#bfe8ff" stop-opacity=".75"/><stop offset="1" stop-color="#bfe8ff" stop-opacity="0"/></radialGradient>
    <linearGradient id="sc-inner" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0f3a86"/><stop offset=".55" stop-color="#1b56b2"/><stop offset="1" stop-color="#2b72d0"/>
    </linearGradient>
    <radialGradient id="sc-tongue" cx="42%" cy="30%" r="75%">
      <stop offset="0" stop-color="#b4e3ff"/><stop offset=".5" stop-color="#62adf0"/><stop offset="1" stop-color="#2f7ed6"/>
    </radialGradient>
    <linearGradient id="sc-lip" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#7cc3f6"/><stop offset=".5" stop-color="#9bd6fb"/><stop offset="1" stop-color="#d4f0ff"/>
    </linearGradient>
    <radialGradient id="sc-floor"><stop offset="0" stop-color="#2a4a7a" stop-opacity=".28"/><stop offset="1" stop-color="#2a4a7a" stop-opacity="0"/></radialGradient>
    <clipPath id="sc-cloud-clip">{cloud_shapes()}</clipPath>
    <clipPath id="sc-mouth-clip"><path class="sc-m" d="{m}"/></clipPath>
  </defs>
  <ellipse class="sc-shadow" cx="200" cy="312" rx="160" ry="16" fill="url(#sc-floor)"/>
  <g class="sc-body">
    <g clip-path="url(#sc-cloud-clip)">
      <rect x="-10" y="-10" width="420" height="310" fill="url(#sc-body)"/>
      <rect x="-10" y="-10" width="420" height="310" fill="url(#sc-shade)"/>
      <ellipse cx="200" cy="296" rx="175" ry="34" fill="url(#sc-bounce)"/>
      <ellipse cx="78" cy="88" rx="30" ry="12" transform="rotate(-42 78 88)" fill="url(#sc-spec)"/>
      <ellipse cx="214" cy="30" rx="46" ry="15" transform="rotate(-12 214 30)" fill="url(#sc-spec)"/>
      <ellipse cx="346" cy="88" rx="22" ry="9" transform="rotate(32 346 88)" fill="url(#sc-spec)" opacity=".8"/>
      <ellipse cx="22" cy="200" rx="8" ry="24" transform="rotate(12 22 200)" fill="url(#sc-spec)" opacity=".7"/>
      <ellipse cx="384" cy="196" rx="7" ry="22" transform="rotate(-12 384 196)" fill="url(#sc-spec)" opacity=".45"/>
    </g>
    <g class="sc-mouth">
      <path class="sc-m" d="{m}" fill="none" stroke="#d6f2ff" stroke-opacity=".55" stroke-width="30" stroke-linejoin="round"/>
      <path class="sc-m" d="{m}" fill="url(#sc-inner)"/>
      <g clip-path="url(#sc-mouth-clip)">
        <path class="sc-tongue" d="{TONGUE}" transform="{tongue_transform(REST[0], REST[1])}" fill="url(#sc-tongue)"/>
        <path class="sc-m" d="{m}" fill="none" stroke="#071f5c" stroke-opacity=".45" stroke-width="22"/>
      </g>
      <path class="sc-m sc-lip" d="{m}" fill="none" stroke="url(#sc-lip)" stroke-width="13" stroke-linejoin="round"/>
    </g>
  </g>
</svg>"""
