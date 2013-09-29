#!/usr/bin/python

import csv
import urllib
import ScikitSatelliteFinder as ssf
import os.path

filename = "sdss_ids_URLs.csv"

i = 1

files = []

with open(filename, 'rb') as csvfile:
    test = csv.reader(csvfile)
    for t in test:
        if i>4731:
            break
        ustring = t[2]
        junk1, junk2, imagename = ustring.rpartition("/")
        print str(i)+" :: "+imagename
        if os.path.exists(imagename):
            if ssf.harness_wrapper(imagename):
                files.append(imagename)
#        else:
#            image = urllib.URLopener()
#            image.retrieve(ustring,imagename)
        i = i + 1

f = open('probably.html','w')

for fname in files:
    f.write("<IMG SRC=\""+fname+"\">\n")

f.close()
