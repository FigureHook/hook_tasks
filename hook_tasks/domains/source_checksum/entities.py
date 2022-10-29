from typing import Optional
from pydantic import BaseModel


class SourceChecksum(BaseModel):
    id: Optional[int] = None
    source_name: str
    value: str = "init"
