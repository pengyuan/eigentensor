#!/usr/bin/env python
# coding: UTF-8
from __future__ import division
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import random
import pylab
from build.multivariate_transition_tensor import mtt
import settings
from utils.sequence import init_data
from utils.tensor import three_tensor_hadarmard, three_order_tensor_first_norm, tensor_three_mode_product, \
    analysis_eigen_tensor, inreducible_tensor, check_six_order_transition_tensor, shifted_tensor_three_mode_product


if __name__ == '__main__':
    # beijing = (39.433333, 41.05, 115.416667, 117.5)
    # haidian = (39.883333, 40.15, 116.05, 116.383333)
    region = (39.883333, 40.05, 116.05, 116.383333)
    filter_count = 500
    alpha_shift1 = -0.01
    alpha_shift2 = 0.01
    alpha_shift3 = 0.02
    alpha_shift4 = 0.1


    data, axis_users, axis_pois, check_data = init_data(region, filter_count)
    user_num = len(axis_users)
    time_num = settings.TIME_SLICE
    poi_num = len(axis_pois)

    # transition_tensor = mtt(data, user_num, poi_num)
    # transition_tensor2 = inreducible_tensor(transition_tensor, user_num, time_num, poi_num, alpha)
    transition_tensor3 = mtt(data, user_num, poi_num, zero_adjustment=False)

    # equal_all_sum_one: equal
    # init_tensor1 = [[[1/(poi_num * time_num * user_num) for i in range(poi_num)] for j in range(time_num)] for k in range(user_num)]
    # # random_all_sum_one: no zero element
    # temp_tensor = [[[random.choice([1, 2, 3, 100]) for i in range(poi_num)] for j in range(time_num)] for k in range(user_num)]
    # init_tensor2 = three_tensor_hadarmard(1/three_order_tensor_first_norm(temp_tensor), temp_tensor)
    #
    # init_tensor3 = [[[0 for i in range(poi_num)] for j in range(time_num)] for k in range(user_num)]
    # init_tensor3[0][0][0] = 1
    # # random_all_sum_one: exist zero element
    # temp_tensor = [[[random.choice([0, 1, 2, 3, 4]) for i in range(poi_num)] for j in range(time_num)] for k in range(user_num)]
    # init_tensor3 = three_tensor_hadarmard(1/three_order_tensor_first_norm(temp_tensor), temp_tensor)
    # # user_slice_sum_one: equal
    # init_tensor4 = [[[1/(poi_num * time_num) for i in range(poi_num)] for j in range(time_num)] for k in range(user_num)]
    # # user_slice_sum_one: no zero element
    # temp_tensor = [[[random.choice([1, 2, 3, 4]) for i in range(poi_num)] for j in range(time_num)] for k in range(user_num)]
    # init_tensor5 = user_slice_sum_one(temp_tensor)
    # # user_slice_sum_one: exist zero element
    # temp_tensor = [[[random.choice([0, 1, 2, 3, 4]) for i in range(poi_num)] for j in range(time_num)] for k in range(user_num)]
    # init_tensor6 = user_slice_sum_one(temp_tensor)

    # res1, iterator_values1 = tensor_three_mode_product(transition_tensor, init_tensor1)
    # res2, iterator_values2 = tensor_three_mode_product(transition_tensor, init_tensor2)
    # res3, iterator_values3 = tensor_three_mode_product(transition_tensor, init_tensor3)
    #
    # print analysis_eigen_tensor(init_tensor1)
    # print analysis_eigen_tensor(init_tensor2)
    # print analysis_eigen_tensor(init_tensor3)
    #
    # print analysis_eigen_tensor(res1)
    # print analysis_eigen_tensor(res2)
    # print analysis_eigen_tensor(res3)

    temp_tensor = [[[random.choice([0, 1, 1000]) for i in range(poi_num)] for j in range(time_num)] for k in range(user_num)]
    temp_tensor = three_tensor_hadarmard(1/three_order_tensor_first_norm(temp_tensor), temp_tensor)

    print "初始张量性质:\n"
    print analysis_eigen_tensor(temp_tensor, "user")
    print analysis_eigen_tensor(temp_tensor, "time")
    print analysis_eigen_tensor(temp_tensor, "poi")
    print "\n"

    temp_tensor1 = temp_tensor
    temp_tensor2 = temp_tensor
    temp_tensor3 = temp_tensor
    temp_tensor4 = temp_tensor

    res1, iterator_values1 = shifted_tensor_three_mode_product(transition_tensor3, temp_tensor1, alpha_shift1)
    res2, iterator_values2 = shifted_tensor_three_mode_product(transition_tensor3, temp_tensor2, alpha_shift2)
    res3, iterator_values3 = shifted_tensor_three_mode_product(transition_tensor3, temp_tensor3, alpha_shift3)
    res4, iterator_values4 = shifted_tensor_three_mode_product(transition_tensor3, temp_tensor4, alpha_shift4)

    print analysis_eigen_tensor(res1, "user")
    print analysis_eigen_tensor(res1, "time")
    print analysis_eigen_tensor(res1, "poi")
    print "\n"

    print analysis_eigen_tensor(res2, "user")
    print analysis_eigen_tensor(res2, "time")
    print analysis_eigen_tensor(res2, "poi")
    print "\n"

    print analysis_eigen_tensor(res3, "user")
    print analysis_eigen_tensor(res3, "time")
    print analysis_eigen_tensor(res3, "poi")
    print "\n"

    print analysis_eigen_tensor(res4, "user")
    print analysis_eigen_tensor(res4, "time")
    print analysis_eigen_tensor(res4, "poi")
    print "\n"

    # init_tensor1 = three_tensor_hadarmard(1/three_order_tensor_first_norm(temp_tensor), temp_tensor)
    #
    # init_tensor2 = [[[1/(poi_num * time_num * user_num) for i in range(poi_num)] for j in range(time_num)] for k in range(user_num)]
    #
    # init_tensor3 = [[[0 for i in range(poi_num)] for j in range(time_num)] for k in range(user_num)]
    # init_tensor3[0][0][0] = 1
    #
    # print analysis_eigen_tensor(init_tensor1, "user")
    # print analysis_eigen_tensor(init_tensor1, "time")
    # print analysis_eigen_tensor(init_tensor1, "poi")
    #
    # print analysis_eigen_tensor(init_tensor2, "user")
    # print analysis_eigen_tensor(init_tensor2, "time")
    # print analysis_eigen_tensor(init_tensor2, "poi")
    #
    # print analysis_eigen_tensor(init_tensor3, "user")
    # print analysis_eigen_tensor(init_tensor3, "time")
    # print analysis_eigen_tensor(init_tensor3, "poi")
    #
    # res1, iterator_values1 = tensor_three_mode_product(transition_tensor, init_tensor1)
    # res2, iterator_values2 = tensor_three_mode_product(transition_tensor, init_tensor2)
    # res3, iterator_values3 = tensor_three_mode_product(transition_tensor, init_tensor3)
    #
    # print analysis_eigen_tensor(res1, "user")
    # print analysis_eigen_tensor(res1, "time")
    # print analysis_eigen_tensor(res1, "poi")
    #
    # print analysis_eigen_tensor(res2, "user")
    # print analysis_eigen_tensor(res2, "time")
    # print analysis_eigen_tensor(res2, "poi")
    #
    # print analysis_eigen_tensor(res3, "user")
    # print analysis_eigen_tensor(res3, "time")
    # print analysis_eigen_tensor(res3, "poi")
    #
    print res1
    print res2
    print res3
    print res4
    # res4, iterator_values4 = tensor_three_mode_product(transition_tensor, init_tensor4)
    # res5, iterator_values5 = tensor_three_mode_product(transition_tensor, init_tensor5)
    # res6, iterator_values6 = tensor_three_mode_product(transition_tensor, init_tensor6)
    # print "res1:", res1
    # print "res2:", res2
    # print "res3:", res3
    #
    # print "res4:", res4
    # res4_ = three_tensor_hadarmard(1/three_order_tensor_first_norm(res4), res4)
    # print "res4_:", res4_
    #
    # print "res5:", res5
    # res5_ = three_tensor_hadarmard(1/three_order_tensor_first_norm(res5), res5)
    # print "res5_:", res5_
    #
    # print "res6:", res6
    # res6_ = three_tensor_hadarmard(1/three_order_tensor_first_norm(res6), res6)
    # print "res6_:", res6_
    #
    x_values = []
    y_values1 = []
    y_values2 = []
    y_values3 = []
    y_values4 = []
    # # y_values5 = []
    # # y_values6 = []
    # #
    order = 1
    while order <= 50:
        x_values.append(order)
        y_values1.append(iterator_values1[order])
        y_values2.append(iterator_values2[order])
        y_values3.append(iterator_values3[order])
        y_values4.append(iterator_values4[order])
    #     y_values5.append(iterator_values5[order])
    #     y_values6.append(iterator_values6[order])
        order += 1
    #
    pylab.plot(x_values, y_values1, 'rs', linewidth=1, linestyle="-", label=u"shifted(α=-0.01)")
    pylab.plot(x_values, y_values2, 'ks', linewidth=1, linestyle="-", label=u"shifted(α=0.01)")
    pylab.plot(x_values, y_values3, 'bs', linewidth=1, linestyle="-", label=u"shifted(α=0.02)")
    pylab.plot(x_values, y_values4, 'ys', linewidth=1, linestyle="-", label=u"shifted(α=0.1)")
    # pylab.plot(x_values, y_values5, 'gs', linewidth=1, linestyle="-", label=u"用户-随机")
    # pylab.plot(x_values, y_values6, 'cs', linewidth=1, linestyle="-", label=u"用户-随机：含零元素")

    pylab.xlabel(u"迭代次数")
    pylab.ylabel(u"delta")
    pylab.title(u"迭代次数与收敛关系")
    pylab.legend(loc='center right')
    pylab.show()