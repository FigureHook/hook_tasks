from typing import List

import requests as rq

from figure_hook.constants import SourceSite

from .abcs import ShipmentChecksum
from .spider_config import EmptyConfig, SpiderConfig

__all__ = ["GSCShipmentChecksum"]


class GSCShipmentChecksum(ShipmentChecksum):
    __source_site__ = SourceSite.GSC_SHIPMENT
    __spider__ = "gsc_shipment"

    @property
    def spider_configs(self) -> List[SpiderConfig]:
        return [EmptyConfig()]

    def _extract_feature(self) -> bytes:
        url = "https://www.goodsmile.info/ja/releaseinfo"
        response = rq.get(url)
        response.raise_for_status()

        return response.content
