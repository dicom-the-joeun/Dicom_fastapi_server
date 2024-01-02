

from typing import Optional
from pydantic import BaseModel


class SelectStudyViewTab(BaseModel):
    PID : str
    PNAME : str
    MODALITY : str
    STUDYDESC : Optional[str] = ""
    STUDYDATE : int
    REPORTSTATUS : int
    SERIESCNT : int
    IMAGECNT : int
    EXAMSTATUS : int


class SelectPatient(BaseModel):
    PID: Optional[str] = None
    PNAME: Optional[str] = None
    PATKEY: Optional[str] = None
    PATIENTKEY: Optional[int] = None
    PLASTNAME: Optional[str] = None
    PFIRSTNAME: Optional[str] = None
    PSEX: Optional[str] = None
    PBIRTHDATE: Optional[str] = None
    PBIRTHTIME: Optional[str] = None
    COMMENTS: Optional[str] = None
    INSERTDATE: Optional[str] = None
    INSERTTIME: Optional[str] = None
    HOSPITALID: Optional[int] = None
    PKNAME: Optional[str] = None
    PENAME: Optional[str] = None
    INSNAME: Optional[str] = None
    DELFLAG: Optional[str] = None
    INSERTED: Optional[str] = None
    UPDATED: Optional[str] = None
    RESERVED1: Optional[int] = None
    RESERVED2: Optional[int] = None
    RESERVED3: Optional[int] = None
    RESERVED4: Optional[str] = None
    RESERVED5: Optional[str] = None
    RESERVED6: Optional[str] = None
    RESERVED7: Optional[str] = None
    RESERVED8: Optional[str] = None
    RESERVED9: Optional[str] = None
    RESERVED10: Optional[str] = None


class TokenData(BaseModel):
    ID: Optional[str] = None


class CreateUser(BaseModel):
    ID: str
    PASSWORD: str
