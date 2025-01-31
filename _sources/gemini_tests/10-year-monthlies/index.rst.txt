Full page extraction - 10-year monthlies
========================================

The :doc:`test on the daily-rainfall page <../10-year-monthlies/index>` suggested that Gemini worked almost perfectly, but struggled with the missing entries in a table. To check this, I'm going to try a test with a page that has no missing data - the 10-year monthly totals for a station. (:doc:`Image <test_image>`)

The code is almost the same - I've just changed the metadata names to match the image, and tweaked the data structure for monthly totals rather than daily. 

.. literalinclude :: ../../../gemini_tests/10-year-monthlies/extract.py

Producing three JSON output files:

.. literalinclude :: ../../../gemini_tests/10-year-monthlies/metadata.json
.. literalinclude :: ../../../gemini_tests/10-year-monthlies/monthly.json
.. literalinclude :: ../../../gemini_tests/10-year-monthlies/totals.json

And this works pretty-much perfectly. 

.. image:: ../../../gemini_tests/10-year-monthlies/result.webp
   :alt: Image showing extracted data
   :align: center


.. toctree::
    :maxdepth: 1
    
    Program to plot the extracted data from the Ten Year Rainfall image <plot_digitised>
