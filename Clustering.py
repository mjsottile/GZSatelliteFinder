##
##
##
from sklearn import metrics, cluster
from sklearn.preprocessing import StandardScaler
import os
import csv
import numpy as np
import config as cfg

params = cfg.read_gztf_config("trailfinder.cfg")

# read one CSV file representing a set of line signatures.
# if the file is empty, return None.
def readone(fname):
    f = open(fname,'r')
    dat = csv.reader(f)
    rows = []
    img_name = 0
    for l in dat:
        img_name = l[0]
        rows.append(map(float,l[1:]))
    if len(rows) == 0:
        return None
    
    return (img_name, rows)

listing = os.listdir(params["measurements_root"])

print "Reading data."

data = []
labels = []
for infile in listing:
    d = readone(params["measurements_root"]+infile)
    if not (d == None):
        lbl,dat = d
        for i in range(len(dat)):
            labels.append(lbl)
        data.extend(dat)
x = np.array(data)

### debugging : save data in a big file
# np.savetxt('data.dat',x,delimiter=',')

# get the interp length
ilen = params["interp_length"]

num_comp = params["feature_dim_per_chan"]

print x.shape

print "Computing feature vectors."

# 6 elements (mean + std for each channel), and num_comp * 3 features from line data
fvec = np.empty([len(x),6+(num_comp*3)])

# for each line, create a compressed feature vector.  THIS IS EXPERIMENTAL
for i in range(0,len(x)):
    line = x[i,6:]
#    rline = np.sort(abs(np.diff(line[0:ilen])))
#    gline = np.sort(abs(np.diff(line[ilen:(2*ilen)])))
#    bline = np.sort(abs(np.diff(line[(2*ilen):(3*ilen)])))
    rline = np.sort(line[0:ilen]) 
    gline = np.sort(line[ilen:(2*ilen)]) 
    bline = np.sort(line[(2*ilen):(3*ilen)]) 

    fvec[i,0:num_comp] = rline[-num_comp:]
    fvec[i,num_comp:(2*num_comp)] = gline[-num_comp:]
    fvec[i,(2*num_comp):(3*num_comp)] = bline[-num_comp:]
    fvec[i,(3*num_comp):] = x[i,0:6]

## PERFORM CLUSTERING

print "Clustering kmeans."

km=cluster.KMeans(n_clusters=params["kmeans_num_clusters"])
km.fit(fvec)
#km.labels_

print "Dumping."

didprint = {}

the_labels = km.labels_
f = open("foo_km.html",'w')
for i in range(0,max(the_labels)+1):
    for j in range(0,len(labels)):
        didprint[labels[j]] = False
    f.write("<H1>"+str(i)+"</H1>\n")
    for j in range(0,len(labels)):
        if (the_labels[j] == i) and (didprint[labels[j]] == False):
            didprint[labels[j]] = True
            f.write("<IMG TEXT=\""+labels[j]+"\" SRC=\"images/"+labels[j]+".jpg\" WIDTH=80>\n")
    f.write("<P>\n")
f.close()

print "Clustering af."

af=cluster.AffinityPropagation(damping=params["ap_damping"]).fit(fvec)
#af.labels_

print "Dumping."

the_labels = af.labels_
f = open("foo_af.html",'w')
for i in range(0,max(the_labels)+1):
    for j in range(0,len(labels)):
        didprint[labels[j]] = False
    f.write("<H1>"+str(i)+"</H1>\n")
    for j in range(0,len(labels)):
        if (the_labels[j] == i) and (didprint[labels[j]] == False):
            didprint[labels[j]] = True
            f.write("<IMG TEXT=\""+labels[j]+"\" SRC=\"images/"+labels[j]+".jpg\" WIDTH=80>\n")
    f.write("<P>\n")
f.close()