#!/usr/bin/env python

import numpy;
import sptenmat;
import tenmat;
import tensor;
from scipy import sparse;
import tools;

class sptensor:
    
    subs = None;
    vals = None;
    shape = None;
    func = sum.__call__;
    
    def __init__(self,
                 subs,
                 vals,
                 shape = None,
                 func = sum.__call__):
        """Create a sptensor object"""
        
        if(subs.__class__ == list):
            subs = numpy.array(subs);
        if(vals.__class__ == list):
            vals = numpy.array(vals);
        if(shape.__class__ == list):
            shape = numpy.array(shape);
            
        
        if not(tools.tt_subscheck(subs)):
            raise ValueError("Error in subscripts");
        if not(tools.tt_valscheck(vals)):
            raise ValueError("Error in values");
        if (shape != None and not tools.tt_sizecheck(shape)):
            raise ValueError("Error in shape");
        
        if(vals.size != 0 and vals.size != 1 and len(vals) != len(subs)):
            raise ValueError("Number of subscripts and values must be equal");
        
        if (shape == None):
            self.shape = tuple(subs.max(0) + 1);
        else:
            self.shape = tuple(shape);
        
        # if func is given by user
        if(func != None):
            self.func = func;
        
        if(subs.size == 0):
            nzsub = numpy.array([]);
            nzval = numpy.array([]);
        else:
            (newsub, loc) = uniquerows(subs);
            newval = numpy.ndarray([len(newsub), 1]);
            newval.fill(0);
            
            for i in range(0, len(loc)):
                newval[(int)(loc[i])] = func(vals[i], newval[(int)(loc[i])]);
        
            nzsub = newsub.tolist();
            nzval = newval.tolist();
            
            
            i = 0;
            while (i < len(nzsub)):
                if(nzval[i][0] == 0):
                    nzsub.remove(nzsub[i]);
                    nzval.remove(nzval[i]);
                else:
                    i = i+1;
                
        self.subs = numpy.array(nzsub);
        self.vals = numpy.array(nzval);        

    def ndims(self):
        return len(self.shape);
        
    def dimsize(self, ind):
        """ returns the size of the specified dimension.
        Same as shape[ind]."""
        return self.shape[ind];
    
    def nnz(self):
        """returns the number of non-zero elements in the sptensor"""
        return len(self.subs);
    
    def totensor(self):
        """returns a new tensor object that contains the same values"""
        temp = numpy.ndarray(self.shape);
        temp.fill(0);
        
        for i in range(0, len(self.vals)):
            temp.put(tools.sub2ind(self.shape, self.subs[i])[0], self.vals[i][0]);
        
        return tensor.tensor(temp, self.shape);
    
    
    
    def __str__(self):
        if (self.nnz() == 0):
            return "all zero sparse tensor of size {0}".format(self.shape);
        else:
            ret = "sparse tensor of size {0} with {1} non-zero elements\n".format(self.shape, self.nnz());
            for i in range (0, len(self.subs)):
                ret += "\n{0} {1}".format(self.subs[i], self.vals[i]);
            return ret;

    def copy(self):
        return sptensor(self.subs.copy(), self.vals.copy(),
                        self.shape, self.func);


    
      
    def permute(self, order):
        """returns a new sptensor permuted by the given order"""
        if (order.__class__ == list):
            order = numpy.array(order);
            
        if(self.ndims() != len(order)):
            raise ValueError("invalid permutation order")
        
        sortedorder = order.copy();
        sortedorder.sort();
        
        if not ((sortedorder == numpy.arange(len(self.shape))).all()):
            raise ValueError("invalid permutation order");
        
        neworder = numpy.arange(len(order)).tolist();
        newsiz = list(self.shape);
        newval = self.vals.copy();
        newsub = self.subs.copy();

        for i in range(0,len(order)-1):
            index = tools.find(neworder, order[i]);            
            
            for s in newsub:
                temp = s[i];
                s[i] = s[index];
                s[index] = temp;
            
            temp = newsiz[i];
            newsiz[i] = newsiz[index];
            newsiz[index] = temp;
            
            temp = neworder[i];
            neworder[i] = neworder[index];
            neworder[index] = temp;
            
        return sptensor(newsub, newval, newsiz, self.func);
    
    
    
    def ttm(self, mat, dims = None, option = None):
        """ computes the sptensor times the given matrix.
        arrs is a single 2-D matrix/array or a list of those matrices/arrays."""
        
        if(dims == None):
            dims = range(0,self.ndims());
        
        #Handle when arrs is a list of arrays
        if(mat.__class__ == list):
            if(len(mat) == 0):
                raise ValueError("the given list of arrays is empty!");
            
            (dims,vidx) = tools.tt_dimscehck(dims, self.ndims(), len(mat));
            
            Y = self.ttm(mat[vidx[0]],dims[0],option);
            for i in range(1, len(dims)):
                Y = Y.ttm(mat[vidx[i]],dims[i],option);
                
            return Y;                
        
        if(mat.ndim != 2):
            raise ValueError ("matrix in 2nd armuent must be a matrix!");

        if(option != None):
            if (option == 't'):
                mat = mat.transpose();
            else:
                raise ValueError ("unknown option.");          
        
        
        if(dims.__class__ == list):
            if(len(dims) != 1):
                raise ValueError("Error in number of elements in dims");
            else:
                dims = dims[0];
        
        if(dims < 0 or dims > self.ndims()):
            raise ValueError ("Dimension N must be between 1 and num of dimensions");
        
        #Check that sizes match
        if(self.shape[dims] != mat.shape[1]):
            raise ValueError ("size mismatch on V");
        
        #Compute the new size
        newsiz = list(self.shape);
        newsiz[dims] = mat.shape[0];
        
        #Compute Xn
        Xnt = sptenmat.sptenmat(self,None,[dims],None,'t');
        rdims = Xnt.rdims;
        cdims = Xnt.cdims;
        
        I = [];
        J = [];
        for i in range(0, len(Xnt.subs)):
            I.extend([Xnt.subs[i][0]]);
            J.extend([Xnt.subs[i][1]]);
        
        
        Z = (sparse.coo_matrix((Xnt.vals.flatten(),(I,J)),
            shape = (tools.getelts(Xnt.tsize, Xnt.rdims).prod(),
                     tools.getelts(Xnt.tsize, Xnt.cdims).prod()))
             * mat.transpose());
        
        Z = tensor.tensor(Z,newsiz).tosptensor();
        
        
        if(Z.nnz() <= 0.5 * numpy.array(newsiz).prod()):
            Ynt = sptenmat.sptenmat(Z, rdims, cdims);
            return Ynt.tosptensor();
        else:
            Ynt = tenmat.tenmat(Z.totensor(), rdims, cdims);
            return Ynt.totensor();
    
    def tondarray(self):
        """returns an ndarray that contains the data of the sptensor"""
        return self.totensor().tondarray();
    
    
    def __add__(self, other):
        if (other.__class__ == sptensor):
            if (not self.shape == other.shape):
                raise ValueError("Two sparse tensors must have the same shape");
            return sptensor(self.subs.tolist() + other.subs.tolist(),
                        self.vals.tolist() + other.vals.tolist(), self.shape);
        
        #other is a tensor or a scalar value
        return self.totensor() + other;

    def __sub__(self, other):
        if (other.__class__ == sptensor):
            if (not self.shape == other.shape):
                raise ValueError("Two sparse tensors must have the same shape");
            return sptensor(self.subs.tolist() + other.subs.tolist(),
                        self.vals.tolist() + (-other.vals).tolist(), self.shape);
            
        #other is a tensor or a scalar value
        return self.totensor() - other;
        

    def __eq__(self, oth):
        if(oth.__class__ == sptensor):
            if(self.shape != oth.shape):
                raise ValueError("Size Mismatch");
            sub1 = self.subs;
            sub2 = oth.subs;
            usub = union(sub1, sub2);
            ret = (tools.allIndices(oth.shape));
            
        elif(oth.__class__ == tensor):
            return self.__eq__(oth.tosptensor());
            
        elif(oth.__class__ == int or oth.__class__ == float or oth.__class__ == bool):
            newvals = (self.vals == oth);
            newvals = booltoint(newvals);
            return sptensor(self.subs, newvals, self.size);
            
        else:
            raise ValueError("error");

    def __ne__(self, oth):
        pass
        

    def __mul__(self, scalar):
        """multiples each element by the given scalar value"""
        if(scalar.__class__ == numpy.ndarray or
           scalar.__class__ == tensor.tensor or
           scalar.__class__ == sptensor):
            raise ValueError("multiplication is only with scalar value. use ttm, ttv, or ttt instead.");
        return sptensor(self.subs.copy(), self.vals.copy()*scalar, self.shape);
    
    def __pos__(self):
        pass; #do nothing
    def __neg__(self):
        return sptensor(self.subs.copy(), self.vals.copy() * -1 , self.shape);
    
    
    
