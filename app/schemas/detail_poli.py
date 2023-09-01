from pydantic import BaseModel, validator
from app import schemas
from typing import List

class DetailPoli(BaseModel):
    poli: List[schemas.Poli]
    tindakan: List[schemas.Tindakan]

    @validator('poli', pre=True, allow_reuse=True)
    def pony_set_to_list(cls, values):
        return [v.to_dict() for v in values]
    
    @validator('tindakan', pre=True, allow_reuse=True)
    def pony_set_to_list(cls, values):
        return [v.to_dict() for v in values]
    
    class Config:
        orm_mode = True