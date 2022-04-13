from hook_tasks.SourceChecksum.abcs import generate_checksum
from hook_tasks.SourceChecksum.product_announcement_checksum import (
    AlterProductAnnouncementChecksum, GSCProductAnnouncementChecksum,
    NativeProductAnnouncementChecksum)

from .base_test import BaseTestAnnouncementChecksum


def test_checksum_generation():
    checksum = generate_checksum('kappa'.encode('utf-8'))
    assert checksum


class TestGSCAnnouncement(BaseTestAnnouncementChecksum):
    __checksum_cls__ = GSCProductAnnouncementChecksum


class TestAlterAnnouncement(BaseTestAnnouncementChecksum):
    __checksum_cls__ = AlterProductAnnouncementChecksum


class TestNativeAnnouncement(BaseTestAnnouncementChecksum):
    __checksum_cls__ = NativeProductAnnouncementChecksum
