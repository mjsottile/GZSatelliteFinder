#!/usr/bin/python

##
# stage 1 script: generation of feature vectors from
# source images.
##

import csv
import ScikitSatelliteFinder as ssf
import os.path
import config as cfg

params = cfg.read_gztf_config("trailfinder.cfg")

i = 0
with open(params["sdss_id_database"], 'rb') as csvfile:
    test = csv.reader(csvfile)
    for t in test:
        ustring = t[2]
        junk1, junk2, imagename = ustring.rpartition("/")
        if os.path.exists(params["images_root"]+imagename):
            print str(i)+" :: "+imagename
            identifier, junk1, junk2 = imagename.rpartition(".")
            if not os.path.exists(params["measurements_root"]+identifier+".dat"):
                ssf.measurement_wrapper(params["images_root"]+imagename, \
                    identifier, params["measurements_root"]+identifier+".dat")
        i = i + 1
