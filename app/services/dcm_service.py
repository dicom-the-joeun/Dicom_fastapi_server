from app.conf.ftp_config import FTPConfig
from app.models.api_model import SelectThumbnail
from app.util.dcm_gen import ConvertDCM
from typing import List
ftp = FTPConfig()


class DcmService:
    @staticmethod
    def get_dcm(filepath, filename):
        conv = ConvertDCM()
        try:
            ftp.connect()
            data = ftp.getdata(filepath=filepath, filename=filename)
        except Exception as e:
            print(f'문제는 {e}')
        finally:
            ftp.disconnect()
            return conv.dicomToJSON(data)
        
    @staticmethod
    def get_dcm_thumbnail(db) -> List[SelectThumbnail]:
        # TODO: thumbnail 빌드 만들었다.
        thumbnail = db.query()