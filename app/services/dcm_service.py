import json
from app.conf.ftp_config import FTPConfig
from app.models.api_model import SelectThumbnail
from app.models.db_model import SeriesTab
from app.util.dcm_gen import ConvertDCM
from typing import List
ftp = FTPConfig()


class DcmService:
    @staticmethod
    def get_dcm_json(filepath, filename):
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
    def get_dcm_img(filepath, filename):
        conv = ConvertDCM()
        try:
            ftp.connect()
            data = ftp.getdata(filepath=filepath, filename=filename)
        except Exception as e:
            print(f'문제는 {e}')
        finally:
            ftp.disconnect()
            return conv.dicomToPNG(data)

    @staticmethod
    async def get_dcm_thumbnails(studykey, db) -> List[SelectThumbnail]:
        thumbnails = db.query(SeriesTab).filter(
            SeriesTab.STUDYKEY == studykey).all()
        return thumbnails
