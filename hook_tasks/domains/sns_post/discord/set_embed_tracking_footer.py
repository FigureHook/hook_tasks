from discord import Embed


def set_release_embed_tracking_footer(embed: Embed, ticket_id: str) -> Embed:
    tracking_text = f"ticket: {ticket_id}"
    embed.set_footer(text=tracking_text)
    return embed
