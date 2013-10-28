#!/usr/bin/python

##
# stage 1 script: generation of feature vectors from
# source images.
##

import csv
import FeatureExtractor as features
import os.path
import config as cfg

params = cfg.read_gztf_config("trailfinder.cfg")

i = 0
with open(params["sdss_database"], 'rb') as csvfile:
    test = csv.reader(csvfile)
    for t in test:
        ustring = t[2]
        junk1, junk2, imagename = ustring.rpartition("/")

        image_file = params["images_root"]+imagename

        if os.path.exists(image_file):
            print str(i)+" :: "+imagename

            identifier, junk1, junk2 = imagename.rpartition(".")
            measurement_file = params["measurements_root"]+identifier+".dat"

            if not os.path.exists(measurement_file):
                features.line_signature_wrapper(image_file, identifier, \
                                                measurement_file, params)
        i = i + 1
