from pydantic import BaseModel, HttpUrl
from datetime import datetime

class AuditRequestSchema(BaseModel):
    url: HttpUrl

class AuditResponseSchema(BaseModel):
    id: str
    timestamp: datetime
    url: HttpUrl
    audit_summary: str
