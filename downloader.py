import csv
import urllib
import os.path
import config as cfg

params = cfg.read_gztf_config("trailfinder.cfg")

sdss_database = params["sdss_database"]
images_root = params["images_root"]

##
## spin through full set of IDs in the SDSS file and
## download them if they aren't already downloaded.
##
i = 1
with open(sdss_database, 'rb') as csvfile:
    entries = csv.reader(csvfile)
    for entry in entries:
        ustring = entry[2]
        junk1, junk2, imagename = ustring.rpartition("/")
        if not os.path.exists(images_root+imagename):
            print str(i)+" :: "+imagename
            image = urllib.URLopener()
            image.retrieve(ustring,images_root+imagename)
        i = i + 1

