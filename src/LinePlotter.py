import matplotlib
matplotlib.use('Agg')
import pylab
import matplotlib.pyplot as plt
plt.ioff()
import scipy.ndimage as I
import math as M
import os.path
import segmentation as seg
import csv
from skimage.transform import (hough_line, hough_line_peaks)
from skimage import data
from scipy.interpolate import interp1d

import numpy as np

import config as cfg

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

    matplotlib.pyplot.clf()

    rows, cols = bin_img.shape

    fig, (ax1, ax2) = plt.subplots(1,2)
    ax1.imshow(bin_img, cmap=plt.cm.gray)
    ax2.imshow(im)

    for _, angle, dist in zip(*hough_line_peaks(h, theta, d, 
                                                threshold=params["threshold_scale"]*np.max(h), 
                                                min_angle=params["min_angle"], 
                                                min_distance=params["min_distance"])):
        y0 = (dist - 0 * np.cos(angle)) / np.sin(angle)
        y1 = (dist - cols * np.cos(angle)) / np.sin(angle)

        ax1.plot((0, cols), (y0, y1), '-m')
        ax2.plot((0, cols), (y0, y1), '-m')

    ax1.axis((0, cols, rows, 0))
    ax2.axis((0, cols, rows, 0))
    ax1.axis('off')
    ax2.axis('off')

    pylab.savefig(fname,format='jpg')

