#!/usr/bin/env python
# coding: UTF-8
from __future__ import division
import sys
import settings
from utils.sequence import init_data
from utils.tensor import three_tensor_hadarmard

reload(sys)
sys.setdefaultencoding('utf-8')
import pickle


# map方法
def map(distribution_tensor, user_num, time_num, poi_num):
    for i in range(user_num):
        for j in range(time_num):
            for k in range(poi_num):
                file_name = str(i)+"_"+str(j)+"_"+str(k)+".db"
                file_path = "data/step_two/"+file_name
                print file_path
                tensor_tensor_db = open(file_path, 'rw')
                tensor_tensor = pickle.load(tensor_tensor_db)
                res = three_tensor_hadarmard(distribution_tensor[i][j][k], tensor_tensor)
                pickle.dump(res, tensor_tensor_db)
                tensor_tensor_db.close()


if __name__ == '__main__':
    # beijing = (39.433333, 41.05, 115.416667, 117.5)
    # haidian = (39.883333, 40.15, 116.05, 116.383333)
    region = (39.883333, 40.05, 116.05, 116.383333)
    filter_count = 600
    zero_adjustment = True
    time_num = settings.TIME_SLICE

    data, axis_users, axis_pois, check_data = init_data(region, filter_count)
    user_num = len(axis_users)
    poi_num = len(axis_pois)

    init_tensor = [[[1/(poi_num * time_num * user_num) for i in range(poi_num)] for j in range(time_num)] for k in range(user_num)]
    map(init_tensor, user_num, time_num, poi_num)

