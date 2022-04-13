from hook_tasks.SourceChecksum.shipment_checksum import GSCShipmentChecksum

from .base_test import BaseTestAnnouncementChecksum


class TestGSCShipment(BaseTestAnnouncementChecksum):
    __checksum_cls__ = GSCShipmentChecksum
