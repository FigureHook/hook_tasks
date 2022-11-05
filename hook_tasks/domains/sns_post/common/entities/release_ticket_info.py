from datetime import datetime

from pydantic import BaseModel


class ReleaseTicketInfo(BaseModel):
    id: str
    purpose: str
    created_at: datetime
