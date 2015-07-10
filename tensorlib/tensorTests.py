#!/usr/bin/env python

import numpy;
import tensor;


def ctor(verbose):
    dat = numpy.arange(24);
    dat[10] = 100;
    dat[16] = -1;
    siz = numpy.array([4,3,2]);
    
    obj = tensor.tensor(dat, siz);
    if(verbose == 1):
        print obj;
        print obj.ndims();
    
    obj2 = tensor.tensor(dat.reshape([2,3,4]),siz);
    if(verbose == 1):
        print obj;
        print obj.shape;
    
    dat = numpy.array([1,2,3,4,5,6,7,8,9,10,0,0,13,14,15,16,17,18]);
    obj2 = tensor.tensor(dat);
    if(verbose == 1):
        print obj2;
        print obj2.shape;

def specialctor(verbose):
    print tensor.tenrands([2,3,4]);
    print tensor.tenones([2,3,4]);
    print tensor.tenzeros([2,3,4]);
    print tensor.tendiag([11,22,33],[2,3,4]);
    print tensor.tendiag([11,22],[1,3,4]);

def tosptensor(verbose):
    
    dat = numpy.array([1,2,3,4,5,6,7,8,9,10,0,0,13,14,15,16,17,18]);
    siz = numpy.array([3,3,2]);
    
    obj = tensor.tensor(dat, siz);
    if(verbose == 1):
        print obj;
        print (obj.tosptensor());
    
def permutetest(verbose):
    
    dat = numpy.arange(24).reshape([2,3,4]);
    siz = numpy.array([2,3,4]);
    
    obj = tensor.tensor(dat, siz);
    if(verbose == 1):
        print obj;
        print "permute by {0}".format("[2,0,1]");
        print obj.permute([2,0,1]);
        print "permute by {0}".format("[1,2,0]");
        print obj.permute([1,2,0]);
        print "ipermuted by {0}".format("[1,2,0]");
        print obj.ipermute([1,2,0]);
        print obj.permute([1,2,0]).ipermute([1,2,0]);

def ttmTest(verbose):
    dat = numpy.arange(24).reshape([2,3,4]);
    siz = numpy.array([2,3,4]);
    obj = tensor.tensor(dat, siz);
    
    A = numpy.arange(18).reshape([6,3]);
    
    print obj.ttm(A,1);
    B = numpy.arange(12).reshape([3,4]);
    print obj.ttm([A,B],[1,2]);
    print "a";
    print obj.ttm([A.transpose(),B.transpose()],[1,2],'t');

def mathlogicops(verbose):
    dat = numpy.arange(24).reshape([2,3,4]);
    siz = numpy.array([2,3,4]);
    obj = tensor.tensor(dat, siz);
    
    print obj + 100;
    print obj - 100;
    print obj + (obj + 10);
    print obj * 1.5;
    print obj < 10;
    print obj > 10l
    print obj == 10;
    print obj == obj;
    