'''
    Convert Dicom
    FTP -> binarydata -> ds -> toJSON
    Description : FTP에서 받은 binary data -> ds로 JSON 직렬화
    Author : Okrie, Oh-Kang94
    Ver : 0.1
    Site : https://github.com/Okrie/DicomToPng
    Lisence : MIT
'''

from PIL import Image
import numpy as np
import pydicom 
import io
import json
import logging
import base64
from pydicom.pixel_data_handlers.util import apply_voi_lut


class ConvertDCM:

    def dicomToJSON(self, data):
        ds = pydicom.dcmread(io.BytesIO(data))
        """
        ### Front Info for list
        @Params : fname -> SC 판단 후, Slice Score를 뱉어냄
        """
        result = {}
        info_list = ["Patient ID", "Patient's Name", "Patient's Birth Date", "Series Number", "Study Date", "Study Time", "Image Comments", "Series Description",
                    "Manufacturer", "Manufacturer's Model Name", "Rows", "Columns", "Window Width", "Window Center", "Operator's Name"]

        for elem in ds:
            if elem.name in info_list:
                if elem.name == "Window Width":
                    width_value = elem.value if elem.value is not None else 0
                    result[elem.name] = str(width_value)
                elif elem.name == "Window Center" and elem.value is None:
                    result[elem.name] = str(1)
                else:
                    result[elem.name] = str(elem.value)
        return json.dumps(result)
    
    def dicomToPNG(self, data):
        ds = pydicom.dcmread(io.BytesIO(data))
        print(ds.pixel_array.shape)
        # new_image = ds.pixel_array[0].astype(float)
        if len(ds.pixel_array.shape) == 4:  # 4차원 배열인 경우
            new_image = ds.pixel_array.astype(float)
            new_image = np.reshape(ds.pixel_array[0, :, :, 0], (-1, ds.pixel_array.shape[2]))
        elif len(ds.pixel_array.shape) == 3:  # 3차원 배열인 경우
            new_image = ds.pixel_array[0].astype(float)
        else:
            new_image = ds.pixel_array.astype(float)
        # normalization 작업
        scaled_image = (np.maximum(new_image, 0) / new_image.max()) * 255.0
        scaled_image = np.uint8(scaled_image)
        # 흑백 반전 작업
        # scaled_image = 255 - scaled_image
        img = Image.fromarray(scaled_image)
        img_io = io.BytesIO()
        img.save(img_io, 'PNG', quality=70)
        img_io.seek(0)  # BytesIO의 커서를 처음으로 이동
        return img_io
