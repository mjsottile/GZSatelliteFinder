#!/usr/bin/python

import csv
import urllib
import os.path

filename = "sdss_ids_URLs.csv"

i = 1

files = []

with open(filename, 'rb') as csvfile:
    test = csv.reader(csvfile)
    for t in test:
        ustring = t[2]
        junk1, junk2, imagename = ustring.rpartition("/")
        if not os.path.exists(imagename):
            print str(i)+" :: "+imagename
            image = urllib.URLopener()
            image.retrieve(ustring,imagename)
        i = i + 1

