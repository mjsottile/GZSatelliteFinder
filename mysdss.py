"""Module to work with the CSV database of SDSS identifiers and AWS
   URLs for use with the image set for GalaxyZoo"""
import csv

def read_sdss_database(sdss_file):
    """return a list of records, each of which maps an SDSS ID to a
       GZ ID as well as the amazon cloud service URL for the image"""
    dbdata = []
    with open(sdss_file, 'rb') as csvfile:
        entries = csv.reader(csvfile)
        for entry in entries:
            entry_dict = {}
            entry_dict['GZ_ID'] = entry[0]
            entry_dict['SDSS_ID'] = entry[1]
            entry_dict['amazon_url'] = entry[2]
            dbdata.append(entry_dict)
    return dbdata
