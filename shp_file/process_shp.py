# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 22:16:26 2020

@author: User
"""

import pandas as pd
import shapely.geometry as geo
import fiona
from shapely.geos import TopologicalError


def process_target(target, final_poly):
    """ 기존의 Polygon과 새로 들어온 좌표값을 Polygon으로 바꿔 합쳐주는 함수.
        만약 좌표가 Polygon 형태가 아니면 LineString, Point 객체로 바꿈.
    
    Parameters
    ----------
    target : like array
        Polygon 등의 객체로 만들기 위한 좌표값.
        ex) [[126,32.5],[126.99,32.456],[126.97,32.431]]

    final_poly : shapely.geometry.polygon.Polygon
        기존에 만들어진 Polygon 객체.

    Returns
    -------
    final_poly : like shapely.geometry.polygon.Polygon
        target의 값을 Polygon 등의 객체로 바꾸고 기존의 final_poly와 합친 결과값.

    """
    

    try:
        geo_polygon = geo.Polygon(target)
    
    except ValueError:
        # 객체가 LineString일 때 처리하는 방법
        geo_polygon = geo.LineString(target)
    
    except TypeError:
        # 객체가 point일 때 처리하는 방법
        if type(target[0]) == float or type(target[0]) == int:
            geo_polygon = geo.Point(target)

    try:
        final_poly = final_poly.union(geo_polygon)
    
    # buffer가 없어서 union을 못할 때 처리하는 
    except TopologicalError:  
        final_poly = final_poly.buffer(0)
        geo_polygon = geo_polygon.buffer(0)   
        final_poly = final_poly.union(geo_polygon)
    
    return final_poly



def make_tt_geo_df(file_path, zip_option=True):
    
    """ 우리나라 집계구 데이터를 가진 shp 파일에서 좌표, 집계구 값을 추출하는 함수.
    
    Parameters
    ----------
    file_path : str
        파일 path와 위치.
        ex) C:/seoul/seoul.shp
    
    zip_option : boolean, optional
        zip 번호를 수집할지에 대한 옵션. True일 경우 집계구번호를 추가로 수집함.
        기본값은 True.
    
    
    Returns
    -------
    result_df : pandas.core.frame.DataFrame
        zip_option이 True면 집계구 코드값, 집계구 polygon을 가진 dataframe 객체 반환.
        False면 집계구 polygon을 가진 dataframe만 반환.

    """

    
    tot_reg_cd_list = []
    geo_poly_list = []

    count = 0

    
    with fiona.open(file_path) as src:
        
        
        """
        for f in src : shp 파일에 들은 정보를 1개 단위씩 꺼내는 형식임. 
        f에 polygon이나 point에 대한 각종 지리적 정보들이 있으며 이는 
        dict 형식으로 key값으로 접근함.
        
        """
        
        count = 0
        for f in src:
       
            try :
                target_coordinate = f['geometry']['coordinates']
                
                
                if zip_option == True:
                    tot_num = f['properties']['TOT_REG_CD']
                    
            except(TypeError):
                print('객체에 대한 정보가 없습니다.')
                continue
            
            
            
            # 객체가 두 개 이상의 Polygon으로 나눠져 있는 경우 처리하기 위한 코드
            final_geo_poly = geo.Polygon()
            if type(target_coordinate) == tuple:
                final_geo_poly = process_target(target_coordinate, final_geo_poly)
                
            else:
                if type(target_coordinate[0]) == tuple:
                    final_geo_poly = process_target(target_coordinate, final_geo_poly)
                
                else:
                    for target_1 in target_coordinate:
                        
                        if type(target_1[0]) == tuple:
                            final_geo_poly = process_target(target_1, final_geo_poly)
                        
                        else:
                            
                            for target_2 in target_1:
                                
                                if type(target_2[0]) == tuple:
                                    final_geo_poly = process_target(target_2, final_geo_poly)
    
                                else:
                                    
                                    for target_3 in target_2:
                                        if type(target_3[0]) == tuple:
    
                                            final_geo_poly = process_target(target_2, final_geo_poly)
    
                                        else:
                                            raise ValueError("알 수 없는 좌표값입니다.")

            count +=1
            geo_poly_list.append(final_geo_poly)
            if zip_option == True:
                tot_reg_cd_list.append(tot_num)
    
    if zip_option == True:
        tot_reg_cd_list = list(map(int, tot_reg_cd_list))
    
    if zip_option == True:
        result_df = pd.DataFrame({'tot_reg_cd':tot_reg_cd_list, 'geo_poly':geo_poly_list})
    else:
        result_df = pd.DataFrame({'geo_poly':geo_poly_list})
        
    return result_df


