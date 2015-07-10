#!/usr/bin/env python
# coding: UTF-8
from __future__ import division
from eigentensor.hosvd import HOSVD, unfold, reconstruct, frobenius_norm
from eigentensor.mobility import trans, init_data, init_data2, trans2
import numpy as np
import math
import pylab
# 第一步：构建转移概率tensor
# tensor = trans(count(init_db()))

# tensor = trans(count([0,1,0,1,0,1,1],2))
from util.tensor import hosvd
from util.tensor_old import hosvd2
from util.util import sparse


def recommend(users, time_slice, train_percent, top_n, use_type):
    axis_poi, data_map, predicts, recommends = init_data2(users, train_percent, time_slice)
    print "predicts: ", predicts
    print "recommends: ", recommends
    print "data_map: ", data_map
    poi_dimension = len(axis_poi)

    tensor = trans2(data_map, poi_dimension, users, time_slice)

    print "tensor: ", tensor
    # sparse(np.array(tensor))

    threshold = 0.8
    U, S, D = HOSVD(np.array(tensor), threshold)

    # new_T, T, Z, Un, Sn, Vn = hosvd(tensor)
    # new_T2, Z2, Un2, Sn2, Vn2 = hosvd2(tensor)

    print "the mode-1 unfold of core tensor:"
    print unfold(S, 1)

    print "The n-mode singular values:"
    print D

    A = reconstruct(S, U)
    print "reconstruct tensor: ", A


    print frobenius_norm(tensor-A)

    # sparse(A)
    #
    # print tensor[0][0][6]
    # print A[0][0][6]

    total = 0
    available = 0
    sum_precision = 0
    sum_recall = 0
    sum_f1_score = 0

    for user in users:
        data = data_map[user]
        # print "data: ", data
        for slot in range(0, time_slice):
            check_list = data[slot]

            data = A[users.index(user)][slot]
            sort_data = []
            for item in range(0, len(data)):
                meta_data = (item, data[item])
                sort_data.append(meta_data)
            sort_data.sort(key=lambda x: x[1], reverse=True)

            result_predict = []
            result_recommend = []
            for item in range(0, len(sort_data)):
                if (sort_data[item][0] in set(data_map[user][slot])) and (len(result_predict) < top_n):
                    result_predict.append(sort_data[item][0])
                else:
                    if len(result_recommend) < top_n:
                        result_recommend.append(sort_data[item][0])

            # 1. 正确率 = 提取出的正确信息条数 /  提取出的信息条数
            # 2. 召回率 = 提取出的正确信息条数 /  样本中的信息条数
            # 两者取值在0和1之间，数值越接近1，查准率或查全率就越高。
            # 3. F值  = 正确率 * 召回率 * 2 / (正确率 + 召回率) （F 值即为正确率和召回率的调和平均值）

            check_predict = predicts[user][slot]
            check_recommend = recommends[user][slot]

            count_predict = 0
            count_recommend = 0
            for item in result_predict:
                if item in check_predict:
                    count_predict += 1

            for item in result_recommend:
                if item in check_recommend:
                    count_recommend += 1

            total += 1

            if use_type == "recommendation":
                if len(result_recommend) == 0:
                    print "用户"+str(user)+"在时间"+str(slot)+"的f1_score（推荐）: 没有生成推荐数据,无法完成推荐"
                else:
                    precision = count_recommend / len(result_recommend)
                    if len(check_recommend) == 0:
                        print "用户"+str(user)+"在时间"+str(slot)+"的f1_score（推荐）: 校验推荐数据缺失,无法有效计算f1值"
                    else:
                        available += 1
                        recall = count_recommend / len(check_recommend)
                        if precision + recall == 0:
                            f1_score = 0
                            print "用户"+str(user)+"在时间"+str(slot)+"的f1_score（推荐）: "+str(f1_score)
                        else:
                            f1_score = (2 * precision * recall) / (precision + recall)
                            print "用户"+str(user)+"在时间"+str(slot)+"的f1_score（推荐）: "+str(f1_score)+",准确率为"+\
                                  str(precision)+",召回率为"+str(recall)
                        sum_precision += precision
                        sum_recall += recall
                        sum_f1_score += f1_score

            else:
                if len(result_predict) == 0:
                    print "用户"+str(user)+"在时间"+str(slot)+"的f1_score（预测）: 没有生成预测数据,无法完成预测"
                else:
                    precision = count_predict / len(result_predict)
                    if len(check_predict) == 0:
                        print "用户"+str(user)+"在时间"+str(slot)+"的f1_score（预测）: 校验预测数据缺失,无法有效计算f1值"
                    else:
                        available += 1
                        recall = count_predict / len(check_predict)
                        if precision + recall == 0:
                            f1_score = 0
                            print "用户"+str(user)+"在时间"+str(slot)+"的f1_score（预测）: "+str(f1_score)
                        else:
                            f1_score = (2 * precision * recall) / (precision + recall)
                            print "用户"+str(user)+"在时间"+str(slot)+"的f1_score（预测）: "+str(f1_score)+",准确率为"+\
                                  str(precision)+",召回率为"+str(recall)
                        sum_precision += precision
                        sum_recall += recall
                        sum_f1_score += f1_score

    return sum_precision / total, sum_recall / total, sum_f1_score / total, available / total


if __name__ == '__main__':
    users = tuple(range(20, 30))
    time_slice = 24
    train_percent = 0.35
    top_n = 3
    use_type = "recommendation"

    # use_type = "prediction"
    train_percent = 0.1
    y_values = []
    x_values = []
    y_values2 = []
    y_values3 = []
    y_values4 = []
    while train_percent <= 0.8:
        avg_precision, avg_recall, avg_f1_score, availability = recommend(users, time_slice, train_percent, top_n, use_type)
        print "avg_precision: ", avg_precision
        print "avg_recall: ", avg_recall
        print "avg_f1_score: ", avg_f1_score
        print "availability: ", availability
        y_values.append(avg_precision)
        y_values2.append(avg_recall)
        y_values3.append(avg_f1_score)
        y_values4.append(availability)
        x_values.append(train_percent)
        train_percent += 0.01

    pylab.plot(x_values, y_values, color="blue", linewidth=1, linestyle="-", label="precision")
    pylab.plot(x_values, y_values2, color="red",  linewidth=1, linestyle="-", label="recall")
    pylab.plot(x_values, y_values3, color="green",  linewidth=1, linestyle="-", label="f1_score")
    pylab.plot(x_values, y_values4, color="yellow",  linewidth=1, linestyle="-", label="availability")
    pylab.xlabel("train percent")
    pylab.ylabel("result")
    pylab.title("relation between train set and result（top_k=3, time_slice=24）")
    pylab.legend(loc='upper right')
    pylab.show()

    # # train_percent 0.35左右f1 score达到极值
    # avg_precision, avg_recall, avg_f1_score, availability = recommend(users, time_slice, train_percent, top_n, use_type)
    # print "avg_precision: ", avg_precision
    # print "avg_recall: ", avg_recall
    # print "avg_f1_score: ", avg_f1_score
    # print "availability: ", availability