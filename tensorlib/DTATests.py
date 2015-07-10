#!/usr/bin/env python

import DTA;
import tensor;
import ttensor;
import numpy;


def test1():
    A = ttensor.ttensor(tensor.tenrands([2,3,4]),
                    [numpy.random.random([10,2]),
                    numpy.random.random([30,3]),
                    numpy.random.random([40,4])]).totensor();

    [a,b] = DTA.DTA(A, [1,2,3]);
    #print a;
    #print b;

    Core = numpy.arange(24).reshape([2,3,4]);
    #Core = numpy.array([[1,3,5],[2,4,6]] , [[7,9,11],[8,10,12]])
    u1 = numpy.array([[1,2],[3,4]]);
    u2 = numpy.array([[0,1,0],[1,0,1],[1,1,1]]);
    u3 = numpy.array([[1,1,1,1],[1,2,3,4],[1,1,1,1]]);
    tt = ttensor.ttensor(tensor.tensor(Core), [u1,u2,u3]);
    
    print tt;
    [a,b] = DTA.DTA(tt.totensor(), [1,2,3]);
    print a;
    print a.totensor();
    print b;
    
def test2():
#    A = numpy.array([[1, 4, 7, 10], [2, 5, 8, 11], [3, 6, 9, 12]]);
#    A = numpy.arange(12).reshape([4,3]) + 1;
    A = numpy.arange(1000).reshape([10,10,10])+1;
    (ans1, ans2) = DTA.DTA(tensor.tensor(A), [2,2,2]);
    print ans1;
    for i in range(0, len(ans2)):
        print "{0} th array\n {1}".format(i, ans2[i]);
        
    print ans1.totensor();
    
    
test2();


def eigwrappertest():
    A = numpy.arange(9).reshape([3,3])+1;
    (ans1, ans2) = numpy.linalg.eig(A);
    print ans1;
    print ans2;
    (ans1, ans2) = DTA.eigwrapper(A,3);
    print ans1;
    print ans2;
    
    
    
    
    