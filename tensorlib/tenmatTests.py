#!/usr/bin/env python

import numpy;
import tenmat;
import tensor;

def ctor(verbose):
    
    dat = numpy.arange(24).reshape([2,3,4]);
    
    t = tensor.tensor(dat);
    print t;
    if (verbose):
        obj = tenmat.tenmat(t, [1,0]);
        print obj;
        print obj.copy();
        
    dat = dat.reshape([4,6]);
    t = tensor.tensor(dat);
    if (verbose):
        obj = tenmat.tenmat(t, [0], [1], [4,6]);
        print obj;

def totensorTests(verbose):
    
    dat = numpy.arange(24).reshape([2,3,4]);
    t = tensor.tensor(dat);
    obj = tenmat.tenmat(t,[2,1]);
    if(verbose):
        print obj;
        print obj.totensor();
    