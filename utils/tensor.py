#!/usr/bin/env python
# coding: UTF-8

# 计算张量稀疏度
from __future__ import division
from math import sqrt
import numpy
import ctypes as ct

# 三阶张量数值积
import settings
from utils.sequence import init_data


def inreducible_tensor(transition_tensor, user_num, time_num, poi_num, alpha):
    for i in range(user_num):
        for j in range(time_num):
            for k in range(poi_num):
                for l in range(user_num):
                    for m in range(time_num):
                        for n in range(poi_num):
                            transition_tensor[i][j][k][l][m][n] = alpha * transition_tensor[i][j][k][l][m][n] + (1 - alpha) * (1 / (user_num * time_num * poi_num))

    return transition_tensor


def three_tensor_hadarmard(param, tensor):
    user_num = len(tensor)
    time_num = len(tensor[0])
    poi_num = len(tensor[0][0])
    for i in range(user_num):
        for j in range(time_num):
            for k in range(poi_num):
                    tensor[i][j][k] = param * tensor[i][j][k]
    return tensor


# 四阶张量数值积
def fouth_tensor_hadarmard(param, tensor):
    time_num = len(tensor)
    poi_num = len(tensor[0])
    for i in range(time_num):
        for j in range(poi_num):
            for k in range(time_num):
                for l in range(poi_num):
                    tensor[i][j][k][l] = param * tensor[i][j][k][l]
    return tensor


class float_bits(ct.Structure):
    _fields_ = [('M', ct.c_uint, 23),
                ('E', ct.c_uint, 8),
                ('S', ct.c_uint, 1)
                ]

    ''' 针对IEEE754标准的32位浮点数的Python版的eps函数 '''
    def epsf(innum):
        f1 = ct.c_float(innum)
        f2 = ct.c_float(innum)
        # p1 = (float_bits*)&f1;
        p1 = ct.cast(ct.byref(f1), ct.POINTER(float_bits))
        # p2 = (float_bits*)&f2;
        p2 = ct.cast(ct.byref(f2), ct.POINTER(float_bits))
        # p1->M = 1;
        p1.contents.M = 1
        # p2->M = 0;
        p2.contents.M = 0
        p1.contents.S = p2.contents.S = 0
        return f1.value - f2.value


def sparsity(tensor, tolerance=1e-10):
    shape = numpy.array(tensor).shape
    # print shape
    order = len(shape)
    count_zero = 0
    count_total = 0
    if order == 2:
        for i in range(shape[0]):
            for j in range(shape[1]):
                    if tensor[i][j] == 0:
                        count_zero += 1
                    count_total += 1
    elif order == 3:
        for i in range(shape[0]):
            for j in range(shape[1]):
                for k in range(shape[2]):
                    if tensor[i][j][k] == 0:
                        count_zero += 1
                    count_total += 1
    elif order == 4:
        for i in range(shape[0]):
            for j in range(shape[1]):
                for k in range(shape[2]):
                    for l in range(shape[3]):
                        if tensor[i][j][k][l] == 0:
                            count_zero += 1
                        count_total += 1
    elif order == 5:
        for i in range(shape[0]):
            for j in range(shape[1]):
                for k in range(shape[2]):
                    for l in range(shape[3]):
                        for m in range(shape[4]):
                            if tensor[i][j][k][l][m] == 0:
                                count_zero += 1
                            count_total += 1

    elif order == 6:
        for i in range(shape[0]):
            for j in range(shape[1]):
                for k in range(shape[2]):
                    for l in range(shape[3]):
                        for m in range(shape[4]):
                            for n in range(shape[5]):
                                if tensor[i][j][k][l][m] == 0:
                                    count_zero += 1
                                count_total += 1
    else:
        raise "order值不正确，无法计算稀疏度"

    # print count_zero
    return str(round((100*(count_total - count_zero) / count_total), 2))+str("%")


