"""Utility functions for use in the GZ code.
"""
import numpy as np

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
