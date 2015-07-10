#!/usr/bin/env python

import numpy;
import sptenmat;
import sptensor;

def ctor(verbose):
    x = numpy.array([
        [[0,0,0.9052],[0.9121,0,0.7363]],
        [[0.1757,0.2089,0],[0,0.7455,0]],
        [[0,0,0.6754],[0,0,0]]
        ])
    obj = sptenmat.sptenmat(x, [0], [1,2], [10,10,10]);
    print obj;
    
    subs = numpy.array([[1, 3, 5], [1, 1, 0], [2, 2, 2], [3, 4, 4], [1, 1, 1], [1, 1, 1]]);
    vals = numpy.array([[0.5], [1.5], [100], [3.5], [4.5], [5.5]]);
    siz = numpy.array([4, 5, 6]);
    spt = sptensor.sptensor(subs, vals, siz);
    
    print spt;
    
    obj = sptenmat.sptenmat(spt, [0,1], [2]);
    print obj;
    
def tosptensorTest(verbose):
    
    subs = numpy.array([[1, 3, 5], [1, 1, 0], [2, 2, 2], [3, 4, 4], [1, 1, 1], [1, 1, 1]]);
    vals = numpy.array([[0.5], [1.5], [100], [3.5], [4.5], [5.5]]);
    siz = numpy.array([4, 5, 6]);
    spt = sptensor.sptensor(subs, vals, siz);
    print spt;
    
    sptm = sptenmat.sptenmat(spt,[1]);
    print sptm;
    
    temp = sptm.tosptensor();
    print temp;
    
def tosparsematTest(verbose):
    subs = numpy.array([[1, 3, 5], [1, 1, 0], [2, 2, 2], [3, 4, 4], [1, 1, 1], [1, 1, 1]]);
    vals = numpy.array([[0.5], [1.5], [100], [3.5], [4.5], [5.5]]);
    siz = numpy.array([4, 5, 6]);
    spt = sptensor.sptensor(subs, vals, siz);
    print spt;
    
    sptm = sptenmat.sptenmat(spt,[1]);
    print sptm;
    
    print sptm.tosparsemat();