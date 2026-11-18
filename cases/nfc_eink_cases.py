"""Parametric casings for 1.54" NFC-powered 4-colour e-ink modules.

Run:  python3 cases/nfc_eink_cases.py        (needs `pip install cadquery`)
Out:  cases/out/*.stl (print) and *.step (edit in any CAD tool)

Every dimension lives in the dataclasses below. Values marked VERIFY are
estimates or come from a reseller listing, not from a measured part: put
calipers on the real module, change the number, re-run.

Builds
  A  two-part enclosure for a BARE module (panel + NFC driver board on an FPC):
     Shellrus "4-color e-Ink NFC Module", or Good Display GDEM0154F51H panel +
     NFC-D1-0154 driver board.
  B  cradle for the Waveshare "1.54inch NFC-Powered e-Paper (G)" (already cased)
  C  cradle for the Good Display finished tag (GDNS0154AL / GDP0154NF2)
  D  screenless "tap to share" puck for a round anti-metal (ferrite) NFC
     sticker, NTAG213/215/216 or NTAG424 DNA, 25 mm or 30 mm

Each build comes in two mounting variants:
  *_adhesive  flat back for a gel pad / VHB tape
  *_magnet    side wings with 4 disc-magnet pockets on a 51 mm circle (the
              MagSafe ring), deliberately kept off the NFC coil
"""
from dataclasses import dataclass
from math import sqrt
from pathlib import Path

import cadquery as cq

OUT = Path(__file__).parent / "out"


# ----------------------------------------------------------------- parameters
@dataclass
class Magnets:
    dia: float = 5.0          # disc magnet diameter
    thick: float = 1.5        # disc magnet thickness
    fit: float = 0.2          # diametral clearance of the pocket
    extra_depth: float = 0.2  # pocket deeper than magnet (glue + flush)
    wing: float = 7.0         # width of each side wing
    ring_radius: float = 25.5  # MagSafe ring mean radius (46 ID / 56 OD)


@dataclass
class BareModule:
    """Build A: panel folded over its NFC driver board."""
    panel_w: float = 31.80    # GDEM0154F51H outline, datasheet
    panel_h: float = 37.32    # datasheet (long side, FPC exits here)
    panel_t: float = 1.00     # datasheet
    active: float = 27.00     # 200 x 200 px active area, datasheet
    active_top: float = 1.90  # VERIFY: panel top edge -> first pixel row
    board_w: float = 31.85    # VERIFY: reseller figure for the NFC board
    board_h: float = 37.65    # VERIFY
    board_t: float = 0.58     # VERIFY: bare PCB
    parts_t: float = 1.00     # VERIFY: tallest component on the board
    tape_t: float = 0.20      # double-sided tape between panel and board
    fpc_bend: float = 1.50    # room for the FPC fold below the panel
    fit: float = 0.20         # clearance per side around the stack
    window_margin: float = 0.20  # window larger than active area, per side
    face: float = 0.60        # front bezel thickness (3 layers @ 0.2)
    wall: float = 1.60
    rebate: float = 0.80      # ledge the back lid sits on
    lid_t: float = 0.80
    lid_fit: float = 0.10     # clearance per side, lid in rebate
    corner_r: float = 2.5


@dataclass
class CasedModule:
    """Builds B and C: a finished tag pressed into a cradle."""
    w: float
    h: float
    t: float
    fit: float = 0.20         # clearance per side
    floor: float = 1.00
    wall: float = 1.40
    rim_frac: float = 0.70    # low rim height as a fraction of module t
    lip: float = 0.50         # overhang of the two retaining clips
    lip_t: float = 0.60
    clip_frac: float = 0.60   # clip width as a fraction of module width
    corner_r: float = 3.0


WAVESHARE_G = CasedModule(w=41.28, h=47.84, t=4.5)   # w,h listing; t VERIFY
GOODDISPLAY_TAG = CasedModule(w=36.59, h=47.09, t=3.0)  # manufacturer figures


