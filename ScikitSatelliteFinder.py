from skimage.transform import (hough_line, hough_peaks,
                               probabilistic_hough)
from skimage.filter import canny
from skimage import data
import numpy as np
import matplotlib.pyplot as plt
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
    
# TODO: this has to be part of the imaging tools that I'm using...
def rgb2gray(img_array):
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

def compute_image_properties(im, identifier, outputfile, thresh=145, bins=51):
    """Compute properties of an image for later clustering and analysis

    Parameters
    ----------

    im
    thresh
    bins
    identifier
    outputfile
    """

    # convert image into single gray channel for Hough transform
    gim = rgb2gray(im)
    max_val = np.amax(im)
    h, theta, d = hough_line(rgb2gray(im)>thresh)
    rows, cols = gim.shape
    
    largest_kl_dist = 0.0
    numhits = 0
 
    lines_to_write = []

    # spin through full set of lines that match via the Hough
    # transform.  hough_peaks takes the theta/rho form and
    # filters it for significant peaks corresponding to strong
    # line signals in the image. 
    for _, angle, dist in zip(*hough_peaks(h, theta, d)):
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

        # basic statistics about each channel
        rmean = np.mean(red_pixels)
        rstd = np.std(red_pixels)
        gmean = np.mean(green_pixels)
        gstd = np.std(green_pixels)
        bmean = np.mean(blue_pixels)
        bstd = np.std(blue_pixels)

        lines_to_write.append(str(rmean)+","+str(rstd)+","+
                              str(gmean)+","+str(gstd)+","+
                              str(bmean)+","+str(bstd)+",")

        # distance based on bulk statistics
        tot_diff_std = abs(rstd-gstd)+abs(rstd-bstd)+abs(gstd-bstd)
        tot_diff_mean = abs(rmean-gmean)+abs(rmean-bmean)+abs(gmean-bmean)
        
        # generate bin boundaries for histogramming
        bin_vals = np.arange(0,bins+2.0)*(max_val / bins)
        
        # compute histograms
        rhist,junk = np.histogram(red_pixels, bins=bin_vals)
        ghist,junk = np.histogram(green_pixels, bins=bin_vals)
        bhist,junk = np.histogram(blue_pixels, bins=bin_vals)
        
        lines_to_write.append(intercalate(rhist)+",")
        lines_to_write.append(intercalate(ghist)+",")
        lines_to_write.append(intercalate(bhist))

        # compute KL dist between channels.  +1 to avoid div-by-zero and
        # subsequent inf.  this assumes that kl is a symmetric distance
        # function
        ks = [kl(rhist+1,ghist+1), kl(rhist+1,bhist+1),
              kl(ghist+1,bhist+1)]

        ### TODO: better method for distinguishing differences in histograms
        
        # biggest difference in KL divergence difference
        kl_dist = max(ks)-min(ks)
        if largest_kl_dist < kl_dist:
            largest_kl_dist = kl_dist

    # write out
    if numhits > 1:
        return

    # file format:
    #
    # identifier
    # largest_kl_dist
    # num lines
    # rmean rstd gmean gstd bmean bstd
    # rhist
    # ghist
    # bhist
    # (repeat previous four on each hough line)
    f = open(outputfile,'w')

    f.write(identifier+",")
    f.write(str(largest_kl_dist)+",")
    #f.write(str(numhits)+"\n")
    for l in lines_to_write:
        f.write(l)
    f.write("\n")
    f.close()
    

def show_with_line(im, thresh=145):
    gim=rgb2gray(im)
    h, theta, d = hough_line(gim>thresh)
    plt.imshow(gim, cmap=plt.cm.gray)
    rows, cols = gim.shape
    for _, angle, dist in zip(*hough_peaks(h, theta, d)):
        y0 = (dist - 0 * np.cos(angle)) / np.sin(angle)
        y1 = (dist - cols * np.cos(angle)) / np.sin(angle)
        plt.plot((0, cols), (y0, y1), '-r')
    plt.axis((0, cols, rows, 0))
    plt.title('Detected lines')

