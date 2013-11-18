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

params = cfg.read_gztf_config("trailfinder.cfg")

do_parallel = False

if do_parallel:
    rc = Client()
    lview = rc.load_balanced_view()

# first, build up a list of files that exist from the SDSS database
image_files = []
with open(params["sdss_database"], 'rb') as csvfile:
    test = csv.reader(csvfile)
    for t in test:
        ustring = t[2]
        junk1, junk2, imagename = ustring.rpartition("/")
        image_file = params["images_root"]+imagename
        if os.path.exists(image_file):
            # check if it has already been measured
            identifier, junk1, junk2 = imagename.rpartition(".")
            measurement_file = params["measurements_root"]+identifier+".dat"
            if not os.path.exists(measurement_file):
                image_files.append((imagename,image_file,measurement_file))

# second, spin through files that exist and have not been
# measured yet, and invoke the measurer

def process_func(x):
    (ident,imfile,mfile) = x
    print ident
    features.line_signature_wrapper(imfile,ident,mfile,params)


if do_parallel:
    lview.map(lambda (ident,imfile,mfile) : features.line_signature_wrapper(imfile,ident,mfile,params), \
              image_files)
else:
    map(process_func, image_files)
