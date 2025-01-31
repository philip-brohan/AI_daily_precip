Basic use of the Gemini API
===========================

To use the `Gemini API <https://ai.google.dev/gemini-api/docs/>`_ first set up :doc:`the code environment <../../how_to>`, then `register for an API key <https://ai.google.dev/gemini-api/docs/quickstart>`_ and save the key in a file called ``.gemini_api`` in your home directory:

Then the API is simple to use: authenticate, load :doc:`the image <../../test_image>`, and make a query with the image and a question in natural language. Essentially we just ask 'In this image, what is the rainfall for January 5th'.

.. literalinclude :: ../../../gemini_tests/basic_api.py

The output is a data structure including the answer to the question.

.. literalinclude :: ../../../gemini_tests/result.txt

We asked "What is this document?" and got the response "This is a **British Rainfall Organization register of rainfall** for the year 1947, specifically for the station located at **Badworthy Cottage, S. Brent** in **Devon**. It records daily rainfall measurements in inches."

This answer is correct in all respects (compare :doc:`the image <../../test_image>`), and shows the power of modern AIs. Gemini has read *and understood* the document, so we can transcribe data just by asking for what we want to know.
This is vanilla Gemini - no specialist fine-tuneing, and it's never seen this document before. This is basically magic - how far can we go with it?

The output also tells us what the query cost: 312 tokens. At the time of writing, tokens are `approximately $0.30 / 1 million tokens <https://ai.google.dev/pricing>`_, so this query cost about $0.0001 (one hundredth of one U.S. cent). 
