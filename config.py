import ConfigParser

def read_gztf_config(fname):
	##
	## read the config file for paths and other parameters
	##
	config = ConfigParser.RawConfigParser()
	config.read('trailfinder.cfg')

	cfg = {}

	cfg["data_root"] = config.get('Paths', 'DataRoot')
	cfg["sdss_database"] = cfg["data_root"] + "sdss_ids_URLs.csv"
	cfg["images_root"] = cfg["data_root"] + "images/"

	return cfg