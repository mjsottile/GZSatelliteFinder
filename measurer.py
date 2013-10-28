#!/usr/bin/python

##
# stage 1 script: generation of feature vectors from
# source images.
##

import csv
import ScikitSatelliteFinder as ssf
import os.path

data_root = "/Users/Matt/data/GZTrailFinder/"
sdss_id_database = data_root+"sdss_ids_URLs.csv"
images_root = data_root+"images/"
measurements_root = "./measurements/"

i = 0

with open(sdss_id_database, 'rb') as csvfile:
    test = csv.reader(csvfile)
    for t in test:
        ustring = t[2]
        junk1, junk2, imagename = ustring.rpartition("/")
        if os.path.exists(images_root+imagename):
            print str(i)+" :: "+imagename
            identifier, junk1, junk2 = imagename.rpartition(".")
            if not os.path.exists(measurements_root+identifier+".dat"):
                ssf.measurement_wrapper(images_root+imagename, identifier, measurements_root+identifier+".dat")
        i = i + 1
