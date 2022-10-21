from datetime import date
from pydantic import BaseModel
from typing import Optional


class ReleaseFeed(BaseModel):
    name: str
    url: str
    is_adult: bool
    rerelease: bool
    series: str
    maker: str
    size: Optional[int]
    scale: Optional[int]
    price: Optional[int]
    release_date: Optional[date]
    image_url: str
    thumbnail: Optional[str]
    og_image: Optional[str]

    @property
    def media_image(self):
        if self.thumbnail == self.og_image:
            return self.image_url
        return self.og_image
