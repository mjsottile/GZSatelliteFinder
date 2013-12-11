from skimage.transform import (hough_line, hough_line_peaks)
from skimage import data
from scipy.interpolate import interp1d
import pylab
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import scipy.ndimage as I
import math as M
import segmentation as seg
import Utilities as U 
import pandas as pd

def line_signature_wrapper(fname, params):
    try:
        im = I.imread(fname)
    except:
        print fname+" could not be processed."
        return

    if len(im.shape) < 3:
        print fname+" is not color.  skipping."
        return

    return compute_line_signatures(im, params)

def compute_line_signatures(im, params):
    # convert image into single gray channel for Hough transform
    bin_img = seg.binarize(im)
    h, theta, d = hough_line(bin_img)

    rows, cols = bin_img.shape
    
    # want to count the number of lines detected
    numhits = 0 

    # rows list
    rowdata = []

    # spin through full set of lines that match via the Hough
    # transform.  hough_peaks takes the theta/rho form and
    # filters it for significant peaks corresponding to strong
    # line signals in the image. 
    for _, angle, dist in zip(*hough_line_peaks(h, theta, d)):
        # compute coordinate set for pixels that lie along the line
        xs = np.arange(0,cols-1)
        ys = (dist - xs*np.cos(angle))/np.sin(angle)

        # likely have points outside the bounds of the image, so mask
        # those out and ignore them
        mask = (ys >= 0) & (ys < rows)
        xs_mask = xs[mask]
        ys_mask = np.floor(ys[mask])

        # split image into channels
        rchan = im[:,:,0]
        gchan = im[:,:,1]
        bchan = im[:,:,2]
        
        # color channels along line
        red_pixels = rchan[ys_mask.astype(int), xs_mask.astype(int)]
        green_pixels = gchan[ys_mask.astype(int), xs_mask.astype(int)]
        blue_pixels = bchan[ys_mask.astype(int), xs_mask.astype(int)]

        # create an interpolator for each channel
        npix = len(red_pixels)

        # don't bother with tiny lines.
        if npix < params["min_line_length"]:
            continue

        x = np.linspace(0,1,npix)
        y = np.linspace(0,1,params["interp_length"])
        r_interp = interp1d(x,red_pixels)
        g_interp = interp1d(x,green_pixels)
        b_interp = interp1d(x,blue_pixels)

        # resample lines using interpolators for each channel
        r_fit = r_interp(y)
        g_fit = g_interp(y)
        b_fit = b_interp(y)

        # count the line
        numhits = numhits+1

        # add a row to the list with the color channels appended RGB
        rowdata.append(np.append(np.append(r_fit,g_fit),b_fit))

    # done, mash all together
    return np.array(rowdata)