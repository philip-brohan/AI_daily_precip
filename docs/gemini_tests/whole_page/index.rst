Full page extraction
====================

Enough tests - let's try and extract all the data from a page - the station metadata, the daily rainfall observations, and the monthly totals.

The code is a straightforward extension adding required structures for each data section. One complication is that 

.. literalinclude :: ../../../gemini_tests/page_locations/locations.py

And bounding boxes are indeed added to the JSON output

.. literalinclude :: ../../../gemini_tests/page_locations/locations.json

Unfortunately it doesn't work - the locations are not correct. It sort-of-works, and it's not clear exactly what is going wrong, but at the moment this feature is not useable.

.. image:: ../../../gemini_tests/page_locations/result.webp
   :alt: Image showing bounding boxes for extracted data
   :align: center


.. toctree::
    :maxdepth: 1
    
    Program to plot the bounding box diagnostic <plot_digitised>
