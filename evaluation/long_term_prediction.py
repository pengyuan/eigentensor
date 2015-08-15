#!/usr/bin/env python
# coding: UTF-8
from __future__ import division
import pylab
from build.multivariate_transition_tensor import mtt
import settings
from utils.sequence import init_data
from utils.tensor import tensor_three_mode_product, delta_tensor_norm, get_check_tensor, \
    tensor_three_mode_product_with_norm, inreducible_tensor


if __name__ == '__main__':
    # beijing = (39.433333, 41.05, 115.416667, 117.5)
    # haidian = (39.883333, 40.15, 116.05, 116.383333)
    region = (39.883333, 40.05, 116.05, 116.383333)
    filter_count = 800
    time_num = settings.TIME_SLICE
    alpha = 0.95
    train_percent = 0.9

    x_values = []
    y_values1 = []
    y_values2 = []
    y_values3 = []

    order = 1
    data, axis_users, axis_pois, check_data = init_data(region, filter_count, train_percent)
    user_num = len(axis_users)
    poi_num = len(axis_pois)

    transition_tensor = inreducible_tensor(mtt(data, user_num, poi_num), user_num, time_num, poi_num, alpha)

    # equal_all_sum_one: equal
    init_tensor = [[[1/(poi_num * time_num * user_num) for i in range(poi_num)] for j in range(time_num)] for k in range(user_num)]
    res, iterator_values, norms = tensor_three_mode_product_with_norm(transition_tensor, init_tensor)
    index = 1

    while index <= settings.ITERATOR_NUMBER:
        x_values.append(index)
        y_values1.append(norms[index][0])
        y_values2.append(norms[index][1])
        y_values3.append(norms[index][2])
        index += 1

    pylab.plot(x_values, y_values1, 'rs', linewidth=1, linestyle="-", label=u"一范数")
    pylab.plot(x_values, y_values2, 'gs', linewidth=1, linestyle="-", label=u"二范数")
    pylab.plot(x_values, y_values3, 'bs', linewidth=1, linestyle="-", label=u"最大值范数")
    pylab.xlabel(u"迭代次数")
    pylab.ylabel(u"范数大小")
    pylab.title(u"迭代次数与各范数大小关系")
    pylab.legend(loc='center right')
    pylab.show()