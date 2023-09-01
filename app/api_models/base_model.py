from pydantic import BaseModel
from typing import Union

class BaseResponseModel(BaseModel):
  status_code: int = 200
  success: bool = True
  message: str = 'Success'
  data: Union[dict, list] = None

  class Config:
    json_schema_extra = {
      'example': {
        'status_code': 200,
        'success': True,
        'message': 'Success',
        'data': None
      }
    }