from datetime import datetime

from figure_hook_client.api.source_checksum import (
    create_source_checksum_api_v1_source_checksums_post,
    get_source_checksums_api_v1_source_checksums_get,
    patch_source_checksum_api_v1_source_checksums_source_checksum_id_patch)
from figure_hook_client.models.source_checksum_create import \
    SourceChecksumCreate
from figure_hook_client.models.source_checksum_in_db import SourceChecksumInDB
from figure_hook_client.models.source_checksum_update import \
    SourceChecksumUpdate
from hook_tasks.api_clients import hook_api_client

from ..entities import DTOSourceChecksum


class ChecksumRepository:
    @staticmethod
    def create_checksum(source_checksum: "DTOSourceChecksum") -> "DTOSourceChecksum":
        checksum_create = SourceChecksumCreate(
            source=source_checksum.source_name,
            checksum=source_checksum.value,
            checked_at=datetime.now(),
        )
        created_checksum = create_source_checksum_api_v1_source_checksums_post.sync(
            client=hook_api_client, json_body=checksum_create
        )

        if isinstance(created_checksum, SourceChecksumInDB):
            source_checksum.id = created_checksum.id
            source_checksum.value = created_checksum.checksum
            return source_checksum

        raise NotImplementedError

    @staticmethod
    def get_checksum_by_source(source_name: str) -> "DTOSourceChecksum":
        fetched_checksums = get_source_checksums_api_v1_source_checksums_get.sync(
            source=source_name, client=hook_api_client, limit=1
        )

        if isinstance(fetched_checksums, list):
            if len(fetched_checksums) > 0:
                return DTOSourceChecksum(
                    id=fetched_checksums[0].id,
                    value=fetched_checksums[0].checksum,
                    source_name=source_name,
                )
            return DTOSourceChecksum(source_name=source_name)

        raise NotImplementedError

    @staticmethod
    def update_checksum(source_checksum: "DTOSourceChecksum") -> "DTOSourceChecksum":
        assert source_checksum.id
        checksum_update = SourceChecksumUpdate(
            source=source_checksum.source_name,
            checksum=source_checksum.value,
            checked_at=datetime.now(),
        )
        updated_checksum = (
            patch_source_checksum_api_v1_source_checksums_source_checksum_id_patch.sync(
                source_checksum_id=source_checksum.id,
                client=hook_api_client,
                json_body=checksum_update,
            )
        )
        if isinstance(updated_checksum, SourceChecksumInDB):
            source_checksum.id = updated_checksum.id
            source_checksum.value = updated_checksum.checksum
            source_checksum.source_name = updated_checksum.source
            return source_checksum

        raise NotImplementedError
