from datetime import datetime
from typing import List

from figure_hook_client.api.release_feed import (
    create_release_ticket_api_v1_release_tickets_post,
    get_multi_release_tickets_api_v1_release_tickets_get,
    get_release_ticket_api_v1_release_tickets_ticket_id_get,
)
from figure_hook_client.models.page_release_ticket_in_db import PageReleaseTicketInDB
from figure_hook_client.models.release_ticket_create import ReleaseTicketCreate
from figure_hook_client.models.release_ticket_in_db import ReleaseTicketInDB

from hook_tasks.api_clients import AuthenticatedClient
from hook_tasks.domains.sns_post.common.entities.release_ticket_info import (
    ReleaseTicketInfo,
)
from hook_tasks.domains.sns_post.common.repositories.release_ticket_repository import (
    ReleaseTicketRepositoryInterface,
)
from hook_tasks.domains.sns_post.common.value_objects.release_feed import ReleaseFeed


class ReleaseTicketRepository(ReleaseTicketRepositoryInterface[str]):
    api_client: AuthenticatedClient

    def __init__(self, api_client: AuthenticatedClient) -> None:
        self.api_client = api_client

    def get_release_feeds_by_ticket_id(self, ticket_id: str) -> List[ReleaseFeed]:
        release_feeds = get_release_ticket_api_v1_release_tickets_ticket_id_get.sync(
            ticket_id=ticket_id, client=self.api_client
        )
        if isinstance(release_feeds, list):
            feeds: List[ReleaseFeed] = []
            for feed in release_feeds:
                feed_dict = feed.to_dict()
                feeds.append(
                    ReleaseFeed(
                        name=feed_dict["name"],
                        url=feed_dict["souce_url"],
                        is_adult=feed_dict["is_nsfw"],
                        release_date=feed_dict["release_date"],
                        rerelease=feed_dict["is_rerelease"],
                        series=feed_dict["series"],
                        maker=feed_dict["manufacturer"],
                        size=feed["size"],
                        scale=feed["scale"],
                        price=feed["price"],
                        image_url=feed_dict["image_url"],
                    )
                )
            return feeds

        raise NotImplementedError

    def get_release_ticket_infos(self, limit: int = 50) -> List[ReleaseTicketInfo]:
        ticket_pagination = get_multi_release_tickets_api_v1_release_tickets_get.sync(
            client=self.api_client, size=limit
        )
        if isinstance(ticket_pagination, PageReleaseTicketInDB):
            return [
                ReleaseTicketInfo(
                    id=db_ticket.id,
                    purpose=db_ticket.purpose,
                    created_at=db_ticket.created_at,
                )
                for db_ticket in ticket_pagination.results
            ]

        raise NotImplementedError

    def create_release_ticket_info_by_time_with_purpose(
        self, time: datetime, purpose: str
    ) -> ReleaseTicketInfo:
        ticket_create = ReleaseTicketCreate(from_=time, purpose=purpose)
        release_ticket = create_release_ticket_api_v1_release_tickets_post.sync(
            client=self.api_client, json_body=ticket_create
        )

        if isinstance(release_ticket, ReleaseTicketInDB):
            return ReleaseTicketInfo(
                id=release_ticket.id,
                purpose=release_ticket.purpose,
                created_at=release_ticket.created_at,
            )

        raise NotImplementedError

    def get_last_ticket_created_time_with_purpose(self, purpose: str) -> datetime:
        ticket_pagination = get_multi_release_tickets_api_v1_release_tickets_get.sync(
            client=self.api_client, size=1
        )
        if isinstance(ticket_pagination, PageReleaseTicketInDB):
            if len(ticket_pagination.results):
                return ticket_pagination.results[0].created_at
            return datetime.now()

        raise NotImplementedError
