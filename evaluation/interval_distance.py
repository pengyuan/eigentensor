#!/usr/bin/env python
# coding: UTF-8
from __future__ import division
import pylab
from numpy import *


# 计算两个经纬度之间的距离，单位千米
from utils.sequence import init_data_by_user, init_data_by_user_return_gps


def calculate_distance(lat1, lng1, lat2, lng2):
    earth_radius = 6378.137
    rad_lat1 = rad(lat1)
    rad_lat2 = rad(lat2)
    a = rad_lat1 - rad_lat2
    b = rad(lng1) - rad(lng2)
    s = 2 * math.asin(
        math.sqrt(math.pow(math.sin(a / 2), 2) + math.cos(rad_lat1) * math.cos(rad_lat2) * math.pow(math.sin(b / 2), 2)))
    s *= earth_radius
    if s < 0:
        return round(-s, 2)
    else:
        return round(s, 2)


def rad(flo):
    return flo * math.pi / 180.0


# Calculating kernel density estimates
# z: position, w: bandwidth, xv: vector of points
def kde(z, w, xv):
    return sum(exp(-0.5*((z-xv)/w)**2)/sqrt(2*pi*w**2))


if __name__ == '__main__':
    filter_count = 800
    train_data, axis_users, axis_pois, check_data = init_data_by_user_return_gps(tuple(range(0, 180)), filter_count=0)
    data_length = len(train_data)
    print "data_length: ", data_length
    # print train_data
    y_data = []

    for key in train_data.keys():
        data_key = train_data[key]
        for i in range(len(data_key)-1):
            # print data_key
            y_data.append(calculate_distance(data_key[i][3], data_key[i][4], data_key[i+1][3], data_key[i+1][4]))

    print min(y_data), max(y_data)
    w = 0.1
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
    pylab.xlabel(u"跳转间距（千米）")
    pylab.ylabel(u"核密度分布值")
    pylab.title(u"跳转间距的核密度分布")
    pylab.legend(loc='upper right')
    pylab.show()