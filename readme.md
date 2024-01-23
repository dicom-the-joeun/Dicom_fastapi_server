# 기본구조 
conf : DB설정, 
    - DB_CONFIG : Mysql, Oracle든 모든 할수 있게, SqlAlchemy 라이브러리를 써서 만들었습니다.  
    - FTP CONFIG : FTP연결 도와주는 애   
    - config.ini : 
    - log_config_prod.ini : 

controller : Router줄 데이터들을 꾸며서준다.

models : 
    - DBModel : DB 모델은 실제 DB와 같아야함. 
    - APIModel : API 모델은 input output 지정해주는것.
      -> 좋은 점은 미리 거름. TYPE체크 할때.

Service : 데이터만 들고 온다. 

Util : 서버 연결 안하고, 너무자주쓰이는 함수들 묶어서, 만들어놓고 그때그떄 부르려고.



