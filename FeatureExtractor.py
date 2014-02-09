"""Module of functions related to feature extraction for the 
   ZooniBot artifact detection helper."""
from skimage.transform import (hough_line, hough_line_peaks)
from scipy.interpolate import interp1d
import numpy as np
import scipy.ndimage as I
import segmentation as seg

def line_signature_wrapper(fname, params):
    """Wrapper around the line signature computation that tries
       to load the image and then passes it off to the actual
       feature computation."""
    try:
        im = I.imread(fname)
    except:
        print fname+" could not be processed."
        return

    if len(im.shape) < 3:
        print fname+" is not color.  skipping."
        return

    if saturated_channel(im):
        return None

    return compute_line_signatures(im, params)

def compute_line_signatures(im, params):
    """Using the Hough transform, create a signature for an image
       based on extracted lines."""
    # convert image into single gray channel for Hough transform
    bin_img = seg.binarize(im)
    h, theta, d = hough_line(bin_img)

    rows, cols = bin_img.shape
    
    # want to count the number of lines detected
    numhits = 0 

    # rows list
    row_data = []
    row_hists = []
    row_line = []

    # spin through full set of lines that match via the Hough
    # transform.  hough_peaks takes the theta/rho form and
    # filters it for significant peaks corresponding to strong
    # line signals in the image. 
    for _, angle, dist in zip(*hough_line_peaks(h, theta, d, threshold=0.8*np.max(h), min_angle=30, min_distance=20)):
        # compute coordinate set for pixels that lie along the line
        xs = np.arange(0, cols-1)
        ys = (dist - xs*np.cos(angle))/np.sin(angle)

        # likely have points outside the bounds of the image, so mask
        # those out and ignore them
        mask = (ys >= 0) & (ys < rows)
        xs_mask = xs[mask]
        ys_mask = np.floor(ys[mask])

        # split image into channels
        rchan = im[:, :, 0]
        gchan = im[:, :, 1]
        bchan = im[:, :, 2]
        
        # color channels along line
        red_pixels = rchan[ys_mask.astype(int), xs_mask.astype(int)]
        green_pixels = gchan[ys_mask.astype(int), xs_mask.astype(int)]
        blue_pixels = bchan[ys_mask.astype(int), xs_mask.astype(int)]

        # create an interpolator for each channel
        npix = len(red_pixels)

        # don't bother with tiny lines.
        if npix < params["min_line_length"]:
            continue

        x = np.linspace(0, 1, npix)
        y = np.linspace(0, 1, params["interp_length"])
        r_interp = interp1d(x, red_pixels)
        g_interp = interp1d(x, green_pixels)
        b_interp = interp1d(x, blue_pixels)

        # resample lines using interpolators for each channel
        r_fit = r_interp(y)
        g_fit = g_interp(y)
        b_fit = b_interp(y)

        # compute histograms for each line
        (r_hist,junk) = np.histogram(r_fit, bins=255, range=(0,255))
        (g_hist,junk) = np.histogram(g_fit, bins=255, range=(0,255))
        (b_hist,junk) = np.histogram(b_fit, bins=255, range=(0,255))

        # count the line
        numhits = numhits+1

        # add a row to the list with the color channels appended RGB
        row_data.append(np.append(np.append(r_fit, g_fit), b_fit))
        row_hists.append(np.append(np.append(r_hist, g_hist), b_hist))
        row_line.append((angle,dist))

    # done, mash all together
    return (np.array(row_data), np.array(row_hists), row_line)

def compute_sig_objects(rd,rh,rl):
    if (rd.size == 0):
        return []

    (numlines,_) = rd.shape
    
    objs = []
    
    for i in range(0,numlines):
        objs.append(LineSignature(rd[i,:],rh[i,:],rl[i]))
        
    return objs

def saturated_channel(im):
    rv = im[:,:,0].mean() - im[:,:,0].std()
    gv = im[:,:,1].mean() - im[:,:,1].std()
    bv = im[:,:,2].mean() - im[:,:,2].std()

    if (rv > 10):
        return True
    elif (gv > 10):
        return True
    elif (bv > 10):
        return True
    else:
        return False

def is_it_a_trail(o):
    rg=np.sqrt(1./200. * sum((o.r_data-o.g_data)**2))*max(o.r_data.mean(),o.g_data.mean())/min(o.r_data.mean(),o.g_data.mean())
    rb=np.sqrt(1./200. * sum((o.r_data-o.b_data)**2))*max(o.r_data.mean(),o.b_data.mean())/min(o.r_data.mean(),o.b_data.mean())
    gb=np.sqrt(1./200. * sum((o.g_data-o.b_data)**2))*max(o.g_data.mean(),o.b_data.mean())/min(o.g_data.mean(),o.b_data.mean())
    
    rgrb = abs(np.log(rg)-np.log(rb))
    rggb = abs(np.log(rg)-np.log(gb))
    rbgb = abs(np.log(rb)-np.log(gb))
    
    if (rgrb > 3 and rbgb > 3 and rggb < 1):
        return True
        #print "Dominant green."
    elif (rgrb > 3 and rggb > 3 and rbgb < 1):
        return True
        #print "Dominant blue"
    elif (rgrb < 1 and rbgb > 3 and rggb > 3):
        return True
        #print "Dominant red"
    else:
        return False
        #print "No dominant line."

class LineSignature:
    def __init__(self, rd, rh, rl):
        cols = rd.size

        perchan = cols/3

        self.r_data = rd[0:perchan]
        self.g_data = rd[perchan:perchan*2]
        self.b_data = rd[perchan*2:perchan*3]

        self.r_hist = rh[0:255]
        self.g_hist = rh[255:255*2]
        self.b_hist = rh[255*2:255*3]

        (self.angle, self.dist) = rl