# 差矩阵二范数
def delta_matrix_norm(matrix_last, matrix):
    time_num = len(matrix)
    poi_num = len(matrix[0])
    sum = 0
    for i in range(time_num):
        for j in range(poi_num):
            sum += pow(abs(matrix[i][j]-matrix_last[i][j]), 2)
    return sqrt(sum)


# 差张量二范数
def delta_tensor_norm(tensor_last, tensor):
    user_num = len(tensor)
    time_num = len(tensor[0])
    poi_num = len(tensor[0][0])
    sum = 0
    for i in range(user_num):
        for j in range(time_num):
            for k in range(poi_num):
                sum += pow(abs(tensor[i][j][k]-tensor_last[i][j][k]), 2)
    return sqrt(sum)


# 三阶张量相加
def three_order_tensor_add(tensor1, tensor2):
    user_num = len(tensor1)
    time_num = len(tensor1[0])
    poi_num = len(tensor1[0][0])
    for i in range(user_num):
        for j in range(time_num):
            for k in range(poi_num):
                tensor1[i][j][k] += tensor2[i][j][k]
    return tensor1


# 三阶张量1-范数
def three_order_tensor_first_norm(tensor):
    sum = 0
    user_num = len(tensor)
    time_num = len(tensor[0])
    poi_num = len(tensor[0][0])
    for i in range(user_num):
        for j in range(time_num):
            for k in range(poi_num):
                sum += abs(tensor[i][j][k])
    return sum


# 三阶张量2-范数
def three_order_tensor_second_norm(tensor):
    user_num = len(tensor)
    time_num = len(tensor[0])
    poi_num = len(tensor[0][0])
    sum = 0
    for i in range(user_num):
        for j in range(time_num):
            for k in range(poi_num):
                sum += pow(abs(tensor[i][j][k]), 2)
    return sqrt(sum)


# 三阶张量无穷-范数
def three_order_tensor_max_norm(tensor):
    max = 0
    user_num = len(tensor)
    time_num = len(tensor[0])
    poi_num = len(tensor[0][0])
    for i in range(user_num):
        for j in range(time_num):
            for k in range(poi_num):
                if abs(tensor[i][j][k]) > max:
                    max = abs(tensor[i][j][k])
    return max


# 张量二模乘
def tensor_two_mode_tensor(transition_tensor, init_tensor):
    time_num = len(init_tensor)
    poi_num = len(init_tensor[0])
    res = [[0 for i in range(poi_num)] for j in range(time_num)]
    for i in range(time_num):
        for j in range(poi_num):
            res[i][j] = 0
            for k in range(time_num):
                for l in range(poi_num):
                    res[i][j] += transition_tensor[k][l][i][j] * init_tensor[k][l]
    return res


# 张量二模乘
def tensor_two_mode_product(transition_tensor, init_tensor):
    time_num = len(init_tensor)
    poi_num = len(init_tensor[0])
    index = 1
    res = [[0 for i in range(poi_num)] for j in range(time_num)]
    while index <= settings.ITERATOR_NUMBER:
        for i in range(time_num):
            for j in range(poi_num):
                res[i][j] = 0
                for k in range(time_num):
                    for l in range(poi_num):
                        res[i][j] += transition_tensor[k][l][i][j] * init_tensor[k][l]
        delta = delta_matrix_norm(init_tensor, res)
        print "index:"+str(index)+",delta:"+str(delta)
        if delta < settings.ITERATOR_TOLERANCE:
            break
        else:
            for i in range(time_num):
                for j in range(poi_num):
                    init_tensor[i][j] = res[i][j]

        index += 1

    # if index == settings.ITERATOR_NUMBER:
    #     raise "无法收敛"

    return res


# 张量三模乘
def tensor_mode_tensor(tensor, init_tensor):
    user_num = len(init_tensor)
    time_num = len(init_tensor[0])
    poi_num = len(init_tensor[0][0])
    res = [[[0 for i in range(poi_num)] for j in range(time_num)] for k in range(user_num)]
    for i in range(user_num):
        for j in range(time_num):
            for k in range(poi_num):
                res[i][j][k] = 0
                for l in range(user_num):
                    for m in range(time_num):
                        for n in range(poi_num):
                            res[i][j][k] += tensor[l][m][n][i][j][k] * init_tensor[l][m][n]

    return res


