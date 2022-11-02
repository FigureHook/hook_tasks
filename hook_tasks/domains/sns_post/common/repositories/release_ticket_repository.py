from datetime import datetime
from typing import Generic, List, Protocol, TypeVar

from ..entities.release_ticket_info import ReleaseTicketInfo
from ..value_objects.release_feed import ReleaseFeed

TicketID = TypeVar("TicketID", contravariant=True)


class ReleaseTicketRepositoryInterface(Protocol, Generic[TicketID]):
    def get_release_feeds_by_ticket_id(self, ticket_id: TicketID) -> List[ReleaseFeed]:
        raise NotImplementedError

    def create_release_ticket_by_time_with_purpose(
        self, time: datetime, purpose: str
    ) -> ReleaseTicketInfo:
        raise NotImplementedError

    def get_last_ticket_created_time_with_purpose(self, purpose: str) -> datetime:
        raise NotImplementedError
