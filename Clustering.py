# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from sklearn import metrics, cluster
from sklearn.preprocessing import StandardScaler
import os
import csv
import numpy as np

# <codecell>

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

# <codecell>

path = 'measurements/'
listing = os.listdir(path)
data = []
labels = []
for infile in listing:
    d = readone("measurements/"+infile)
    if not (d == None):
        lbl,dat = d
        for i in range(len(dat)):
            labels.append(lbl)
        data.extend(dat)
x = np.array(data)
np.savetxt('data.dat',x,delimiter=',')

# <codecell>

num_comp = 4
fvec = np.empty([len(x),6+(num_comp*3)])
for i in range(0,len(x)):
    line = x[i,6:]
    rline = sort(abs(diff(line[0:300])))
    gline = sort(abs(diff(line[300:600])))
    bline = sort(abs(diff(line[600:900])))
    
    fvec[i,0:num_comp] = rline[-num_comp:]
    fvec[i,num_comp:(2*num_comp)] = gline[-num_comp:]
    fvec[i,(2*num_comp):(3*num_comp)] = bline[-num_comp:]
    fvec[i,(3*num_comp):] = x[i,0:6]

# <codecell>

km=cluster.KMeans(n_clusters=15)
km.fit(fvec)
km.labels_

# <codecell>

af=cluster.AffinityPropagation(damping=0.9).fit(fvec)
af.labels_

# <codecell>

s_x=StandardScaler().fit_transform(x)
db=cluster.DBSCAN(eps=0.1).fit(s_x)
db.labels_

# <codecell>

wd=cluster.Ward(n_clusters=5).fit(x)
wd.labels_

# <codecell>

the_labels = km.labels_
f = open("foo_km.html",'w')
for i in range(0,max(the_labels)+1):
    f.write("<H1>"+str(i)+"</H1>\n")
    for j in range(0,len(labels)):
        if the_labels[j] == i:
            f.write("<IMG TEXT=\""+labels[j]+"\" SRC=\"images/"+labels[j]+".jpg\" WIDTH=80>\n")
    f.write("<P>\n")
f.close()

# <codecell>

the_labels = wd.labels_
f = open("foo_wd.html",'w')
for i in range(0,max(the_labels)+1):
    f.write("<H1>"+str(i)+"</H1>\n")
    for j in range(0,len(labels)):
        if the_labels[j] == i:
            f.write("<IMG TEXT=\""+labels[j]+"\" SRC=\"images/"+labels[j]+".jpg\" WIDTH=80>\n")
    f.write("<P>\n")
f.close()

# <codecell>

the_labels = af.labels_
f = open("foo_af.html",'w')
for i in range(0,max(the_labels)+1):
    f.write("<H1>"+str(i)+"</H1>\n")
    for j in range(0,len(labels)):
        if the_labels[j] == i:
            f.write("<IMG TEXT=\""+labels[j]+"\" SRC=\"images/"+labels[j]+".jpg\" WIDTH=80>\n")
    f.write("<P>\n")
f.close()

# <codecell>


