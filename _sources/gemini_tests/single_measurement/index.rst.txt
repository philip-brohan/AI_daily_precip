Extracting a single measurement
===============================

We've shown that Gemini can read and understand a document, but can it extract data from it? Let's start with a simple query: "What is the rainfall for January 5th?".

The code is simple: we load the image, ask the question, and print the answer.

.. literalinclude :: ../../../gemini_tests/single_measurement/single_ob.py

I chose January 5th because the page is very messy in that region, and I wanted to see how well Gemini could extract data from a difficult area. It works perfectly.

.. literalinclude :: ../../../gemini_tests/single_measurement/result.txt

The answer is correct: (Compare a section cropped out of the image - below).

.. image:: ./image_subset.jpg
   :alt: Subset of image showing successfully extracted data
   :align: center

