# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 22:23:14 2020

@author: User
"""

import requests
import json

def make_sample_n(dist, per_dist):
    """
    dist에 대해 per_dist 값을 가지는 샘플을 만들 때 최대한 per_dist에 가깝도록 path를 나눔
    예를들어 800m를 100m 단위로 쪼개고 싶으면 시작점부터 끝점까지 9개의 점을 가지게 됨 
    
    Parameters
    ----------
    dist : int
        시작점에서 끝점까지 총 거리.
    per_dist : int
        구하고 싶은 구간 거리.

    Returns
    -------
    sample_n : int
        총 거리를 구간 거리로 나눌 때 가장 적절한 숫자.

    """
    
    
    mul1 = dist // per_dist
    mul2 = mul1 + 1
    
    # per_dist에 가까운 sample_n 찾기
    if mul1 != 0:
        check_mul1 = abs(per_dist - (dist / mul1))
    else :
        check_mul1 = per_dist * dist * 100
        
    check_mul2 = abs(per_dist - (dist / mul2))
    
    # 차이가 더 작은 값으로!
    if check_mul1 >= check_mul2:
        sample_n = int(mul2 + 1)
    else:
        sample_n = int(mul1 + 1)

    return sample_n


def request_api(start_coor, end_coor, dist, per_dist, api_key, auto_sample_n):
    """
    시작지점에서 끝지점까지의 거리를 일정 거리값으로 나누어 나누어진 
    point(지점)별로 고도값을 구함.
    
    * 만약 특정 point 지점의 고도만 구하고자 한다면 end_coor=[], 
    auto_sample_n=False로 해야함
    

    Parameters
    ----------
    start_coor : like 1d array(just 2 element)
        시작 지점의 위도와 경도. 
        ex) [32.561, 127.5123]
    end_coor : like 1d array(just 2 element or 0)
        끝 지점의 위도와 경도(start_coor과 유사함).
        단, 특정 point에 대한 좌표만 구하고자 한다면 '[]'와 같이 빈 array 객체를 넣으면 됨
        
    dist : int
        시작점에서 끝점까지 총 거리.
    per_dist : int
        구하고 싶은 구간 거리.
    api_key : str
        구글 elevation api를 쓰는데 사용하는 api_key.
    sample_n : boolen
        True면 dist와 per_dist값에 맞춰 생성.
        특정 point에 대한 좌표만 구하고자 한다면 False
        
    Returns
    -------
    result : dict
        api request 결과.

    """
    
    if auto_sample_n == True:
        sample_n = make_sample_n(dist, per_dist)
        url = 'https://maps.googleapis.com/maps/api/elevation/json?path=%s,%s|%s,%s&samples=%s&key=%s'%(start_coor[0],start_coor[1], end_coor[0], end_coor[1], sample_n, api_key)
    elif auto_sample_n == False and len(end_coor) == 0:
        url = 'https://maps.googleapis.com/maps/api/elevation/json?locations=%s,%s&key=%s'%(start_coor[0],start_coor[1], api_key)
        
    result = json.loads(requests.get(url).text)       
    result = result['results']
    
    return result


def make_elevational_df(start_coor, end_coor, dist, per_dist, api_key):
    """
    시작지점에서 끝지점까지의 거리를 일정 거리값으로 나누어 나누어진 
    point(지점)별로 고도값을 구한 뒤 각 지점의 고도 및 좌표값을 매칭시키는 dict 형성

    Parameters
    ----------
    start_coor : like 1d array(just 2 element)
        시작 지점의 위도와 경도. 
        ex) [32.561, 127.5123]
    end_coor : like 1d array(just 2 element or 0)
        끝 지점의 위도와 경도(start_coor과 유사함).
        단, 특정 point에 대한 좌표만 구하고자 한다면 '[]'와 같이 빈 array 객체를 넣으면 됨
        
    dist : int
        시작점에서 끝점까지 총 거리.
    per_dist : int
        구하고 싶은 구간 거리.
    api_key : str
        구글 elevation api를 쓰는데 사용하는 api_key.
    
    Returns
    -------
    final_dict : dict
        결과값인 elevation, lat 등의 정보를 담은 dict. 
        각 key값의 value는 list로 index 순서에 각 정보가 매칭됨
    
        key값
        resolution : 해상도 (고도 값의 정확도랑 관련된 값)
        elevation : 해당 지점(point)의 고도값
        lat : 해당 지점의 위도값
        long : 해당 지점의 경도값
        path : 해당 지점의 번호
            ex) 0 ~ 500m까지 100m 구간으로 나누면 0m는 0, 100m는 1, ..., 500m는 5
    
    """
    
    resolution_list = []
    elevation_list = []
    lat_list = []
    long_list = []
    path_list = []
    
    
    api_result = request_api(start_coor, end_coor, dist, per_dist, api_key)
    
    path = 0
    for r_i in range(len(api_result)):
        result_dict = api_result[r_i]
        loc = result_dict['location']
        elev = result_dict['elevation']
        resol = result_dict['resolution']
        lat = loc['lat']
        lng = loc['lng']
        
        resolution_list.append(resol)
        elevation_list.append(elev)
        lat_list.append(lat)
        long_list.append(lng)
        path_list.append(path)
                    
        path +=1
    
    
    final_dict = {}
    
    final_dict['resolution'] = resolution_list
    final_dict['elevation'] = elevation_list
    final_dict['lat'] = lat_list
    final_dict['long'] = long_list
    final_dict['path'] = path_list
    
    return final_dict





#%%
#start_coor = []
#end_coor = []
#dist= 1000
#per_dist = 100
#api_key = ''

#result = make_elevational_df(start_coor, end_coor, dist, per_dist, api_key)


 