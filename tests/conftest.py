import os

import pytest
from sqlalchemy.orm import Session

from figure_hook.Models.base import Model
from hook_tasks.app import app

os.environ['POSTGRES_DATABASE'] = "figure_testing"


@pytest.fixture()
def db_session():
    from figure_hook.database import PostgreSQLDB

    pgsql = PostgreSQLDB()
    Model.metadata.drop_all(bind=pgsql.engine)

    session = Session(pgsql.engine)
    Model.set_session(session)
    Model.metadata.create_all(bind=pgsql.engine)

    yield

    Model.set_session(None)  # type: ignore
    Model.metadata.drop_all(bind=pgsql.engine)
