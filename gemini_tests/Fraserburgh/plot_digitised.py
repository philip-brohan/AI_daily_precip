#!/usr/bin/env python

# Plot the data digitised by Gemini from a Fraserburg image

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
args = parser.parse_args()

# load the image
img = PIL.Image.open("../../images/SAWS/Fraserburg/Fraseburg_1892_Mar.jpg")

# load the digitised data
page = json.load(open("page.json"))

# Create the figure
fig = Figure(
    figsize=(28, 10),  # Width, Height (inches)
    dpi=100,
    facecolor=(0.95, 0.95, 0.95, 1),
    edgecolor=None,
    linewidth=0.0,
    frameon=True,
    subplotpars=None,
    tight_layout=None,
)
canvas = FigureCanvas(fig)

# Image in the left
ax_original = fig.add_axes([0.01, 0.02, 0.47, 0.96])
ax_original.set_axis_off()
imgplot = ax_original.imshow(img, zorder=10)

# Metadata top right
ax_metadata = fig.add_axes([0.52, 0.9, 0.47, 0.075])
ax_metadata.set_xlim(0, 1)
ax_metadata.set_ylim(0, 1)
ax_metadata.set_xticks([])
ax_metadata.set_yticks([])
ax_metadata.text(
    0.05,
    0.75,
    "Year: %d" % page["Metadata"]["Year"],
    fontsize=12,
    color="black",
)
ax_metadata.text(
    0.05,
    0.55,
    "Month: %s" % page["Metadata"]["Month"],
    fontsize=12,
    color="black",
)

ax_metadata.text(
    0.05,
    0.35,
    "Hour: %s" % page["Metadata"]["Hour"],
    fontsize=12,
    color="black",
)
ax_metadata.text(
    0.05,
    0.15,
    "Location: %s" % page["Metadata"]["Location"],
    fontsize=12,
    color="black",
)

# # Digitised numbers on the right
ax_digitised = fig.add_axes([0.52, 0.13, 0.47, 0.73])
ax_digitised.set_xlim(0.5, 18.5)
ax_digitised.set_xticks(range(1, 19))
ax_digitised.set_xticklabels(
    (
        "T: Dry",
        "T: Wet",
        "T: Max",
        "T: Min",
        "T: Max AR",
        "T: Min AR",
        "T: Hum",
        "T: Dew P.",
        "T: Tens.",
        "P: Uscale",
        "P: Lscale",
        "P: Height",
        "P: Att. T",
        "P: @ 32F",
        "Wind: D",
        "Wind: F",
        "Cloud",
        "Rain",
    )
)
ax_digitised.xaxis.set_ticks_position("top")
ax_digitised.xaxis.set_label_position("top")
ax_digitised.set_ylim(0, 32)
ax_digitised.set_yticks(range(1, 32))
ax_digitised.set_yticklabels(range(1, 32))
ax_digitised.invert_yaxis()
ax_digitised.set_aspect("auto")

# Temperature
xidx = 0
for var in [
    "Dry_Bulb",
    "Wet_Bulb",
    "Maximum",
    "Minimum",
    "Maximium_after_resetting",
    "Minimum_after_resetting",
    "Humidity",
    "Dew_Point",
    "Tension",
]:
    xidx += 1
    for day in range(1, 32):
        try:
            dv = page["Days"][day - 1]["Day"]
            value = page["Days"][day - 1]["Temperature"][var]
            if str(value) == "999":
                continue
            ax_digitised.text(
                xidx,
                dv,
                value,
                ha="center",
                va="center",
                fontsize=12,
                color="black",
            )
        except Exception as e:
            print(e)
            continue

# Pressure
for var in [
    "Upper_scale",
    "Lower_scale",
    "Height",
    "Attached_T",
    "Reduced_to_32F",
]:
    xidx += 1
    for day in range(1, 32):
        try:
            dv = page["Days"][day - 1]["Day"]
            value = page["Days"][day - 1]["Pressure"][var]
            if str(value) == "999":
                continue
            ax_digitised.text(
                xidx,
                dv,
                value,
                ha="center",
                va="center",
                fontsize=12,
                color="black",
            )
        except Exception as e:
            print(e)
            continue

# Wind
for var in ["Direction", "Force"]:
    xidx += 1
    for day in range(1, 32):
        try:
            dv = page["Days"][day - 1]["Day"]
            value = page["Days"][day - 1]["Wind"][var]
            if str(value) == "999":
                continue
            ax_digitised.text(
                xidx,
                dv,
                value,
                ha="center",
                va="center",
                fontsize=12,
                color="black",
            )
        except Exception as e:
            print(e)
            continue

# Weather
for var in ["Cloud", "Rain"]:
    xidx += 1
    for day in range(1, 32):
        try:
            dv = page["Days"][day - 1]["Day"]
            value = page["Days"][day - 1]["Weather"][var]
            if str(value) == "999":
                continue
            ax_digitised.text(
                xidx,
                dv,
                value,
                ha="center",
                va="center",
                fontsize=12,
                color="black",
            )
        except Exception as e:
            print(e)
            continue

# # Totals along the bottom
# ax_totals = fig.add_axes([0.52, 0.09, 0.47, 0.03])
# ax_totals.set_xlim(0.5, 12.5)
# ax_totals.set_ylim(0, 1)
# ax_totals.set_xticks([])
# ax_totals.set_yticks([])

# for i, total in enumerate(totals["Totals"]):
#     ax_totals.text(
#         i + 1,
#         0.5,
#         total,
#         ha="center",
#         va="center",
#         fontsize=12,
#         color="black",
#     )

# Render
fig.savefig(
    "result.webp",
)
