import matplotlib.pyplot as plt
import numpy as np
from pydicom import dcmread, multival
# Load pixel_data with Dicom Header


class bin:
    @staticmethod
    def loadData(self, ds):
        """
        ### DCM Convert pixel_data      
        require : fileName, i      
        i : 1 (pixel_data), 2 (Dicom Header)     
        information : Check Header data and convert pixel_data
        """

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

        return pixel_array