#def sptenrand(shape, numelements):
#    """Special constructor. Construct an sptensor with the given shape and the number of elements."""
#    
#    count = 0;
#    
#    while(count < numelements && cnt)


def sptendiag(vals, shape = None):
    """special constructor, construct a sptensor with the given values in the diagonal"""
    #if shape is None or
    #number of dimensions of shape is less than the number of values given
    if (shape == None or len(shape) < len(vals)):
        shape = [len(vals)]*len(vals);
    else:
        shape = list(shape);
        for i in range(0, len(vals)):
            if(shape[i] < len(vals)):
                shape[i] = len(vals);
    
    subs = [];
    for i in range(0, len(vals)):
        subs.extend([[i]*len(shape)]);
    
    vals = numpy.array(vals).reshape([len(vals),1]);
    
    return sptensor(subs, vals, shape);







# Given 2-d array arr, find the unique rows and return the rows as 2-d array.
def uniquerows(arr):
    arrlist = arr.tolist();
    sortedlist = list(arrlist);
    sortedlist.sort();
    loc = numpy.ndarray([len(arrlist), 1]);
    
    if(len(sortedlist) != 0):
        i = 1;
        while i < len(sortedlist):
            if(sortedlist[i] == sortedlist[i-1]):
                sortedlist.remove(sortedlist[i]);
            else:
                i = i+1;
            
        for i in range(0, len(arrlist)):
            for j in range(0, len(sortedlist)):
                if(arrlist[i] == sortedlist[j]):
                    loc[i] = j;
                    break;
    
    return (numpy.array(sortedlist), loc);
    

