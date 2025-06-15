from pydantic import BaseModel
from typing import Optional

class AuditInfo(BaseModel):
    status: str
    score: int


class ParsedJSON(BaseModel):
    name:str
    email: str
    role: str
    audit: AuditInfo