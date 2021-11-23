import sys
import time

import click
from figure_hook.database import PostgreSQLDB


@click.group()
def check():
    pass


@check.command()
def checkdb():
    db = PostgreSQLDB()
    db_exist = False
    try_count = 0
    max_retry_times = 10
    interval = 1

    click.echo("Building database connection...")
    while not db_exist and try_count < max_retry_times:
        try:
            conn = db.engine.connect()
            conn.close()
            db_exist = True
            click.echo("Successfully build connection with database.")
        except:
            click.echo(
                f"Failed to build connection with database. Retry after {interval} seconds. ({try_count + 1}/{max_retry_times})"
            )
            time.sleep(interval)
        finally:
            try_count += 1

    exit_code = 0 if db_exist else 1
    sys.exit(exit_code)


if __name__ == '__main__':
    check()
