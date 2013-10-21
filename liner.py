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
