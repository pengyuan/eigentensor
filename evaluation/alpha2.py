#!/usr/bin/env python
# coding: UTF-8
from __future__ import division
import math
import matplotlib.pyplot as plt
from build.multivariate_transition_tensor import mtt
import settings
from utils.sequence import init_data
from utils.tensor import tensor_three_mode_product, delta_tensor_norm, get_check_tensor, \
    tensor_three_mode_product_with_norm, inreducible_tensor


if __name__ == '__main__':
    # beijing = (39.433333, 41.05, 115.416667, 117.5)
    # haidian = (39.883333, 40.15, 116.05, 116.383333)
    region = (39.883333, 40.05, 116.05, 116.383333)
    filter_count = 600
    time_num = settings.TIME_SLICE
    alpha = 0.9
    train_percent = 0.5

    values = []
    x_values = []
    y_values1 = []
    y_values2 = []
    y_values3 = []
    y_values4 = []

    order = 1
    while alpha >= 0.2:
        data, axis_users, axis_pois, check_data = init_data(region, filter_count, train_percent)
        user_num = len(axis_users)
        poi_num = len(axis_pois)

        transition_tensor = inreducible_tensor(mtt(data, user_num, poi_num), user_num, time_num, poi_num, alpha)

        # equal_all_sum_one: equal
        init_tensor = [[[1/(poi_num * time_num * user_num) for i in range(poi_num)] for j in range(time_num)] for k in range(user_num)]
        res, iterator_values = tensor_three_mode_product(transition_tensor, init_tensor)

        values.append(iterator_values)
        alpha -= 0.2

    print values
    # print values.keys()
    value1 = values[0]
    value2 = values[1]
    value3 = values[2]
    value4 = values[3]
    for index in range(1, settings.ITERATOR_NUMBER+1):
        x_values.append(index)
        y_values1.append(math.log10(value1[index]))
        y_values2.append(math.log10(value2[index]))
        y_values3.append(math.log10(value3[index]))
        y_values4.append(math.log10(value4[index]))

    plt.plot(x_values, y_values1, 'rs', linewidth=1, linestyle="-", label=u"α=0.9")
    plt.plot(x_values, y_values2, 'gs', linewidth=1, linestyle="-", label=u"α=0.7")
    plt.plot(x_values, y_values3, 'bs', linewidth=1, linestyle="-", label=u"α=0.5")
    plt.plot(x_values, y_values4, 'ks', linewidth=1, linestyle="-", label=u"α=0.3")

    plt.xlabel(u"迭代次数")
    plt.ylabel(u"log(连续两次迭代结果差的二范数)")
    plt.title(u"不同α值的收敛速度")
    plt.legend(loc='center right')
    plt.show()