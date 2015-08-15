#!/usr/bin/env python
# coding: UTF-8

# 计算两个经纬度之间的距离，单位千米
from __future__ import division
import MySQLdb
import settings


# 初始化数据
def init_data(region, filter_count, train_percent=1):
    conn = MySQLdb.connect(host=settings.HOST, user=settings.USER, passwd=settings.PASSWORD, db=settings.DB)
    cursor = conn.cursor()
    result = 0

    try:
        sql = "select user_id from staypoint where mean_coordinate_latitude between "+str(region[0])+" and "+str(region[1])+" and mean_coordinate_longtitude between "+str(region[2])+" and "+str(region[3])+" group by user_id having count(*) > "+str(filter_count)
        result = cursor.execute(sql)
        result = cursor.fetchall()
        conn.commit()
    except Exception, e:
        print e
        conn.rollback()

    user_available = []
    for item in result:
        user_available.append(int(item[0]))
    if len(user_available) == 0:
        raise "没有足够数据"
    print user_available

    try:
        if len(user_available) == 1:
            sql = "select user_id, arrival_timestamp, poi_name from staypoint where user_id = "+str(user_available[0])+ " and mean_coordinate_latitude between "+str(region[0])+" and "+str(region[1])+" and mean_coordinate_longtitude between "+str(region[2])+" and "+str(region[3])+" order by id"
        else:
            sql = "select user_id, arrival_timestamp, poi_name from staypoint where user_id in "+tuple(user_available).__str__()+ " and mean_coordinate_latitude between "+str(region[0])+" and "+str(region[1])+" and mean_coordinate_longtitude between "+str(region[2])+" and "+str(region[3])+" order by id"
        print sql
        result = cursor.execute(sql)
        result = cursor.fetchall()
        conn.commit()
    except Exception, e:
        print e
        conn.rollback()
    cursor.close()
    conn.close()

    print result
    poi_set = set()
    user_set = set()
    for item in result:
        poi_set.add(item[2])
        user_set.add(item[0])

    poi_num = len(poi_set)
    user_num = len(user_set)
    print "poi数目：", poi_num
    print "用户数目：", user_num

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

    data = {}
    train_data = {}
    check_data = {}
    for user in range(user_num):
        data[user] = []
        train_data[user] = []
        check_data[user] = []
    for item in result:
        data[users_axis[item[0]]].append((stamp2slice(item[1]), pois_axis[item[2]], item[1]))  # (用户，时间，地点)

    for key in data.keys():
        print "用户" + str(key) + "序列长度为" + str(len(data[key]))
    if train_percent < 1:
        for key in data.keys():
            length = int(train_percent * len(data[key]))
            train_data[key] = data[key][:length]
            check_data[key] = data[key][length:]
    else:
        train_data = data
        check_data = None
    return train_data, axis_users, axis_pois, check_data


def init_data_by_user(users, filter_count, train_percent=1, split_percent=1, filter_poi_count=0):
    conn = MySQLdb.connect(host=settings.HOST, user=settings.USER, passwd=settings.PASSWORD, db=settings.DB)
    cursor = conn.cursor()
    result = 0

    try:
        if len(users) == 1:
            sql = "select user_id from staypoint where user_id = "+str(users[0]) +" and province = '北京市' and district = '海淀区' group by user_id having count(*) > "+str(filter_count)
        else:
            sql = "select user_id from staypoint where user_id in "+users.__str__() +" and province = '北京市' and district = '海淀区' group by user_id having count(*) > "+str(filter_count)
        result = cursor.execute(sql)
        result = cursor.fetchall()
        conn.commit()
    except Exception, e:
        print e
        conn.rollback()

    user_available = []
    for item in result:
        user_available.append(int(item[0]))
    if len(user_available) == 0:
        raise "没有足够数据"
    print user_available

    db_data = {}
    try:
        if len(user_available) == 1:
            sql = "select user_id, arrival_timestamp, poi_name from staypoint where user_id = "+str(user_available[0])+" order by id"
        else:
            for user in user_available:
                sql = "select user_id, arrival_timestamp, poi_name from staypoint where user_id in "+tuple(user_available).__str__()+" order by id"
                print sql
                result = cursor.execute(sql)
                result = cursor.fetchall()
                conn.commit()
    except Exception, e:
        print e
        conn.rollback()
    cursor.close()
    conn.close()

    if split_percent < 1:
        length = len(result) * split_percent
        result = result[:length]
    print result

    poi_set = set()
    user_set = set()
    for item in result:
        poi_set.add(item[2])
        user_set.add(item[0])

    poi_num = len(poi_set)
    user_num = len(user_set)
    print "poi数目：", poi_num
    print "用户数目：", user_num

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

    data = {}
    train_data = {}
    check_data = {}
    for user in range(user_num):
        data[user] = []
        train_data[user] = []
        check_data[user] = []
    for item in result:
        data[users_axis[item[0]]].append((stamp2slice(item[1]), pois_axis[item[2]], item[1]))  # (用户，时间，地点)

    for key in data.keys():
        print "用户" + str(key) + "序列长度为" + str(len(data[key]))
    if train_percent < 1:
        for key in data.keys():
            length = int(train_percent * len(data[key]))
            train_data[key] = data[key][:length]
            check_data[key] = data[key][length:]
    else:
        train_data = data
        check_data = None
    return train_data, axis_users, axis_pois, check_data


