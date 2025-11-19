# star_map_3d_from_extracted_json.py
# Build a 3D star map from decade generator's extracted_data.json
# Coordinates are stored as (Altitude°, Azimuth°, Distance m).
# Frame: X=East, Y=North, Z=Up. Azimuth measured clockwise from North by default.

import json
import pathlib
import re
import math
import argparse
from typing import Tuple, Optional, Dict, Any, List

# ---------- Defaults ----------
CONTENT_ROOT = pathlib.Path("content")
JSON_CANDIDATES = [
    CONTENT_ROOT / "Meta" / "Programs" / "debug" / "decade_article_generator" / "extracted_data.json",
]
OUT_DIR = CONTENT_ROOT / "Meta" / "Programs" / "star_map_generator" / "output"
OUT_PNG_3D = OUT_DIR / "star_map_3d.png"
OUT_PNG_TOP = OUT_DIR / "star_map_topdown.png"
OUT_SVG_3D = OUT_DIR / "star_map_3d.svg"
OUT_CSV = OUT_DIR / "stars_cartesian.csv"

# ---------- Parsing ----------
_num = r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)"
TRIPLE_RE = re.compile(rf"^\s*\(?\s*({_num})\D+({_num})\D+({_num})\s*\)?\s*$")
PAIR_RE = re.compile(rf"({_num})\D+({_num})")

def _to_float(x: str) -> float:
    return float(x.replace("°", "").replace(",", " ").strip())

def parse_alt_az_dist(s: Any) -> Optional[Tuple[float, float, float]]:
    """
    Accepts examples:
      "(35, 120, 2000)"
      "35° 120° 2000"
      "alt 35, az 120, dist 2000"
      "az 120; alt 35; distance=2000"
      Also falls back to first three numbers in the string.
    Returns (alt_deg, az_deg, dist_m).
    """
    if not isinstance(s, str) or not s.strip():
        return None
    t = s.strip()

    # Label-aware pass
    alt_m = re.search(rf"\balt(?:itude)?\D*({_num})", t, re.I)
    az_m  = re.search(rf"\baz(?:imuth)?\D*({_num})", t, re.I)
    d_m   = re.search(rf"\b(dist(?:ance)?)\D*({_num})", t, re.I)

    if alt_m and az_m and d_m:
        alt = _to_float(alt_m.group(1))
        az  = _to_float(az_m.group(1))
        dist = _to_float(d_m.group(2))
        return sanitize_aad(alt, az, dist)

    # Triple-of-numbers pass
    m3 = TRIPLE_RE.match(t)
    if m3:
        alt = _to_float(m3.group(1))
        az  = _to_float(m3.group(2))
        dist = _to_float(m3.group(3))
        return sanitize_aad(alt, az, dist)

    # Fallback: find three numbers anywhere (assume alt, az, dist)
    nums = re.findall(_num, t)
    if len(nums) >= 3:
        alt = _to_float(nums[0])
        az  = _to_float(nums[1])
        dist = _to_float(nums[2])
        return sanitize_aad(alt, az, dist)

    return None

def sanitize_aad(alt: float, az: float, dist: float) -> Tuple[float, float, float]:
    alt = max(0.0, min(90.0, alt))
    az  = az % 360.0
    dist = max(0.0, dist)
    return (alt, az, dist)

# ---------- Data loading ----------
def load_extracted_json(path: Optional[pathlib.Path]) -> Dict[str, Any]:
    if path:
        if not path.is_file():
            raise FileNotFoundError(path)
        return json.loads(path.read_text(encoding="utf-8"))
    for p in JSON_CANDIDATES:
        if p.is_file():
            print(f"[READ] {p}")
            return json.loads(p.read_text(encoding="utf-8"))
    raise FileNotFoundError("Cannot find extracted_data.json in expected locations.")

