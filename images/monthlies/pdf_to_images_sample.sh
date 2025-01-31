#!/bin/bash

# Stop imagemagick from using all the memory and crashing vdi.
export MAGICK_MAP_LIMIT=2GB
export MAGICK_MEMORY_LIMIT=2GB

magick -density 300 $SCRATCH/monthly_rainfall/TYRain_1941-1950_25_pt1.pdf $SCRATCH/monthly_rainfall/jpgs_300dpi/TYRain_1941-1950_25_pt1.jpg
