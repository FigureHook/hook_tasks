#!/bin/bash

arg1=$1

if [ "$arg1" == "" ]; then
    exit 1
fi


check_scrapy () {
    echo "Building connection with scrapy at '$SCRAPYD_URL'"
    if ! curl -s $SCRAPYD_URL; then
        echo "Can't get connection with scrapyd."
        exit 1
    fi
}


check_db () {
    if ! hooktasks check db; then
        echo "Can't get connection with database."
        exit 1
    fi
}


if [ $arg1 == "start" ]; then
    check_scrapy
    check_db
    hooktasks run
fi

