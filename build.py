#!/usr/bin/env python
# coding: UTF-8
from __future__ import division
from eigentensor.hosvd import HOSVD, reconstruct, frobenius_norm
from eigentensor.mobility import init_data, user_preference
import numpy as np


def recommend(A, data_map, predicts, recommends, top_k, use_type):
    total = 0
    available = 0
    sum_precision = 0
    sum_recall = 0
    sum_f1_score = 0

    shape = np.array(A).shape     # (用户，时间，poi)
    user_num = shape[0]
    time_num = shape[1]
    poi_num = shape[2]

    for user in range(user_num):
        for time in range(time_num):
            data = A[user][time]
            sort_data = []
            for item in range(0, len(data)):
                meta_data = (item, data[item])
                sort_data.append(meta_data)
            sort_data.sort(key=lambda x: x[1], reverse=True)

            result_data = sort_data[:top_k]
            result_set = set()
            for item in result_data:
                result_set.add(item[0])

            result_length = len(result_set)

            # 1. 正确率 = 提取出的正确信息条数 /  提取出的信息条数
            # 2. 召回率 = 提取出的正确信息条数 /  样本中的信息条数
            # 两者取值在0和1之间，数值越接近1，查准率或查全率就越高。
            # 3. F值  = 正确率 * 召回率 * 2 / (正确率 + 召回率) （F 值即为正确率和召回率的调和平均值）

            check_predict = predicts[user][time]
            check_recommend = recommends[user][time]

            count_predict = 0
            count_recommend = 0
            for item in result_set:
                if item in check_predict:
                    count_predict += 1

            for item in result_set:
                if item in check_recommend:
                    count_recommend += 1

            if use_type == "recommendation":
                if len(check_recommend) == 0:
                    print "用户"+str(user)+"在时间"+str(time)+"的f1_score（推荐）: 校验推荐数据缺失,无法有效计算f1值"
                else:
                    precision = count_recommend / len(check_recommend)

                    recall = count_recommend / result_length
                    if precision + recall == 0:
                        f1_score = 0
                        print "用户"+str(user)+"在时间"+str(time)+"的f1_score（推荐）: "+str(f1_score)
                    else:
                        available += 1
                        f1_score = (2 * precision * recall) / (precision + recall)
                        print "用户"+str(user)+"在时间"+str(time)+"的f1_score（推荐）: "+str(f1_score)+",准确率为"+\
                              str(precision)+",召回率为"+str(recall)
                    sum_precision += precision
                    sum_recall += recall
                    sum_f1_score += f1_score
                    total += 1

            else:
                if len(check_predict) == 0:
                    print "用户"+str(user)+"在时间"+str(time)+"的f1_score（预测）: 校验预测数据缺失,无法有效计算f1值"
                else:
                    precision = count_predict / len(check_predict)
                    recall = count_predict / result_length
                    if precision + recall == 0:
                        f1_score = 0
                        print "用户"+str(user)+"在时间"+str(time)+"的f1_score（预测）: "+str(f1_score)
                    else:
                        available += 1
                        f1_score = (2 * precision * recall) / (precision + recall)
                        print "用户"+str(user)+"在时间"+str(time)+"的f1_score（预测）: "+str(f1_score)+",准确率为"+\
                              str(precision)+",召回率为"+str(recall)
                    sum_precision += precision
                    sum_recall += recall
                    sum_f1_score += f1_score
                    total += 1

    return sum_precision / total, sum_recall / total, sum_f1_score / total, available / total


if __name__ == '__main__':
    # beijing = (39.433333, 41.05, 115.416667, 117.5)
    # haidian = (39.883333, 40.15, 116.05, 116.383333)
    region = (39.88, 40.10, 116.05, 116.25)
    time_slice = 1
    order = 2
    train_percent = 0.4
    top_k = 1
    use_type = "prediction"

    data, axis_user, axis_poi, predicts, recommends = init_data(region, time_slice, train_percent)
    # print "predicts: ", predicts
    # print "recommends: ", recommends

    preference = user_preference(data, len(axis_poi), order)
    # print "preference: ", preference

    tensor = [[[0 for i in range(len(axis_poi))] for j in range(time_slice)] for user in range(len(axis_user))]

    print len(axis_poi)
    for user in preference.keys():
        user_data = preference[user]
        for time in user_data.keys():
            time_data = user_data[time]
            if time_data:
                for poi_index in range(len(axis_poi)):
                    # print user, time, poi_index
                    tensor[user][time][poi_index] = time_data[poi_index]

    U, S, D = HOSVD(np.array(tensor), 0.6)

    A = reconstruct(S, U)
    print "reconstruct tensor: ", A
    print frobenius_norm(tensor-A)

    avg_precision, avg_recall, avg_f1_score, availability = recommend(A, data, predicts, recommends, top_k, use_type)
    print "avg_precision: ", avg_precision
    print "avg_recall: ", avg_recall
    print "avg_f1_score: ", avg_f1_score
    print "availability: ", availability





    # 构建转移概率张量
    # grid_transition = trans(trains, grid_num, 2)
    # for key in grid_transition.keys():
    #     print "key: ", grid_transition[key]




    # for key in data_map:
    #     data = data_map[key]
    #     # print data
    #     # tensor为列表
    #     tensor = trans(data, dimension, 3)
    #     # print tensor
    #
    #
    #
    # # afunc(tensor)
    # # 第二步：HOSVD，重构tensor
    #
    # # threshold = 0.8
    #
    # # 将列表转化为高维数组
    # tensor = np.array(tensor)
    #
    # print "tensor:"
    # print tensor
    #
    # # sparse(tensor)
    #
    # threshold = 1.0
    # U, S, D = HOSVD(tensor, 0.8)
    #
    # # new_T, T, Z, Un, Sn, Vn = hosvd(tensor)
    # # new_T2, Z2, Un2, Sn2, Vn2 = hosvd2(tensor)
    #
    # print "the mode-1 unfold of core tensor:"
    # print unfold(S, 1)
    #
    # print "The n-mode singular values:"
    # print D
    #
    # A = reconstruct(S, U)
    # print "reconstruct tensor: ", A
    #
    #
    # print frobenius_norm(tensor-A)
    #
    # # sparse(A)