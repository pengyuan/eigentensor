#!/usr/bin/env python
# coding: UTF-8

from __future__ import division
import math
import MySQLdb
import numpy
import settings

__author__ = 'Peng Yuan <pengyuan.org@gmail.com>'
__copyright__ = 'Copyright (c) 2014 Peng Yuan'
__license__ = 'Public domain'


# 连接数据库
def init_data(region, train_percent, filter_count):
    conn = MySQLdb.connect(host=settings.HOST, user=settings.USER, passwd=settings.PASSWORD, db=settings.DB)
    cursor = conn.cursor()
    result = 0

    # 得到区域用户所有位置移动信息，按时间排序
    try:
        sql = "select user_id from geolife where latitude between "+str(region[0])+" and "+str(region[1])+" and longtitude between "+str(region[2])+" and "+str(region[3])+" group by user_id having count(*) > "+str(filter_count)
        result = cursor.execute(sql)
        result = cursor.fetchall()
        conn.commit()
    except Exception, e:
        print e
        conn.rollback()

    user_available = []
    for item in result:
        user_available.append(int(item[0]))

    db_data = {}
    if len(user_available) == 0:
        raise "没有足够数据"
    try:
        for user in user_available:
            sql = "select user_id, latitude, longtitude, gps_datetime from geolife where user_id = "+str(user)+" and latitude between "+str(region[0])+" and "+str(region[1])+" and longtitude between "+str(region[2])+" and "+str(region[3])+" order by id"
            result = cursor.execute(sql)
            result = cursor.fetchall()
            conn.commit()
            db_data[user] = result
    except Exception, e:
        print e
        conn.rollback()

    temp_data = []
    for item in result:
        temp_data.append((item[0], item[1], item[2], item[3], item[4], item[5]))

    cursor.close()
    conn.close()
    return temp_data, time_slice, train


def init_gps(users, return_gps=False):
    conn = MySQLdb.connect(host=settings.HOST, user=settings.USER, passwd=settings.PASSWORD, db=settings.DB)
    cursor = conn.cursor()
    result = 0

    try:
        if len(users) == 1:
            sql = "select latitude, longitude from geolife where user_id = "+str(users[0])+" order by id"
        else:
            sql = "select latitude, longitude from geolife where user_id in "+users.__str__()+" order by id"
        result = cursor.execute(sql)
        result = cursor.fetchall()
        conn.commit()
    except Exception, e:
        print e
        conn.rollback()

    print len(result)

    data = []
    for item in result:
        data.append((item[0], item[1]))

    cursor.close()
    conn.close()

    return data


def get_length_height(beijing):
    # calculate_distance(lat1, lng1, lat2, lng2)
    length = calculate_distance(beijing[0], beijing[2], beijing[0], beijing[3])
    length2 = calculate_distance(beijing[1], beijing[2], beijing[1], beijing[3])
    height = calculate_distance(beijing[0], beijing[2], beijing[1], beijing[2])
    height2 = calculate_distance(beijing[0], beijing[3], beijing[1], beijing[3])
    print "length: ", length, length2
    print "height: ", height, height2

    return length, height, (beijing[1], beijing[2])


# 计算两个经纬度之间的距离，单位千米
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


def get_grid_num(grid_matrix, index_i, index_j):
    return grid_matrix[index_i][index_j]


def get_axis(grid_matrix, grid_num):
    horizontal_size = numpy.array(grid_matrix).shape[0]
    vertical_size = numpy.array(grid_matrix).shape[1]

    return int(math.floor(grid_num / horizontal_size)), int(math.floor(grid_num) % vertical_size)


if __name__ == '__main__':
    grid_matrix = [[i for i in range(j*6, (j+1)*6)] for j in range(0, 6)]
    print "grid_matrix: ", grid_matrix

    print get_grid_num(grid_matrix, 1, 3)     # 16
    print get_axis(grid_matrix, 30)