#!/usr/bin/env python
# coding: UTF-8
from __future__ import division
import settings
from tensorlib import tensor, ttensor, tenmat, sptenmat, sptensor
import numpy
from scipy import sparse
from utils.sequence import init_data
from utils.tensor import sparsity, delta_tensor_norm, get_check_tensor, three_tensor_hadarmard, \
    three_order_tensor_first_norm, dta_normalize_tensor, validate_eigen_tensor


def dta(new_tensor, rank, variance_matrix_list=None, alpha=None):
    """Dynamic Tensor Analysis"""
    # number of order of the input tensor.
    order = new_tensor.ndims()

    # If the co-variacne matrices are not given,
    # initialize all of them to be 0
    if variance_matrix_list is None:
        variance_matrix_list = []
        dv = new_tensor.shape
        for i in range(0, order):
            variance_matrix_list.extend([sparse.coo_matrix(([], ([], [])), [dv[i], dv[i]])])

    # If the forgetting factor is not given, it is 1.
    if alpha is None:
        alpha = 1

    u = []
    new_variance_matrix_list = []
    for i in range(0, order):
        if new_tensor.__class__ == tensor.tensor:
            new_tensor_matricize = tenmat.tenmat(new_tensor, [i]).tondarray()
        elif new_tensor.__class__ == sptensor.sptensor:
            new_tensor_matricize = sptenmat.sptenmat(new_tensor, [i]).tosparsemat()
        elif new_tensor.__class__ == ttensor.ttensor:
            raise TypeError("It is not supported yet.")
            return
        else:
            raise TypeError("1st argument must be tensor, sptensor, or ttensor")
            return

        new_variance_matrix_list.extend([numpy.array(alpha*variance_matrix_list[i] + numpy.dot(new_tensor_matricize, new_tensor_matricize.transpose()))])
        # print "new,", new_variance_matrix_list
        (eigenvalue, eigenmatrix) = eigwrapper(new_variance_matrix_list[i], rank[i])
        u.extend([numpy.array(eigenmatrix)])

    # print new_tensor
    core = new_tensor.ttm(u, None, 't')
    reconstruct_tensor = ttensor.ttensor(core, u)
    print "core:", sparsity(core.tondarray().tolist())
    return reconstruct_tensor, new_variance_matrix_list


def eigwrapper(arr, n):
    """wrapper funcion for numpy.linalg.eig function.
    It returns (w,v) such that
    w is 1-d array of n largest magnitude eigenvalues
    v is 2-d array of normalized eigenvectors that v[:,i] is corresponding to
    the eigenvalue w[i]."""


    if n > len(arr):
        raise ValueError("n has to be less than or equal to the number of rows in arr")

    # print "arr:", arr
    (w, v) = numpy.linalg.eigh(arr)
    # print "wv:", w, v
    absw = numpy.abs(w)
    ind = absw.argsort()
    ind = list(ind)
    ind.reverse()

    # print "ind:", ind
    neww = numpy.array([]).reshape([1, 0])
    newv = numpy.array([]).reshape([len(arr), 0])
    for i in range(0, n):
        neww = numpy.concatenate((neww, w[ind[i]].reshape([1, 1])), axis=1)
        newv = numpy.concatenate((newv, v[:, ind[i]].reshape([len(arr), 1])), axis=1)

    return neww, newv


def test1():
    A = ttensor.ttensor(tensor.tenrands([2, 3, 4]), [numpy.random.random([10, 2]), numpy.random.random([30, 3]), numpy.random.random([40, 4])]).totensor()
    [a, b] = dta(A, [1, 2, 3])
    print a
    print b
    Core = numpy.arange(24).reshape([2, 3, 4])
    # Core = numpy.array([[1,3,5],[2,4,6]] , [[7,9,11],[8,10,12]])
    u1 = numpy.array([[1, 2], [3, 4]])
    u2 = numpy.array([[0, 1, 0], [1, 0, 1], [1, 1, 1]])
    u3 = numpy.array([[1, 1, 1, 1], [1, 2, 3, 4], [1, 1, 1, 1]])
    tt = ttensor.ttensor(tensor.tensor(Core), [u1, u2, u3])

    print tt
    [a, b] = dta(tt.totensor(), [1, 2, 3])
    print a
    print a.totensor()
    print b


def test2():
    # A = numpy.array([[1, 4, 7, 10], [2, 5, 8, 11], [3, 6, 9, 12]])
    # A = numpy.arange(12).reshape([4,3]) + 1
    A = numpy.arange(1000).reshape([10, 10, 10])+1
    (ans1, ans2) = dta(tensor.tensor(A), [2, 2, 2])
    print ans1
    for i in range(0, len(ans2)):
        print "{0} th array\n {1}".format(i, ans2[i])

    print ans1.totensor()


