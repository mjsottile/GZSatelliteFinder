#!/usr/bin/python

import csv
import urllib
import os.path

data_root = "/Users/Matt/Data/GZTrailFinder/"
filename = data_root+"sdss_ids_URLs.csv"
images_root = data_root+"images/"

i = 1

files = []

with open(filename, 'rb') as csvfile:
    test = csv.reader(csvfile)
    for t in test:
        ustring = t[2]
        junk1, junk2, imagename = ustring.rpartition("/")
        if not os.path.exists(images_root+imagename):
            print str(i)+" :: "+imagename
            image = urllib.URLopener()
            image.retrieve(ustring,images_root+imagename)
        i = i + 1

