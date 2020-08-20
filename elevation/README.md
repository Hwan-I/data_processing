# elevation

* 구글 api를 활용하여 특정 지점의 고도값을 추출합니다. (It extracts an elevation value a specific position using Google API.)
* 출발지점 ~ 도착지점까지 100m 등 특정 meter로 나눈 지점들의 고도값을 구할 수 있습니다  (you can find elevation values of the points that are divided position by interval like 100 meter from a starting point to a arrival point)
* input 변수는 'start_coor', 'end_coor', 'dist', 'per_dist', 'api_key'로 구성되어 있습니다. (input arguments are 'start_coor', 'end_coor', 'dist', 'per_dist', 'api_key')
  * 자세한 부분은 코드 안의 docstring을 참고하시면 됩니다. (if you want to know detail related to arguments and more, you can refer docstring in the code called 'elevation_api.py')


### 설치해야하는 패키지(required packages)
* 없음 : python 3 버전 설치시 기본 제공되는 패키지 사용함 (none : packages using just default packages in python 3)

### 기타사항
* api key 변수에 할당 받은 api key를 str 변수로 넣으면 됩니다. (you need to input your api key from Google into variable called 'api_key'.)