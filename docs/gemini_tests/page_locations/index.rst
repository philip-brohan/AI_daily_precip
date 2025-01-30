Page locations
==============

The Gemini documentation describes `a way to get page bounding boxes for items on the page <https://ai.google.dev/gemini-api/docs/vision?lang=python#bbox>`_. This is not a vital feature, but it is useful for debugging and for understanding how Gemini is interpreting the page.

So we modify :doc:`the existing code <../structured_output/index>` to request a bounding box for each item.

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
