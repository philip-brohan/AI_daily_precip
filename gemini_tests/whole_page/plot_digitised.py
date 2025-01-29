#!/usr/bin/env python

# Plot the data digitised by Gemini from a daily rainfall image

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
img = PIL.Image.open(
    "../../images/jpgs_300dpi/Devon_1941-1950_RainNos_1651-1689-293.jpg"
)

# load the digitised data
metadata = json.load(open("metadata.json"))
dd1 = json.load(open("daily1.json"))
dd2 = json.load(open("daily2.json"))
totals = json.load(open("totals.json"))

# Create the figure
fig = Figure(
    figsize=(13, 10),  # Width, Height (inches)
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
ax_original = fig.add_axes([0.02, 0.02, 0.47, 0.96])
ax_original.set_axis_off()
imgplot = ax_original.imshow(img, zorder=10)

# Metadata top right
ax_metadata = fig.add_axes([0.51, 0.8, 0.47, 0.15])
ax_metadata.set_xlim(0, 1)
ax_metadata.set_ylim(0, 1)
ax_metadata.set_xticks([])
ax_metadata.set_yticks([])
ax_metadata.text(
    0.05,
    0.8,
    "Year: %d" % metadata["Year"],
    fontsize=12,
    color="black",
)
ax_metadata.text(
    0.05,
    0.7,
    "Station Number: %d" % metadata["StationNumber"],
    fontsize=12,
    color="black",
)
ax_metadata.text(
    0.05,
    0.6,
    "Location: %s" % metadata["Location"],
    fontsize=12,
    color="black",
)
ax_metadata.text(
    0.05,
    0.5,
    "County: %s" % metadata["County"],
    fontsize=12,
    color="black",
)
ax_metadata.text(
    0.05,
    0.4,
    "Height above sea-level: %d" % metadata["Sea_level_height"],
    fontsize=12,
    color="black",
)
ax_metadata.text(
    0.05,
    0.3,
    "Gauge diameter: %d" % metadata["Gauge_diameter"],
    fontsize=12,
    color="black",
)
ax_metadata.text(
    0.05,
    0.2,
    "Gauge height: %d ft %d in"
    % (metadata["Gauge_height_feet"], metadata["Gauge_height_inches"]),
    fontsize=12,
    color="black",
)

# Digitised numbers on the right
ax_digitised = fig.add_axes([0.51, 0.13, 0.47, 0.63])
ax_digitised.set_xlim(0.5, 12.5)
ax_digitised.set_xticks(range(1, 13))
ax_digitised.set_xticklabels(
    ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
)
ax_digitised.xaxis.set_ticks_position("top")
ax_digitised.xaxis.set_label_position("top")
ax_digitised.set_ylim(0, 32)
ax_digitised.set_yticks(range(1, 32))
ax_digitised.set_yticklabels(range(1, 32))
ax_digitised.invert_yaxis()
ax_digitised.set_aspect("auto")

monthNames = (
    "Jan",
    "Feb",
    "Mar",
    "April",
    "May",
    "June",
    "July",
    "Aug",
    "Sept",
    "Oct",
    "Nov",
    "Dec",
)
monthNumbers = {month: i + 1 for i, month in enumerate(monthNames)}
for month in dd1["Month"] + dd2["Month"]:
    for day in month["rainfall"]:
        ax_digitised.text(
            monthNumbers[month["Month"]],
            day["Day"],
            day["rainfall"],
            ha="center",
            va="center",
            fontsize=12,
            color="black",
        )


# Totals along the bottom
ax_totals = fig.add_axes([0.51, 0.09, 0.47, 0.03])
ax_totals.set_xlim(0.5, 12.5)
ax_totals.set_ylim(0, 1)
ax_totals.set_xticks([])
ax_totals.set_yticks([])

for i, total in enumerate(totals["Totals"]):
    ax_totals.text(
        i + 1,
        0.5,
        total,
        ha="center",
        va="center",
        fontsize=12,
        color="black",
    )

# Render
fig.savefig(
    "result.webp",
)
