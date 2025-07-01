from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime

class AuditRequest(BaseModel):
    url: HttpUrl

class AuditResponse(BaseModel):
    id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    url: HttpUrl
    audit_summary: str
