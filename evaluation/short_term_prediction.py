#!/usr/bin/env python
# coding: UTF-8
from __future__ import division
import pylab
from build.multivariate_transition_tensor import mtt
import settings
from utils.sequence import init_data, init_data_by_user
from utils.tensor import tensor_three_mode_product, delta_tensor_norm, get_check_tensor, \
    tensor_three_mode_product_with_norm, inreducible_tensor, tensor_mode_tensor, build_fouth_order_transition_tensor, \
    tensor_two_mode_tensor, build_time_transition_matrix, build_location_transition_matrix


def get_init_tensor(check_data, user_now, time_int, user_num, time_num, poi_num):
    init_tensor = [[[0 for i in range(poi_num)] for j in range(time_num)] for k in range(user_num)]
    for user in range(user_num):
        if user == user_now:
            continue
        check = check_data[user]
        for item in check:
            if item[2] < time_int and ((time_int - item[2]) < 24*60*60):
                init_tensor[user][item[0]][item[1]] = 1
                break
    return init_tensor


def get_top_k(res_distribution, time_num, poi_num, top_k):
    res = set()
    sort_list = []
    for time in range(time_num):
        for poi in range(poi_num):
            sort_list.append((time, poi, res_distribution[time][poi]))

    sort_list.sort(key=lambda x: x[2], reverse=True)
    print "sort_list: ",  sort_list
    for item in sort_list[:top_k]:
        res.add((item[0], item[1]))
    return res


# 计算用户不进行交互的平均准确率
def predict_by_top_k_without_user_influence(data, check_data, user_num, time_num, poi_num, top_k):
    prediction = {}
    for user in range(user_num):
        predict_num = 0
        train = data[user]
        check = check_data[user]
        transition_tensor = build_fouth_order_transition_tensor(train, poi_num)
        for index in range(len(check)-1):
            user_now = check[index]
            user_next = check[index+1]
            time = user_now[0]
            poi = user_now[1]
            predict = (user_next[0], user_next[1])
            init_tensor = [[0 for i in range(poi_num)] for j in range(time_num)]
            init_tensor[time][poi] = 1
            res_tensor = tensor_two_mode_tensor(transition_tensor, init_tensor)
            res = get_top_k(res_tensor, time_num, poi_num, top_k)
            if predict in res:
                predict_num += 1
        prediction[user] = predict_num / (len(check)-1)
        print "user" + str(user)+" precision(二元分析) is "+str(prediction[user])

    sum = 0
    for key in prediction.keys():
        sum += prediction[key]

    return sum / user_num


# 计算用户不进行交互，时间地点分别考虑的平均准确率
def predict_by_top_k_by_time_and_location_separately(data, check_data, user_num, time_num, poi_num, top_k):
    prediction = {}
    for user in range(user_num):
        predict_num = 0
        train = data[user]
        check = check_data[user]
        time_transiton = build_time_transition_matrix(train)
        location_transition = build_location_transition_matrix(train, poi_num)
        for index in range(len(check)-1):
            user_now = check[index]
            user_next = check[index+1]
            time = user_now[0]
            poi = user_now[1]
            predict = (user_next[0], user_next[1])
            res_tensor = [[0 for i in range(poi_num)] for j in range(time_num)]
            for i in range(time_num):
                for j in range(poi_num):
                    res_tensor[i][j] = time_transiton[time][i] * location_transition[poi][j]
            res = get_top_k(res_tensor, time_num, poi_num, top_k)
            if predict in res:
                predict_num += 1
        prediction[user] = predict_num / (len(check)-1)
        print "user" + str(user)+" precision(时间地点分别考虑) is "+str(prediction[user])

    sum = 0
    for key in prediction.keys():
        sum += prediction[key]

    return sum / user_num