# 张量三模乘
def tensor_three_mode_product(tensor, init_tensor):
    iterator__values = {}
    user_num = len(init_tensor)
    time_num = len(init_tensor[0])
    poi_num = len(init_tensor[0][0])
    index = 1
    res = [[[0 for i in range(poi_num)] for j in range(time_num)] for k in range(user_num)]
    while index <= settings.ITERATOR_NUMBER:
        for i in range(user_num):
            for j in range(time_num):
                for k in range(poi_num):
                    res[i][j][k] = 0
                    for l in range(user_num):
                        for m in range(time_num):
                            for n in range(poi_num):
                                res[i][j][k] += tensor[l][m][n][i][j][k] * init_tensor[l][m][n]
        delta = delta_tensor_norm(init_tensor, res)
        print "index:"+str(index)+",delta:"+str(delta)
        if delta < settings.ITERATOR_TOLERANCE:
            break
        else:
            for i in range(user_num):
                for j in range(time_num):
                    for k in range(poi_num):
                        init_tensor[i][j][k] = res[i][j][k]

        iterator__values[index] = delta
        index += 1
    # if index == settings.ITERATOR_NUMBER:
    #     raise "无法收敛"

    return res, iterator__values


# 张量三模乘迭代中范数的变化
def tensor_three_mode_product_with_norm(tensor, init_tensor):
    iterator__values = {}
    norms = {}
    user_num = len(init_tensor)
    time_num = len(init_tensor[0])
    poi_num = len(init_tensor[0][0])
    index = 1
    res = [[[0 for i in range(poi_num)] for j in range(time_num)] for k in range(user_num)]
    while index <= settings.ITERATOR_NUMBER:
        for i in range(user_num):
            for j in range(time_num):
                for k in range(poi_num):
                    res[i][j][k] = 0
                    for l in range(user_num):
                        for m in range(time_num):
                            for n in range(poi_num):
                                res[i][j][k] += tensor[l][m][n][i][j][k] * init_tensor[l][m][n]
        norm_one = three_order_tensor_first_norm(res)
        norm_two = three_order_tensor_second_norm(res)
        norm_three = three_order_tensor_max_norm(res)

        delta = delta_tensor_norm(init_tensor, res)
        print "index:"+str(index)+",delta:"+str(delta)
        if delta < settings.ITERATOR_TOLERANCE:
            break
        else:
            for i in range(user_num):
                for j in range(time_num):
                    for k in range(poi_num):
                        init_tensor[i][j][k] = res[i][j][k]

        iterator__values[index] = delta
        norms[index] = (norm_one, norm_two, norm_three)
        index += 1

    # if index == settings.ITERATOR_NUMBER:
    #     raise "无法收敛"

    return res, iterator__values, norms


# 张量三模乘
def shifted_tensor_three_mode_product(tensor, init_tensor, alpha, shifted=True):
    iterator__values = {}
    user_num = len(init_tensor)
    time_num = len(init_tensor[0])
    poi_num = len(init_tensor[0][0])
    index = 1
    res = [[[0 for i in range(poi_num)] for j in range(time_num)] for k in range(user_num)]
    while index <= settings.ITERATOR_NUMBER:
        for i in range(user_num):
            for j in range(time_num):
                for k in range(poi_num):
                    res[i][j][k] = 0
                    for l in range(user_num):
                        for m in range(time_num):
                            for n in range(poi_num):
                                res[i][j][k] += tensor[l][m][n][i][j][k] * init_tensor[l][m][n]
        if shifted:
            temp_tensor = three_order_tensor_add(res, three_tensor_hadarmard(alpha, init_tensor))
        else:
            temp_tensor = res
        res = three_tensor_hadarmard(1/three_order_tensor_second_norm(temp_tensor), temp_tensor)
        delta = delta_tensor_norm(init_tensor, res)
        print "index:"+str(index)+",delta:"+str(delta)
        if delta < settings.ITERATOR_TOLERANCE:
            break
        else:
            for i in range(user_num):
                for j in range(time_num):
                    for k in range(poi_num):
                        init_tensor[i][j][k] = res[i][j][k]

        iterator__values[index] = delta

        index += 1
        # print "res", str(index)+": ", res
        # print three_order_tensor_first_norm(res)

    # if index == settings.ITERATOR_NUMBER:
    #     raise "无法收敛"

    return res, iterator__values


