import urllib
import os.path
import config as cfg
import mysdss

params = cfg.read_gztf_config("trailfinder.cfg")

sdss_database = params["sdss_database"]
images_root = params["images_root"]

sdss_db = mysdss.read_sdss_database(sdss_database)

##
## spin through full set of IDs in the SDSS file and
## download them if they aren't already downloaded.
##
i = 1
for entry in sdss_db:
    imagename = entry['SDSS_ID']+".jpg"
    if not os.path.exists(images_root+imagename):
        print str(i)+" :: "+imagename
        image = urllib.URLopener()
        image.retrieve(entry["amazon_url"], images_root+imagename)
    i = i + 1

