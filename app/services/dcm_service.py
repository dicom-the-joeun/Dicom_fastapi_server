from io import BytesIO
from app.conf.ftp_config import FTPConfig
from app.util.dcm_gen import ConvertDCM

ftp = FTPConfig()


class DcmService:
    @staticmethod
    def get_dcm(filepath, filename):
        # filepath = f'/{filename}'
        conv = ConvertDCM()
        try:
            ftp.connect()
            print(filepath)
            data = ftp.getdata(filepath=filepath, filename=filename)
        except Exception as e:
            print(f'문제는 {e}')
        finally:
            ftp.disconnect()
            return conv.dicomToJSON(data)
