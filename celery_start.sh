#!/bin/bash

if ! curl $SCRAPYD_URL; then
    echo "Can't get connection with scrapyd."
    exit 1
fi

if ! python _cmd.py checkdb; then
    echo "Can't get connection with database."
    exit 1
fi

celery -A hook_tasks.app worker -B --loglevel=INFO
