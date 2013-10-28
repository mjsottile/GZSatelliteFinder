import numpy as np

def rgb2gray(img_array):
  if len(img_array.shape) < 3:
    return img_array
  assert(img_array.shape[2] == 3)
  img_gray_array = np.zeros((img_array.shape[0], img_array.shape[1]), dtype=np.float32)
  img_gray_array = (0.333*img_array[:,:,0] + 0.333*img_array[:,:,1] + 0.333*img_array[:,:,2])
  return img_gray_array

def binarize(gray, tau):
    maxval = np.amax(gray)
    mean = np.mean(gray)
    stdev = np.std(gray)

    return gray > mean + stdev
