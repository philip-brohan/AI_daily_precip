Pre-processing
==============

Missing data is a problem. We'd get much more accurate data extractions if originally, when filling out the forms, we'd put in zero values explicitly, and a nominal value (say `99.9`) for missing data. Then the forms would always have a complete grid of entries. Can we deal with this after the fact - by pre-processing the images to add numbers in the missing spaces?

.. table:: An example showing missing data infilling: Almost all the missing cells actually have 0.0mm precipitation. But I don't want to infill with 0, because it might occur as a genuine entry somewhere. So I'm using '99.9' as a missing data value. (Nowhere in the UK is going to see that much actual precipitation in a day - I hope.)
   :widths: 50 50

   +-----------------------------------------------------------------------+-----------------------------------------------------------------------+
   | .. image:: ../../pre-processing/original.jpg                          | .. image:: ../../pre-processing/missing_infilled.jpg                  |
   |    :alt: Original version of an image with missing data               |    :alt: Same image after missing data has been infilled              |
   |    :width: 100%                                                       |    :width: 100%                                                       |
   +-----------------------------------------------------------------------+-----------------------------------------------------------------------+

This works very well. Running exactly the same :doc:`whole-page data extraction <../gemini_tests/whole_page/index>` process as before, but on the infilled images, we get excellent results. (I've filtered the '99.9's out of the results.)

.. image:: ../../pre-processing/result.webp
   :alt: Data extraction results from the infilled images
   :align: center

This is great, but the obvious catch is that the pre-processing is not easy to do. Here I've used the `OpenCV <https://opencv.org/>`_ library to find the empty boxes and fill them in. The process is to find the horizontal and vertical lines that make up the table, then find empty cells between those lines, and fill those in. This is too fussy a process to work generally - it depends precisely on the image colour, contrast and format - so it's not a general solution. But this probably could be used to produce a few hundred successful page digitisations, which could then be used to fine-tune the LLM (to cope better with missing data) - so we might be able to bootstrap our way to a more general solution.

.. literalinclude :: ../../pre-processing/fill_empty_boxes.py
