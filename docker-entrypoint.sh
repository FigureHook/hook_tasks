#!/bin/bash

arg1=$1

if [ -z $arg1 ]; then
    exit 1
fi


check_scrapy () {
    local scrapyd_exist=false
    local max_retry=10
    local interval=5s
    local count=0

    echo "Building connection with scrapy at '$SCRAPYD_URL'..."
    while [[ ($scrapyd_exist == false) && ($count -lt $max_retry) ]]; do
        ((count++))

        if ! curl -fs --connect-timeout 2 --url $SCRAPYD_URL; then
            echo "Can't get connection with scrapyd. Retry after $interval. ($count/$max_retry)"
        else
            scrapyd_exist=true
        fi

        sleep $interval
    done

    if [ $scrapyd_exist == false ]; then
        echo "Failed to build connection with scrapyd."
        exit 1
    else
        echo "Successfully build connection with scrapyd."
    fi
}


check_db () {
    if ! hooktasks check db; then
        echo "Can't get connection with database."
        exit 1
    fi
}


if [ $arg1 == "start" ]; then
    check_db && check_scrapy && hooktasks run
fi