# 随机性修正 (stochasticity adjustment)
def fouth_order_tensor_stochasticity(tensor, poi_num, zero_adjustment):
    for i in range(settings.TIME_SLICE):
        for j in range(poi_num):
            sum = 0
            for k in range(settings.TIME_SLICE):
                for l in range(poi_num):
                    sum += tensor[i][j][k][l]

            if sum > 0:
                for k in range(settings.TIME_SLICE):
                    for l in range(poi_num):
                        tensor[i][j][k][l] = tensor[i][j][k][l] / sum
            else:
                if zero_adjustment:
                    for k in range(settings.TIME_SLICE):
                        for l in range(poi_num):
                            tensor[i][j][k][l] = 1 / (settings.TIME_SLICE * poi_num)
    return tensor


# 随机性修正 (stochasticity adjustment)
def transition_matrix_stochasticity(matrix, zero_adjustment):
    time_num = settings.TIME_SLICE
    for i in range(time_num):
        sum = 0
        for j in range(time_num):
            sum += matrix[i][j]
        if sum > 0:
            for j in range(time_num):
                    matrix[i][j] = matrix[i][j] / sum
        else:
            if zero_adjustment:
                for j in range(time_num):
                    matrix[i][j] = 1 / time_num
    return matrix


# 构建时间序列转移矩阵
def build_time_transition_matrix(temp, zero_adjustment=True):
    matrix = [[0 for time_to in range(settings.TIME_SLICE)] for time_from in range(settings.TIME_SLICE)]
    for temp_index in range(len(temp)-1):
        from_state = temp[temp_index]
        to_state = temp[temp_index+1]
        matrix[from_state[0]][to_state[0]] += 1
        temp_index += 1
    return transition_matrix_stochasticity(matrix, zero_adjustment)


# 构建地点序列转移矩阵
def build_location_transition_matrix(temp, poi_num, zero_adjustment=True):
    matrix = [[0 for poi_to in range(poi_num)] for poi_from in range(poi_num)]
    for temp_index in range(len(temp)-1):
        from_state = temp[temp_index]
        to_state = temp[temp_index+1]
        matrix[from_state[1]][to_state[1]] += 1
        temp_index += 1
    return transition_matrix_stochasticity(matrix, zero_adjustment)


# 构建某用户序列（时间，地点）转移张量
def build_fouth_order_transition_tensor(temp, poi_num, zero_adjustment=True):
    tensor = [[[[0 for poi_to in range(poi_num)] for time_to in range(settings.TIME_SLICE)] for poi_from in range(poi_num)] for time_from in range(settings.TIME_SLICE)]
    for temp_index in range(len(temp)-1):
        from_state = temp[temp_index]
        to_state = temp[temp_index+1]
        tensor[from_state[0]][from_state[1]][to_state[0]][to_state[1]] += 1
        temp_index += 1
    return fouth_order_tensor_stochasticity(tensor, poi_num, zero_adjustment)


