FROM python:3.9-buster

ENV POETRY_VERSION=1.1.8

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /workspace

COPY poetry.lock .
COPY pyproject.toml .
COPY hook_tasks hook_tasks/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

CMD /bin/bash celery_start.sh
