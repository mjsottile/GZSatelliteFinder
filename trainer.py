"""
trainer.py

given a set of labeled images, train a classifier to then evaluate against
a test set.

training data is specified as a set of pairs that map GZ identifiers
to labels.  labels are integers whose interpretation is left up to the user.

mjsottile@gmail.com // dec. 2013
"""
import mysdss
import config as cfg
import FeatureExtractor as features
import numpy as np
from sklearn import cluster

# read configuration
params = cfg.read_gztf_config("trailfinder.cfg")

sdss_database = params["sdss_database"]
images_root = params["images_root"]

# read training set
db = mysdss.read_sdss_trainingset("training_set.csv")

# convert labels to ints
for gz_id in db:
    db[gz_id] = int(db[gz_id])
max_category = max(db.values())
min_category = min(db.values())

totrows = 0
data = []
print "Computing features."
i = 0
labels = []
for gz_id in db:
    imagefile = params["images_root"]+gz_id+".jpg"
    x = features.line_signature_wrapper(imagefile, params)
    labels.extend([gz_id for j in range(len(x))])
    data.append(x)
    print str(int(100 * (float(i) / float(len(db))))) + "% done."
    i = i+1
d = np.concatenate(data)

print "Clustering."

lookup = {}
for gz_id in db:
    lookup[gz_id] = []

km = cluster.KMeans(n_clusters=params["kmeans_num_clusters"])
km.fit(d)
n = len(km.labels_)
for l in range(n):
    lookup[labels[l]].append(km.labels_[l])

# remove duplicates
for gz_id in db:
    lookup[gz_id] = list(set(lookup[gz_id]))

# perform binning
bins = np.zeros((params["kmeans_num_clusters"], (max_category-min_category)+1))

# create matrix of kmeans category vs training set label to determine which
# kmeans category most frequently patches a given training label
for gz_id in db:
    for km_cat in lookup[gz_id]:
        bins[km_cat-1, db[gz_id]-1] = bins[km_cat-1, db[gz_id]-1]+1

print bins
