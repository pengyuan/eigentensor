#!/usr/bin/env python
# coding: UTF-8
from __future__ import division
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import numpy
import pylab
from build.dynamic_tensor_analysis import dta, tensor_stream
from build.multivariate_transition_tensor import mtt
import settings
from tensorlib import tensor
from utils.sequence import init_data
from utils.tensor import tensor_three_mode_product, delta_tensor_norm, get_check_tensor, inreducible_tensor, sparsity, \
    dta_normalize_tensor


if __name__ == '__main__':
    # beijing = (39.433333, 41.05, 115.416667, 117.5)
    # haidian = (39.883333, 40.15, 116.05, 116.383333)
    region = (39.883333, 40.05, 116.05, 116.383333)
    filter_count = 600
    train_percent = 0.8
    alpha = 0.95

    x_values = []
    y_values1 = []
    y_values2 = []
    y_values3 = []

    while train_percent < 1:
        data, axis_users, axis_pois, check_data = init_data(region, filter_count, train_percent)
        user_num = len(axis_users)
        time_num = settings.TIME_SLICE
        poi_num = len(axis_pois)

        transition_tensor = inreducible_tensor(mtt(data, user_num, poi_num), user_num, time_num, poi_num, alpha)
        # equal_all_sum_one: equal
        init_tensor1 = [[[1/(poi_num * time_num * user_num) for i in range(poi_num)] for j in range(time_num)] for k in range(user_num)]

        res1, iterator_values = tensor_three_mode_product(transition_tensor, init_tensor1)
        # print res

        check_tensor = get_check_tensor(check_data, user_num, time_num, poi_num)
        residual1 = delta_tensor_norm(res1, check_tensor)

        tensor_stream_res = tensor_stream(data, user_num, poi_num, 10)
        print "张量流长度:"+str(len(tensor_stream_res))

        data_stream_res = data_stream(data, user_num, poi_num, 10)
        print "数据流长度:"+str(len(data_stream_res))
        # def dta(new_tensor, rank, variance_matrix_list=None, alpha=None):
        #     return reconstruct_tensor, new_variance_matrix_list

        reconstruct_tensor = None
        variance_matrix_list = None
        for tensor_data in tensor_stream_res[:-2]:
            # print "data:", sparsity(tensor_data)
            reconstruct_tensor, variance_matrix_list = dta(tensor.tensor(numpy.array(tensor_data)), (4, 2, 200), variance_matrix_list)
            # print sparsity(reconstruct_tensor.totensor().tondarray().tolist())

        res2 = reconstruct_tensor.totensor().tondarray().tolist()
        print res2

        nor_res = dta_normalize_tensor(res2, user_num, time_num, poi_num)
        print "最终张量:", sparsity(res2)
        print nor_res

        # check_tensor = get_check_tensor(check_data, user_num, time_num, poi_num)
        # print check_tensor
        residual2 = delta_tensor_norm(nor_res, check_tensor)

        statistic_res = get_check_tensor(data, user_num, time_num, poi_num)
        residual3 = delta_tensor_norm(statistic_res, check_tensor)

        x_values.append(train_percent)
        y_values1.append(residual1)
        y_values2.append(residual2)
        y_values3.append(residual3)
        train_percent += 0.2

    pylab.plot(x_values, y_values1, 'rs', linewidth=1, linestyle="-", label=u"MTT")
    pylab.plot(x_values, y_values2, 'ks', linewidth=1, linestyle="-", label=u"DTA")
    pylab.plot(x_values, y_values3, 'gs', linewidth=1, linestyle="-", label=u"Baseline")
    pylab.xlabel(u"训练集比重")
    pylab.ylabel(u"平均误差")
    pylab.title(u"训练集比重与平均误差的关系")
    pylab.legend(loc='center right')
    pylab.show()