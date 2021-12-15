import pathlib
import sys
import time

import click
from figure_hook.database import PostgreSQLDB

module_dir = pathlib.Path(__file__).parent.resolve()


@click.group()
def main():
    pass


@main.group()
def check():
    """connection checking tool."""
    pass


@main.command('initdb')
def init_db():
    "initialize database."
    from figure_hook.Models.base import Model
    pgsql = PostgreSQLDB()
    Model.metadata.create_all(pgsql.engine)


@main.command('dropdb')
def drop_db():
    "drop database."
    from figure_hook.Models.base import Model
    pgsql = PostgreSQLDB()
    Model.metadata.drop_all(pgsql.engine)

@ check.command('db')
def check_db():
    db=PostgreSQLDB()
    db_exist=False
    try_count=0
    max_retry_times=10
    interval=1

    click.echo("Building database connection...")
    while not db_exist and try_count < max_retry_times:
        try:
            conn=db.engine.connect()
            conn.close()
            db_exist=True
            click.echo("Successfully build connection with database.")
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            click.echo(
                f"Failed to build connection with database. Retry after {interval} seconds. ({try_count + 1}/{max_retry_times})"
            )
            time.sleep(interval)
        finally:
            try_count += 1

    exit_code=0 if db_exist else 1
    sys.exit(exit_code)


@ main.command()
def run():
    """run development server."""
    from .app import app
    app.worker_main(argv=[
        "worker",
        "-B",
        "--loglevel=INFO"
    ])


if __name__ == '__main__':
    main()
