from app.conf.ftp_config import FTPConfig
from app.models.api_model import SelectSereies, SelectThumbnail
from app.models.db_model import ImageViewTab, SeriesTab
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
    def get_dcm_img(filepath, filename, index=0):
        conv = ConvertDCM()
        try:
            ftp.connect()
            data = ftp.getdata(filepath=filepath, filename=filename)
        except Exception as e:
            print(f'문제는 {e}')
        finally:
            ftp.disconnect()
            return conv.dicomToPNG(data, index)

    @staticmethod
    async def get_seriestab_all_studykey(studykey, db) -> List[SelectThumbnail]:
        thumbnails = db.query(SeriesTab).filter(
            SeriesTab.STUDYKEY == studykey).all()
        return thumbnails

    @staticmethod
    async def get_seriestab_one(studykey, serieskey, db) -> List[SelectSereies]:
        image_fname_all = db.query(ImageViewTab.IMAGEKEY, ImageViewTab.PATH, ImageViewTab.FNAME).filter(
            ImageViewTab.STUDYKEY == studykey, ImageViewTab.SERIESKEY == serieskey).all()
        return [SelectSereies(IMAGEKEY=row.IMAGEKEY, PATH=row.PATH, FNAME=row.FNAME) for row in image_fname_all]