def init_data_by_user_return_gps(users, filter_count, train_percent=1):
    conn = MySQLdb.connect(host=settings.HOST, user=settings.USER, passwd=settings.PASSWORD, db=settings.DB)
    cursor = conn.cursor()
    result = 0

    try:
        if len(users) == 1:
            sql = "select user_id from staypoint where user_id = "+str(users[0]) +" and province = '北京市' and district = '海淀区' group by user_id having count(*) > "+str(filter_count)
        else:
            sql = "select user_id from staypoint where user_id in "+users.__str__() +" and province = '北京市' and district = '海淀区' group by user_id having count(*) > "+str(filter_count)
        result = cursor.execute(sql)
        result = cursor.fetchall()
        conn.commit()
    except Exception, e:
        print e
        conn.rollback()

    user_available = []
    for item in result:
        user_available.append(int(item[0]))
    if len(user_available) == 0:
        raise "没有足够数据"
    print user_available

    try:
        if len(user_available) == 1:
            sql = "select user_id, arrival_timestamp, poi_name, mean_coordinate_latitude, mean_coordinate_longtitude from staypoint where user_id = "+str(user_available[0])+" and province = '北京市' and district = '海淀区' order by id"
        else:
            sql = "select user_id, arrival_timestamp, poi_name, mean_coordinate_latitude, mean_coordinate_longtitude from staypoint where user_id in "+tuple(user_available).__str__()+" and province = '北京市' and district = '海淀区' order by id"
        print sql
        result = cursor.execute(sql)
        result = cursor.fetchall()
        conn.commit()
    except Exception, e:
        print e
        conn.rollback()
    cursor.close()
    conn.close()

    print result
    poi_set = set()
    user_set = set()
    for item in result:
        poi_set.add(item[2])
        user_set.add(item[0])

    poi_num = len(poi_set)
    user_num = len(user_set)
    print "poi数目：", poi_num
    print "用户数目：", user_num

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

    data = {}
    train_data = {}
    check_data = {}
    for user in range(user_num):
        data[user] = []
        train_data[user] = []
        check_data[user] = []
    for item in result:
        data[users_axis[item[0]]].append((stamp2slice(item[1]), pois_axis[item[2]], item[1], item[3], item[4]))  # (用户，时间，地点)

    for key in data.keys():
        print "用户" + str(key) + "序列长度为" + str(len(data[key]))
    if train_percent < 1:
        for key in data.keys():
            length = int(train_percent * len(data[key]))
            train_data[key] = data[key][:length]
            check_data[key] = data[key][length:]
    else:
        train_data = data
        check_data = None
    return train_data, axis_users, axis_pois, check_data


# 计算time_stamp所处时间片
def stamp2slice(time_stamp):
    return int(time_stamp % 86400 // (3600 * (24 // settings.TIME_SLICE)))


# 将两个序列进行相交操作
def intersect_sequence(sequence_a, sequence_b):
    start_a = sequence_a[0][2]
    end_a = sequence_a[-1][2]
    start_b = sequence_b[0][2]
    end_b = sequence_b[-1][2]
    start = max(start_a, start_b)
    end = min(end_a, end_b)
    # print "开始-结束时间片: ", start, end
    if start > end:
        return None, None
    else:
        new_sequence_a = []
        new_sequence_b = []
        for i in range(len(sequence_a)):
            if start <= sequence_a[i][2] <= end:
                new_sequence_a.append(sequence_a[i])
        for j in range(len(sequence_b)):
            if start <= sequence_b[j][2] <= end:
                new_sequence_b.append(sequence_b[j])
        return new_sequence_a, new_sequence_b


# 将两个序列进行对齐操作
def alignment_sequence(sequence_a, sequence_b):
    print "对齐前序列长度: ", len(sequence_a), len(sequence_b)
    for i in range(len(sequence_a)):
        flag = False
        index = 0
        time = sequence_a[i][2]
        for j in range(len(sequence_b)):
            align_time = sequence_b[j][2]
            if align_time < time:
                index += 1
            if abs(align_time - time) <= (5 * 60):
                flag = True
                break
        if flag:
            continue
        else:
            insert_item = (sequence_a[i][0], sequence_b[index-1][1], time)
            sequence_b.insert(index, insert_item)

    for i in range(len(sequence_b)):
        flag = False
        index = 0
        time = sequence_b[i][2]
        for j in range(len(sequence_a)):
            align_time = sequence_a[j][2]
            if align_time < time:
                index += 1
            if abs(align_time - time) <= (5 * 60):
                flag = True
                break
        if flag:
            continue
        else:
            insert_item = (sequence_b[i][0], sequence_a[index-1][1], time)
            sequence_a.insert(index, insert_item)

    print "对齐后序列长度: ", len(sequence_a), len(sequence_b)
    return sequence_a, sequence_b