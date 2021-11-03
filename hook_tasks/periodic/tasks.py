from figure_hook.database import pgsql_session
from figure_hook.Tasks.periodic import (DiscordNewReleasePush,
                                        PlurkNewReleasePush)

from ..app import app


@app.task
def push_discord_new_releases():
    with pgsql_session() as session:
        news_push = DiscordNewReleasePush(session=session)
        result = news_push.execute()

    return result


@app.task
def push_plurk_new_releases():
    with pgsql_session() as session:
        news_push = PlurkNewReleasePush(session=session)
        result = news_push.execute()

    return result
