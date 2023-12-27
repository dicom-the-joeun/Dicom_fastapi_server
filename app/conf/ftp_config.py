from ftplib import FTP
import os

from dotenv import load_dotenv


load_dotenv("./app/.env")
FTP_SERVER = os.environ.get("FTP_SERVER")
FTP_USERNAME = os.environ.get("FTP_USERNAME")
FTP_PASSWORD = os.environ.get('FTP_PASSWORD')

class FTPConfig:
    def __init__(self):
        self.host = FTP_SERVER
        self.username = FTP_USERNAME
        self.password = FTP_PASSWORD
        self.ftp = FTP()

    def connect(self):
        self.ftp.connect(self.host)
        self.ftp.login(self.username, self.password)
        print(f"Connected to {self.host}")
    
    def disconnect(self):
        self.ftp.quit()
        print("Disconnected from FTP server")