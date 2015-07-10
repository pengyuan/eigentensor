#!/usr/bin/env python
# coding: UTF-8
import json
import urllib

import MySQLdb
import settings


def main():
    conn = MySQLdb.connect(host = settings.HOST, user = settings.USER, passwd = settings.PASSWORD, db = settings.DB)
    cursor = conn.cursor()
    
    try:
        sql = "select max(id) from staypoint4"
        cursor.execute(sql)
        count = cursor.fetchall()
        conn.commit()
    except Exception, e:
        print e

    staypoint_count = count[0][0]
    # print "staypoint_count: ", staypoint_count
    trans_error_count = 0
    trans_error_id = []
    geocode_error_count = 0
    geocode_error_id = []
    poi_empty_count = 0
    poi_empty_id = []
    
    for i in range(25046, staypoint_count):
        staypoint_id = str(i+1)
        # print "staypoint_id: ", staypoint_id
        try:
            sql = "select * from staypoint4 where id = '"+ staypoint_id + "'"
            cursor.execute(sql)
            result = cursor.fetchall()
            conn.commit()
        except Exception, e:
            print e
        # print result
        param = str(result[0][5]) + "," + str(result[0][4])
        trans = "http://api.map.baidu.com/geoconv/v1/?coords="+ param +"&from=1&to=5&ak=DYP2kZ5ya82AoymqK7mg8ves"
        
        
        # ak=DYP2kZ5ya82AoymqK7mg8ves
                
                
        f = urllib.urlopen(trans)
        s = f.read() 
        #print s

        trans_result = json.loads(s)
        #print trans_result.keys()
        if trans_result["status"] == 0:
            result_x = trans_result["result"][0]["x"]
            result_y = trans_result["result"][0]["y"]
            new_param = str(result_y) + "," + str(result_x)
            
            url = "http://api.map.baidu.com/geocoder/v2/?ak=DYP2kZ5ya82AoymqK7mg8ves&location="+ new_param +"&output=json&pois=1"
            f = urllib.urlopen(url)
            s = f.read() 
            #print s
            
            geocode_result = json.loads(s)
            #print geocode_result  
            poi_name = u"[]"
            
            if geocode_result["status"] == 0:
                #print geocode_result["result"]["formatted_address"]
                formatted_address = geocode_result["result"]["formatted_address"]
                business = geocode_result["result"]["business"]
                addressComponent = geocode_result["result"]["addressComponent"]
                province = addressComponent["province"]
                city = addressComponent["city"]
                district = addressComponent["district"]
                street = addressComponent["street"]
                
                pois = geocode_result["result"]["pois"]
                if pois: 
                    ordered_pois = sorted(pois, key=lambda poi: int(poi["distance"]))
                    #for item in ordered_pois:
                    #    print item["distance"] +" "+item["name"]
                    poi_address = ordered_pois[0]["addr"]
                    poi_name = ordered_pois[0]["name"]
                    poi_type = ordered_pois[0]["poiType"]
                    poi_distance = ordered_pois[0]["distance"]
                    poi_uid = ordered_pois[0]["uid"]
                    
                    sql = "update staypoint4 set formatted_address='"+formatted_address+"',business='"+business+"',province='"+province+"',city='"+city+"',district='"+district +"',street='"+street+"',poi_address='"+poi_address+"',poi_name='"+poi_name+"',poi_type='"+poi_type+"',poi_distance="+poi_distance+",poi_uid='"+poi_uid+"' where id='"+staypoint_id+"'"
                 
                else:
                    poi_empty_count += 1
                    poi_empty_id.append(staypoint_id)
                    sql = "update staypoint4 set formatted_address='"+formatted_address+"',business='"+business+"',province='"+province+"',city='"+city+"',district='"+district +"',street='"+street+"' where id='"+staypoint_id+"'"
                       
                try:
                    cursor.execute(sql)
                    conn.commit()
                except Exception, e:
                    print e
                    conn.rollback()
                
            else:
                geocode_error_count +=1
                geocode_error_id.append(staypoint_id)
                
            print staypoint_id+ " " +param+" "+formatted_address+" "+poi_name+". status["+str(trans_error_count)+","+str(geocode_error_count)+","+str(poi_empty_count)+"]"
    
        else:
            trans_error_count += 1
            trans_error_id.append(staypoint_id)
        
        #new_param = str(result_y) + "," + str(result_x)
        #print new_param
  

    print "任务已完成"
    if trans_error_count > 0:
        print "GPS坐标转换为百度坐标的错误数为"+str(trans_error_count)+",具体ID为"+trans_error_id
    if geocode_error_count > 0:    
        print "百度坐标转换为POI的错误数为"+str(geocode_error_count)+",具体ID为"+geocode_error_id
    if poi_empty_count > 0:
        print "百度坐标转换为POI结果为空的数目为"+str(poi_empty_count)+",具体ID为"+poi_empty_id
    cursor.close()
    conn.close()


if __name__ == '__main__':
    main()