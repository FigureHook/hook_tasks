from pydantic import BaseModel

from ..entities.release_ticket_info import ReleaseTicketInfo
from ..value_objects.release_feed import ReleaseFeed


class ReleaseTicket(BaseModel):
    info: ReleaseTicketInfo
    feeds: ReleaseFeed
