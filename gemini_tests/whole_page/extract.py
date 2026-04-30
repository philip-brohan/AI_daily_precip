#!/usr/bin/env python3

# Get all required data from the page
# Supports --scale argument to test effect of image resolution on results

import os
import argparse
import PIL.Image
import google.generativeai as genai
import typing_extensions as typing

parser = argparse.ArgumentParser()
parser.add_argument(
    "--scale",
    help="Scale factor for image resolution (1.0 = full 300dpi, 0.5 = half, etc.)",
    type=float,
    required=False,
    default=1.0,
)
args = parser.parse_args()

outdir = "res_%.2f" % args.scale
os.makedirs(outdir, exist_ok=True)

# You will need an API key get it from https://ai.google.dev/gemini-api/docs/api-key

# I keep my API key in the .gemini_api file in my home directory.
with open("%s/.gemini_keys/data_rescue" % os.getenv("HOME"), "r") as file:
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


# Load the sample image and resize to requested scale
img = PIL.Image.open(
    "../../images/jpgs_300dpi/Devon_1941-1950_RainNos_1651-1689-293.jpg"
)
if args.scale != 1.0:
    new_size = (int(img.width * args.scale), int(img.height * args.scale))
    img = img.resize(new_size, PIL.Image.LANCZOS)
print("Image size: %dx%d (scale=%.2f)" % (img.width, img.height, args.scale))

# Pick an AI to use - this one is the latest as of 2025-01-29
# List available models
# models = genai.list_models()
# for model in models:
#     print(model.name)

# model = genai.GenerativeModel("gemini-3-pro-preview")
model = genai.GenerativeModel("gemini-flash-latest")
# model = genai.GenerativeModel("gemini-2.5-pro")

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
with open("%s/metadata.json" % outdir, "w") as file:
    file.write(result.text)
with open("%s/metadata.txt" % outdir, "w") as file:
    file.write(str(result))

# Get the daily observations from the image
# In two batches because of output size limits
result = model.generate_content(
    [
        img,
        "\n\n",
        "List the daily observations  for months January to December. "
        + "Be careful of missing data. Several days have missing data and "
        + "These days will have an entry that is blank or has a dash '-'. "
        + "Return the character '-' for missing data.",
    ],
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json", response_schema=Annual
    ),
)
with open("%s/daily1.json" % outdir, "w") as file:
    file.write(result.text)
with open("%s/daily1.txt" % outdir, "w") as file:
    file.write(str(result))

# result = model.generate_content(
#     [
#         img,
#         "\n\n",
#         "List the daily observations for months July to December. "
#         + "Be careful of missing data. Several days have missing data and "
#         + "These days will have an entry that is blank or has a dash '-'. "
#         + "Return the character '-' for missing data.",
#     ],
#     generation_config=genai.GenerationConfig(
#         response_mime_type="application/json", response_schema=Annual
#     ),
# )
# with open("daily2.json", "w") as file:
#     file.write(result.text)
# with open("daily2.txt", "w") as file:
#     file.write(str(result))

# Get the Monthly totals
result = model.generate_content(
    [img, "\n\n", "List the monthly totals for each month."],
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json", response_schema=Totals
    ),
)
with open("%s/totals.json" % outdir, "w") as file:
    file.write(result.text)
with open("%s/totals.txt" % outdir, "w") as file:
    file.write(str(result))