def gather_stars(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    stars = []
    star_block = payload.get("star", {}) or {}
    bases = star_block.get("bases", []) or []
    for b in bases:
        name = b.get("star_name") or ""
        coords = b.get("coordinates") or ""
        if not name or not coords:
            continue
        parsed = parse_alt_az_dist(coords)
        if not parsed:
            continue
        alt, az, dist = parsed
        stars.append({"name": str(name), "alt": alt, "az": az, "dist": dist, "coordinates_raw": str(coords)})
    return stars

# ---------- Geometry ----------
def aad_to_xyz(alt_deg: float, az_deg: float, r: float, az_from_east=False) -> Tuple[float, float, float]:
    """
    Convert (alt, az, r) to Cartesian with X=East, Y=North, Z=Up.
    Default azimuth measured clockwise from North (astronomy convention).
    If az_from_east=True: azimuth measured CCW from East (math convention).
    """
    alt = math.radians(alt_deg)
    az  = math.radians(az_deg)

    if az_from_east:
        # 0° at +X (East), increase CCW: x=r*cos alt * cos az; y=r*cos alt * sin az
        x = r * math.cos(alt) * math.cos(az)
        y = r * math.cos(alt) * math.sin(az)
    else:
        # 0° at +Y (North), increase CW: x=r*cos alt * sin az; y=r*cos alt * cos az
        x = r * math.cos(alt) * math.sin(az)
        y = r * math.cos(alt) * math.cos(az)

    z = r * math.sin(alt)
    return (x, y, z)

# ---------- Plotting ----------
def plot_3d_and_topdown(stars_xyz: List[Dict[str, Any]], show_labels: bool, dpi: int, elev: float, azim: float):
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (needed for 3D)

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    xs = [s["x"] for s in stars_xyz]
    ys = [s["y"] for s in stars_xyz]
    zs = [s["z"] for s in stars_xyz]
    names = [s["name"] for s in stars_xyz]

    # 3D figure
    fig3d = plt.figure(figsize=(8, 7), dpi=dpi)
    ax3 = fig3d.add_subplot(111, projection="3d")
    ax3.scatter(xs, ys, zs, s=20)

    if show_labels:
        for x, y, z, label in zip(xs, ys, zs, names):
            ax3.text(x, y, z, f" {label}", fontsize=7, zdir=None)

    ax3.set_xlabel("X (East, m)")
    ax3.set_ylabel("Y (North, m)")
    ax3.set_zlabel("Z (Up, m)")
    ax3.set_title("Star Map (3D)")
    _set_equal_aspect_3d(ax3, xs, ys, zs)

    ax3.view_init(elev=elev, azim=azim)
    fig3d.tight_layout()
    fig3d.savefig(OUT_PNG_3D)
    fig3d.savefig(OUT_SVG_3D)
    print(f"[WROTE] {OUT_PNG_3D}")
    print(f"[WROTE] {OUT_SVG_3D}")

    # Top-down (Z ignored)
    fig2d = plt.figure(figsize=(7, 6), dpi=dpi)
    ax2 = fig2d.add_subplot(111)
    ax2.scatter(xs, ys, s=20)
    if show_labels:
        for x, y, label in zip(xs, ys, names):
            ax2.text(x, y, f" {label}", fontsize=8, va="center", ha="left")

    ax2.set_xlabel("X (East, m)")
    ax2.set_ylabel("Y (North, m)")
    ax2.set_title("Star Map (Top-down)")
    ax2.grid(True, linewidth=0.4, alpha=0.4)
    ax2.set_aspect("equal", adjustable="box")
    _pad_axes_2d(ax2, xs, ys)

    fig2d.tight_layout()
    fig2d.savefig(OUT_PNG_TOP)
    print(f"[WROTE] {OUT_PNG_TOP}")

def _set_equal_aspect_3d(ax, xs, ys, zs):
    # cube bounds so spheres look like spheres
    import numpy as np
    x_min, x_max = np.min(xs), np.max(xs)
    y_min, y_max = np.min(ys), np.max(ys)
    z_min, z_max = np.min(zs), np.max(zs)
    max_range = max(x_max - x_min, y_max - y_min, z_max - z_min)
    if max_range == 0:
        max_range = 1.0
    x_mid = (x_max + x_min) / 2
    y_mid = (y_max + y_min) / 2
    z_mid = (z_max + z_min) / 2
    r = max_range / 2
    ax.set_xlim(x_mid - r, x_mid + r)
    ax.set_ylim(y_mid - r, y_mid + r)
    ax.set_zlim(z_mid - r, z_mid + r)

def _pad_axes_2d(ax, xs, ys, pad_frac=0.05):
    import numpy as np
    x_min, x_max = np.min(xs), np.max(xs)
    y_min, y_max = np.min(ys), np.max(ys)
    dx = max(1.0, x_max - x_min)
    dy = max(1.0, y_max - y_min)
    ax.set_xlim(x_min - dx * pad_frac, x_max + dx * pad_frac)
    ax.set_ylim(y_min - dy * pad_frac, y_max + dy * pad_frac)

# ---------- CSV ----------
def write_csv(stars_xyz: List[Dict[str, Any]]):
    import csv
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with (OUT_CSV).open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["name", "alt_deg", "az_deg", "dist_m", "x_east_m", "y_north_m", "z_up_m"])
        for s in stars_xyz:
            w.writerow([s["name"], s["alt"], s["az"], s["dist"], s["x"], s["y"], s["z"]])
    print(f"[WROTE] {OUT_CSV}")

# ---------- CLI ----------
def main():
    ap = argparse.ArgumentParser(description="Generate a 3D star map from extracted_data.json")
    ap.add_argument("--json", type=pathlib.Path, default=None,
                    help="Path to extracted_data.json (optional; defaults to known locations)")
    ap.add_argument("--no-labels", action="store_true", help="Do not draw star name labels")
    ap.add_argument("--dpi", type=int, default=150, help="Figure DPI")
    ap.add_argument("--view-elev", type=float, default=20.0, help="3D view elevation (deg)")
    ap.add_argument("--view-azim", type=float, default=-60.0, help="3D view azimuth (deg)")
    ap.add_argument("--az-from-east", action="store_true",
                    help="Interpret azimuth 0° as +X (East) growing CCW (math convention).")
    args = ap.parse_args()

    payload = load_extracted_json(args.json)
    stars = gather_stars(payload)
    if not stars:
        print("[NOTE] No stars with parseable coordinates found.")
        return

    # Convert to Cartesian
    stars_xyz = []
    for s in stars:
        x, y, z = aad_to_xyz(s["alt"], s["az"], s["dist"], az_from_east=args.az_from_east)
        stars_xyz.append({**s, "x": x, "y": y, "z": z})

    plot_3d_and_topdown(stars_xyz, show_labels=not args.no_labels, dpi=args.dpi,
                        elev=args.view_elev, azim=args.view_azim)
    write_csv(stars_xyz)

if __name__ == "__main__":
    main()
