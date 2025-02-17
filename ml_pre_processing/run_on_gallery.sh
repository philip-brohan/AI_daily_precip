#!/bin/bash

# Run the infiller on all the gallery images

for img in {1..90}; do ./ml_pp.py --img=$img --gallery --debug; done

