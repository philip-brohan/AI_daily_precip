#!/usr/bin/env python3

# Get all required data from the page
# This version does a sample from the 10-year monthlies

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


# Specify a structure for the station metadata
class MetaData(typing.TypedDict):
    Year: int
    StationNumber: int
    Location: str
    County: str
    River_basin: str
    Type_of_gauge: str
    Observer: str


# Specify a structure for the daily observations
class Monthly(typing.TypedDict):
    Month: str
    rainfall: str


class Annual(typing.TypedDict):
    Year: int
    rainfall: list[Monthly]


class Decadal(typing.TypedDict):
    rainfall: list[Annual]


class Totals(typing.TypedDict):
    Totals: list[str]


# Load the sample image
img = PIL.Image.open("../../images/monthlies/TYRain_1941-1950_25_pt1-10.jpg")

# Pick an AI to use - this one is the latest as of 2025-01-29
model = genai.GenerativeModel("gemini-2.0-flash-exp")

# Get metadata from the image
result = model.generate_content(
    [
        img,
        "\n\n",
        "List the station metadata",
    ],
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json", response_schema=MetaData
    ),
)
# Structured data as JSON
with open("metadata.json", "w") as file:
    file.write(result.text)
with open("metadata.txt", "w") as file:
    file.write(str(result))

# Get the Monthly observations from the image
result = model.generate_content(
    [img, "\n\n", "List the monthly observations. "],
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json", response_schema=Decadal
    ),
)
with open("monthly.json", "w") as file:
    file.write(result.text)
with open("monthly.txt", "w") as file:
    file.write(str(result))


# Get the Annually totals
result = model.generate_content(
    [img, "\n\n", "List the abnnualy totals for each year."],
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json", response_schema=Totals
    ),
)
with open("totals.json", "w") as file:
    file.write(result.text)
with open("totals.txt", "w") as file:
    file.write(str(result))
