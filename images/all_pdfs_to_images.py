#!/usr/bin/env python

# Make individual page jpgs from the Archive pdfs

import os

base_dir = "%s/Daily_Rainfall_UK" % os.getenv("SCRATCH")
imgs_dir = "%s/jpgs_300dpi/" % base_dir
if not os.path.exists(imgs_dir):
    os.makedirs(imgs_dir)

# Walk the directory tree down from the base, collecting pdf filenames
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith(".pdf"):
            pdf_file = os.path.join(root, file)
            # Get the base filename
            base_file = os.path.basename(pdf_file)
            base_name = os.path.splitext(base_file)[0]
            # Make the output directory
            out_dir = "%s/%s" % (imgs_dir, base_name)
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)
            # Make the output filenames
            out_file = "%s/%s.jpg" % (out_dir, base_name)
            # Convert the pdf to jpg
            print("magick -density 300 %s %s" % (pdf_file, out_file))
