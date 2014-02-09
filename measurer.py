#!/usr/bin/python

##
# stage 1 script: generation of feature vectors from
# source images.
##

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
    imagename = params["data_root"]+"/images/"+entry['SDSS_ID']+".jpg"
    if os.path.exists(imagename):
        (rd,rh,rl) = features.line_signature_wrapper(imagename,params)

        ### NO LINES.
        if (rd.size == 0):
            continue

        objs = features.compute_sig_objects(rd,rh,rl)

        for o in objs:
            if (features.is_it_a_trail(o)):
                print imagename
                break

# second, spin through files that exist and have not been
# measured yet, and invoke the measurer

def process_func(x):
    (imfile,mfile) = x
    features.line_signature_wrapper(imfile,params)

map(process_func, image_files)
