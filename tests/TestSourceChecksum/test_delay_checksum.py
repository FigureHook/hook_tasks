from hook_tasks.SourceChecksum.delay_checksum import GSCDelayChecksum

from .base_test import BaseTestAnnouncementChecksum


class TestGSCDelay(BaseTestAnnouncementChecksum):
    __checksum_cls__ = GSCDelayChecksum
