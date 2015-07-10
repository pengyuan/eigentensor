#!/usr/bin/env python
# coding: UTF-8
from __future__ import division
import json
import urllib
import MySQLdb
from scipy import linalg
import numpy as np
from numpy.matlib import eye, identity
import run_time
from eigentensor import pykov
from eigentensor.poi_rank import POIRank
from pmpt.util import *
from preprocess import settings

__author__ = 'Peng Yuan <pengyuan.org@gmail.com>'
__copyright__ = 'Copyright (c) 2014 Peng Yuan'
__license__ = 'Public domain'


#
def init_data(region, time_slice, train_percent):
    conn = MySQLdb.connect(host=settings.HOST, user=settings.USER, passwd=settings.PASSWORD, db=settings.DB)
    cursor = conn.cursor()
    result = 0

    try:
        sql = "select user_id, poi_name, arrival_timestamp from staypoint2 where mean_coordinate_longtitude between "+str(region[0])+" and "+str(region[1])+" and mean_coordinate_latitude between "+str(region[2])+" and "+str(region[3])+" order by id"
        # print sql
        result = cursor.execute(sql)
        result = cursor.fetchall()
        conn.commit()
    except Exception, e:
        print e
        conn.rollback()

    length = int(len(result) * train_percent)
    train_data = result[:length]
    remain_data = result[length:]
    predicts = {}
    recommends = {}

    # 结果数据初步处理
    result_data = []
    for item in train_data:
        result_data.append((item[0], item[1], item[2]))

    poi_set = set()
    user_set = set()
    for item in result:
        poi_set.add(item[1])
        user_set.add(item[0])

    poi_num = len(poi_set)
    user_num = len(user_set)
    print "POI数目: ", poi_num
    print "用户数目: ", user_num

    pois_axis = {}
    axis_pois = {}
    index = 0
    for item in poi_set:
        pois_axis[item] = index
        axis_pois[index] = item
        index += 1

    users_axis = {}
    axis_users = {}
    index = 0
    for item in user_set:
        users_axis[item] = index
        axis_users[index] = item
        index += 1

    # POI，用户坐标转换
    trans_result_data = []
    for item in result_data:
        trans_result_data.append((users_axis[item[0]], pois_axis[item[1]], item[2]))  #[(用户1，poi1，时间1),(用户2，poi2，时间2)]

    # 以用户聚合
    user_base_data = {}
    for user in range(user_num):
        user_base_data[user] = []
        predicts[user] = {}
        recommends[user] = {}
    for item in trans_result_data:
        user_base_data[item[0]].append((item[1], item[2]))    # {用户1:[(POI1,时间1),(POI2,时间2)], 用户2:[1,2,3]}

    # 再以时间聚合
    time_slot = range(0, time_slice)
    return_data = {}
    for key in user_base_data.keys():
        time_slice_data = {}
        for slot in time_slot:
            time_slice_data[slot] = []
            predicts[key][slot] = set()
            recommends[key][slot] = set()
        user_base_data_item = user_base_data[key]

        for item in user_base_data_item:
            index = int(item[1] % 86400 // (3600 * (24 // time_slice)))
            time_slice_data[index].append(item[0])

        return_data[key] = time_slice_data

    for item in remain_data:
        user = users_axis[item[0]]
        time = int(item[2] % 86400 // (3600 * (24 // time_slice)))
        if pois_axis[item[1]] in set(return_data[user][time]):
            predicts[user][time].add(pois_axis[item[1]])
        else:
            recommends[user][time].add(pois_axis[item[1]])

    return return_data, axis_users, axis_pois, predicts, recommends


# 需要归一化
def user_preference(raw_data, dimensionality, order):
    return_data = {}
    for key1 in raw_data.keys():
        user_data = raw_data[key1]
        user_time_data = {}
        for key2 in user_data.keys():
            time_data = user_data[key2]
            data_length = len(time_data)
            if order == 2:
                if data_length >= 2:
                    data_set = set()
                    for item in range(data_length):
                        data_set.add(time_data[item])
                    state_num = len(data_set)
                    if state_num <= 1:
                        user_time_data[key2] = None
                        continue

                    pois_axis = {}
                    axis_pois = {}
                    index = 0
                    for item in data_set:
                        pois_axis[item] = index
                        axis_pois[index] = item
                        index += 1

                    process_data = []
                    for item in time_data:
                        process_data.append(pois_axis[item])

                    tensor = [[0 for i in range(state_num)] for j in range(state_num)]
                    for index in range(data_length-1):
                        check_list = process_data[index:index+2]
                        tensor[check_list[0]][check_list[1]] += 1
                    for item in range(state_num):
                        count_sum = 0
                        for item2 in range(state_num):
                            count_sum += tensor[item][item2]
                        if 0 == count_sum:
                            continue
                        else:
                            for item3 in range(state_num):
                                tensor[item][item3] = tensor[item][item3] / count_sum

                    # print "tensor ", tensor
                    result = param(tensor)
                    T = pykov.Chain(result)
                    preference_raw = T.steady()
                    preference = vec(preference_raw, dimensionality, axis_pois)
                    print preference_raw

                else:
                    preference = None

            elif order == 3:
                if data_length >= 3:
                    # 三维数组，元素初始化为零
                    tensor = [[[0 for i in range(dimensionality)] for j in range(dimensionality)] for k in range(dimensionality)]

                    for index in range(data_length-2):
                        check_list = time_data[index:index+3]
                        tensor[check_list[0]][check_list[1]][check_list[2]] += 1

                    for item in range(dimensionality):
                        for item2 in range(dimensionality):
                            count_sum = 0
                            for item3 in range(dimensionality):
                                count_sum += tensor[item][item2][item3]
                            if 0 == count_sum:
                                continue
                            else:
                                for item4 in range(dimensionality):
                                    tensor[item][item2][item4] = tensor[item][item2][item4] / count_sum
                    alpha = 0.95
                    v = []
                    for i in range(dimensionality):
                        v.append(1/dimensionality)
                    preference, hist, flag, ihist = POIRank(np.array(tensor), alpha, v).solve()
                else:
                    preference = None

            user_time_data[key2] = preference
        return_data[key1] = user_time_data

    return return_data


def param(tensor):
    result = {}
    #{('A','B'): .3, ('A','A'): .7, ('B','A'): 1.}
    dimen = len(tensor)
    #print "dimen", dimen
    for i in range(dimen):
        for j in range(dimen):
            if tensor[i][j] != 0:
                result[(i,j)] = tensor[i][j]

    return result


def vec(param, dimen, axis_pois):
    parameter = {}
    for key in param.keys():
        parameter[axis_pois[key]] = param[key]

    preference = []
    for i in range(dimen):
        if parameter.has_key(i):
            preference.append(parameter[i])
        else:
            preference.append(0.0)

    return preference


if __name__ == '__main__':
    # init_data((0, 3, 4, 5, 30))
    print "here"