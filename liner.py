#!/usr/bin/python

import csv
import ScikitSatelliteFinder as ssf
import os.path
import matplotlib

data_root = "/home/matt/data/GZTrailFinder/"
interesting_images = ["known_spikes.txt", "known_trails.dat"]
lineplots_root = "./lineplots/"

matplotlib.use('Agg')

i = 0

def lineplot_wrapper(fname, outfile):
    try:
        im = I.imread(fname)
    except:
        print fname+" could not be processed."
        return

    show_with_lines(outfile, im, thresh=50)


def show_with_lines(fname, im, thresh=145):
    gim=rgb2gray(im)

    stats = str(np.amax(im)) + " " + str(np.mean(im)) + " " + str(np.std(im))

    matplotlib.pyplot.clf()

    fig, (ax1, ax2) = plt.subplots(1,2)

    bw_image = gim > (np.std(im) + np.mean(im))
    h, theta, d = hough_line(bw_image)

    ax1.imshow(bw_image, cmap=plt.cm.gray)
    ax2.imshow(im)

    rows, cols = gim.shape
    i = 0
    for _, angle, dist in zip(*hough_peaks(h, theta, d)):
        y0 = (dist - 0 * np.cos(angle)) / np.sin(angle)
        y1 = (dist - cols * np.cos(angle)) / np.sin(angle)

        ax1.plot((0, cols), (y0, y1), '-r')
        ax2.plot((0, cols), (y0, y1), '-r')

        i = i + 1

    ax1.axis((0, cols, rows, 0))
    ax2.axis((0, cols, rows, 0))
    ax1.axis('off')
    ax2.axis('off')

    pylab.savefig(fname,format='png')



for filename in interesting_images:
    with open(data_root + "/"+ filename, 'rb') as listfile:
        for imgfile in listfile:
            imgfile = imgfile[:-1]
            junk1, junk2, fname = imgfile.rpartition("/")
            outfile = lineplots_root + "line_" + fname[:-4] + ".png"
            print imgfile
            print outfile
            if not os.path.exists(outfile):
                ssf.lineplot_wrapper(imgfile, outfile)
        i = i + 1
