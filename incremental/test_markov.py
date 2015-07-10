#!/usr/bin/env python
# coding: UTF-8
from __future__ import division
import math
from random import randint
import numpy
import pylab
from eigentensor import pykov


# A:宿舍  B:食堂  C:实验室
# ABCBACBCA
# {('A','A'): 0, ('A','B'): .5, ('A','C'): .5, ('B','A'): 1/3, ('B','B'):0, ('B','C'):2/3, ('C','A'):1/3, ('C','B'):2/3, ('C','C'):0}
if __name__ == '__main__':
    T = pykov.Chain({('A','A'): 0, ('A','B'): .5, ('A','C'): .5, ('B','A'): 1/3, ('B','B'):0, ('B','C'):2/3, ('C','A'):1/3, ('C','B'):2/3, ('C','C'):0} )
    print T.steady()


