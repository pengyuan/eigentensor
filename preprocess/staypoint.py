#!/usr/bin/env python
# coding: UTF-8
# extract stay points from a GPS log file
# implementation of algorithm in 
# [1] Q. Li, Y. Zheng, X. Xie, Y. Chen, W. Liu, and W.-Y. Ma, "Mining user similarity based on location history", in Proceedings of the 16th ACM SIGSPATIAL international conference on Advances in geographic information systems, New York, NY, USA, 2008, pp. 34:1--34:10.
 
from ctypes import *
from math import radians, cos, sin, asin, sqrt
import run_time
import MySQLdb
import settings


time_format = '%Y-%m-%d,%H:%M:%S'
 
# structure of stay point
class stayPoint(Structure):
    _fields_ = [
        ("longitude", c_double),
        ("latitude", c_double),
        ("arrivTime", c_uint64),
        ("leaveTime", c_uint64)
    ]
 
# calculate distance between two points from their coordinate
def getDistance(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    m = 6371000 * c
    return m
    
def computMeanCoord(gpsPoints):
    lon = 0.0
    lat = 0.0
    for point in gpsPoints:
        #fields = point.rstrip().split(',')
        lon += float(point[3])
        lat += float(point[2])
    return (lon/len(gpsPoints), lat/len(gpsPoints))
 
# extract stay points from a GPS log file
# input:
#        file: the name of a GPS log file
#        distThres: distance threshold
#        timeThres: time span threshold
# default values of distThres and timeThres are 200 m and 30 min respectively, according to [1]

# staypoint1: 200m, 30min
# staypoint2: 50m, 10min
# staypoint3: 50m, 5min
# staypoint4: 50m, 2min
# staypoint5: 200m, 15min

def stayPointExtraction(result, distThres = 200, timeThres = 15*60):
    stayPointList = []
    #log = open(file, 'r')
    #points = log.readlines()[6:] # first 6 lines are useless
    pointNum = len(result)
    i = 0
    while i < pointNum-1: 
        j = i+1
        while j < pointNum:
            field_pointi = result[i]
            field_pointj = result[j]
            dist = getDistance(float(field_pointi[3]),float(field_pointi[2]),
                               float(field_pointj[3]),float(field_pointj[2]))
            
            if dist > distThres: 
                deltaT = (field_pointj[-1] - field_pointi[-1]).seconds
                #print "deltaT: ", deltaT
                if deltaT > timeThres:
                    sp = stayPoint()
                    sp.latitude, sp.longitude = computMeanCoord(result[i:j+1])
                    sp.arrivTime, sp.leaveTime = int(run_time.mktime(field_pointi[-1].timetuple())), int(run_time.mktime(field_pointj[-1].timetuple()))
                    stayPointList.append(sp)
                i = j
                break
            j += 1
        # Algorithm in [1] lacks following line
        i += 1
    return stayPointList


def main():
    conn = MySQLdb.connect(host = settings.HOST, user = settings.USER, passwd = settings.PASSWORD, db=settings.DB)
    cursor = conn.cursor()
    
    try:
        sql = "select max(user_id) from geolife"
        cursor.execute(sql)
        count = cursor.fetchall()
        conn.commit()
    except Exception, e:
        print e
        conn.rollback()

        
    user_count = count[0][0] + 1
    
    for i in range(user_count):
        user_id = str(i)
        try:
            sql = "select * from geolife where user_id = '"+ user_id + "' order by gps_datetime"
            cursor.execute(sql)
            result = cursor.fetchall()
            conn.commit()
        except Exception, e:
            print e
            conn.rollback()
            
        staypoint_list = stayPointExtraction(result)
        #print "用户"+ user_id +"有" +str(len(result)) +"个GPS记录，" + str(len(staypoint_list)) +"个停留点"

        for item in staypoint_list:
            try:
                sql = "insert into staypoint5(user_id, arrival_timestamp, leaving_timestamp, mean_coordinate_longtitude, mean_coordinate_latitude) values('%d','%d','%d','%f','%f')" % (int(user_id), item.arrivTime, item.leaveTime, item.latitude, item.longitude)
                cursor.execute(sql)
                conn.commit()
            except Exception, e:
                print e
                conn.rollback()

    cursor.close()
    conn.close()

 
if __name__ == '__main__':
    main()