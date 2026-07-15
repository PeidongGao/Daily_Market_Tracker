"""Create a Market Fingerprint PNG from data/history.csv."""

from __future__ import annotations

import argparse
import csv
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(PROJECT_ROOT / ".matplotlib"))

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

from history import read_history

HISTORY_PATH = PROJECT_ROOT / "data" / "history.csv"
FIGURES_DIR = PROJECT_ROOT / "figures"

INSTRUMENTS = (
    ("sp500", "S&P 500", False),
    ("nasdaq100", "Nasdaq-100", False),
    ("vix", "VIX", True),
    ("tnx", "TNX", False),
    ("dxy", "DXY", True),
    ("wti", "WTI Oil", False),
)


def load_record(target_date: str, history_path: Path = HISTORY_PATH) -> dict[str, str]:
    for row in read_history(history_path):
        if row["date"] == target_date:
            return row
    raise ValueError(f"No history record exists for {target_date}.")


def latest_date(history_path: Path = HISTORY_PATH) -> str:
    dates = [row["date"] for row in read_history(history_path)]
    if not dates:
        raise ValueError("history.csv contains no records.")
    return max(dates)


def generate(target_date: str, output_path: Path | None = None) -> Path:
    row = load_record(target_date)
    labels = [label for _, label, _ in INSTRUMENTS]
    raw_values = np.array([float(row[f"{key}_gap_pct"]) for key, _, _ in INSTRUMENTS])
    adjusted_values = np.array(
        [-value if reverse else value for value, (_, _, reverse) in zip(raw_values, INSTRUMENTS)]
    )

    visual_limit = max(0.5, np.ceil(np.max(np.abs(adjusted_values)) * 1.10 / 0.5) * 0.5)
    clipped = np.clip(adjusted_values, -visual_limit, visual_limit)
    tick_raw = np.linspace(-visual_limit, visual_limit, 5)
    tick_radius = tick_raw + visual_limit

    fig = plt.figure(figsize=(13, 6.5))
    grid = fig.add_gridspec(
        1, 2, width_ratios=[1, 1.45], left=0.06, right=0.97, top=0.86, bottom=0.17, wspace=0.24
    )
    ax_radar = fig.add_subplot(grid[0, 0], polar=True)
    radar_position = ax_radar.get_position()
    ax_radar.set_position(
        [radar_position.x0, radar_position.y0 - 0.10, radar_position.width, radar_position.height]
    )
    ax_heatmap = fig.add_subplot(grid[0, 1])
    fig.suptitle(f"Overnight Market Fingerprint\n{target_date}", fontsize=17, y=0.96)

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
    radii = clipped + visual_limit
    ax_radar.set_theta_offset(np.pi / 2)
    ax_radar.set_theta_direction(-1)
    ax_radar.plot(np.append(angles, angles[0]), np.append(radii, radii[0]), lw=2, marker="o")
    ax_radar.fill(np.append(angles, angles[0]), np.append(radii, radii[0]), alpha=0.15)
    ax_radar.set_xticks(angles, labels, fontsize=10)
    ax_radar.set_ylim(0, 2 * visual_limit)
    ax_radar.set_yticks(tick_radius, ["0%" if abs(value) < 1e-9 else f"{value:+.1f}%" for value in tick_raw], fontsize=8)
    theta = np.linspace(0, 2 * np.pi, 500)
    ax_radar.plot(theta, np.full_like(theta, visual_limit), "--", lw=1.3)
    for angle, radius, raw, adjusted in zip(angles, radii, raw_values, adjusted_values):
        offset = 0.08 * visual_limit if adjusted >= 0 else -0.08 * visual_limit
        ax_radar.text(angle, np.clip(radius + offset, 0.05 * visual_limit, 1.95 * visual_limit), f"{raw:+.3f}%", ha="center", va="center", fontsize=8.5)
    ax_radar.set_title("Market Shape", fontsize=12, pad=18)
    ax_radar.grid(alpha=0.4)

    ax_heatmap.imshow(adjusted_values.reshape(1, -1), cmap="RdYlGn", vmin=-visual_limit, vmax=visual_limit, aspect="auto")
    ax_heatmap.set_xticks(np.arange(len(labels)), labels, fontsize=11)
    ax_heatmap.set_yticks([])
    ax_heatmap.set_box_aspect(0.30)
    for index, (raw, adjusted) in enumerate(zip(raw_values, adjusted_values)):
        color = "white" if abs(adjusted) / visual_limit >= 0.6 else "black"
        ax_heatmap.text(index, 0, f"{raw:+.2f}%", ha="center", va="center", fontsize=12, fontweight="bold", color=color)
    ax_heatmap.set_title("Overnight Changes", fontsize=12, pad=14)
    for boundary in np.arange(0.5, len(labels), 1):
        ax_heatmap.axvline(boundary, lw=1, alpha=0.35)

    heatmap_position = ax_heatmap.get_position()
    width = heatmap_position.width * 0.72
    colorbar_axis = fig.add_axes([(heatmap_position.x0 + (heatmap_position.width - width) / 2), heatmap_position.y0 - 0.10, width, 0.022])
    colorbar = fig.colorbar(ScalarMappable(norm=Normalize(-visual_limit, visual_limit), cmap="RdYlGn"), cax=colorbar_axis, orientation="horizontal")
    colorbar.set_ticks(
        tick_raw,
        labels=["0" if abs(value) < 1e-9 else f"{value:+.1f}" for value in tick_raw],
    )
    colorbar.ax.tick_params(labelsize=8, length=3)
    colorbar.set_label("Direction-Adjusted Overnight Change (%)", fontsize=9, labelpad=4)
    fig.text(0.5, 0.015, "Labels show raw Gap %. Radar position and heatmap color use direction-adjusted values; VIX and DXY are reversed.", ha="center", fontsize=8.5)

    output_path = output_path or FIGURES_DIR / f"{target_date}.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=160)
    plt.close(fig)
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a Market Fingerprint PNG.")
    parser.add_argument("--date", default=None, help="ISO date in data/history.csv; defaults to latest.")
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    target_date = args.date or latest_date()
    print(f"Wrote {generate(target_date, args.output)}")


if __name__ == "__main__":
    main()
