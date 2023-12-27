import matplotlib.pyplot as plt
from pydicom import dcmread, multival
import numpy as np
import base64
from pydicom import dcmread
from ftplib import FTP
from conf.ftp_config import FTPConfig


# FTB Config Load
CONFTP = FTPConfig()

"""
    TODO : 
    1) .dcm -> .JSON
     ** 단일 책임, 구분을 위해, FTP 연결은 dcm_service 진행.
     ** 앞단, 데이터 전송은 여기서 하는 것이 아닌, dcm_ctrl.
    
    ## 일단, 의존성 설치는 끝마쳤고, DICOMTOPNG proj에서 Method 만 복붙함.
"""

class recontrol:
    
    def __init__(self):
        CONFTP.connect()
    
    # byte to ndarray
    @staticmethod
    def Recontrol(co, arrdType, arrShape):
        """
            ### Recontrol
            Reshape Array
        """
        
        convertArray = np.frombuffer(co, dtype=arrdType)
        arrRes = np.reshape(convertArray, arrShape)
        return arrRes

    # Convert Pixel data
    @staticmethod
    def convertPixel(filename, type='b'):
        """
            ### convertPixel
            require input paths = FTP folder paths
        """
        
        '''
            TODO:
            filename을 FTP 형식으로 불러와야 함
        '''
        
        data = ''
        f = CONFTP.getFTP()
        f.retrbinary(f'RESP {filename}', data)
        if f:
            ds = dcmread(data)
            
            keys = list(ds.keys())
            ds_keys = []
            result = '{'

            for v in keys:
                ds_keys.append(str(v).replace('(', '0x').replace(', ', '').replace(')', ''))

            for i, v in enumerate(ds):
                if i < len(keys) - 1:
                    result = result + f'"{ds[ds_keys[i]].name}" : "{ds[ds_keys[i]].value}" , '
                else:
                    result = result + f'"{ds[ds_keys[i]].name}" : "{base64.b64encode(ds[ds_keys[i]].value)}"'
            result = result + "}"

        f.close()
        return result


class viewDCM:
    @staticmethod
    def viewDCM(filename, arr):
        """
        ### View Dicom Image by MatPlotLib
        """
        plt.title(filename)
        plt.imshow(arr, cmap='gray')
        plt.show()

    # Save Pixel_data to Image File

    @staticmethod
    def saveTopng(filename, arr, dpi=500, type='png'):
        """
        ### Dcm Image to Png    
        require : filename, arr    
        arr : dicom pixel_data    
        default dpi : 1000    
        default type : png    
        """

        plt.axis('off')
        plt.imshow(arr, cmap='gray')
        plt.savefig(f'{filename}.{type}', dpi=dpi, transparent=True)

    # Load pixel_data with Dicom Header

    @staticmethod
    def loadFile(filename, i):
        """
        ### DCM Convert pixel_data      
        require : fileName, i      
        i : 1 (pixel_data), 2 (Dicom Header)     
        information : Check Header data and convert pixel_data
        """

        ds = dcmread(filename + '.dcm', force=True)
        if ds is None:
            raise Exception('File Exits')
        pixel_array = ds.pixel_array

        img = ds.pixel_array.astype(np.float32)

        # Noramalization
        img = (img / (2 ** ds.BitsStored))

        # Convert Rescale
        if (('RescaleSlope' in ds) and ('RescaleIntercept' in ds)):
            pixel_array = (pixel_array * ds.RescaleSlope) + ds.RescaleIntercept

        if ('WindowCenter' in ds):
            if (type(ds.WindowCenter) == multival.MultiValue):
                window_center = float(ds.WindowCenter[0])
                window_width = float(ds.WindowWidth[0])
                lwin = window_center - (window_width / 2.0)
                rwin = window_center + (window_width / 2.0)
            else:
                window_center = float(ds.WindowCenter)
                window_width = float(ds.WindowWidth)
                lwin = window_center - (window_width / 2.0)
                rwin = window_center + (window_width / 2.0)
        else:
            lwin = np.min(pixel_array)
            rwin = np.max(pixel_array)

        pixel_array[np.where(pixel_array < lwin)] = lwin
        pixel_array[np.where(pixel_array > rwin)] = rwin
        pixel_array = pixel_array - lwin

        if (ds.PhotometricInterpretation == 'MONOCHROME1'):
            pixel_array[np.where(pixel_array < lwin)] = lwin
            pixel_array[np.where(pixel_array > rwin)] = rwin
            pixel_array = pixel_array - lwin
            pixel_array = 1.0 - pixel_array

        else:
            pixel_array[np.where(pixel_array < lwin)] = lwin
            pixel_array[np.where(pixel_array > rwin)] = rwin
            pixel_array = pixel_array - lwin

        if i == 1:
            return pixel_array
        elif i == 2:
            return ds
