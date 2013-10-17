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

def measurement_wrapper(fname, ident, outfile):
    try:
        im = I.imread(fname)
    except:
        print fname+" could not be processed."
        return

    compute_image_properties(im, ident, outfile, thresh=50)

def lineplot_wrapper(fname, outfile):
    try:
        im = I.imread(fname)
    except:
        print fname+" could not be processed."
        return

    show_with_lines(outfile, im, thresh=50)

# TODO: this has to be part of the imaging tools that I'm using...
def rgb2gray(img_array):
  if len(img_array.shape) < 3:
    return img_array
  assert(img_array.shape[2] == 3)
  img_gray_array = np.zeros((img_array.shape[0], img_array.shape[1]), dtype=np.float32)
  img_gray_array = 0.2989*img_array[:,:,0] + 0.5870*img_array[:,:,1] + 0.1140*img_array[:,:,2]
  return img_gray_array

def kl(p, q):
    """Kullback-Leibler divergence D(P || Q) for discrete distributions
 
    Parameters
    ----------
    p, q : array-like, dtype=float, shape=n
        Discrete probability distributions.
    """
    p = np.asarray(p, dtype=np.float)
    q = np.asarray(q, dtype=np.float)
 
    return np.sum(np.where(p != 0, p * np.log(p / q), 0))

def intercalate(l):
    return ",".join(map(str,l))

def compute_image_properties(im, identifier, outputfile, outimage, thresh=145, bins=51):
    """Compute properties of an image for later clustering and analysis

    Parameters
    ----------

    im
    thresh
    bins
    identifier
    outputfile
    """

    # for images that aren't color, write an empty file and abort
    if len(im.shape) < 3:
        f = open(outputfile,'w')
        f.close()
        return

    # convert image into single gray channel for Hough transform
    gim = rgb2gray(im)
    max_val = np.amax(im)
    h, theta, d = hough_line(gim>thresh)
    rows, cols = gim.shape
    
    numhits = 0
 
    lines_to_write = []

    # spin through full set of lines that match via the Hough
    # transform.  hough_peaks takes the theta/rho form and
    # filters it for significant peaks corresponding to strong
    # line signals in the image. 
    for _, angle, dist in zip(*hough_peaks(h, theta, d)):
        this_line = ""

        numhits = numhits+1

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

        # don't bother with tiny lines.  they are weird.  TODO: print when
        # we see these to see why.
        if npix < 10:
            continue
        num_interp = 300

        x = np.linspace(0,1,npix)
        y = np.linspace(0,1,num_interp)
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
        this_line = this_line + (intercalate(r_interp(y)) + ",")
        this_line = this_line + (intercalate(g_interp(y)) + ",")
        this_line = this_line + (intercalate(b_interp(y)) + "\n")

        # distance based on bulk statistics
        tot_diff_std = abs(rstd-gstd)+abs(rstd-bstd)+abs(gstd-bstd)
        tot_diff_mean = abs(rmean-gmean)+abs(rmean-bmean)+abs(gmean-bmean)

        lines_to_write.append(this_line)
        
    f = open(outputfile,'w')

    if numhits < 4:
        for l in lines_to_write:
            f.write(identifier+",")
            f.write(l)
    f.close()    

def show_with_lines(fname, im, thresh=145):
    gim=rgb2gray(im)
    matplotlib.pyplot.clf()
    h, theta, d = hough_line(gim>thresh)
    plt.imshow(gim, cmap=plt.cm.gray)
    rows, cols = gim.shape
    for _, angle, dist in zip(*hough_peaks(h, theta, d)):
        y0 = (dist - 0 * np.cos(angle)) / np.sin(angle)
        y1 = (dist - cols * np.cos(angle)) / np.sin(angle)
        plt.plot((0, cols), (y0, y1), '-r')
    plt.axis((0, cols, rows, 0))
    plt.title('Detected lines')
    pylab.savefig(fname,format='png')