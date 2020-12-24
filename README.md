# data_processing

* 각종 데이터들을 전처리하는 코드입니다. (It is code files for proccessing a variable of data.)
* 서울시 자전거 수요 분석을 위한 각종 데이터를 전처리합니다. (It is to process a variety of data for analysing The public bike demand in the Seoul, Korea)

### 설치해야하는 패키지(required packages)
* numpy : 1.18.1
* pandas : 1.0.3
* fiona : 1.8.13.post1
* geopandas : 0.8.1
* 기타 (further information)
  * 위의 패키지 설치시 그 외 다른 패키지들은 자동으로 설치됨 (if you install these packages, you don't need to setup other packages like shapely.geometry)
  * python version : 3.7.7 

### 패키지 설치방법 (package installation method)
  -> 아나콘다3 설치해야 함(you need to install Anaconda3)
* conda create -n my_python python==3.7.7
* conda activate my_python
* conda install spyder
* conda install numpy=1.18.1 pandas=1.0.3
* conda install fiona=1.8.13.post1
* conda install geopandas==0.8.1

Dacon 대회의 코드공유에서 오신 분들은 아래 패키지를 추가설치 해야 합니다. (If you are from code sharing in Dacon conference, you need to install following packages)
* conda install plotly == 4.14.1
* conda install descartes == 1.1.0
