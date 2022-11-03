from discord import Embed
from typing import TypeVar

Embed_T = TypeVar("Embed_T", bound=Embed)


class MakeEmbedTrackableUseCase:
    @staticmethod
    def could_be_tracked_by_ticket_id(embed: Embed_T, ticket_id: str) -> Embed_T:
        tracking_text = f"ticket: {ticket_id}"
        embed.set_footer(text=tracking_text)
        return embed
