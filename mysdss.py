import csv

# return a list of records, each of which maps an SDSS ID to a
# GZ ID as well as the amazon cloud service URL for the image
def read_sdss_database(sdss_file):
    dbdata = []
    with open(sdss_file, 'rb') as csvfile:
        entries = csv.reader(csvfile)
        for entry in entries:
            e = {}
            e['SDSS_ID'] = entry[0]
            e['GZ_ID'] = entry[1]
            e['amazon_url'] = entry[2]
            dbdata.append(e)
    return dbdata

# return a map of GZ_ID to classification
def read_sdss_trainingset(training_file):
    dbdata = {}
    with open(training_file, 'rb') as csvfile:
        entries = csv.reader(csvfile)
        for entry in entries:
            if entry[0][0] == "#":
                continue
            dbdata[entry[0]] = entry[1]
    return dbdata