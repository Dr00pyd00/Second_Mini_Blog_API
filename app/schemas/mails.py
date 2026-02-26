from typing import List

from pydantic import BaseModel
from fastapi_mail import NameEmail

class EmailSchema(BaseModel):
    email: List[NameEmail]