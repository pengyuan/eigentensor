#!/usr/bin/env python
# coding: UTF-8
from __future__ import division
import pylab
from numpy import *


# 计算两个经纬度之间的距离，单位千米
from utils.sequence import init_data_by_user, init_data_by_user_return_gps


def calculate_time(time_from, time_to):
    interval = (time_to - time_from)//60
    if interval > 60*60:
        print interval, "...................."
        return None
    else:
        return interval


# Calculating kernel density estimates
# z: position, w: bandwidth, xv: vector of points
def kde(z, w, xv):
    return sum(exp(-0.5*((z-xv)/w)**2)/sqrt(2*pi*w**2))


if __name__ == '__main__':
    filter_count = 0
    train_data, axis_users, axis_pois, check_data = init_data_by_user_return_gps(tuple(range(0, 180)), filter_count)
    data_length = len(train_data)
    print "data_length: ", data_length
    # print train_data
    y_data = []

    for key in train_data.keys():
        data_key = train_data[key]
        for i in range(len(data_key)-1):
            # print data_key
            interval = calculate_time(data_key[i][2], data_key[i+1][2])
            if interval:
                y_data.append(interval)

    print min(y_data), max(y_data)
    w = 1.0
    y_values = []
    x_values = []
    res = 0
    max_y_value = 0
    for index, x in enumerate(linspace(min(y_data), max(y_data), 1000)):
        y = kde(x, w, y_data)
        y_values.append(y)
        x_values.append(x)

        # flag += 1
        if y >= max_y_value:
            max_y_value = y
            res = index

    print res
    print x_values[res]

    pylab.plot(x_values, y_values, 'r.')
    pylab.xlabel(u"跳转时间（分钟）")
    pylab.ylabel(u"核密度分布值")
    pylab.title(u"跳转时间的核密度分布")
    pylab.legend(loc='upper right')
    pylab.show()