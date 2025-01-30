AI Data Rescue: Daily Precipitation
===================================

Can we use Artificial Intelligence (AI) to rapidly transcribe vital climate data from paper archives? (SPOILER: Yes).

Datasets of historical weather observations are vital to our understanding of climate change and variability, and improving those datasets means transcribing millions of observations - converting paper records into a digital form. Doing such transcription manually is `expensive and slow <http://brohan.org/transcription_methods_review/>`_, and we have a backlog of millions of pages of potentially valuable records which have never been transcribed. We would dearly like a cheap, fast, software tool for extracting weather observations from (photographs of) archived paper documents. Can modern multimodal large language models be that tool?

I'm going to test using the `Gemini 2.0 Flash Experimental <https://deepmind.google/technologies/gemini/flash/>`_ multimodal large language model (latest model from Google at the time of writing) to transcribe daily precipitation data from the `UK Daily Rainfall Reports <https://https://digital.nmla.metoffice.gov.uk/index.php?name=SO_9903efdf-7f99-4cae-a723-8b3f426eea20>`_ .

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





.. toctree::
   :maxdepth: 1

   How to reproduce or extend this work <how_to>
   Authors and acknowledgements <credits>

This document is distributed under the terms of the `Open Government Licence <https://www.nationalarchives.gov.uk/doc/open-government-licence/version/2/>`_. Source code included is distributed under the terms of the `BSD licence <https://opensource.org/licenses/BSD-2-Clause>`_.

