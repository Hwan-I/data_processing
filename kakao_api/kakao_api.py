# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 23:15:47 2020

@author: User
"""

import requests
import json
import account_loader as acc


class ExceedError(Exception):
    """
    api 사용량이 초과했을 때 발생하는 Error입니다.
    """
    
    def __init__(self):
        super().__init__('the amount used is exceeded.')


def neighbor_category_search_dist(coor_list, category, total_check_option = True):
    """
    kakao rest api를 이용하여 특정 구역 안에 있는 카테고리 변수에 대한 정보를 
    추출합니다.
    
    참고로 아래 rest_api, headers에 해당 값을 넣어줘야합니다.
    
    left_x, left_y, right_x, right_y
    
    Parameters
    ----------
    coor_list : like list, array
        좌표 값을 가진 list 타입의 객체입니다. 원소는 다음과 같이 정의해야 합니다.
        사각형 객체를 기준으로 합니다.(0,1을 SW, 2,3을 NE로 잡을 때 기준입니다.)
        좀 더 자세한 사항을 알고 싶으시면 아래 링크를 참조하시기 바랍니다.
        https://devtalk.kakao.com/t/rest-api-rect/105852
        
        coor_list[0] : 왼쪽 x좌표
        coor_list[1] : 아래 y좌표
        coor_list[2] : 오른쪽 x 좌표 
        coor_list[3] : 위쪽 y 좌표 
        ex) [1,1,3,4]
        
    category : str
        rest api의 카테고리. 자세한 사항은 아래 주석 참조.
    total_check_option : TYPE, optional
        total 값만 출력할지 여부를 결정. 기본값은 True.

    Raises
    ------
    ExceedError
         api 사용량이 초과했을 때 발생하는 Error

    Returns
    -------
    place_list : list
        해당 장소의 이름입니다.
    address_list : list
        해당 장소의 주소입니다.
    x_list : list
        해당 장소의 위도입니다.
    y_list : list
        해당 장소의 경도입니다.
    id_list : list
        해당 장소의 id값입니다.
    total_count : int
        조건에 만족하는 카테고리의 총 개수입니다.

    
    category : 카테고리 코드(아래 코드 참조)
    MT1 : 대형마트       |    CS2 : 편의점    |  PS3 : 어린이집, 유치원
    SC4 : 학교           |    AC5 : 학원      | PK6 : 주차장
    OL7 : 주유소, 충전소 |    SW8 : 지하철역   | BK9 : 은행
    CT1 : 문화시설       |    AG2 : 중개업소  |  PO3 : 공공기관
    AT4 : 관광명소       |    AD5 : 숙박      | FD6 : 음식점
    CE7 : 카페           |    HP8 : 병원      | PM9 : 약국
    
    """

    # url : 바꿀 주소.
    
    
    
    # rest_api, headers를 아래 변수에 넣으면 됨.
    rest_api, headers = acc.kakao_api()
    
    left_x, left_y, right_x, right_y = coor_list
    
    url = 'https://dapi.kakao.com/v2/local/search/category.json?category_group_code='+str(category)+'&rect=%s,%s,%s,%s'%(left_x, left_y, right_x, right_y)
    
    result = json.loads(requests.get(url,headers=headers).text)
        
    try:
        total_count = result['meta']['total_count']
        
    except KeyError:
        message = result['message']
        print(message)
        if 'exceeded.' in message :
            raise ExceedError
    
    if total_check_option == True:
        if total_count> 45:
            return 0, 0, 0, 0, 0, total_count
    
    
    # 각 정류소에 해당하는 위치이름, 주소, 거리값을 넣을 리스트
    place_list = []
    address_list = []
    x_list = []
    y_list = []
    id_list = []
    
    # 한번에 최대 45개의 독립된 객체값을 가지며 그 이후 페이지는 중복된 장소가 나옵니다.
    for page_num in range(1,4) :

        url = 'https://dapi.kakao.com/v2/local/search/category.json?category_group_code='+str(category)+'&rect=%s,%s,%s,%s'%(left_x, left_y, right_x, right_y)+'&page='+str(page_num)
        result = json.loads(requests.get(url,headers=headers).text)
        #print(result)
        
        try:
            each_result = result['documents']
        
        except KeyError:
            message = result['message']
            if 'exceeded.' in message :
                raise ExceedError
        for j in each_result :
            

            place_name = j['place_name']
            address = j['road_address_name']
            x = j['x']
            y = j['y']
            ids = j['id']
            
            # 각 리스트에 추가함.
            place_list.append(place_name)
            address_list.append(address)
            x_list.append(x)
            y_list.append(y)
            id_list.append(ids)
            #print(j['distance'])
        
        if result['meta']['is_end'] == True:
            break
        
    return place_list, address_list, x_list, y_list, id_list, total_count