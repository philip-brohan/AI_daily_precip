#!/bin/bash

# Run the infiller on all the gallery images

# Gallery images from 
# https://github.com/rjmeats/DailyRainfall/blob/master/Notes/Daily_Rainfall_Form_Gallery.md

for img in {1..90}; do ./fill_empty_boxes.py --img=$img --gallery --debug; done

