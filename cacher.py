# cacher
import inspect
import md5
import pickle
import sqlite3

class DataCacher:
    """Class for caching data"""

    def __init__(self, dbname):
        self.dbname = dbname

    def cacher(self, fn, *args, **kv)
        code = inspect.getsource(fn)
        code_hash = md5.new(code).hexdigest()
        args_string = pickle.dumps(args)
        kvs_string = pickle.dump(kv)
        args_hash = md5.new(args_string).hexdigest()
        kvs_hash = md5.new(kvs_string).hexdigest()
        print code_hash + " " + args_hash + " " + kvs_hash
        return fn(*args, **kv)
    