@dataclass
class TapTag:
    """Build D: round anti-metal NFC sticker, inserted from the back."""
    tag_dia: float = 30.0     # 25 or 30 mm are the common sizes
    tag_t: float = 1.0        # VERIFY: anti-metal stickers are ~0.4-1.0 mm
    fit: float = 0.25         # clearance per side
    face: float = 0.6         # plastic over the antenna: keep it thin
    wall: float = 1.8
    edge_r: float = 0.6       # rounded front edge
    magnet_dia: float = 58.0  # puck size for the magnet variant (MagSafe ring)


# -------------------------------------------------------------------- helpers
def rbox(w, h, t, r, z=0.0):
    b = cq.Workplane("XY").box(w, h, t, centered=(True, True, False))
    if r > 0:
        b = b.edges("|Z").fillet(r)
    return b.translate((0, 0, z))


def magnet_positions(x, m: Magnets, y_limit):
    """Four pockets at +-x, on the MagSafe circle where geometry allows."""
    y = sqrt(m.ring_radius ** 2 - x ** 2) if x < m.ring_radius else 0.0
    y = min(max(y, m.dia / 2 + 1.5), y_limit)
    return [(sx * x, sy * y) for sx in (-1, 1) for sy in (-1, 1)]


def cut_magnets(body, pts, m: Magnets, z_open, from_top):
    depth = m.thick + m.extra_depth
    z0 = z_open - depth if from_top else z_open
    for px, py in pts:
        body = body.cut(
            cq.Workplane("XY").circle((m.dia + m.fit) / 2).extrude(depth)
            .translate((px, py, z0)))
    return body


# -------------------------------------------------------------------- build A
def bare_dims(p: BareModule):
    cav_w = max(p.panel_w, p.board_w) + 2 * p.fit
    cav_h = max(p.panel_h, p.board_h) + 2 * p.fit + p.fpc_bend
    cav_d = p.panel_t + p.tape_t + p.board_t + p.parts_t + 0.1
    return cav_w, cav_h, cav_d


def bare_shell(p: BareModule, m: Magnets = None):
    """Front shell. Modelled (and printed) display-face down on the bed."""
    cav_w, cav_h, cav_d = bare_dims(p)
    w, h = cav_w + 2 * p.wall, cav_h + 2 * p.wall
    t = p.face + cav_d + p.lid_t
    full_w = w + (2 * m.wing if m else 0)
    body = rbox(full_w, h, t, p.corner_r)
    body = body.cut(rbox(cav_w, cav_h, t, 0.3, z=p.face))
    body = body.cut(rbox(cav_w + 2 * p.rebate, cav_h + 2 * p.rebate,
                         p.lid_t, 0.8, z=t - p.lid_t))
    # window: panel sits against the top of the cavity, FPC fold at the bottom
    win = p.active + 2 * p.window_margin
    win_y = cav_h / 2 - p.fit - p.active_top - p.active / 2
    body = body.cut(rbox(win, win, p.face, 0.4).translate((0, win_y, 0)))
    if m:
        pts = magnet_positions(w / 2 + m.wing / 2, m,
                               h / 2 - m.dia / 2 - 1.5)
        body = cut_magnets(body, pts, m, t, from_top=True)
    return body, dict(outer=(round(full_w, 2), round(h, 2), round(t, 2)),
                      cavity=(round(cav_w, 2), round(cav_h, 2),
                              round(cav_d, 2)),
                      window=(win, win), window_centre_y=round(win_y, 2))


def bare_lid(p: BareModule):
    cav_w, cav_h, _ = bare_dims(p)
    return rbox(cav_w + 2 * (p.rebate - p.lid_fit),
                cav_h + 2 * (p.rebate - p.lid_fit), p.lid_t, 0.7)


