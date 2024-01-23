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




error memo:
1. studykey 3번 요청시 해당사항 발생,
C:\Users\TJ\dicom\dicom_fastapi_server\env\Lib\site-packages\pydicom\valuerep.py:443: UserWarning: Invalid value for VR UI: '1.2.410.200013.1.510.1.20210310170346701.0009'. Please see <https://dicom.nema.org/medical/dicom/current/output/html/part05.html#table_6.2-1> for allowed values for each VR.
  warnings.warn(msg)
C:\Users\TJ\dicom\dicom_fastapi_server\env\Lib\site-packages\pydicom\valuerep.py:443: UserWarning: Invalid value for VR UI: '1.2.410.200013.1.510.1.20210310170346491.0007'. Please see <https://dicom.nema.org/medical/dicom/current/output/html/part05.html#table_6.2-1> for allowed values for each VR.
  warnings.warn(msg)
C:\Users\TJ\dicom\dicom_fastapi_server\env\Lib\site-packages\pydicom\valuerep.py:443: UserWarning: Invalid value for VR UI: '1.2.410.200013.1.510.1.20210310170346596.0008'. Please see <https://dicom.nema.org/medical/dicom/current/output/html/part05.html#table_6.2-1> for allowed values for each VR.
  warnings.warn(msg)
해석 : 이 경고는 pydicom 라이브러리에서 발생한 것으로 보입니다. 이는 VR(값 표현)이 UI(고유 식별자)에 대해 잘못된 값이 사용되었다는 경고입니다. 경고에서 제공된 링크를 통해 허용된 값에 대한 자세한 정보를 확인할 수 있습니다. 라이브러리를 사용하는 코드에서 이러한 VR에 대한 올바른 값으로 수정하거나, VR이 필요하지 않은 경우에는 해당 필드를 수정하여 경고를 해결할 수 있습니다.
