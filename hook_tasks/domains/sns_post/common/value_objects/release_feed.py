from pydantic import BaseModel
from typing import Optional
from datetime import date


class ReleaseFeed(BaseModel):
    name: str
    url: str
    is_adult: bool
    rerelease: bool
    series: str
    maker: str
    size: Optional[int] = None
    scale: Optional[int] = None
    price: Optional[int] = None
    release_date: Optional[date] = None
    image_url: str
    thumbnail: Optional[str] = None
    og_image: Optional[str] = None

    @property
    def media_image(self):
        if self.thumbnail == self.og_image:
            return self.image_url
        return self.og_image
