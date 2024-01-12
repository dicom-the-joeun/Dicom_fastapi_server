import json
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
    async def get_dcm_img_compressed(studykey, serieskey, db):
        '''
            이미지들을 반환해야함.
            @return : images `list`

            TODO: 3차원 4차원 예외 처리 필요!
        '''
        conv = ConvertDCM()
        images = []
        result = await DcmService.get_seriestab_one(studykey, serieskey, db)
        json_data =  json.loads(DcmService.get_dcm_json(filepath=result[0].PATH,
                                      filename=result[0].FNAME))
        print("jsondata", json_data)
        print(json_data["pixel array shape"])
        if json_data["pixel array shape"] == "2":
            try:
                ftp.connect()
                for one_result in result:
                    data = ftp.getdata(one_result.PATH, one_result.FNAME)
                    images.append(conv.dicomToPNG(data, 0))
            except Exception as e:
                print(f'문제는 {e}')
            finally:
                ftp.disconnect()
            return images

    @staticmethod
    def get_dcm_images_windowCenter(filepath, filename, index=0):
        conv = ConvertDCM()
        images = []
        try:
            ftp.connect()
            data = ftp.getdata(filepath=filepath, filename=filename)
            images = conv.dicomToPNGs_windows(data, index)
        except Exception as e:
            print(f'문제는 {e}')
        finally:
            ftp.disconnect()
        return images

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
