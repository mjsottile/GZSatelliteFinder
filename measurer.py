#!/usr/bin/python

import csv
import ScikitSatelliteFinder as ssf
import os.path

data_root = "/Users/Matt/Data/GZTrailFinder/"
filename = data_root+"sdss_ids_URLs.csv"
images_root = data_root+"images/"
measurements_root = "./measurements/"

i = 0

with open(filename, 'rb') as csvfile:
    test = csv.reader(csvfile)
    for t in test:
        if i > 30:
            break
        ustring = t[2]
        junk1, junk2, imagename = ustring.rpartition("/")
        if os.path.exists(images_root+imagename):
            print str(i)+" :: "+imagename
            identifier, junk1, junk2 = imagename.rpartition(".")
            if os.path.exists(measurements_root+identifier+".dat"):
                print "SKIPPED"
            else:
                ssf.measurement_wrapper(images_root+imagename, identifier, \
                                        measurements_root+identifier+".dat")
        i = i + 1
