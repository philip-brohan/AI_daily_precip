#!/usr/bin/env python3

# Basic test of the Gemini API - get one observation.

import os
import PIL.Image
import google.generativeai as genai

# You will need an API key get it from https://ai.google.dev/gemini-api/docs/api-key

# I keep my API key in the .gemini_api file in my home directory.
with open("%s/.gemini_api" % os.getenv("HOME"), "r") as file:
    api_key = file.read().strip()

# Default protocol is 'GRPC' - but that is blocked by the Office firewall.
#  Use 'REST' instead.
genai.configure(api_key=api_key, transport="rest")

# Load the sample image
img = PIL.Image.open(
    "../../images/jpgs_300dpi/Devon_1941-1950_RainNos_1651-1689-293.jpg"
)

# Pick an AI to use - this one is the latest as of 2025-01-29
model = genai.GenerativeModel("gemini-2.0-flash-exp")

# Ask a question about the image
result = model.generate_content([img, "\n\n", "What was the rainfall on January 5th?"])
with open("result.txt", "w") as file:
    file.write(str(result))

# print(result)