def eigwrappertest():
    A = numpy.arange(9).reshape([3, 3]) + 1
    (ans1, ans2) = numpy.linalg.eig(A)
    print ans1
    print ans2
    (ans1, ans2) = eigwrapper(A, 3)
    print ans1
    print ans2


# 得到数据序列
def data_stream(data, user_num, poi_num, time_interval):
    data_stream = []
    min_time = data[0][0][2]
    max_time = data[0][0][2]
    for key in data.keys():
        for item in data[key]:
            if min_time > item[2]:
                min_time = item[2]
            if item[2] > max_time:
                max_time = item[2]
    print min_time, max_time
    increment = 24 * 60 * 60 * time_interval
    start = int(min_time / increment)
    end = int(max_time / increment)
    if max_time % increment > 0:
        end += 1

    print "total "+str(end - start)+" days"

    for time_index in range(start, end):
        data_block = {}
        begin = time_index * increment
        end = (time_index + 1) * increment
        for key in data.keys():
            data_block[key] = []
            for item in data[key]:
                if begin <= item[2] <= end:
                    data_block[key].append(item)
        if len(data_block.keys()) > 0:
            data_stream.append(data_block)
        # else:
            # tensor_stream.append(None)
    return data_stream


# 得到张量序列
def tensor_stream(data, user_num, poi_num, time_interval):
    tensor_stream = []
    min_time = data[0][0][2]
    max_time = data[0][0][2]
    for key in data.keys():
        for item in data[key]:
            if min_time > item[2]:
                min_time = item[2]
            if item[2] > max_time:
                max_time = item[2]
    print min_time, max_time
    increment = 24 * 60 * 60 * time_interval
    start = int(min_time / increment)
    end = int(max_time / increment)
    if max_time % increment > 0:
        end += 1

    print "total "+str(end - start)+" days"

    for time_index in range(start, end):
        temp_tensor = []
        begin = time_index * increment
        end = (time_index + 1) * increment
        for key in data.keys():
            for item in data[key]:
                if begin <= item[2] <= end:
                    element = (key, item[0], item[1])
                    temp_tensor.append(element)
        if len(temp_tensor) > 0:
            tensor = [[[0 for i in range(poi_num)] for j in range(settings.TIME_SLICE)] for k in range(user_num)]
            for item in temp_tensor:
                tensor[item[0]][item[1]][item[2]] += 1
            tensor_stream.append(tensor)
        # else:
            # tensor_stream.append(None)
    return tensor_stream


if __name__ == '__main__':
    # print numpy.random.random([10, 2])
    # print tensor.tenrands([2, 3, 4])
    # A = ttensor.ttensor(tensor.tenrands([2, 3, 4]), [numpy.random.random([10, 2]), numpy.random.random([30, 3]), numpy.random.random([40, 4])]).totensor()
    # print A
    # [a, b] = dta(A, [1, 2, 3])
    # print "a:", a
    # print "b:", b
    region = (39.883333, 40.05, 116.05, 116.383333)
    filter_count = 600
    time_num = settings.TIME_SLICE
    train_percent = 0.4
    data, axis_users, axis_pois, check_data = init_data(region, filter_count, train_percent)
    user_num = len(axis_users)
    poi_num = len(axis_pois)

    # print data

    tensor_stream_res = tensor_stream(data, user_num, poi_num, 2)
    print len(tensor_stream_res)

    # def dta(new_tensor, rank, variance_matrix_list=None, alpha=None):
    #     return reconstruct_tensor, new_variance_matrix_list

    reconstruct_tensor = None
    variance_matrix_list = None
    for tensor_data in tensor_stream_res:
        # print "data:", sparsity(tensor_data)
        reconstruct_tensor, variance_matrix_list = dta(tensor.tensor(numpy.array(tensor_data)), (4, 2, 10), variance_matrix_list)
        # print sparsity(reconstruct_tensor.totensor().tondarray().tolist())

    res = reconstruct_tensor.totensor().tondarray().tolist()
    # print res
    print "最终张量:", sparsity(res)

    nor_res = dta_normalize_tensor(res, user_num, time_num, poi_num)
    check_tensor = get_check_tensor(check_data, user_num, time_num, poi_num)
    # print check_tensor
    residual = delta_tensor_norm(nor_res, check_tensor)

    print residual
    print nor_res
    print check_data
    print sparsity(check_tensor)
    print validate_eigen_tensor(nor_res), validate_eigen_tensor(check_tensor)