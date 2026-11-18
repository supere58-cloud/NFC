"""Render cases/out/preview.png from the generated parts (needs matplotlib)."""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

sys.path.insert(0, str(Path(__file__).parent))
from nfc_eink_cases import OUT, build_all

parts, _ = build_all()
names = list(parts)
fig = plt.figure(figsize=(16, 12))
for i, name in enumerate(names):
    ax = fig.add_subplot(3, 4, i + 1, projection="3d")
    verts, tris = parts[name].val().tessellate(0.05)
    v = np.array([(p.x, p.y, p.z) for p in verts])
    # shells are modelled face-down; flip them so the window faces the viewer
    if "shell" in name or "puck" in name:
        v[:, 2] = v[:, 2].max() - v[:, 2]
        v[:, 0] = -v[:, 0]
    faces = v[np.array(tris)]
    n = np.cross(faces[:, 1] - faces[:, 0], faces[:, 2] - faces[:, 0])
    n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
    shade = 0.35 + 0.65 * np.abs(n @ np.array([0.3, -0.4, 0.87]))
    col = np.outer(shade, [0.45, 0.62, 0.85])
    ax.add_collection3d(Poly3DCollection(faces, facecolors=col, edgecolors="none"))
    r = 32
    ax.set_xlim(-r, r); ax.set_ylim(-r, r); ax.set_zlim(-r, r)
    ax.set_box_aspect((1, 1, 1)); ax.view_init(elev=55, azim=-60); ax.set_axis_off()
    ax.set_title(name, fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "preview.png", dpi=110)
