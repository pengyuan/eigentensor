#!/usr/bin/env python

import ttensor;
import tensor;
import numpy;


def ctorTests(verbose):
    arr = numpy.arange(24).reshape([2,3,4]);
    A = numpy.array([[1,2],[3,4],[5,6]]);
    B = numpy.array([[1,2,3],[4,5,6]]);
    C = numpy.array([[1,2,3,4]]);
    
    obj = ttensor.ttensor(tensor.tensor(arr), [A, B, C]);
    print obj;
    print obj.shape;
    
def totensorTests(verbose):
    arr = numpy.arange(24).reshape([2,3,4]);
    A = numpy.array([[1,2],[3,4],[5,6]]);
    B = numpy.array([[1,2,3],[4,5,6]]);
    C = numpy.array([[1,2,3,4]]);
    
    obj = ttensor.ttensor(tensor.tensor(arr), [A, B, C]);
    print obj;
    print obj.totensor();