#!/usr/bin/env bash

#!/bin/bash

NAME="apitest" # Name of the application
USER=nobody # the user to run as
GROUP=nobody # the group to run as
NUM_WORKERS=4 # how many worker processes should Gunicorn spawn
TIMEOUT=600
DJANGO_WSGI_MODULE=djapi_manager.wsgi # WSGI module name

echo "Starting $NAME as `whoami`"

exec pipenv run gunicorn ${DJANGO_WSGI_MODULE}:application \
--name $NAME \
--workers $NUM_WORKERS \
--timeout $TIMEOUT \
--user=$USER --group=$GROUP \
--bind=0.0.0.0:8000 \
--log-level=debug \
--log-file=-