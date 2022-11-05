#!/bin/bash

check_http_api() {
    local service_url=$1
    local service_name=$2

    local is_exist=false
    local max_retry=10
    local retry_count=0
    local factor_base=2

    echo "Test connection with $service_name at '$service_url'"
    while [[ ($is_exist == false) && ($retry -lt $max_retry) ]]; do
        ((retry_count++))
        local retry_after=$(($factor_base ** $retry_count))

        if ! curl -fs --connect-timeout $factor_base --url $service_url &>/dev/null; then
            echo "Cannot establish connection with $service_name. Retry after ${retry_after}s. ($retry_count/$max_retry)"
        else
            is_exist=true
        fi

        sleep $retry_after
    done

    if $is_exist; then
        echo "Successfully establish connection with $service_name at '$service_url'."
    else
        echo "Failed to establish connection with $service_name at '$service_url'."
        exit 1
    fi
}

main() {
    local arg1=$1

    echo
    if [ -z $arg1 ]; then
        echo "No argument provided."
        exit 1
    fi

    if [ $arg1 == "worker" ]; then
        check_http_api $HOOK_API_URL hook_api &&
        check_http_api $SCRAPY_URL scrapyd &&
        celery -A hook_tasks worker -l INFO
    fi

    if [ $arg1 == "beat" ]; then
        celery -A hook_tasks beat -l INFO
    fi
}

main "$@"
