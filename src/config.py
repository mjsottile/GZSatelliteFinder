"""Support code for reading and interpreting configuration files
   such that a data structure is created that can be used throughout
   the program so different functions can access the appropriate
   parameters."""
import ConfigParser

def read_gztf_config(fname):
    """read the config file for paths and other parameters"""
    config = ConfigParser.RawConfigParser()
    config.read(fname)

    cfg = {}

    # parameters related to file locations
    cfg["data_root"] = config.get('Paths', 'DataRoot')
    cfg["sdss_database"] = cfg["data_root"] + "sdss_ids_URLs.csv"
    cfg["images_root"] = cfg["data_root"] + "images/"
    cfg["measurements_root"] = config.get('Paths', 'MeasurementsRoot')
    cfg["signatures_root"] = config.get('Paths', 'SignaturesRoot')
    cfg["lineplots_root"] = config.get('Paths', 'LineplotsRoot')

    # parameters related to feature identification
    cfg["interp_length"] = config.getint("LineFinding", "InterpLength")
    cfg["min_line_length"] = config.getint("LineFinding", "MinLineLength")
    cfg["max_line_count"] = config.getint("LineFinding", "MaxLineCount")
    cfg["min_angle"] = config.getint("LineFinding", "MinAngle")
    cfg["min_distance"] = config.getint("LineFinding", "MinDistance")
    cfg["threshold_scale"] = config.getfloat("LineFinding", "ThresholdScale")

    return cfg
