#!/bin/bash

# Make a montage of infilling results for all the images in the gallery

montage /data/scratch/philip.brohan/gemini/gallery/blob_array/*/marked.jpg -tile 5x3 -geometry +10+10 montage.jpg

