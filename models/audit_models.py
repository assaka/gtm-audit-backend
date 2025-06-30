from pydantic import BaseModel, HttpUrl

class AuditRequest(BaseModel):
    url: HttpUrl

class AuditResponse(BaseModel):
    id: str
    timestamp: str
    url: HttpUrl
    audit_summary: str
