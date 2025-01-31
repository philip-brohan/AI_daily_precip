Structured output
=================

It's great to be able to ask questions in natural language, but we don't want answers in natural language - we don't want answers like '1.03 inches of rain fell on January 5th', or 'The rainfall on January 5th was 1.03 inches', because we then have to parse those answers to use them in further processing. We just want the value - 1.03. We want specific, structured output.

A great virtue of Gemini is that it supports this, the API allows you to `specify the output structure you want <https://ai.google.dev/gemini-api/docs/structured-output?lang=python>`_.

So we modify the code to define a data structure containing the exact output we want, and then we ask Gemini to populate that data structure from the image. We can then output the data structure as a JSON file, ready to use directly in our data processing pipeline.

.. literalinclude :: ../../../gemini_tests/structured_output/metadata.py

This script extracts the station metadata, and stores it as JSON

.. literalinclude :: ../../../gemini_tests/structured_output/metadata.json

The data are all correct (compare :doc:`the image <../../test_image>`), and are ready to be used in further processing.



