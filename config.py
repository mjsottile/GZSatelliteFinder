import ConfigParser

def read_gztf_config(fname):
    ##
    ## read the config file for paths and other parameters
    ##
    config = ConfigParser.RawConfigParser()
    config.read('trailfinder.cfg')

    cfg = {}

    # parameters related to file locations
    cfg["data_root"] = config.get('Paths', 'DataRoot')
    cfg["sdss_database"] = cfg["data_root"] + "sdss_ids_URLs.csv"
    cfg["images_root"] = cfg["data_root"] + "images/"
    cfg["measurements_root"] = config.get('Paths', 'MeasurementsRoot')
    cfg["signatures_root"] = config.get('Paths', 'SignaturesRoot')
    cfg["lineplots_root"] = config.get('Paths', 'LineplotsRoot')

    # parameters related to segmentation
    cfg["tau"] = config.getfloat("Segmentation", "Tau")

    # parameters related to feature identification
    cfg["interp_length"] = config.getint("LineFinding", "InterpLength")
    cfg["min_line_length"] = config.getint("LineFinding", "MinLineLength")
    cfg["max_line_count"] = config.getint("LineFinding", "MaxLineCount")

    # parameters related to clustering
    cfg["feature_dim_per_chan"] = config.getint("Clustering", "FeatureDimensionPerChannel")
    cfg["kmeans_num_clusters"] = config.getint("Clustering", "KMeansNumClusters")
    cfg["ap_damping"] = config.getfloat("Clustering", "APDamping")

    return cfg
