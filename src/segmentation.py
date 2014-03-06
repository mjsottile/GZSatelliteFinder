"""Code related to segmentation of GZ images
"""
import numpy as np
import skimage.filter as F

def binarize_denoised(img_array):
    return binarize(F.denoise_tv_chambolle(img_array, multichannel=True,
                                           n_iter_max=50))

def binarize(img_array):
    """Given an RGB image, create a 2D binary image from it using Otsu's
       method in each color channel to adaptively compute thresholds."""
    if len(img_array.shape) < 3:
        return img_array
    assert(img_array.shape[2] == 3)

    img_bin_array = np.zeros((img_array.shape[0], img_array.shape[1]), 
                             dtype=np.float32)

    rchan = img_array[:, :, 0]
    gchan = img_array[:, :, 1]
    bchan = img_array[:, :, 2]

    # use Otsu's method to determine which threshold value is appropriate
    # in each color channel
    rthresh = F.threshold_otsu(rchan)
    gthresh = F.threshold_otsu(gchan)
    bthresh = F.threshold_otsu(bchan)

    img_bin_array = ((rchan > rthresh) + (gchan > gthresh) + 
                     (bchan > bthresh)) > 0.99

    return img_bin_array
