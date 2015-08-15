#!/usr/bin/env python
# coding: UTF-8
#Mutual information(MI) and Normalized mutual information(NMI) are often used to evaluate #clustering result. Here is a numpy and scipy implementation. I have verifed the result against #examples from Internet.
#http://blog.sun.tc/2010/10/mutual-informationmi-and-normalized-mutual-informationnmi-for-numpy.html
import numpy
from scipy import *


def mean(input_array):
    for i in range(0,(len(input_array)-1)):
        input_array[i] = float(input_array[i])
    total_sum = 0.00
    for value in input_array:
        total_sum = total_sum + value
    return float(total_sum/len(input_array))


def standard_deviation(input_array):
    mu = mean(input_array)
    variance_numerator = 0.00
    for val in input_array:
        variance_numerator += (val - mu)**2
    variance = variance_numerator/len(input_array)
    return sqrt(variance)


def covariance(x_array, y_array):
    if len(x_array) != len(y_array):
        return None
    x_mu = mean(x_array)
    y_mu = mean(y_array)
    covariance_numerator = 0.00
    for i in range(len(x_array)):
        covariance_numerator += (x_array[i] - x_mu)*(y_array[i] - y_mu)
    return covariance_numerator/len(x_array)


def correlation(x_array, y_array):
    if covariance(x_array, y_array) != None:
        dev_a = standard_deviation(x_array)
        dev_b = standard_deviation(y_array)
        if dev_a != 0 and dev_b != 0:
            return covariance(x_array, y_array)/(dev_a * dev_b)
        else:
            return None
    else:
        return None

#Mutual information
def mutual_info(x,y):
    N=float(x.size)
    I=0.0
    eps = numpy.finfo(float).eps
    for l1 in unique(x):
        for l2 in unique(y):
            #Find the intersections
            l1_ids=nonzero(x==l1)[0]
            l2_ids=nonzero(y==l2)[0]
            pxy=(float(intersect1d(l1_ids,l2_ids).size)/N)+eps
            I+=pxy*log2(pxy/((l1_ids.size/N)*(l2_ids.size/N)))
    return I

#Normalized mutual information
def nmi(x,y):
    N=x.size
    I=mutual_info(x,y)
    Hx=0
    for l1 in unique(x):
        l1_count=nonzero(x==l1)[0].size
        Hx+=-(float(l1_count)/N)*log2(float(l1_count)/N)
    Hy=0
    for l2 in unique(y):
        l2_count=nonzero(y==l2)[0].size
        Hy+=-(float(l2_count)/N)*log2(float(l2_count)/N)
    return I/((Hx+Hy)/2)


if __name__ == '__main__':
    xinp = [1, 2, 2, 4]
    yinp = [2, 2, 2, 4]
    zinp = [1, 4, 6, 8]
    tinp = [23, 34, 46, 57]
    print correlation(xinp, yinp)
    print correlation(xinp, zinp)
    print correlation(xinp, tinp)
    #Example from http://nlp.stanford.edu/IR-book
    #/html/htmledition/evaluation-of-clustering-1.html
    # print nmi(array([1,1,1,1,1,1,2,2,2,2,2,2,3,3,3,3,3], array([1,1,1,1,2,1,2,2,2,2,3,1,3,3,3,2,2,2])))
    print nmi(array(xinp), array(yinp))
    print nmi(array(xinp), array(zinp))
    print nmi(array(xinp), array(tinp))
    # print nmi(array([12]), array([12]))
    print nmi(array([1,2,3,4,24325]), array([2,23,32,621,123124]))
    print nmi(array([1,2,3,4,5]), array([5,4,3,2,1]))
    print correlation([1,2,3,4], [2,3,4,235])
    print numpy.corrcoef([[1,2,3],[2,3,4]])