# ---------------------------------------------------------------- builds B, C
def cradle(p: CasedModule, m: Magnets = None):
    """Open tray; two sprung clips (top and bottom) hold the tag in."""
    iw, ih = p.w + 2 * p.fit, p.h + 2 * p.fit
    w, h = iw + 2 * p.wall, ih + 2 * p.wall
    rim_z = p.floor + p.rim_frac * p.t
    clip_z = p.floor + p.t + 0.15
    top = clip_z + p.lip_t
    full_w = w + (2 * m.wing if m else 0)
    body = rbox(full_w, h, top, p.corner_r)
    body = body.cut(rbox(iw, ih, top, 0.5, z=p.floor))
    clip_w = p.clip_frac * iw
    # retaining lips, then trim everything but the two clips down to the rim
    for sy in (-1, 1):
        body = body.union(
            cq.Workplane("XY").box(clip_w, p.lip + 0.2, p.lip_t,
                                   centered=(True, True, False))
            .translate((0, sy * (ih / 2 - p.lip / 2 + 0.1), clip_z)))
    keep = cq.Workplane("XY").box(clip_w, h + 2, top,
                                  centered=(True, True, False))
    trim = (cq.Workplane("XY").box(full_w + 2, h + 2, top,
                                   centered=(True, True, False))
            .cut(keep).translate((0, 0, rim_z)))
    body = body.cut(trim)
    if m:
        pts = magnet_positions(w / 2 + m.wing / 2, m,
                               h / 2 - m.dia / 2 - 1.5)
        body = cut_magnets(body, pts, m, 0.0, from_top=False)
    return body, dict(outer=(round(full_w, 2), round(h, 2), round(top, 2)),
                      pocket=(round(iw, 2), round(ih, 2), p.t))


# -------------------------------------------------------------------- build D
def tap_puck(p: TapTag, m: Magnets = None):
    """Printed face down. Tag goes in from the back, ferrite side out, and the
    adhesive pad (or the magnets' side) closes the back against the phone."""
    pocket_d = p.tag_dia + 2 * p.fit
    depth = p.tag_t + 0.1
    t = p.face + depth
    dia = p.magnet_dia if m else pocket_d + 2 * p.wall
    if m:
        t = max(t, p.face + m.thick + m.extra_depth + 0.4)
    body = cq.Workplane("XY").circle(dia / 2).extrude(t)
    body = body.faces("<Z").edges().fillet(p.edge_r)
    body = body.cut(cq.Workplane("XY").circle(pocket_d / 2).extrude(depth)
                    .translate((0, 0, t - depth)))
    if m:
        r = m.ring_radius
        pts = [(r, 0), (-r, 0), (0, r), (0, -r)]
        body = cut_magnets(body, pts, m, t, from_top=True)
    return body, dict(outer=(round(dia, 2), round(dia, 2), round(t, 2)),
                      pocket=(round(pocket_d, 2), round(depth, 2)))


# ----------------------------------------------------------------------- main
def build_all():
    a, mg = BareModule(), Magnets()
    parts, info = {}, {}
    parts["A_bare_shell_adhesive"], info["A_bare_shell_adhesive"] = \
        bare_shell(a)
    parts["A_bare_shell_magnet"], info["A_bare_shell_magnet"] = \
        bare_shell(a, mg)
    parts["A_bare_lid"] = bare_lid(a)
    for tag, prm in (("B_waveshare", WAVESHARE_G),
                     ("C_gooddisplay_tag", GOODDISPLAY_TAG)):
        parts[f"{tag}_cradle_adhesive"], info[f"{tag}_cradle_adhesive"] = \
            cradle(prm)
        parts[f"{tag}_cradle_magnet"], info[f"{tag}_cradle_magnet"] = \
            cradle(prm, mg)
    for size in (25.0, 30.0):
        tag = TapTag(tag_dia=size)
        n = f"D_tap_puck_{int(size)}mm"
        parts[f"{n}_adhesive"], info[f"{n}_adhesive"] = tap_puck(tag)
    parts["D_tap_puck_30mm_magnet"], info["D_tap_puck_30mm_magnet"] = \
        tap_puck(TapTag(), mg)
    return parts, info


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    parts, info = build_all()
    for name, solid in parts.items():
        cq.exporters.export(solid, str(OUT / f"{name}.stl"),
                            tolerance=0.01, angularTolerance=0.1)
        cq.exporters.export(solid, str(OUT / f"{name}.step"))
        s = solid.val()
        bb = s.BoundingBox()
        print(f"{name:34s} valid={s.isValid()} solids={len(solid.solids().vals())} "
              f"bbox={bb.xlen:.2f} x {bb.ylen:.2f} x {bb.zlen:.2f}  "
              f"vol={s.Volume() / 1000:.2f} cm3  {info.get(name, '')}")
