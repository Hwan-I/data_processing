# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 19:20:50 2019

@author: User
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 18:35:23 2019

@author: User
"""

# 날씨 변수 전처리.

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import configparser
import sys

defalut_path = os.getcwd()
load_weather_path = os.path.join(defalut_path,'data\\var\\raw\\weather/')
save_weather_path = os.path.join(defalut_path,'data\\var\\processed\\weather/')

load_weather_train_path = os.path.join(load_weather_path, 'train\\')
load_weather_test_path = os.path.join(load_weather_path, 'test\\')

save_weather_train_path = os.path.join(save_weather_path, 'train\\')
save_weather_test_path = os.path.join(save_weather_path, 'test\\')

config = configparser.ConfigParser()
config.read(sys.argv[1])
train_year = config['settings']['train']
test_year = config['settings']['test']

train_start = config['settings']['train_start']
train_end = config['settings']['train_end']
test_start = config['settings']['test_start']
test_end = config['settings']['test_end']



def change_df(df, value_name):
    """
    *** 필요한 컬럼 추출 및 컬럼 이름 변환 ***
    
    df : 변환할 dataframe
    value_name : 측정치가 저장된 컬럼 이름.
    """

    # 컬럼길이가 3과 같거나 크면 가공 안된 데이터임.
    if len(df.columns) >=3:
        
        # dust_data는 끝의 데이터 1개를 삭제해야 함
            
        # 날짜, value 값 추출
        extracted_df = df.iloc[:,[-2,-1]]
        # 컬럼 이름 바꿈.
        
        # 3보다 작으면 가공 된 데이터
        extracted_df.columns = ['date', value_name]
        extracted_df['date'] = pd.to_datetime(extracted_df['date']) 
        
        # 마지막 row 값이 year가 다른지 찾음.
       
        last_row_year = extracted_df.loc[len(extracted_df)-1,'date'].year
        
        compared_row_year = extracted_df.loc[0,'date'].year
        
        if last_row_year != compared_row_year:
            last_label = len(extracted_df)-1
            extracted_df.drop(last_label, inplace=True)
            
        return extracted_df


def fill_nan_hum_cloud(df_):
    """
    습도, 운량의 NaN값에 값을 넣음
    앞 뒤 1시간의 값을 기준으로 함.
    """
    
    for col in ['humidity', 'cloud']:
        for ind in range(len(df_)):
            if np.isnan(df_.loc[ind,col]):
                
                # ind가 0인 경우 처리법.
                if ind == 0:
                     df_.loc[ind,col] = df_[~df_[col].isnull()].reset_index().loc[0,col].squeeze()
                     continue
                
                try :
                    if np.isnan(df_.loc[ind+1,col]):
                        df_.loc[ind,col] = df_.loc[ind-1,col]
                    else:
                        df_.loc[ind,col] = np.mean([df_.loc[ind-1,col], df_.loc[ind+1,col]])
                
                except(KeyError):
                    print("끝")
                    break
    
    return df_


def fill_nan_rain_binary(df_):
    """
    비 데이터를 비가 안오면 0, 오면 1로 처리함
    """
    
    df_['rain_state'] = 1
    one_ind = df_[~df_['rain'].isnull()].index
    
    one_ind = df_[(df_['rain'].isnull())].index.tolist()
    one_ind2 = df_[df_['rain'] == 0].index.tolist()
    one_ind = one_ind + one_ind2
    
    df_.loc[one_ind, 'rain_state'] = 0
    df_['rain'] = df_['rain_state']
    df_ = df_.drop('rain_state', axis=1)
    
    
    return df_


def rain_data_processing():   
    
    rain_data_name = ['rain_%s'%(train_year), 'rain_%s'%(test_year)]
    train_test_path = [load_weather_train_path, load_weather_test_path]
    rain_train_test_list = []
    
    for num_i in range(2):
        r_data_name = rain_data_name[num_i]
        t_t_path = train_test_path[num_i]
        
        try :
            rain_hour = pd.read_csv(t_t_path+'%s_hour.csv' %r_data_name, encoding='euckr', parse_dates=['일시'])
        except(FileNotFoundError):
            return []
            
        rain_day = pd.read_csv(t_t_path+'%s_day.csv' %r_data_name, encoding='euckr', parse_dates=['일시'])
        rain_hour.columns = ['sta', 'sta_name','date', 'rain', 'humidity', 'cloud']
        rain_day.columns = ['sta','sta_name','date','hr','d_rain']
        

        
        
        rain_hour = fill_nan_hum_cloud(rain_hour)
        
        # 비 결측값 채우기
        rain_hour = fill_nan_rain_binary(rain_hour)
        
        rain_train_test_list.append(rain_hour)
        
    return rain_train_test_list


def distinc_train_test(num):
    """
    train, test 데이터 처리에 따라 변수 할당
    """
    
    if num == 0:
        t_t = 'train'
        year = train_year
        start_date = train_start
        end_date = train_end
        load_path = load_weather_train_path
        save_path = save_weather_train_path
    else :
        t_t = 'test'
        year = test_year
        start_date = test_start
        end_date = test_end
        load_path = load_weather_test_path
        save_path = save_weather_test_path
        
    return t_t, year, start_date, end_date, load_path, save_path


def load_file(path_, file_name, skip_option=False):
    if skip_option == True:
        df = pd.read_csv(path_ + file_name, encoding='euc-kr', skiprows=5)
    else:
        df = pd.read_csv(path_ + file_name, encoding='euc-kr')

    return df


def fill_nan(df_, nan_check_col_, target_date):
    for i in nan_check_col_:
        
        # null인 index 값들 구함.
        null_index = df_[i][df_[i].isnull()].index.values
        
        # 과거 3일, 미래 3일 값을 기준으로 합할 값을 구함.
        for j in null_index:
            target_mean_list = []
            
            for k in range(target_date):
                
                try:
                    before_data = df_.loc[j-24*(k+1),i].squeeze()
                    after_data = df_.loc[j-24*((k+1)*-1),i].squeeze()
                    if np.isnan(before_data) == False:
                        target_mean_list.append(df_.loc[j-24*(k+1),i])
                    if np.isnan(after_data) == False:
                        target_mean_list.append(df_.loc[j-24*((k+1)*-1),i])
                
                # 만약 과거 데이터, 미래 데이터가 없는경우 pass 시킴.
                except(KeyError):
                    pass
                
            df_.loc[j, i] = np.mean(target_mean_list)
            
    df_.fillna(0, inplace=True)
    
    return df_



def check_variable(load_path_):
    
    """
    실제로 있는 변수만 추출하게 만드는 함수
    """
    
    check_var_list = [i.split('_')[0] for i in os.listdir(load_path_)]
    t_weather_list = ['dust', 'snow', 'sun', 'temp', 'wind']
    ind_list = []
    for i in range(len(t_weather_list)):
        
        c_var = t_weather_list[i]
        
        if c_var in check_var_list:
            ind_list.append(i)
            continue
        
    t_weather_list = np.array(t_weather_list)[ind_list].tolist()

    return t_weather_list
            
            



def main():
    
    
    

    rain_train_test_list = rain_data_processing()
    
    for k in range(2):
        
        t_t, year, start_date, end_date, load_path, save_path = distinc_train_test(k)
        
        
        t_weather_list = check_variable(load_path)
        
        variable_list = []

        for t_var in t_weather_list:

            if t_var == 'dust':
                t_data = load_file(load_path, '%s_%s.csv'%(t_var, year), skip_option=True)
            else:
                t_data = load_file(load_path, '%s_%s.csv'%(t_var, year))
            variable_list.append(t_data)
        
        
        if len(rain_train_test_list) != 0:
            rain_data = rain_train_test_list[k][['sta','date','rain']]
            humidity_data = rain_train_test_list[k][['sta','date','humidity']]
            cloud_data = rain_train_test_list[k][['sta','date','cloud']]
            
            variable_list.append(rain_data)
            variable_list.append(humidity_data)
            variable_list.append(cloud_data)
            
            t_weather_list.append('rain')
            t_weather_list.append('humidity')
            t_weather_list.append('cloud')
            
        
        for i in range(len(variable_list)):
            variable_list[i] = change_df(variable_list[i], t_weather_list[i])

        data_period = pd.date_range(start=start_date ,freq='H',end = end_date)
        
        weather_data = pd.DataFrame({'date': data_period})

        
        # 데이터를 merge하여 없는 값은 0 또는 평균값으로 처리함.
        # 왼쪽 데이터를 기준으로 합치는 작업임
        
        for i in variable_list:
            weather_data = pd.merge(weather_data, i, how='left', on='date')
        
            
        weather_data = weather_data.reset_index(drop=True)
        
        # null 값 처리 : 온도, 풍속, 습도 빼고 전부 0으로 처리함
        # 온도
            # 1. NaN 값 확인
        
        nan_check_col = ['temp','wind']
                # NaN값을 평균 6일치 이전, 이후(각 3일) 데이터의 값을 기준으로 구함

        weather_data = fill_nan(weather_data, nan_check_col, 3)
        
        weather_data.to_csv(save_path+'weather_%s_data.csv'%year, index=False)



if __name__ == "__main__":
    main()
    
    
    