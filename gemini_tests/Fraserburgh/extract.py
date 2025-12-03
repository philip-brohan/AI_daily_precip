#!/usr/bin/env python3

# Get all required data from the page

import os
import PIL.Image
import google.generativeai as genai
import typing_extensions as typing
import json

# You will need an API key. Get it from https://ai.google.dev/gemini-api/docs/api-key

# I keep my API key in the .gemini_api file in my home directory.
with open("%s/.gemini_api" % os.getenv("HOME"), "r") as file:
    api_key = file.read().strip()

# Default protocol is 'GRPC' - but that is blocked by the Office firewall.
#  Use 'REST' instead.
genai.configure(api_key=api_key, transport="rest")


# Specify a structure for the station metadata
class MetaData(typing.TypedDict):
    Year: int
    Month: str
    Location: str
    Hour: int


class Thermometer(typing.TypedDict):
    Dry_Bulb: int
    Wet_Bulb: int
    Maximum: int
    Minimum: int
    Maximium_after_resetting: int
    Minimum_after_resetting: int
    Humidity: int
    Dew_Point: int
    Tension: int


class Barometer(typing.TypedDict):
    Upper_scale: int
    Lower_scale: int
    Height: int
    Attached_T: int
    Reduced_to_32F: int


class Wind(typing.TypedDict):
    Direction: str
    Force: str


class Weather(typing.TypedDict):
    Cloud: str
    Rain: float


# Specify a structure for the daily observations
class Daily(typing.TypedDict):
    Day: int
    Temperature: Thermometer
    Pressure: Barometer
    Wind: Wind
    Weather: Weather


class Mean(typing.TypedDict):
    Temperature: Thermometer
    Pressure: Barometer
    Wind: Wind
    Weather: Weather


class Page(typing.TypedDict):
    Days: list[Daily]
    Mean: Mean
    Metadata: MetaData


# Load the sample image
img = PIL.Image.open("../../images/SAWS/Fraserburg/Fraseburg_1892_Mar.jpg")

# Pick an AI to use - this one is the latest as of 2025-01-29
# List available models
# models = genai.list_models()
# for model in models:
#     print(model.name)

model = genai.GenerativeModel("gemini-3-pro-preview")
# model = genai.GenerativeModel("gemini-flash-latest")


# Get the daily observations from the image
result = model.generate_content(
    [
        img,
        "\n\n",
        "This page is a weather log for one month from a single station. "
        + "List the daily weather observations for each day"
        + "Each day should have entries for Temperature, Pressure, Wind and Weather. "
        + "Be careful of missing data. Several days have missing data and "
        + "These days will have an entry that is blank or has a dash '-'. "
        + "Return 999 for missing data.",
    ],
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json", response_schema=Page
    ),
)
try:
    obj = json.loads(result.text)
    with open("page.json", "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
except Exception:
    with open("page.json", "w", encoding="utf-8") as f:
        f.write(result.text)

    file.write(result.text)
with open("page.txt", "w") as file:
    file.write(str(result))
