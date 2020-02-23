#!/usr/bin/env bash
set -e

if [ "$POSTGRES_DB" = "iot_farm" ]
then
    echo "Waiting for postgres..."

    while ! netcat -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# python manage.py flush --no-input
python manage.py migrate

exec "$@"