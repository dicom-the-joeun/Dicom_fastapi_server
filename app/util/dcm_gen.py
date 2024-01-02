'''
    Convert Dicom
    FTP -> binarydata -> ds -> toJSON
    Description : FTP에서 받은 binary data -> ds로 JSON 직렬화
    Author : Okrie, Oh-Kang94
    Ver : 0.1
    Site : https://github.com/Okrie/DicomToPng
    Lisence : MIT
'''

import json
import logging
import matplotlib.pyplot as plt
import numpy as np
import base64
import io
from pydicom import dcmread, multival
import pydicom
from PIL import Image


class ConvertDCM:
    '''
        Convert Dicom
        FTP -> binarydata -> ds -> toJSON
    '''

    def dicomToJSON(self, data):
        ds = pydicom.dcmread(io.BytesIO(data))
        # Number of Frames가 있으면 [0]만 가져온다.
        try:
            pixel_array = ds.pixel_array[0]
            image = Image.fromarray(pixel_array)
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            png_bytes = buffered.getvalue()
            base64_encoded = base64.b64encode(png_bytes).decode('utf-8')
        except Exception as e:
            logging.error(f"이미지 문제 발생 {e}")
            base64_encoded = "None"
        finally:
            result = {}
            for elem in ds:
                if elem.name == "Pixel Data":
                    result[elem.name] = base64_encoded
                else:
                    result[elem.name] = str(elem.value)
            return json.dumps(result)

            # return self.get_front(ds, base64_encoded)

    def get_front(self, ds, base64_encoded):
        """
        ### Front Info for list
        @Params : fname -> SC 판단 후, Slice Score를 뱉어냄
        """
        result = {}
        info_list = ["Patient ID", "Patient's Name", "Patient's Birth Date", "Series Number", "Study Date", "Study Time", "Image Comments",
                     "Manufacturer", "Manufacturer's Model Name", "Rows", "Columns", "Window Width", "Window Center", "Operator's Name"]

        for elem in ds:
            if elem.name == "Pixel Data":
                result[elem.name] = base64_encoded
            elif elem.name in info_list:
                result[elem.name] = str(elem.value)
        return json.dumps(result)
