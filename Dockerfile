FROM python:3.10-buster

WORKDIR /workspace

COPY requirements.txt .
COPY hook_tasks hook_tasks/
COPY docker-entrypoint.sh .

RUN pip install -r requirements.txt && \
    chmod +x docker-entrypoint.sh

ENTRYPOINT [ "./docker-entrypoint.sh" ]
CMD [ "worker" ]
