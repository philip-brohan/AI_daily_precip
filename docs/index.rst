AI Data Rescue: Daily Precipitation
===================================

Summary
-------
Can we use Artificial Intelligence (AI) to rapidly transcribe vital climate data from paper archives? 

Yes we can. The `Gemini 2.0 Flash Experimental <https://deepmind.google/technologies/gemini/flash/>`_ multimodal large language model (latest model from Google at the time of writing) can extract monthly precipitation data from the `UK Ten Year Rainfall Reports <https://digital.nmla.metoffice.gov.uk/index.php?name=SO_d383374a-91c3-4a7b-ba96-41b81cfb9d67>`_ with near-perfect accuracy.

.. figure:: ../gemini_tests/10-year-monthlies/result.webp
   :alt: Image showing extracted data
   :align: center
   
   A sample page from the UK Ten Year Rainfall Reports, with the extracted data shown on the right. (:doc:`Details <../gemini_tests/10-year-monthlies/index>`)

Details
-------

Datasets of historical weather observations are vital to our understanding of climate change and variability, and improving those datasets means transcribing millions of observations - converting paper records into a digital form. Doing such transcription manually is `expensive and slow <http://brohan.org/transcription_methods_review/>`_, and we have a backlog of millions of pages of potentially valuable records which have never been transcribed. We would dearly like a cheap, fast, software tool for extracting weather observations from (photographs of) archived paper documents. Can modern multimodal large language models be that tool?

I'm going to test using the `Gemini 2.0 Flash Experimental <https://deepmind.google/technologies/gemini/flash/>`_ multimodal large language model (latest model from Google at the time of writing) to transcribe daily precipitation data from the `UK Daily Rainfall Reports <https://digital.nmla.metoffice.gov.uk/index.php?name=SO_9903efdf-7f99-4cae-a723-8b3f426eea20>`_ .

Here is a sample Daily Rainfall page:

.. image:: ../images/jpgs_300dpi/Devon_1941-1950_RainNos_1651-1689-293.jpg
   :width: 400px
   :alt: Example page from the UK Daily Rainfall reports
   :align: center

I will extract information from this page using the `Gemini API <https://ai.google.dev/gemini-api/docs/>`_- going through the process in steps:

.. toctree::
   :maxdepth: 1

   Basic API function <gemini_tests/basic_api/index>
   Extracting a single data point <gemini_tests/single_measurement/index>
   Specifying an output structure <gemini_tests/structured_output/index>
   Finding data locations on the page <gemini_tests/page_locations/index>
   Extracting all data from a page <gemini_tests/whole_page/index>

Gemini is extremely capable for this use case, and impressively easy to use. It'll take a little bit more work to get good results for the daily rainfall cases with their variable missing data pattern. but it looks as if it's ready to go as-is for simpler cases with no missing data. Ive tested this on a different example - the 10-year monthly totals for a station.

.. toctree::
   :maxdepth: 1

   10-year monthlies <gemini_tests/10-year-monthlies/index>

In this simpler case it works pretty-much perfectly.

There are various ways we could improve the process, particularly to cope better with missing data:

.. toctree::
   :maxdepth: 1

   Pre-processing <pre-processing/index>


Small print 
-----------

.. toctree::
   :maxdepth: 1

   How to reproduce or extend this work <how_to>
   Authors and acknowledgements <credits>

This document is distributed under the terms of the `Open Government Licence <https://www.nationalarchives.gov.uk/doc/open-government-licence/version/2/>`_. Source code included is distributed under the terms of the `BSD licence <https://opensource.org/licenses/BSD-2-Clause>`_.

