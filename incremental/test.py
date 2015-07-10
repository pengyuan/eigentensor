#!/usr/bin/env python
# coding: UTF-8
from __future__ import division
import math
from random import randint
import numpy
import pylab
from eigentensor import pykov


def param(matrix_param):
    # print "param:::", matrix_param
    size = len(matrix_param)
    result_list = []
    for index in range(size):
        matrix = matrix_param[index]
        result = {}
        #{('A','B'): .3, ('A','A'): .7, ('B','A'): 1.}
        dimen = len(matrix)
        # print "dimen", dimen
        for i in range(dimen):
            for j in range(dimen):
                if matrix[i][j] != 0:
                    result[(i, j)] = matrix[i][j]
        result_list.append(result)
    return result_list


def param_single(matrix):
    result = {}
    #{('A','B'): .3, ('A','A'): .7, ('B','A'): 1.}
    dimen = len(matrix)
    # print "dimen", dimen
    for i in range(dimen):
        for j in range(dimen):
            if matrix[i][j] != 0:
                result[(i, j)] = matrix[i][j]
    return result


def vec(param, dimen):
    # param[(0, 0.3333333333333332), (2, 0.25000000000000006), (9, 0.24999999999999994), (11, 0.16666666666666671)]
    parameter = {}
    for item in param:
        #print "item:",item
        parameter[item[0]] = item[1]
    # print parameter

    preference = []
    for i in range(dimen):
        # print i
        if parameter.has_key(i):
            preference.append(parameter[i])
        else:
            preference.append(0.0)

    return preference


def combine_matrix(matrix_list, state_num, alpha):
    # print "matrix_list:::", matrix_list
    # print "alpha:::", alpha
    size = len(matrix_list)
    res_matrix = [[0 for col in range(state_num)] for row in range(state_num)]

    for index in range(size):
        for i in range(state_num):
            for j in range(state_num):
                res_matrix[i][j] += matrix_list[index][i][j] * alpha[index]
    return res_matrix


def combine_vector(vector_list, state_num, alpha):
    dimen = len(vector_list)
    res_vector = {}
    for state in range(state_num):
        res_vector[state] = 0
    for index in range(dimen):
        res_vector_temp = vector_list[index]
        for state in range(state_num):
            res_vector[state] += res_vector_temp[state] * alpha[index]
    return res_vector


def _norm(res_both, res_res_both):
    dimen = len(res_both.keys())
    sum = 0

    for index in range(dimen):
        sum += (res_both[index] - res_res_both[index])**2
    return math.sqrt(sum)


def stochastic(matrix_param):
    size = len(matrix_param)
    for index in range(size):
        matrix_item = matrix_param[index]
        dimen = len(matrix_item)
        for i in range(dimen):
            sum = 0
            for j in range(dimen):
                sum += matrix_item[i][j]
            for j in range(dimen):
                matrix_item[i][j] = matrix_item[i][j] / sum
    return matrix_param


if __name__ == '__main__':
    # matrix_1 = [[1/2, 1/4, 1/4], [1/3, 2/5, 4/15], [4/7, 2/7, 1/7]]
    # matrix_2 = [[3/8, 1/4, 3/8], [2/5, 1/5, 2/5], [1/9, 7/9, 1/9]]

    # matrix_1 = [[1/2, 1/2], [1/3, 2/3]]
    # matrix_2 = [[4/7, 3/7], [2/5, 3/5]]

    # matrix_1 = [[1/4, 1/4, 1/4, 1/4], [1/3, 2/9, 1/9, 1/3], [1/11, 3/11, 2/11, 5/11], [4/15, 2/15, 7/15, 2/15]]
    # matrix_2 = [[4/7, 1/7, 1/7, 1/7], [2/5, 1/5, 1/5, 1/5], [1/120, 7/120, 111/120, 1/120], [43/47, 2/47, 1/47, 1/47]]

    # matrix_1 = [[1/4, 1/4, 1/4, 1/8, 1/8], [1/3, 2/9, 1/9, 1/6, 1/6], [1/11, 3/11, 2/11, 1/11, 4/11], [4/15, 2/15, 7/15, 1/15, 1/15], [1/17, 2/17, 7/17, 7/34, 7/34]]
    # matrix_2 = [[4/7, 1/7, 1/7, 1/14, 1/14], [2/5, 1/5, 1/5, 1/10, 1/10], [1/120, 7/120, 111/120, 1/240, 1/240], [43/47, 2/47, 1/47, 1/94, 1/94], [15/19, 1/19, 1/19, 1/19, 1/19]]

    state_num = 5
    matrix_num = 50
    # alpha = (0.1, 0.2, 0.3, 0.3, 0.1)

    matrix_list = []
    for i in range(matrix_num):
        matrix_temp = [[randint(0, 100) for i in range(state_num)] for j in range(state_num)]
        matrix_list.append(matrix_temp)

    matrix = stochastic(matrix_list)

    # T = pykov.Matrix({('A','B'): randint(0, 100), ('A','A'): 7, ('B','A'): .2})
    # T.stochastic()

    input_param = param(matrix)
    # print input_param
    vector_list = []
    for index in range(len(input_param)):
        input_item = input_param[index]

        T = pykov.Chain(input_item)
        res = T.steady()
        print "res"+str(index)+": ", res
        vector_list.append(res)


    #
    # # 1/2 1/2
    # matrix_both = [[3/8, 5/8], [11/30, 19/30]]
    # T_both = pykov.Chain(param(matrix_both))
    # res_both = T_both.steady()
    # print "res_both: ", res_both
    #
    # print "res_res_both: ", (res_1[0]+res_2[0])/2, (res_1[1]+res_2[1])/2
    #
    # # 1/5 4/5
    # matrix_both2 = [[(1/2) * (1/5) + (1/4) * (4/5), (1/2) * (1/5) + (3/4) * (4/5)], [(1/3) * (1/5) + (2/5) * (4/5), (2/3) * (1/5) + (3/5) * (4/5)]]
    #
    # T_both2 = pykov.Chain(param(matrix_both2))
    # res_both2 = T_both2.steady()
    # print "res_both2: ", res_both2
    #
    # print "res_res_both2: ", (res_1[0]*(1/5)+res_2[0]*(4/5)), (res_1[1]*(1/5)+res_2[1]*(4/5))


    # depict

    a = 0/100
    x_values = []
    y_values = []

    while a <= 99/100:
        alpha = []
        alpha.append(a)
        for i in range(matrix_num-1):
            alpha.append((1-a)/(matrix_num-1))
        matrix_both = combine_matrix(matrix, state_num, alpha)
        # matrix_both = [[(1/2) * a + (1/4) * (1-a), (1/2) * a + (3/4) * (1-a)], [(1/3) * a + (2/5) * (1-a), (2/3) * a + (3/5) * (1-a)]]

        print "matrix_both:::", param_single(matrix_both)
        T_both = pykov.Chain(param_single(matrix_both))
        res_both = T_both.steady()
        res_dict = combine_vector(vector_list, state_num, alpha)


        norm_res = _norm(res_both, res_dict)

        print "a: ", a, "norm: ", norm_res
        # y_values1.append(sparsity(tensor))
        # y_values2.append(sparsity(A))
        y_values.append(norm_res)
        x_values.append(a)
        a += 1/100

    pylab.plot(x_values, y_values, 'ys', linewidth=1, linestyle="-", label=u"误差")
    pylab.xlabel(u"占比")
    pylab.ylabel(u"误差")
    pylab.title(u"占比与误差关系")
    pylab.legend(loc='upper right')
    # pylab.xlim(1, 10)
    # pylab.ylim(0, 1.)
    pylab.show()