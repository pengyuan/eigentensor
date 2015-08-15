#!/usr/bin/env python
# coding: UTF-8
from __future__ import division
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import random
from mayavi import mlab
import numpy
import settings
from utils.correlation import correlation, nmi
from utils.sequence import init_data, intersect_sequence, alignment_sequence
from utils.tensor import sparsity, normalize, build_six_order_transition_tensor, shifted_tensor_three_mode_product, \
    check_six_order_transition_tensor, tensor_three_mode_product, validate_eigen_tensor, three_order_tensor_first_norm, \
    three_tensor_hadarmard


# 得到相关系数矩阵
def get_correlation_matrix(data, user_num):
    correlation_matrix = [[0 for i in range(user_num)] for j in range(user_num)]
    for i in range(user_num):
        for j in range(user_num):
            print data[i], data[j]
            seq_a, seq_b = intersect_sequence(data[i], data[j])
            if seq_a and seq_b:
                seq_a, seq_b = alignment_sequence(seq_a, seq_b)
                length = min(len(seq_a), len(seq_b))
                seq_a_cor = []
                seq_b_cor = []
                for k in range(length):
                    seq_a_cor.append(seq_a[k][1])
                    seq_b_cor.append(seq_b[k][1])
                # print str(i)+"与"+str(j)+"的互相关系数: "+str(numpy.corrcoef([seq_a_cor, seq_b_cor]))
                # print str(i)+"与"+str(j)+"的互相关系数: "+str(correlation(seq_a_cor, seq_b_cor))
                cor = correlation(seq_a_cor, seq_b_cor)
                if cor > 0:
                    correlation_matrix[i][j] = cor
                else:
                    correlation_matrix[i][j] = 0
                #correlation_matrix[i][j] = nmi(numpy.array(seq_a_cor), numpy.array(seq_b_cor))

            else:
                correlation_matrix[i][j] = 0
    return correlation_matrix


# Multivariate Transition Tensor：High Order State Transition Tensor
# init_tensor_type: 1.all_sum_one; 2.user_slice_sum_one
def mtt(data, user_num, poi_num, zero_adjustment=True):
    print "共有"+str(user_num)+"个用户"
    for key in data.keys():
        print "用户" + str(key) + "序列为" + str(data[key])

    correlation_matrix = get_correlation_matrix(data, user_num)
    nor_cor_matrix = normalize(correlation_matrix)
    print "归一化相关系数矩阵: ", nor_cor_matrix

    transition_tensor = build_six_order_transition_tensor(data, poi_num, nor_cor_matrix, zero_adjustment)
    print "转移张量非零元素占比:", sparsity(transition_tensor)
    print "转移张量是否满足随机性:", check_six_order_transition_tensor(transition_tensor)

    return transition_tensor



if __name__ == '__main__':
    # beijing = (39.433333, 41.05, 115.416667, 117.5)
    # haidian = (39.883333, 40.15, 116.05, 116.383333)
    region = (39.883333, 40.05, 116.05, 116.383333)
    filter_count = 600
    time_num = settings.TIME_SLICE

    data, axis_users, axis_pois, check_data = init_data(region, filter_count)
    user_num = len(axis_users)
    poi_num = len(axis_pois)
    transition_tensor = mtt(data, user_num, poi_num)

    # equal_all_sum_one: equal
    init_tensor1 = [[[1/(poi_num * time_num * user_num) for i in range(poi_num)] for j in range(time_num)] for k in range(user_num)]

    # random_all_sum_one
    temp_tensor = [[[random.random() for i in range(poi_num)] for j in range(time_num)] for k in range(user_num)]
    init_tensor2 = three_tensor_hadarmard(1/three_order_tensor_first_norm(temp_tensor), temp_tensor)

    # user_slice_sum_one
    init_tensor3 = [[[1/(poi_num * time_num * user_num) for i in range(poi_num)] for j in range(time_num)] for k in range(user_num)]

    res1, iterator__values1 = tensor_three_mode_product(transition_tensor, init_tensor1)
    print res1
    print sparsity(res1)

    x, y, z = numpy.mgrid[0:user_num, 0:time_num, 0:poi_num]
    # val = numpy.random.random(z.shape)

    print x.shape, y.shape, z.shape
    # Plot and show in mayavi2
    # pts = mlab.points3d(x, y, z, res1, scale_factor=0.4, transparent=False)
    # mlab.show()