#!/usr/bin/env python

import numpy;
import sptensor;
import tensor;
import tools;

class ttensor:
    core = None;
    u = None;
    
    def __init__(self, core, uIn):
        """ Create a tucker tensor object with the core and matrices.
        NOTE: uIn has to be a list of arrays/matrices"""
        if not(core.__class__ == tensor.tensor or core.__class__ == sptensor.sptensor):
            raise ValueError("core is neither tensor nor sptensor!");
        
        #Handle if the uIn is not a list
        if(uIn.__class__ != list):
            newuIn = [];
            for x in uIn:
                newuIn.extend([x]);
            uIn = newuIn;
           
        newuIn = []; 
        for i in range(0, len(uIn)):
            newuIn.extend([uIn[i].copy()]);
        uIn = newuIn;
        
        # check that each U is indeed a matrix
        for i in range(0,len(uIn)):
            if (uIn[i].ndim != 2):
                raise ValueError("{0} is not a 2-D matrix!".format(uIn[i]));
        
        # Size error checking
        k = core.shape;
        
        if (len(k) != len(uIn)):
            raise ValueError("Number of dims of Core andthe number of matrices are different");
        
        for i in range(0,len(uIn)):
            if (k[i] != len((uIn[i])[0])):
                raise ValueError(
                    "{0} th dimension of Core is different from the number of columns of uIn[i]"
                    .format(i));
         
        self.core = core.copy();
        self.u = uIn;
        
        #save the shape of the ttensor
        shape = [];
        for i in range(0, len(self.u)):
            shape.extend([len(self.u[i])]);
        self.shape = tuple(shape);
        # constructor end #

    def size(self):
        ret = 1;
        for i in range(0, len(self.shape)):
            ret = ret * shape[i];
        return ret;
    
    def dimsize(self, ind):
        return shape[ind];
    
    def copy(self):
        return ttensor(self.core, self.u);
        
    def totensor(self):
        """returns a tensor object that is represented by the tucker tensor"""
        
        #ensure that there is enough space
        X = tensor.tenzeros(self.shape);
        X = self.core.ttm(self.u);
        
        if(X.__class__ == sptensor.sptensor):
            X = X.totensor();
        return X;
        
    def __str__(self):
        ret = "ttensor of size {0}\n".format(self.shape);
        ret += "Core = {0} \n".format(self.core.__str__());
        for i in range(0, len(self.u)):
            ret += "u[{0}] =\n{1}\n".format(i, self.u[i]);
        
        return ret;
    