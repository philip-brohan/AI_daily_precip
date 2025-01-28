#!/bin/bash

# Stop imagemagick from using all the memory and crashing vdi.
export MAGICK_MAP_LIMIT=2GB
export MAGICK_MEMORY_LIMIT=2GB

magick -density 300 ./pdfs/Devon_1941-1950_RainNos_1651-1689.pdf jpgs_300dpi/Devon_1941-1950_RainNos_1651-1689.jpg
