"""
    Dicom Services
    Author : Okrie
    Date : 2023-12-27
    Ver : 0.1
    License : MIT
"""

from ftplib import FTP
from conf.ftp_config import FTPConfig


# FTB Config Load
CONFTP = FTPConfig()


class DicomService:
    def __init__(self):
        pass