#!/usr/bin/python

import csv
import ScikitSatelliteFinder as ssf
import os.path
import matplotlib

data_root = "/home/matt/data/GZTrailFinder/"
filename = data_root+"sdss_ids_URLs.csv"
images_root = data_root+"images/"
measurements_root = "./measurements/"
#lineplots_root = "./lineplots/"

#matplotlib.use('Agg')

i = 0

with open(filename, 'rb') as csvfile:
    test = csv.reader(csvfile)
    for t in test:
        ustring = t[2]
        junk1, junk2, imagename = ustring.rpartition("/")
        if os.path.exists(images_root+imagename):
            print str(i)+" :: "+imagename
            identifier, junk1, junk2 = imagename.rpartition(".")
            if not os.path.exists(measurements_root+identifier+".dat"):
                ssf.measurement_wrapper(images_root+imagename, identifier, measurements_root+identifier+".dat")
#            if not os.path.exists(lineplots_root+identifier+".png"):
#                ssf.lineplot_wrapper(images_root+imagename, \
#                                     lineplots_root+identifier+".png")
        i = i + 1
