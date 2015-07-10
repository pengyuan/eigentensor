#!/usr/bin/env python

import numpy;
import sptensor;
import tools;
from scipy import sparse;

class sptenmat:
    
    subs = None;
    vals = None;
    rdims = None;
    cdims = None;
    tsize = None;
    
    def __init__(self, T, rdim = None, cdim = None, tsiz = None, option = None):
        """Create a sptenmat object from a given ndarray or sptensor T"""
               
        if(rdim != None and rdim.__class__ == list):
            rdim = numpy.array(rdim);
        if(cdim != None and cdim.__class__ == list):
            cdim = numpy.array(cdim);
        if(tsiz != None and tsiz.__class__ == list):
            tsiz = numpy.array(tsiz);
        
        #subs, vals, rdims, cdims, tsize are all given
        
        #When I is a (2-D) ndarray or sptensor, and rdim, cdim, tsiz are given
        if(rdim != None and cdim != None and tsiz != None):
            
            B = T.flatten().reshape(len(T), T.size / len(T));
            subs = [];
            vals = [];
            maxrowind = 0;
            maxcolind = 0;
            for i in range(0,len(B)):
                for j in range(0, len(B[0])):
                    if(B[i][j] != 0):
                        subs.extend([[i,j]]);
                        vals.extend([B[i][j]]);
                        if(i > maxrowind): maxrowind = i;
                        if(j > maxcolind): maxcolind = j;
            
            self.subs = numpy.array(subs);
            self.vals = numpy.array(vals);
            self.rdims = rdim.copy();
            self.cdims = cdim.copy();
            self.tsize = tsiz;
            
            n = len(self.tsize);
            
            temp = numpy.concatenate((self.rdims,self.cdims));
            temp.sort();
            if not ((numpy.arange(n) == temp).all()):
                raise ValueError ("Incorrect specification of dimensions");
            if (tools.getelts(self.tsize, self.rdims).prod() < maxrowind):
                raise ValueError ("error, invalid row index");
            if (tools.getelts(self.tsize, self.cdims).prod() < maxcolind):
                raise ValueError ("error, invalid column index");
            return;
    
    
        # T is a sptensor
        T = T.copy();
        self.tsize = T.shape;
        self.subs = T.subs;
        self.vals = T.vals;
        n = T.ndims();
        
        if (rdim != None):
            if(cdim != None):
                self.rdims = rdim;
                self.cdims = cdim;
                
            elif(option != None):
                if(option == 'fc'):
                    self.rdims = rdim;
                    if(self.rdims.size != 1):
                        raise ValueError ("only one row dimension for 'fc' option");
                    
                    self.cdims = [];
                    for i in range(self.rdim[0]+1,n):
                        self.cdims.append(i);
                    for i in range(0, self.rdim[0]):
                        self.cdims.append(i);
                    self.cdims = numpy.array(self.cdims);
                    
                    
                elif(option == 'bc'):
                    self.rdims = rdim;
                    if(self.rdims.size != 1):
                        raise ValueError ("only one row dimension for 'bc' option");
                    
                    
                    self.cdims = [];
                    for i in range(0, self.rdim[0])[::-1]:
                        self.cdims.append(i);
                    for i in range(self.rdim[0]+1,n)[::-1]:
                        self.cdims.append(i);
                    self.cdims = numpy.array(self.cdims);
                                        
                else:
                    raise ValueError ("unknown option: {0}".format(option));
            
            else:
                self.rdims = rdim;
                self.cdims = tools.notin(n, self.rdims);
                
        elif(cdim != None):
            self.cdims = cdim;
            if(option == 't'):
                self.rdims = tools.notin(n, self.cdims);
            else:
                raise ValueError ("unknown option: {0}".format(option));
        else:
            raise ValueError("Both rdims and cdims are None");
    
    
        #error check
        temp = numpy.concatenate((self.rdims,self.cdims));
        temp.sort();
        if not ((numpy.arange(n) == temp).all()):
            raise ValueError ("Incorrect specification of dimensions");
            
        rsize = tools.getelts(self.tsize, self.rdims);
        csize = tools.getelts(self.tsize, self.cdims);
        
        
        if (len(rsize) == 0):
            ridx = numpy.ndarray([T.nnz()]);
            ridx.fill(0);
        else:
            temp1 = [];
            for i in range (0, len(self.subs)):
                temp2 = [];
                for j in range(0, len(self.rdims)):
                    temp2.extend([self.subs[i][self.rdims[j]]]);
                temp1.extend([temp2]);
            temp1 = numpy.array(temp1);
            ridx = tools.sub2ind(rsize, temp1);
            
    
        if (len(csize) == 0):
            cidx = numpy.ndarray([T.nnz()]);
            cidx.fill(0);
            
        else:
            temp1 = [];
            for i in range (0, len(self.subs)):
                temp2 = [];
                for j in range(0, len(self.cdims)):
                    temp2.extend([self.subs[i][self.cdims[j]]]);
                temp1.extend([temp2]);
                
            temp1 = numpy.array(temp1);
            cidx = tools.sub2ind(csize, temp1);
            
        
        self.subs = [];
        for i in range(0,len(ridx)):
            self.subs.extend([[ridx[i][0], cidx[i][0]]]);
        self.subs = numpy.array(self.subs);
    
    
    def tosptensor(self):
        # extract the shape of sptensor
        newshape = self.tsize;
        
        #extract the subscripts of sptensor
        rowsubs = [];
        if (len(self.rdims) != 0):
            rowshape = [];
            for i in range(0, len(self.rdims)):
                rowshape.extend([self.tsize[self.rdims[i]]]);
                
            for i in range(0, len(self.subs)):
                rowsubs.extend([tools.ind2sub(rowshape,self.subs[i][0])]);
        rowsubs = numpy.array(rowsubs);
        
        colsubs = [];
        if (len(self.cdims) != 0):
            colshape = [];
            for i in range(0, len(self.cdims)):
                colshape.extend([self.tsize[self.cdims[i]]]);
                
            for i in range(0, len(self.subs)):
                colsubs.extend([tools.ind2sub(colshape,self.subs[i][1])]);
        colsubs = numpy.array(colsubs);
        
        newsubs = [];
        for i in range(0, len(self.subs)):
            newsubs.extend([[]]);
        
        
        for k in range(0, len(newshape)):
            find = tools.find(self.rdims,k);
            if(find != -1):
                newsubs = numpy.concatenate((newsubs, rowsubs[:,find].reshape([len(self.subs),1])), axis = 1);
            else:
                find = tools.find(self.cdims,k);
                newsubs = numpy.concatenate((newsubs, colsubs[:,find].reshape([len(self.subs),1])), axis = 1);
        
        #extract the values of sptensor
        newvals = self.vals;
        
        return sptensor.sptensor(newsubs, newvals, newshape);
        
    def tosparsemat(self):
        """returns a sparse matrix object(scipy.sparse) that contains the same values"""
        m = 1;
        for i in range(0, len(self.rdims)):
            m = m * self.tsize[self.rdims[i]];
        n = 1;
        for i in range(0, len(self.cdims)):
            n = n * self.tsize[self.cdims[i]];
        
        return sparse.coo_matrix((self.vals.flatten(),
                               (self.subs[:,0], self.subs[:,1])),
            shape = [m,n]);
            
        
    def __str__(self):
        ret ="";
        ret += "sptenmat from an sptensor of size {0} with {1} nonzeros\n".format(self.tsize, len(self.vals));
        ret += "rindices {0}\n".format(self.rdims);
        ret += "cindices {0}\n".format(self.cdims);
        
        for i in range(0,len(self.vals)):
            ret += "{0} {1}\n".format(self.subs[i], self.vals[i]);
        
        return ret;