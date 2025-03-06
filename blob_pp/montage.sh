#!/bin/bash

# Make a montage of infilling results for all the images in tha gallery

montage /data/scratch/philip.brohan/gemini/gallery/blob_array/*/xy_spectrum_plots.png -tile 5x3 -geometry +10+10 montage.jpg

