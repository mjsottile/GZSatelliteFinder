#!/usr/bin/python

import csv
import ScikitSatelliteFinder as ssf
import os.path

filename = "sdss_ids_URLs.csv"
images_root = "images/"
measurements_root = "measurements/"

i = 0

with open(filename, 'rb') as csvfile:
    test = csv.reader(csvfile)
    for t in test:
        ustring = t[2]
        junk1, junk2, imagename = ustring.rpartition("/")
        if os.path.exists(images_root+imagename):
            print str(i)+" :: "+imagename
            identifier, junk1, junk2 = imagename.rpartition(".")
            ssf.measurement_wrapper(images_root+imagename, identifier, \
                                    measurements_root+identifier+".dat")
        i = i + 1
