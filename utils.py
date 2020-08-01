# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 23:25:55 2020

@author: Lee
"""

import pandas as pd
import geopandas
import shapely.geometry as geo

def convert_coordinate(coor_list, from_c=4326, to_c=5179, point_option=False) :
    """
    pandas의 데이터프레임에 있는 특정 epsg의 좌표값을 타겟 epsg 형태로 바꿔주는
    코드.
    

    Parameters
    ----------
    coor_list : numpy.ndarray
        위도,경도를 2차원형태로 가지고 있는 array.
        0번 column은 위도, 1번 column은 경도값을 가져야 함
        ex) np.array([[127.386131,36.37458], [127.392375,36.374389]])
        
        
    from_c : int
        해당 좌표의 epsg값. The default is 4326.
    to_c : TYPE, optional
        타겟(변환했을 때 결과) 좌표 epsg값. The default is 5179.

    point_option : TYPE, optional
        True면 변환한 좌표값을 Point 객체로 만들어 데이터프레임에 넣음. 
        기본값은 False.
        
    Returns
    -------
    s_pandas3_ : pandas.core.frame.DataFrame
        좌표를 바꾼뒤의 데이터프레임. lati는 위도, long은 경도.
        point_option이 True면 point라는 column은 좌표값을 geo.Point 객체로 만든 결과임.

    """
    
    from_c = 'epsg:%s'%(from_c)
    to_c = 'epsg:%s'%(to_c)
    
    x_coor = coor_list[:,0]
    y_coor = coor_list[:,1]
    
    s_pandas_ = geopandas.GeoDataFrame({'geometry':[]})   
    
    for i in range(len(coor_list)):

        x = x_coor[i]
        y = y_coor[i]
        s_pandas_ = s_pandas_.append({'geometry':geo.Point([x,y])}, ignore_index=True)    

    s_pandas_.crs = from_c
    s_pandas2_ = s_pandas_.to_crs(to_c)
    s_pandas3_ = pd.DataFrame({'lati':[],'long':[]})
    
    for i in range(len(s_pandas2_)):

        point = s_pandas2_.loc[i,'geometry'].coords[:]
        lati = point[0][0]
        long = point[0][1]
        s_pandas3_ = s_pandas3_.append({'lati':lati,'long':long},ignore_index=True)
        print(i)
        
    if point_option == True:    
        convert_coor_list = s_pandas3_[['lati','long']].values.tolist()
        point_list = make_point(convert_coor_list)
        s_pandas3_['point'] = point_list
    
    return s_pandas3_



def make_point(coor_list):
    """ 각 원소가 위도, 경도의 리스트로 구성된 2차원 list에 대해 각 좌표(원소)를
        Point 객체로 바꿔줌.
    

    Parameters
    ----------
    coor_list : like array
        좌표값.
        ex) [[127.63,36.21],[127.64,36.351]]

    Returns
    -------
    point_list : list
        각 좌표값을 Point 객체로 바꾼 리스트 객체. 좌표 개수만큼 리스트 원소가 있음
        ex) [Point([127.63,36.21]), Point([127.64,36.351])]

    """
    
    point_list = []
    for i in range(len(coor_list)):
        coor = coor_list[i]
        point = geo.Point(coor)
        point_list.append(point)
    
    return point_list
