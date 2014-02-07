from skimage.transform import (hough_line, hough_peaks,
                               probabilistic_hough)
from skimage.filter import canny
from skimage import data
from scipy.interpolate import interp1d
import pylab
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import scipy.ndimage as I
import math as M
import os.path
import segmentation as seg
import Utilities as U
import csv

import config as cfg

params = cfg.read_gztf_config("trailfinder.cfg")

matplotlib.use('Agg')

i = 0

def lineplot_wrapper(fname, outfile, params):
    try:
        im = I.imread(fname)
    except:
        print "["+fname+"] could not be processed."
        return

    show_with_lines(outfile, im, params)

def show_with_lines(fname, im, params):
    bin_img = seg.binarize(im)
    h, theta, d = hough_line(bin_img)

    rows, cols = bin_img.shape
    i = 0
    for _, angle, dist in zip(*hough_peaks(h, theta, d)):
        i = i + 1

    if i > params["max_line_count"]:
        return

    matplotlib.pyplot.clf()

    fig, (ax1, ax2) = plt.subplots(1,2)
    ax1.imshow(bin_img, cmap=plt.cm.gray)
    ax2.imshow(im)

    for _, angle, dist in zip(*hough_peaks(h, theta, d)):
        y0 = (dist - 0 * np.cos(angle)) / np.sin(angle)
        y1 = (dist - cols * np.cos(angle)) / np.sin(angle)

        ax1.plot((0, cols), (y0, y1), '-r')
        ax2.plot((0, cols), (y0, y1), '-r')

    ax1.axis((0, cols, rows, 0))
    ax2.axis((0, cols, rows, 0))
    ax1.axis('off')
    ax2.axis('off')

    pylab.savefig(fname,format='png')
