#!/usr/bin/env python

# The LLM is confused by the empty grid-cells in the rainfall data table.
#  This script finds the empty cells and adds a mark to them.

import os
import glob
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
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


# Cut out the centre of an image (for FFT output)
def extract_central_region(img, fraction=0.1):
    # Get the dimensions of the image
    height, width = img.shape[:2]

    # blank the centre lines of the image
    # centre = (img[(height // 2 - 5), :] + img[(height // 2 + 5), :]) / 2
    # img[(height // 2 - 5) : (height // 2 + 5), :] = centre
    # centre = (img[:, (width // 2 - 5)] + img[:, (width // 2 + 5)]) / 2
    # centre = np.tile(centre[:, np.newaxis], (1, 10))
    # img[:, (width // 2 - 5) : (width // 2 + 5)] = centre

    # Calculate the size of the central region
    central_height = int(height * fraction)
    central_width = int(width * fraction)

    # Calculate the starting and ending coordinates
    start_y = (height - central_height) // 2
    end_y = start_y + central_height
    start_x = (width - central_width) // 2
    end_x = start_x + central_width

    # Extract the central region
    central_region = img[start_y:end_y, start_x:end_x]

    return central_region


def periods_to_grid(row_period, col_period, scale_f=30):
    xsize = int(row_period * 12)
    ysize = int(col_period * 31)
    mask = np.zeros((ysize, xsize), np.uint8)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (scale_f, scale_f))
    xy = []
    for xi in range(0, 12):
        for yi in range(0, 31):
            y = int((yi + 0.5) * col_period) - kernel.shape[0] // 2
            x = int((xi + 0.5) * row_period) - kernel.shape[1] // 2
            xy.append((x, y))
    return xy


def xy_to_mask(xsize, ysize, xy, scale_f=30):
    mask = np.zeros((ysize, xsize), np.uint8)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (scale_f, scale_f))
    for x, y in xy:
        mask[y : y + kernel.shape[0], x : x + kernel.shape[1]] = kernel * 255
    return mask


def mark_up_image(img, xy, xoffset, yoffset, scale=1):
    marked = img.copy()
    xsize = img.shape[1] / 50
    ysize = img.shape[0] / 100
    for x, y in xy:
        pt1 = (int(x - xsize / 2 + xoffset), int(y - ysize / 2 + yoffset))
        pt2 = (int(x + xsize / 2 + xoffset), int(y + ysize / 2 + yoffset))
        cv2.rectangle(
            marked,
            pt1,
            pt2,
            (255, 0, 0),
            10,
        )
    return marked


# Smooth inage into blobs
def smooth_image(img):
    scale = img.shape[0] / 4024

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
    # Cut to low-frequency bit
    magnitude_spectrum = extract_central_region(magnitude_spectrum)
    if args.debug:
        cv2.imwrite("%s/magnitude_spectrum.jpg" % opdir, magnitude_spectrum)
    # Find dominant periodicity in each direction
    window_size = 50
    window = np.ones(window_size) / window_size
    rows = np.mean(magnitude_spectrum, axis=0)
    rows -= np.convolve(rows, window, mode="same")
    rows[0:window_size] = 0
    rows[-window_size:] = 0
    row_peaks, _ = find_peaks(rows, distance=10, prominence=2)
    cols = np.mean(magnitude_spectrum, axis=1)
    cols -= np.convolve(cols, window, mode="same")
    cols[0:window_size] = 0
    cols[-window_size:] = 0
    col_peaks, _ = find_peaks(cols, distance=35, prominence=2)
    # Make simple diagnostic plots of rows and cols
    if args.debug:
        fig, axs = plt.subplots(2, 1, figsize=(10, 8))
        x = np.arange(len(rows)) - len(rows) // 2
        axs[0].plot(x, rows, marker=None, linestyle="-", color="b")
        axs[0].scatter(x[row_peaks], rows[row_peaks], marker="o", color="grey")
        axs[0].set_title("Horizontal Spectrum")
        axs[0].set_xlabel("Index")
        axs[0].set_ylabel("Value")
        axs[0].grid(True)
        x = np.arange(len(cols)) - len(cols) // 2
        axs[1].plot(x, cols, marker=None, linestyle="-", color="r")
        axs[1].scatter(x[col_peaks], cols[col_peaks], marker="o", color="grey")
        axs[1].set_title("Vertical Spectrum")
        axs[1].set_xlabel("Index")
        axs[1].set_ylabel("Value")
        axs[1].grid(True)
        plt.tight_layout()
        plt.savefig("%s/xy_spectrum_plots.png" % opdir)

    # Find the dominant periodicity in each direction
    row_period = img.shape[1] / np.median(np.diff(row_peaks))
    col_period = img.shape[0] / np.median(np.diff(col_peaks))

    # Make a mask with theoretical blobs correctly spaced
    xy = periods_to_grid(row_period, col_period)
    mask = xy_to_mask(int(row_period * 12), int(col_period * 31), xy, scale_i(30))
    if args.debug:
        print(mask.shape)
        cv2.imwrite("%s/mask.jpg" % opdir, mask)
    res = cv2.minMaxLoc(cv2.matchTemplate(blobbed, mask, cv2.TM_CCOEFF))

    # Mark up the original image with the inferred grid locations:
    if args.debug:
        marked = mark_up_image(img, xy, res[3][0], res[3][1], scale=1)
        cv2.imwrite("%s/marked.jpg" % opdir, marked)


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
