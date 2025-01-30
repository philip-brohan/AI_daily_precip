#!/usr/bin/env python3

# Basic test of the Gemini API - get the station metadata as
#  structured output.

import os
import PIL.Image
import google.generativeai as genai
import typing_extensions as typing

# You will need an API key get it from https://ai.google.dev/gemini-api/docs/api-key

# I keep my API key in the .gemini_api file in my home directory.
with open("%s/.gemini_api" % os.getenv("HOME"), "r") as file:
    api_key = file.read().strip()

# Default protocol is 'GRPC' - but that is blocked by the Office firewall.
#  Use 'REST' instead.
genai.configure(api_key=api_key, transport="rest")


# Specify a structure for the desired output
class MetaData(typing.TypedDict):
    Year: int
    Year_bounding_box: list[int]
    StationNumber: int
    StationNumber_bounding_box: list[int]
    Location: str
    Location_bounding_box: list[int]
    County: str
    County_bounding_box: list[int]
    Sea_level_height: int
    Sea_level_height_bounding_box: list[int]
    Gauge_diameter: int
    Gauge_diameter_bounding_box: list[int]
    Gauge_height_feet: int
    Gauge_height_feet_bounding_box: list[int]
    Gauge_height_inches: int
    Gauge_height_inches_bounding_box: list[int]


# Load the sample image
img = PIL.Image.open(
    "../../images/jpgs_300dpi/Devon_1941-1950_RainNos_1651-1689-293.jpg"
)

# Pick an AI to use - this one is the latest as of 2025-01-29
model = genai.GenerativeModel("gemini-2.0-flash-exp")

# Ask a question about the image
result = model.generate_content(
    [
        img,
        "\n\n",
        "List the station metadata. Also give the bounding box of each item in [xmin,ymin,xmax,ymax] format.",
    ],
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json", response_schema=MetaData
    ),
)
# Structured data as JSON
with open("locations.json", "w") as file:
    file.write(result.text)
with open("rest.txt", "w") as file:
    file.write(str(result))
