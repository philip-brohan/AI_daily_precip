#!/usr/bin/env python3

# Get all required data from the page

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
    Sea_level_height: int
    Gauge_diameter: int
    Gauge_height_feet: int
    Gauge_height_inches: int


# Specify a structure for the daily observations
class Daily(typing.TypedDict):
    Day: int
    rainfall: str


class Monthly(typing.TypedDict):
    Month: str
    rainfall: list[Daily]


class Annual(typing.TypedDict):
    Month: list[Monthly]


class Totals(typing.TypedDict):
    Totals: list[str]


# Load the sample image
img = PIL.Image.open(
    "../../images/jpgs_300dpi/Devon_1941-1950_RainNos_1651-1689-293.jpg"
)

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

# Get the daily observations from the image
# In two batches because of output size limits
result = model.generate_content(
    [
        img,
        "\n\n",
        "List the daily observations  for months January to June. "
        + "Be careful of missing data. Several days have missing data and "
        + "These days will have an entry that is blank or has a dash '-'. "
        + "Return the character '-' for missing data.",
    ],
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json", response_schema=Annual
    ),
)
with open("daily1.json", "w") as file:
    file.write(result.text)
with open("daily1.txt", "w") as file:
    file.write(str(result))

result = model.generate_content(
    [
        img,
        "\n\n",
        "List the daily observations for months July to December. "
        + "Be careful of missing data. Several days have missing data and "
        + "These days will have an entry that is blank or has a dash '-'. "
        + "Return the character '-' for missing data.",
    ],
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json", response_schema=Annual
    ),
)
with open("daily2.json", "w") as file:
    file.write(result.text)
with open("daily2.txt", "w") as file:
    file.write(str(result))

# Get the Monthly totals
result = model.generate_content(
    [img, "\n\n", "List the monthly totals for each month."],
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json", response_schema=Totals
    ),
)
with open("totals.json", "w") as file:
    file.write(result.text)
with open("totals.txt", "w") as file:
    file.write(str(result))
