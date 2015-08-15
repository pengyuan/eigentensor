#!/usr/bin/env python
# coding: UTF-8
from __future__ import division
import numpy
import pylab
from build.multivariate_transition_tensor import mtt
import settings
from utils.sequence import init_data, init_data_by_user
from utils.tensor import tensor_three_mode_product, delta_tensor_norm, get_check_tensor, inreducible_tensor


if __name__ == '__main__':
    # beijing = (39.433333, 41.05, 115.416667, 117.5)
    # haidian = (39.883333, 40.15, 116.05, 116.383333)
    region = (39.883333, 40.05, 116.05, 116.383333)
    filter_count = 0
    time_num = settings.TIME_SLICE
    train_percent = 0.95
    alpha = 0.95

    x_values = []
    y_values1 = []
    y_values2 = []
    y_values3 = []

    # data, axis_users, axis_pois, check_data = init_data(region, filter_count, train_percent)
    data, axis_users, axis_pois, check_data = init_data_by_user(tuple([0, 3, 4, 5, 30]), filter_count, train_percent)
    user_num = len(axis_users)
    poi_num = len(axis_pois)

    init_tensor = [[[1/(poi_num * time_num * user_num) for i in range(poi_num)] for j in range(time_num)] for k in range(user_num)]
    transition_tensor = inreducible_tensor(mtt(data, user_num, poi_num), user_num, time_num, poi_num, alpha)
    res1, iterator_values1 = tensor_three_mode_product(transition_tensor, init_tensor)

    order = 1
    while order <= settings.ITERATOR_NUMBER:
        x_values.append(order)
        y_values1.append(iterator_values1[order])
        order += 1

    label = ""+str(((settings.TIME_SLICE*user_num*poi_num)**2))
    pylab.plot(x_values, y_values1, 'rs', linewidth=1, linestyle="-", label=label)


    data, axis_users, axis_pois, check_data = init_data_by_user(tuple([0, 3, 4]), filter_count, train_percent)
    user_num = len(axis_users)
    poi_num = len(axis_pois)

    init_tensor = [[[1/(poi_num * time_num * user_num) for i in range(poi_num)] for j in range(time_num)] for k in range(user_num)]
    transition_tensor = inreducible_tensor(mtt(data, user_num, poi_num), user_num, time_num, poi_num, alpha)
    res2, iterator_values2 = tensor_three_mode_product(transition_tensor, init_tensor)

    x_values = []
    order = 1
    while order <= settings.ITERATOR_NUMBER:
        x_values.append(order)
        y_values2.append(iterator_values2[order])
        order += 1

    print type(x_values)
    print x_values
    print type(y_values1)
    print type(y_values2)
    label = ""+str(((settings.TIME_SLICE*user_num*poi_num)**2))
    pylab.plot(x_values, y_values2, 'bs', linewidth=1, linestyle="-", label=label)


    data, axis_users, axis_pois, check_data = init_data_by_user(tuple([0, 3]), filter_count, train_percent)
    user_num = len(axis_users)
    poi_num = len(axis_pois)

    init_tensor = [[[1/(poi_num * time_num * user_num) for i in range(poi_num)] for j in range(time_num)] for k in range(user_num)]
    transition_tensor = inreducible_tensor(mtt(data, user_num, poi_num), user_num, time_num, poi_num, alpha)
    res3, iterator_values3 = tensor_three_mode_product(transition_tensor, init_tensor)

    x_values = []
    order = 1
    while order <= settings.ITERATOR_NUMBER:
        x_values.append(order)
        y_values3.append(iterator_values3[order])
        order += 1

    label = ""+str(((settings.TIME_SLICE*user_num*poi_num)**2))
    pylab.plot(x_values, y_values3, 'bs', linewidth=1, linestyle="-", label=label)


    pylab.xlabel(u"迭代次数")
    pylab.ylabel(u"log(连续两次迭代结果差的二范数)")
    pylab.title(u"不同α值的收敛速度")
    pylab.legend(loc='center right')
    pylab.show()