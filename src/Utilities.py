"""Utility functions
"""
import numpy as np

#
# vectorized version of bresenham's line drawing algorithm
# based on matlab code found online here:
#   http://www.mathworks.com/matlabcentral/fileexchange/28190-bresenham-optimized-for-matlab/content/bresenham.m
#
def bresenham(x1,y1,x2,y2):
    x1 = round(x1)
    x2 = round(x2)
    y1 = round(y1)
    y2 = round(y2)
    dx = abs(x2-x1)
    dy = abs(y2-y1)
    steep = abs(dy)>abs(dx)
    if steep:
        t = dx;
        dx = dy;
        dy = t;
    if dy==0:
        q=np.zeros((dx+1,1))
    else:
        q=np.append(np.array([0]),np.where(np.diff(np.mod(np.arange(np.floor(dx/2),-dy*dx+np.floor(dx/2),-dy),dx))>=0,1,0))
        
    if steep:
        if y1<=y2:
            y = np.arange(y1,y2)
        else:
            y = np.arange(y1,y2,-1)
        if x1<=x2:
            x = x1+np.cumsum(q)
        else:
            x = x1-np.cumsum(q)
    else:
        if x1<=x2:
            x = np.arange(x1,x2)
        else:
            x = np.arange(x1,x2,-1)
        if y1<=y2:
            y = y1 + np.cumsum(q)
        else:
            y = y1 - np.cumsum(q)

    return (x,y)

def kullback_leibler(p, q):
    """Kullback-Leibler divergence D(P || Q) for discrete distributions
 
    Parameters
    ----------
    p, q : array-like, dtype=float, shape=n
        Discrete probability distributions.
    """
    p = np.asarray(p, dtype=np.float)
    q = np.asarray(q, dtype=np.float)
 
    return np.sum(np.where(p != 0, p * np.log(p / q), 0))

def intercalate(l):
    """Specialization of the generic intercalate function that is 
       found in the Haskell Data.List package, to put commas between
       list elements when concatenating them together."""
    return ",".join(map(str, l))
