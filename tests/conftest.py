import os

import pytest
from figure_hook.Models.base import Model
from sqlalchemy.orm import sessionmaker

os.environ['POSTGRES_DATABASE'] = "figure_testing"


@pytest.fixture()
def db_session():
    from figure_hook.database import PostgreSQLDB

    pgsql = PostgreSQLDB()
    Model.metadata.drop_all(bind=pgsql.engine)

    Session = sessionmaker(pgsql.engine)
    with Session() as session:
        Model.set_session(session)
        Model.metadata.create_all(bind=pgsql.engine)
        yield session

    Model.set_session(None)  # type: ignore
    Model.metadata.drop_all(bind=pgsql.engine)
