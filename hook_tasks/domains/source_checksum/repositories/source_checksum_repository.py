from datetime import datetime
from typing import Optional

from figure_hook_client.api.source_checksum import (
    create_source_checksum_api_v1_source_checksums_post,
    get_source_checksums_api_v1_source_checksums_get,
    patch_source_checksum_api_v1_source_checksums_source_checksum_id_patch,
)
from figure_hook_client.client import AuthenticatedClient
from figure_hook_client.models.source_checksum_create import SourceChecksumCreate
from figure_hook_client.models.source_checksum_in_db import SourceChecksumInDB
from figure_hook_client.models.source_checksum_update import SourceChecksumUpdate

from ..entities.source_checksum import SourceChecksum


class SourceChecksumRepository:
    api_client: AuthenticatedClient

    def __init__(self, api_client: AuthenticatedClient) -> None:
        self.api_client = api_client

    def create_checksum(
        self, source_name: str, checksum_value: str
    ) -> "SourceChecksum":
        checksum_create = SourceChecksumCreate(
            source=source_name,
            checksum=checksum_value,
            checked_at=datetime.now(),
        )
        created_checksum = create_source_checksum_api_v1_source_checksums_post.sync(
            client=self.api_client, json_body=checksum_create
        )

        if isinstance(created_checksum, SourceChecksumInDB):
            return SourceChecksum(
                id=created_checksum.id,
                value=created_checksum.checksum,
                source_name=created_checksum.source,
            )

        raise NotImplementedError

    def get_checksum_by_source(self, source_name: str) -> Optional["SourceChecksum"]:
        fetched_checksums = get_source_checksums_api_v1_source_checksums_get.sync(
            source=source_name, client=self.api_client, limit=1
        )

        if isinstance(fetched_checksums, list):
            if len(fetched_checksums) > 0:
                return SourceChecksum(
                    id=fetched_checksums[0].id,
                    value=fetched_checksums[0].checksum,
                    source_name=source_name,
                )
            return None

        raise NotImplementedError

    def save(self, source_checksum: "SourceChecksum") -> "SourceChecksum":
        assert source_checksum.id
        checksum_update = SourceChecksumUpdate(
            source=source_checksum.source_name,
            checksum=source_checksum.value,
            checked_at=datetime.now(),
        )
        updated_checksum = (
            patch_source_checksum_api_v1_source_checksums_source_checksum_id_patch.sync(
                source_checksum_id=source_checksum.id,
                client=self.api_client,
                json_body=checksum_update,
            )
        )
        if isinstance(updated_checksum, SourceChecksumInDB):
            source_checksum.id = updated_checksum.id
            source_checksum.value = updated_checksum.checksum
            source_checksum.source_name = updated_checksum.source
            return source_checksum

        raise NotImplementedError
