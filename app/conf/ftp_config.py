from ftplib import FTP
from io import BytesIO
import os

from dotenv import load_dotenv


load_dotenv("./app/.env")
FTP_SERVER = os.environ.get("FTP_SERVER")   # FTP Full path
FTP_USERNAME = os.environ.get("FTP_USERNAME")
FTP_PASSWORD = os.environ.get('FTP_PASSWORD')


class FTPConfig:
    def __init__(self):
        self.host = FTP_SERVER
        self.username = FTP_USERNAME
        self.password = FTP_PASSWORD
        self.ftp = FTP(host=self.host)

    def getFTP(self):
        return self.ftp

    def connect(self):
        try:
            self.ftp.connect()
            self.ftp.login(user=self.username, passwd=self.password)
            self.ftp.cwd("/sts01")
            print(f"Connected to {self.host}")
        except Exception as e:
            print(f"FTP 연결 문제, {e}")

    def getdata(self, filepath, filename):
        file_data = BytesIO()
        self.ftp.cwd("/sts01/" + filepath)
        print("성공?"+self.ftp.cwd("/sts01/"+filepath))
        self.ftp.retrbinary(f'RETR {filename}', file_data.write)
        file_data.seek(0)
        
        print(type(file_data))
        # data = file_data.getvalue()
        # print(type(data))
        # return data

        # getvalue()로 바꿈 테스트 필요
        return file_data.getvalue()

    def disconnect(self):
        self.ftp.quit()
        print("Disconnected from FTP server")


    # local과 ftp 데이터 같은지 확인용 테스트 함수
    def getdataTestCode(self, filepath, filename):
        '''
            TODO:
            두개 다 동일한 파일로 진행
            Local 파일은 최상단에 위치 시킨다.
            인자 filepath 는 ftp에서만 사용하며 filename은 공용으로 받는다.
        '''
        from pydicom import dcmread
        
        # local file
        local_path = f'./{filename}'
        with open(local_path, 'rb') as file:
            local_data = file.read()

        # ftp file
        file_data = BytesIO()
        self.ftp.retrbinary(f'RETR {filepath}', file_data.write)
        ftp_data = file_data.getvalue()

        # DICOM 파일 해석 및 비교
        local_dicom = dcmread(BytesIO(local_data))
        ftp_dicom = dcmread(BytesIO(ftp_data))

        # 메타데이터 비교
        if local_dicom == ftp_dicom:
            print("메타데이터 일치")
        else:
            print("메타데이터 불일치")

        # 이미지 데이터 비교
        if local_dicom.pixel_array.tobytes() == ftp_dicom.pixel_array.tobytes():
            print("이미지 데이터 일치")
        else:
            print("이미지 데이터 불일치")