# 构建（用户，时间，地点）转移张量
def build_six_order_transition_tensor(data, poi_num, nor_cor_matrix, zero_adjustment):
    user_num = len(data)
    tensor = [[[[[[0 for poi_to in range(poi_num)] for time_to in range(settings.TIME_SLICE)] for user_to in range(user_num)] for poi_from in range(poi_num)] for time_from in range(settings.TIME_SLICE)] for user_from in range(user_num)]

    for i in range(user_num):
        for j in range(user_num):
            if zero_adjustment:
                temp_tensor = build_fouth_order_influence_tensor(data[i], data[j], poi_num, True)
            else:
                temp_tensor = build_fouth_order_influence_tensor(data[i], data[j], poi_num, False)
            print str(i)+"对"+str(j), check_fourth_order_transition_tensor(temp_tensor)
            param_tensor = fouth_tensor_hadarmard(nor_cor_matrix[i][j], temp_tensor)
            for k in range(settings.TIME_SLICE):
                for l in range(poi_num):
                    for m in range(settings.TIME_SLICE):
                        for n in range(poi_num):
                            tensor[i][k][l][j][m][n] = param_tensor[k][l][m][n]
    return tensor


# 构建用户A序列对用户B序列的（时间，地点）影响力张量
def build_fouth_order_influence_tensor(sequence_a, sequence_b, poi_num, zero_adjustment):
    tensor = [[[[0 for poi_to in range(poi_num)] for time_to in range(settings.TIME_SLICE)] for poi_from in range(poi_num)] for time_from in range(settings.TIME_SLICE)]
    for i in range(len(sequence_b)):
        temp_to = sequence_b[i][2]
        temp_from = None
        for j in range(len(sequence_a)):
            # if sequence_b[j][2] > temp_from:
            if (sequence_a[j][2] < temp_to) and ((temp_to - sequence_a[j][2]) < 24*60*60):
                temp_from = sequence_a[j][2]
                break
        if temp_from:
            tensor[sequence_a[j][0]][sequence_a[j][1]][sequence_b[i][0]][sequence_b[i][1]] += 1
        else:
            continue
    return fouth_order_tensor_stochasticity(tensor, poi_num, zero_adjustment)


# 判断时间-地点四阶张量是否满足归一化条件
def check_fourth_order_transition_tensor(tensor, tolerance=1e-10):
    flag = True
    time_num = len(tensor)
    poi_num = len(tensor[0])
    # print time_num, poi_num
    for i in range(time_num):
        for j in range(poi_num):
            sum = 0
            for k in range(time_num):
                for l in range(poi_num):
                    # print i, j, k, l
                    sum += tensor[i][j][k][l]
            if not abs(sum - 1.0) < tolerance:
                # print "sum: ", sum-1.0
                flag = False

    return flag


# 判断用户-时间-地点六阶转移张量是否满足归一化条件
def check_six_order_transition_tensor(tensor, tolerance=1e-10):
    flag = True
    user_num = len(tensor)
    time_num = len(tensor[0])
    poi_num = len(tensor[0][0])
    # print time_num, poi_num
    for i in range(user_num):
        for j in range(time_num):
            for k in range(poi_num):
                sum = 0
                for l in range(user_num):
                    for m in range(time_num):
                        for n in range(poi_num):
                            sum += tensor[i][j][k][l][m][n]
                if not abs(sum - 1.0) < tolerance:
                    flag = False
                    # print "sum: ", sum-1.0
    return flag


# 判断特征矩阵是否满足非负且1-范数为1的条件
def validate_eigen_matrix(eigen_matrix, tolerance=1e-10):
    flag = True
    time_num = len(eigen_matrix)
    poi_num = len(eigen_matrix[0])
    sum = 0
    for i in range(time_num):
        for j in range(poi_num):
            sum += eigen_matrix[i][j]
            if eigen_matrix[i][j] < 0:
                flag = False
    if not abs(sum - 1.0) < tolerance:
        flag = False
    return flag


# 判断特征张量是否满足非负且1-范数为1的条件
def validate_eigen_tensor(eigen_tensor, tolerance=1e-10):
    flag = True
    user_num = len(eigen_tensor)
    time_num = len(eigen_tensor[0])
    poi_num = len(eigen_tensor[0][0])
    sum = 0
    for i in range(user_num):
        for j in range(time_num):
            for k in range(poi_num):
                sum += eigen_tensor[i][j][k]
                if eigen_tensor[i][j][k] < 0:
                    flag = False
    if not abs(sum - 1.0) < tolerance:
        flag = False
    return flag


