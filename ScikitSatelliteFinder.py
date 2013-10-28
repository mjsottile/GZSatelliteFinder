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

def line_signature_wrapper(fname, ident, outfile, params):
    try:
        im = I.imread(fname)
    except:
        print fname+" could not be processed."
        return

    compute_line_signatures(im, ident, outfile, params)

def compute_line_signatures(im, identifier, outputfile, params):
    # for images that aren't color, write an empty file and abort
    if len(im.shape) < 3:
        print "DEBUG: skipping non-color image "+identifier

        f = open(outputfile,'w')
        f.close()
        return

    # convert image into single gray channel for Hough transform
    gim = seg.rgb2gray(im)
    bin_img = seg.binarize(gim, params["tau"])
    h, theta, d = hough_line(bin_img)
    rows, cols = gim.shape
    
    numhits = 0 
    lines_to_write = []

    # spin through full set of lines that match via the Hough
    # transform.  hough_peaks takes the theta/rho form and
    # filters it for significant peaks corresponding to strong
    # line signals in the image. 
    for _, angle, dist in zip(*hough_peaks(h, theta, d)):
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

        # clear the line that we are about to write
        this_line = ""

        # count the line
        numhits = numhits+1

        x = np.linspace(0,1,npix)
        y = np.linspace(0,1,params["interp_length"])
        r_interp = interp1d(x,red_pixels)
        g_interp = interp1d(x,green_pixels)
        b_interp = interp1d(x,blue_pixels)

        # basic statistics about each channel
        rmean = np.mean(red_pixels)
        rstd = np.std(red_pixels)
        gmean = np.mean(green_pixels)
        gstd = np.std(green_pixels)
        bmean = np.mean(blue_pixels)
        bstd = np.std(blue_pixels)

        this_line = this_line + (str(rmean)+","+str(rstd)+","+
                                 str(gmean)+","+str(gstd)+","+
                                 str(bmean)+","+str(bstd)+",")
        this_line = this_line + (U.intercalate(r_interp(y)) + ",")
        this_line = this_line + (U.intercalate(g_interp(y)) + ",")
        this_line = this_line + (U.intercalate(b_interp(y)) + "\n")

        lines_to_write.append(this_line)
        
    # done computing features.
    f = open(outputfile,'w')

    # if we don't have a ton of lines, dump them out
    if numhits < params["max_line_count"]:
        for l in lines_to_write:
            f.write(identifier+",")
            f.write(l)
    f.close()    
