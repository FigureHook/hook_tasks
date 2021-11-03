#!/bin/bash
celery -A hook_tasks.app worker -B --loglevel=INFO