# # 计算用户不进行交互，时间地点分别考虑的平均准确率
# def predict_by_top_k_by_time(data, check_data, user_num, time_num, poi_num, top_k):
#     prediction = {}
#     for user in range(user_num):
#         predict_num = 0
#         train = data[user]
#         check = check_data[user]
#         time_transiton = build_time_transition_matrix(data)
#         for index in range(len(check)-1):
#             user_now = check[index]
#             user_next = check[index+1]
#             time = user_now[0]
#             poi = user_now[1]
#             predict = (user_next[0], user_next[1])
#             res_tensor = [[0 for i in range(poi_num)] for j in range(time_num)]
#             for i in range(time_num):
#                 for j in range(poi_num):
#                     res_tensor[i][j] = time_transiton[time][i] * (1/poi_num)
#             res = get_top_k(res_tensor, time_num, poi_num, top_k)
#             if predict in res:
#                 predict_num += 1
#         prediction[user] = predict_num / (len(check)-1)
#         print "user" + str(user)+" precision(仅考虑时间) is "+str(prediction[user])
#
#     sum = 0
#     for key in prediction.keys():
#         sum += prediction[key]
#
#     return sum / user_num



# 计算三元分析平均准确率
def predict_by_top_k(transition_tensor, check_data, poi_num, top_k):
    prediction = {}
    user_num = len(check_data.keys())
    time_num = settings.TIME_SLICE
    for user in range(user_num):
        predict_num = 0
        user_specific_check_data = check_data[user]
        for index in range(len(user_specific_check_data)-1):
            user_now = user_specific_check_data[index]     # (时间片，地点，绝对时间)
            user_next = user_specific_check_data[index+1]
            time = user_now[0]
            poi = user_now[1]
            time_int = user_next[2]
            predict = (user_next[0], user_next[1])
            init = get_init_tensor(check_data, user, time_int, user_num, time_num, poi_num)
            init[user][time][poi] = 1
            res_tensor = tensor_mode_tensor(transition_tensor, init)
            print "user"+str(user)+": "+str(index)+" of "+str(len(user_specific_check_data)-1)
            res = get_top_k(res_tensor[user], time_num, poi_num, top_k)
            if predict in res:
                predict_num += 1
        prediction[user] = predict_num / (len(user_specific_check_data)-1)
        print "user" + str(user)+" precision is "+str(prediction[user])

    sum = 0
    for key in prediction.keys():
        sum += prediction[key]

    return sum / user_num


if __name__ == '__main__':
    # beijing = (39.433333, 41.05, 115.416667, 117.5)
    # haidian = (39.883333, 40.15, 116.05, 116.383333)
    region = (39.883333, 40.05, 116.05, 116.383333)
    filter_count = 0
    time_num = settings.TIME_SLICE
    alpha = 0.95
    train_percent = 0.95


    top_k = 100

    x_values = []
    y_values1 = []
    y_values2 = []
    y_values3 = []

    # data, axis_users, axis_pois, check_data = init_data(region, filter_count, train_percent)
    data, axis_users, axis_pois, check_data = init_data_by_user(tuple([0, 3]), filter_count, train_percent)
    user_num = len(axis_users)
    poi_num = len(axis_pois)

    transition_tensor = inreducible_tensor(mtt(data, user_num, poi_num), user_num, time_num, poi_num, alpha)
    # transition_tensor1 = mtt(data, user_num, poi_num)

    while top_k <= 200:
        print "top_k: ", top_k
        res1 = predict_by_top_k(transition_tensor, check_data, poi_num, top_k)
        # res2 = predict_by_top_k(transition_tensor1, check_data, poi_num, top_k)
        res2 = predict_by_top_k_without_user_influence(data, check_data, user_num, time_num, poi_num, top_k)
        res3 = predict_by_top_k_by_time_and_location_separately(data, check_data, user_num, time_num, poi_num, top_k)
        x_values.append(top_k)
        y_values1.append(res1)
        y_values2.append(res2)
        y_values3.append(res3)
        print res1, res2, res3
        top_k += 100

    pylab.plot(x_values, y_values1, 'rs', linewidth=1, linestyle="-", label=u"不可约")
    pylab.plot(x_values, y_values2, 'gs', linewidth=1, linestyle="-", label=u"没有用户交互")
    pylab.plot(x_values, y_values3, 'bs', linewidth=1, linestyle="-", label=u"时间地点分别考虑")
    pylab.xlabel(u"top_k")
    pylab.ylabel(u"准确率")
    pylab.title(u"k与准确率的关系")
    pylab.legend(loc='center right')
    pylab.show()