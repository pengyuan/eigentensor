#!/usr/bin/env python

from scipy import sparse;
import numpy;
import tensor;
import tenmat;
import sptensor;
import sptenmat;
import ttensor;

def DTA(Xnew, R, C = None, alpha = None):
    """DTA analysis"""
    
    # number of dimensions of the input tensor.
    N = Xnew.ndims();
    
    # If the co-variacne matrices are not given,
    # initialize all of them to be 0
    if(C == None):
        C = [];
        dv = Xnew.shape;
        for i in range(0, N):
            C.extend([ sparse.coo_matrix(([],([],[])),[dv[i], dv[i]]) ]);
    
    # If the forgetting factor is not given, it is 1.
    if(alpha == None):
        alpha = 1;
    
    U = [];
    Cnew = [];
    for i in range (0,N):
        if(Xnew.__class__ == tensor.tensor):
            XM = tenmat.tenmat(Xnew,[i]).tondarray();
        elif(Xnew.__class__ == sptensor.sptensor):
            XM = sptenmat.sptenmat(Xnew,[i]).tosparsemat();
        elif(Xnew.__class__ == ttensor.ttensor):
            raise TypeError("It is not supported yet.");
        else:
            raise TypeError("1st argument must be tensor, sptensor, or ttensor");
        
        
        Cnew.extend([ numpy.array(alpha*C[i] + numpy.dot(XM, XM.transpose())) ]);
        
        (w,v) = eigwrapper(Cnew[i], R[i]);
        
        U.extend([ numpy.array(v) ]);

    core = Xnew.ttm(U, None, 't');
    T = ttensor.ttensor(core, U);
    return (T, Cnew);



def eigwrapper(arr, n):
    """wrapper funcion for numpy.linalg.eig function.
    It returns (w,v) such that
    w is 1-d array of n largest magnitude eigenvalues
    v is 2-d array of normalized eigenvectors that v[:,i] is corresponding to
    the eigenvalue w[i]."""
    
    
    if (n > len(arr)):
        raise ValueError("n has to be less than or equal to the number of rows in arr");
    
    (w,v) = numpy.linalg.eig(arr);
    absw = numpy.abs(w);
    ind = absw.argsort();
    ind = list(ind);
    ind.reverse();
    
    neww = numpy.array([]).reshape([1,0]);
    newv = numpy.array([]).reshape([len(arr),0]);
    for i in range(0, n):
        neww = numpy.concatenate((neww, w[ind[i]].reshape([1,1])),axis = 1);
        newv = numpy.concatenate((newv, v[:,ind[i]].reshape([len(arr), 1])),axis = 1);
    
    return (neww,newv);
    
    
    