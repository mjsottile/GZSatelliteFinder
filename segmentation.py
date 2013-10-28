import numpy as np

def binarize(img_array):
  if len(img_array.shape) < 3:
    return img_array
  assert(img_array.shape[2] == 3)

  img_bin_array = np.zeros((img_array.shape[0], img_array.shape[1]), dtype=np.float32)

  rchan = img_array[:,:,0]
  gchan = img_array[:,:,1]
  bchan = img_array[:,:,2]

  rmean = np.mean(rchan)
  rstd = np.std(rchan)
  gmean = np.mean(gchan)
  gstd = np.std(gchan)
  bmean = np.mean(bchan)
  bstd = np.std(bchan)

  img_bin_array = ((rchan > rmean + rstd) + (gchan > gmean + gstd) + \
    (bchan > bmean + bstd)) > 0.99

  # each channel contributes 1/3 to each pixel
  #img_gray_array = (0.333*rchan + 0.333*gchan + 0.333*bchan)
  return img_bin_array

#def binarize(gray, tau):
#    maxval = np.amax(gray)
#    mean = np.mean(gray)
#    stdev = np.std(gray)
#
#    return gray > mean + stdev
