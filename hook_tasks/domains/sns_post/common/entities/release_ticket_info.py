from pydantic import BaseModel
from datetime import datetime


class ReleaseTicketInfo(BaseModel):
    id: str
    purpose: str
    created_at: datetime
