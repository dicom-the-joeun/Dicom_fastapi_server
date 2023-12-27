

from typing import Optional
from pydantic import BaseModel


class SelectPatient(BaseModel):
    PID : str
    PNAME : str
    PATKEY : str
    PATIENTKEY : int
    PLASTNAME : str
    PFIRSTNAME : str
    PSEX : str
    PBIRTHDATE : str
    PBIRTHTIME : str
    COMMENTS : str
    INSERTDATE : str
    INSERTTIME : str
    HOSPITALID : int
    PKNAME : str
    PENAME : str
    INSNAME : str
    DELFLAG : str
    INSERTED : str
    UPDATED : str
    RESERVED1 : Optional[int] = None
    RESERVED2: Optional[int] = None
    RESERVED3 : Optional[int] = None
    RESERVED4 : str
    RESERVED5 : str
    RESERVED6 : str
    RESERVED7 : str
    RESERVED8 : str
    RESERVED9 : str
    RESERVED10 : str

class TokenData(BaseModel):
    ID: Optional[str] = None

class CreateUser(BaseModel):
    ID: str
    PASSWORD: str