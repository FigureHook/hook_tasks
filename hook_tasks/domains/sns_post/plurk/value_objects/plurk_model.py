from pydantic import BaseModel

from .plurk_config import PlurkConfig


class PlurkModel(BaseModel):
    content: str
    config: PlurkConfig

    def to_payload(self):
        return {"content": self.content, **self.config.dict()}
