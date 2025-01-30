#!/usr/bin/env python

# Plot the data digitised by Gemini from a daily rainfall image
# With the source locations

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
metadata = json.load(open("locations.json"))

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


def plot_bbox(ax, bbox, color="red"):
    ax.add_line(
        Line2D(
            [
                1.0 * img.size[0] * y / 1000
                for y in [bbox[1], bbox[1], bbox[3], bbox[3], bbox[1]]
            ],
            [
                1.0 * img.size[1] * x / 1000
                for x in [bbox[0], bbox[2], bbox[2], bbox[0], bbox[0]]
            ],
            linewidth=1,
            color=color,
            zorder=20,
        ),
    )


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
plot_bbox(ax_original, metadata["Year_bounding_box"])
ax_metadata.text(
    0.05,
    0.7,
    "Station Number: %d" % metadata["StationNumber"],
    fontsize=12,
    color="black",
)
plot_bbox(ax_original, metadata["StationNumber_bounding_box"])
ax_metadata.text(
    0.05,
    0.6,
    "Location: %s" % metadata["Location"],
    fontsize=12,
    color="black",
)
plot_bbox(ax_original, metadata["Location_bounding_box"])
ax_metadata.text(
    0.05,
    0.5,
    "County: %s" % metadata["County"],
    fontsize=12,
    color="black",
)
plot_bbox(ax_original, metadata["County_bounding_box"])
ax_metadata.text(
    0.05,
    0.4,
    "Height above sea-level: %d" % metadata["Sea_level_height"],
    fontsize=12,
    color="black",
)
plot_bbox(ax_original, metadata["Sea_level_height_bounding_box"])
ax_metadata.text(
    0.05,
    0.3,
    "Gauge diameter: %d" % metadata["Gauge_diameter"],
    fontsize=12,
    color="black",
)
plot_bbox(ax_original, metadata["Gauge_diameter_bounding_box"])
ax_metadata.text(
    0.05,
    0.2,
    "Gauge height: %d ft %d in"
    % (metadata["Gauge_height_feet"], metadata["Gauge_height_inches"]),
    fontsize=12,
    color="black",
)
plot_bbox(ax_original, metadata["Gauge_height_feet_bounding_box"])
plot_bbox(ax_original, metadata["Gauge_height_inches_bounding_box"])


# Render
fig.savefig(
    "result.webp",
)
