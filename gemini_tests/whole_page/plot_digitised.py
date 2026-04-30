#!/usr/bin/env python

# Plot the data digitised by Gemini from a daily rainfall image
# Compares results from multiple image resolutions (scale factors)

import os
import PIL.Image
import json
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--img", help="Image number", type=int, required=False, default=403)
parser.add_argument(
    "--scales",
    help="Scale factors to compare (space-separated, e.g. 1.0 0.5 0.25)",
    type=float,
    nargs="+",
    required=False,
    default=[1.0, 0.5, 0.25],
)
args = parser.parse_args()

scales = args.scales
n_scales = len(scales)

# load the image
img = PIL.Image.open(
    "../../images/jpgs_300dpi/Devon_1941-1950_RainNos_1651-1689-293.jpg"
)

# Load results for each scale from its subdirectory
def load_results(scale):
    d = "res_%.2f" % scale
    metadata = json.load(open("%s/metadata.json" % d))
    dd1 = json.load(open("%s/daily1.json" % d))
    totals = json.load(open("%s/totals.json" % d))
    return metadata, dd1, totals

results = {}
for scale in scales:
    try:
        results[scale] = load_results(scale)
    except FileNotFoundError as e:
        print("Warning: missing results for scale %.2f (%s)" % (scale, e))

available_scales = [s for s in scales if s in results]
n_avail = len(available_scales)

# Create the figure - wider to fit multiple resolution columns
fig = Figure(
    figsize=(10 + 6 * n_avail, 10),
    dpi=100,
    facecolor=(0.95, 0.95, 0.95, 1),
    edgecolor=None,
    linewidth=0.0,
    frameon=True,
    subplotpars=None,
    tight_layout=None,
)
canvas = FigureCanvas(fig)

# Total width is split: image takes ~30%, rest shared among scale columns
img_width = 0.30
col_width = (0.97 - img_width - 0.01) / max(n_avail, 1)

# Image on the left
ax_original = fig.add_axes([0.01, 0.02, img_width - 0.02, 0.96])
ax_original.set_axis_off()
imgplot = ax_original.imshow(img, zorder=10)

monthNumbers = {
    "Jan": 1,
    "January": 1,
    "Feb": 2,
    "February": 2,
    "Mar": 3,
    "March": 3,
    "Apr": 4,
    "April": 4,
    "May": 5,
    "Jun": 6,
    "June": 6,
    "Jul": 7,
    "July": 7,
    "Aug": 8,
    "August": 8,
    "Sep": 9,
    "September": 9,
    "Oct": 10,
    "October": 10,
    "Nov": 11,
    "November": 11,
    "Dec": 12,
    "December": 12,
}

for col_idx, scale in enumerate(available_scales):
    metadata, dd1, totals = results[scale]
    col_left = img_width + col_idx * col_width

    # Column header showing scale
    ax_header = fig.add_axes([col_left, 0.95, col_width - 0.01, 0.04])
    ax_header.set_xlim(0, 1)
    ax_header.set_ylim(0, 1)
    ax_header.set_xticks([])
    ax_header.set_yticks([])
    ax_header.text(
        0.5, 0.5,
        "Scale: %.2f (%.0f dpi)" % (scale, 300 * scale),
        ha="center", va="center", fontsize=11, fontweight="bold", color="black",
    )

    # Metadata
    ax_metadata = fig.add_axes([col_left, 0.80, col_width - 0.01, 0.14])
    ax_metadata.set_xlim(0, 1)
    ax_metadata.set_ylim(0, 1)
    ax_metadata.set_xticks([])
    ax_metadata.set_yticks([])
    ax_metadata.text(0.05, 0.85, "Year: %d" % metadata["Year"], fontsize=9, color="black")
    ax_metadata.text(0.05, 0.72, "Station: %d" % metadata["StationNumber"], fontsize=9, color="black")
    ax_metadata.text(0.05, 0.59, "Location: %s" % metadata["Location"], fontsize=9, color="black")
    ax_metadata.text(0.05, 0.46, "County: %s" % metadata["County"], fontsize=9, color="black")
    ax_metadata.text(0.05, 0.33, "Height: %d m" % metadata["Sea_level_height"], fontsize=9, color="black")
    ax_metadata.text(0.05, 0.20, "Gauge diam: %d" % metadata["Gauge_diameter"], fontsize=9, color="black")
    ax_metadata.text(
        0.05, 0.07,
        "Gauge ht: %d ft %d in" % (metadata["Gauge_height_feet"], metadata["Gauge_height_inches"]),
        fontsize=9, color="black",
    )

    # Digitised daily values
    ax_digitised = fig.add_axes([col_left, 0.13, col_width - 0.01, 0.64])
    ax_digitised.set_xlim(0.5, 12.5)
    ax_digitised.set_xticks(range(1, 13))
    ax_digitised.set_xticklabels(
        ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"),
        fontsize=7,
    )
    ax_digitised.xaxis.set_ticks_position("top")
    ax_digitised.xaxis.set_label_position("top")
    ax_digitised.set_ylim(0, 32)
    ax_digitised.set_yticks(range(1, 32))
    ax_digitised.set_yticklabels(range(1, 32), fontsize=7)
    ax_digitised.invert_yaxis()
    ax_digitised.set_aspect("auto")

    for month in dd1["Month"]:
        for day in month["rainfall"]:
            ax_digitised.text(
                monthNumbers[month["Month"][:3]],
                day["Day"],
                day["rainfall"],
                ha="center", va="center", fontsize=8, color="black",
            )

    # Monthly totals
    ax_totals = fig.add_axes([col_left, 0.09, col_width - 0.01, 0.03])
    ax_totals.set_xlim(0.5, 12.5)
    ax_totals.set_ylim(0, 1)
    ax_totals.set_xticks([])
    ax_totals.set_yticks([])

    for i, total in enumerate(totals["Totals"]):
        ax_totals.text(
            i + 1, 0.5, total,
            ha="center", va="center", fontsize=8, color="black",
        )

# Render
scale_str = "_".join("%.2f" % s for s in available_scales)
fig.savefig("result_scales_%s.webp" % scale_str)