#arr1, arr2: sorted list or sorted numpy.ndarray of subscripts.
#union returns the sorted union of arr1 and arr2.
def union(arr1, arr2):
    if(arr1.__class__ != list):
        a1 = arr1.tolist();
    else:
        a1 = arr1;
    if(arr2.__class__ != list):
        a2 = arr2.tolist();
    else:
        a2 = arr1;
    
    i = 0;
    j = 0;
    ret = numpy.array([]);
    
    if(len(a1) > 0):
        ret = [a1[i]];
        i = i+1;
    elif(len(a2) > 0):
        ret = [a2[j]];
        j = j+1;
    else:
        return numpy.array([[]]);
    
    while(i < len(a1) or j < len(a2)):
        if(i == len(a1)):
            ret = numpy.concatenate((ret, [a2[j]]), axis=0);
            j = j+1;
        elif(j == len(a2)):
            ret = numpy.concatenate((ret, [a1[i]]), axis=0);
            i = i+1;
        elif(a1[i] < a2[j]):
            ret = numpy.concatenate((ret, [a1[i]]), axis=0);
            i = i+1;
        elif(a1[i] > a2[j]):
            ret = numpy.concatenate((ret, [a2[j]]), axis=0);
            j = j+1;
        else:
            i = i+1;
    
    return ret;


    
