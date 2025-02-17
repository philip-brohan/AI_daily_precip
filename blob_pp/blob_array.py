#!/usr/bin/env python

# The LLM is confused by the empty grid-cells in the rainfall data table.
#  This script finds the empty cells and adds a mark to them.

import os
import glob
import numpy as np
import cv2

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--img", help="Image number", type=int, required=False, default=3)
parser.add_argument("--gallery", help="Use RJM's gallery images", action="store_true")
parser.add_argument("--debug", help="Output intermediate images", action="store_true")
parser.add_argument(
    "--threshold",
    help="Value boundary for black:white distinction (0-255)",
    type=int,
    required=False,
    default=180,
)

args = parser.parse_args()

opdir = "."
if args.gallery:
    opdir = "%s/gemini/gallery/blob_array/%04d" % (os.getenv("SCRATCH"), args.img)
    if not os.path.exists(opdir):
        os.makedirs(opdir)


# Make greyscale image from the original
def make_greyscale_image(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img_gray


# Make binary image from greyscale
def make_binary_image(img_gray, threshold_x, invert=True):
    (thresh, img_bin) = cv2.threshold(img_gray, threshold_x, 255, cv2.THRESH_BINARY)
    if not invert:
        return img_bin
    return cv2.bitwise_not(img_bin)


# Smooth inage into blobs
def smooth_image(img):
    scale = img.shape[1] / 4024

    def scale_i(x, odd=True):
        result = int(x * scale)
        if odd and result % 2 == 0:
            result += 1
        return result

    # Convert to greyscale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if args.debug:
        cv2.imwrite("%s/greyed_out.jpg" % opdir, img_gray)
    # Make binary image
    img_bin = make_binary_image(img_gray, args.threshold)
    if args.debug:
        cv2.imwrite("%s/binary.jpg" % opdir, img_bin)
    # Blur  - skip?
    img_blur = cv2.GaussianBlur(img_bin, (scale_i(19), scale_i(19)), scale_i(100))
    if args.debug:
        cv2.imwrite("%s/blur.jpg" % opdir, img_blur)
    img_blur = cv2.GaussianBlur(img_blur, (scale_i(19), scale_i(19)), scale_i(100))
    if args.debug:
        cv2.imwrite("%s/blur2.jpg" % opdir, img_blur)
    # Erode and dilate to get blobs
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (scale_i(10), scale_i(10)))
    eroded = cv2.erode(img_blur, kernel, iterations=4)
    if args.debug:
        cv2.imwrite("%s/eroded.jpg" % opdir, eroded)
    dilated = cv2.dilate(eroded, kernel, iterations=4)
    if args.debug:
        cv2.imwrite("%s/dilated.jpg" % opdir, dilated)
    blobbed = make_binary_image(dilated, 20, invert=False)
    if args.debug:
        cv2.imwrite("%s/blobbed.jpg" % opdir, blobbed)
    # Fourier transform
    dft = cv2.dft(np.float32(blobbed), flags=cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)
    magnitude_spectrum = 10 * np.log(
        cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1])
    )
    if args.debug:
        cv2.imwrite("%s/magnitude_spectrum.jpg" % opdir, magnitude_spectrum)


if args.gallery:
    image_files = sorted(glob.glob(os.path.join("../images/RJM_gallery", "*.jpg")))
    img = cv2.imread(image_files[args.img - 1])
else:
    img = cv2.imread(
        "../images/jpgs_300dpi/Devon_1941-1950_RainNos_1651-1689-%d.jpg" % args.img
    )
# Copy of the original - for plotting
# cv2.imwrite("%s/original.jpg" % opdir, img)
smooth_image(img)
