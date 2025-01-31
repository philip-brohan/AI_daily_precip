Full page extraction
====================

Enough tests - let's try and extract all the data from a page - the station metadata, the daily rainfall observations, and the monthly totals.

The code is a straightforward extension - adding required structures for each data section. One complication is that extracting everything at once runs into Gemini's limit on maximum output. So I'm doing it in four steps - metadata, daily obs Jan-Jun, daily obs Jul-Dec, and monthly totals. 

.. literalinclude :: ../../../gemini_tests/whole_page/extract.py

Producing four JSON output files:

.. literalinclude :: ../../../gemini_tests/whole_page/metadata.json
.. literalinclude :: ../../../gemini_tests/whole_page/daily1.json
.. literalinclude :: ../../../gemini_tests/whole_page/daily2.json
.. literalinclude :: ../../../gemini_tests/whole_page/totals.json

And does it work? Well, almost. Metadata is correct, monthly totals are correct, it's getting the right numbers for daily obs (with a few missing decimal points - but that's easy to fix). But the daily obs are not all associated with the correct dates - it's a bit confused by missing data.

.. image:: ../../../gemini_tests/whole_page/result.webp
   :alt: Image showing bounding boxes for extracted data
   :align: center

The full data extraction costs a bit less than 10,000 tokens. About 1/4 of a U.S. cent.

.. toctree::
    :maxdepth: 1
    
    Program to plot the whole page diagnostic <plot_digitised>