# 按特征张量的某个阶的切片进行分析
def analysis_eigen_tensor(eigen_tensor, strategy="user"):
    user_num = len(eigen_tensor)
    time_num = len(eigen_tensor[0])
    poi_num = len(eigen_tensor[0][0])
    total = 0
    res = ""
    if strategy == "user":
        for i in range(user_num):
            sum = 0
            for j in range(time_num):
                for k in range(poi_num):
                    sum += eigen_tensor[i][j][k]
            total += sum
            res += "用户切面"+str(i)+"的概率和为"+str(sum)+" "
    elif strategy == "time":
        for i in range(time_num):
            sum = 0
            for j in range(user_num):
                for k in range(poi_num):
                    sum += eigen_tensor[j][i][k]
            total += sum
            res += "时间切面"+str(i)+"的概率和为"+str(sum)+" "
    elif strategy == "poi":
        for i in range(poi_num):
            sum = 0
            for j in range(user_num):
                for k in range(time_num):
                    sum += eigen_tensor[j][k][i]
            total += sum
            res += "地点切面"+str(i)+"的概率和为"+str(sum)+" "
    return res+"总和为:"+str(total)


# 归一化相关系数矩阵
def normalize(correlation_matrix):
    for i in range(len(correlation_matrix)):
        sum = 0
        for j in range(len(correlation_matrix[0])):
            sum += correlation_matrix[i][j]
        for j in range(len(correlation_matrix[0])):
            correlation_matrix[i][j] /= sum

    return correlation_matrix


def get_check_tensor(check_data, user_num, time_num, poi_num, strategy="all"):
    check_tensor = [[[0 for i in range(poi_num)] for j in range(time_num)] for k in range(user_num)]
    for key in check_data.keys():
        for item in check_data[key]:
            check_tensor[key][item[0]][item[1]] += 1

    if strategy == "user":
        for i in range(user_num):
            sum = 0
            for j in range(time_num):
                for k in range(poi_num):
                    sum += check_tensor[i][j][k]
            if sum > 0:
                for j in range(time_num):
                    for k in range(poi_num):
                        check_tensor[i][j][k] /= sum
    elif strategy == "all":
        check_tensor = three_tensor_hadarmard(1/three_order_tensor_first_norm(check_tensor), check_tensor)
    else:
        raise

    return check_tensor


def dta_normalize_tensor(res_tensor, user_num, time_num, poi_num, strategy="all"):
    if strategy == "user":
        for i in range(user_num):
            sum = 0
            for j in range(time_num):
                for k in range(poi_num):
                    sum += res_tensor[i][j][k]
            if sum != 0:
                for j in range(time_num):
                    for k in range(poi_num):
                        res_tensor[i][j][k] /= sum
    elif strategy == "all":
        res_tensor = three_tensor_hadarmard(1/three_order_tensor_first_norm(res_tensor), res_tensor)
    else:
        raise

    return res_tensor


if __name__ == '__main__':
    # beijing = (39.433333, 41.05, 115.416667, 117.5)
    # haidian = (39.883333, 40.15, 116.05, 116.383333)
    region = (39.883333, 40.05, 116.05, 116.383333)
    filter_count = 600
    data, axis_users, axis_pois = init_data(region, filter_count)
    for key in data.keys():
        print "用户" + str(key) + "序列为" + str(data[key])

    tensor_list = {}
    poi_num = len(axis_pois)
    for index in range(len(data.keys())):
        temp = data[index]
        tensor_list[index] = build_fouth_order_transition_tensor(temp, poi_num)

    for user_index in range(len(axis_users)):
        print sparsity(tensor_list[user_index])
        print check_fourth_order_transition_tensor(tensor_list[user_index])

    # 等价关系
    print "transition: ", sparsity(build_fouth_order_transition_tensor(data[1], poi_num))
    print "influence: ", sparsity(build_fouth_order_influence_tensor(data[1], data[1], poi_num))