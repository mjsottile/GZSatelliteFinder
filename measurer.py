#!/usr/bin/python

##
# stage 1 script: generation of feature vectors from
# source images.
##

from IPython.parallel import Client
import csv
import FeatureExtractor as features
import os.path
import config as cfg
import mysdss

params = cfg.read_gztf_config("trailfinder.cfg")

sdss_database = params["sdss_database"]
sdss_db = mysdss.read_sdss_database(sdss_database)

# first, build up a list of files that exist from the SDSS database
image_files = []
for entry in sdss_db:
    imagename = entry['SDSS_ID']+".jpg"
    if os.path.exists(imagename):
        # check if it has already been measured
        measurement_file = params["measurements_root"]+entry['SDSS_ID']+".dat"
        if not os.path.exists(measurement_file):
            image_files.append((imagename,measurement_file))

# second, spin through files that exist and have not been
# measured yet, and invoke the measurer

def process_func(x):
    (imfile,mfile) = x
    features.line_signature_wrapper(imfile,params)

map(process_func, image_files)
