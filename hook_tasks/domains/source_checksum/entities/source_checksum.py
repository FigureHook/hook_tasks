from pydantic import BaseModel


class SourceChecksum(BaseModel):
    id: int
    source_name: str
    value: str = "init"
