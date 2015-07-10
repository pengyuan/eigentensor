#!/usr/bin/env python
import numpy;
import sptensor;


def ctor(verbose):
    subs = numpy.array([[0, 0, 0], [0, 0, 2], [1, 1, 1], [3, 3, 3], [0, 0, 0], [0, 0, 0]]);
    subs2 = numpy.array([[0, 2, 3], [0, 0, 2], [1, 1, 1], [3, 3, 3], [0, 0, 0], [0, 0, 0]]);
    vals = numpy.array([[0.5], [1.5], [2.5], [3.5], [4.5], [5.5]]);
    vals2 = numpy.array([[0.5], [1.5], [100], [3.5], [4.5], [5.5]]);
    siz = numpy.array([5, 5, 5]);


    if(verbose == 1):
        print sptensor.sptensor(subs, vals, siz);
        print sptensor.sptensor(subs, vals);
    
    obj2 = sptensor.sptensor(subs2, vals2, siz);
    if(verbose == 1):
        print obj2;
        print obj2.totensor();
        print sptensor.sptensor(subs, vals).totensor();

def specialctor(verbose):
    print sptensor.sptendiag([11,22,33]);
    print sptensor.sptendiag([11,22,33], [2,3,4,5]);

def mathops(verbose):
    subs = numpy.array([[0, 0, 0], [0, 0, 2], [1, 1, 1], [3, 3, 3], [0, 0, 0], [0, 0, 0]]);
    subs2 = numpy.array([[0, 2, 4], [0, 0, 2], [1, 1, 1], [3, 3, 3], [0, 0, 0], [0, 0, 0]]);
    vals = numpy.array([[0.5], [1.5], [2.5], [3.5], [4.5], [5.5]]);
    vals2 = numpy.array([[0.5], [1.5], [100], [3.5], [4.5], [5.5]]);
    siz = numpy.array([4, 4, 4]);

    obj = sptensor.sptensor(subs, vals, siz);
    obj2 = sptensor.sptensor(subs2, vals2, siz);
    if(verbose == 1):
        print obj == obj2;
    if(verbose == 1):
        print obj == obj;
    if(verbose == 1):
        print obj + 100;
        print obj - 100;
        print obj * 3.4;
    if(verbose == 1):
        print obj + obj2;
        print obj - obj2;

def permute(verbose):
    subs = numpy.array([[1, 2, 3], [1, 1, 3], [2, 0, 1], [4, 3, 4], [1, 0, 1], [1, 0, 0]]);
    vals = numpy.array([[0.5], [1.5], [10], [3.5], [4.5], [5.5]]);
    siz = numpy.array([5, 5, 5]);
    obj = sptensor.sptensor(subs, vals, siz);
    if (verbose):
        print obj;
        print obj.permute([2,0,1]);

#def logicops():
    
def ttmTests(verbose):
    
    subs = numpy.array([[0,0,0],[0,1,1],[1,0,1],[1,1,1],[0,1,2]]);
    vals = numpy.array([[1],[2],[3],[4],[5]]);
    obj = sptensor.sptensor(subs,vals);
    A = numpy.array([[10,20],[30,40]]);
    print obj.ttm(A,0);
    
    
    subs = numpy.array([[1, 2, 2], [1, 1, 2], [2, 0, 1], [1, 0, 1], [1, 0, 0]]);
    vals = numpy.array([[0.5], [1.5], [3.5], [4.5], [5.5]]);
    obj = sptensor.sptensor(subs, vals);
    print obj;
    A = numpy.arange(18).reshape([6,3]);
    
    print obj.ttm(A,2);
    
    print obj.ttm([A,A],[1,2]);
    
    
    
    
    
    
