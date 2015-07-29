#!/usr/bin/env python
# coding: UTF-8
from __future__ import division
import sys
from build.multivariate_transition_tensor import get_correlation_matrix
import settings
from utils.sequence import init_data
from utils.tensor import normalize, build_fouth_order_influence_tensor, check_fourth_order_transition_tensor, \
    fouth_tensor_hadarmard

reload(sys)
sys.setdefaultencoding('utf-8')
import pickle


'''
serialization函数将transition tensor序列化到张量-张量的形式（即三阶张量的元素为三阶张量）
第一步：将四阶影响力张量分别序列化
第二步：将上述（四阶张量-矩阵）转为（三阶张量-三阶张量）的形式并序列化，参考numpy.reshape
'''
# 第一步
def serialization(data, user_num, poi_num):
    correlation_matrix = get_correlation_matrix(data, user_num)
    nor_cor_matrix = normalize(correlation_matrix)
    print "归一化相关系数矩阵: ", nor_cor_matrix

    for i in range(user_num):
        for j in range(user_num):
            if zero_adjustment:
                temp_tensor = build_fouth_order_influence_tensor(data[i], data[j], poi_num, True)
            else:
                temp_tensor = build_fouth_order_influence_tensor(data[i], data[j], poi_num, False)
            print str(i)+"对"+str(j)+"是否满足随机性条件", check_fourth_order_transition_tensor(temp_tensor)

            fouth_influence_tensor = fouth_tensor_hadarmard(nor_cor_matrix[i][j], temp_tensor)
            file_name = str(i)+"_"+str(j)+".db"
            file_path = "data/step_one/"+file_name
            print file_path
            transition_tensor_db = open(file_path, 'w')
            pickle.dump(fouth_influence_tensor, transition_tensor_db)
            transition_tensor_db.close()


# 第二步
def reshape(user_num, time_num, poi_num):
    for i_1 in range(user_num):
        for j in range(time_num):
            for k in range(poi_num):
                res = [0 for u in range(user_num)]
                for i_2 in range(user_num):
                    file_name = str(i_1)+"_"+str(i_2)+".db"
                    file_path = "data/step_one/"+file_name
                    # print file_path
                    transition_tensor_db = open(file_path, 'r')
                    fouth_influence_tensor = pickle.load(transition_tensor_db)
                    res[i_2] = fouth_influence_tensor[j][k]
                    transition_tensor_db.close()

                file_name = str(i_1)+"_"+str(j)+"_"+str(k)+".db"
                file_path = "data/step_two/"+file_name
                print file_path
                tensor_tensor_db = open(file_path, 'w')
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

    serialization(data, user_num, poi_num)
    reshape(user_num, time_num, poi_num)