#!/usr/bin/env bash
set -e

if [ "$DATABASE_NAME" = "iot_farm" ]
then
    echo "Waiting for postgres..."

    while ! netcat -z $DATABASE_HOST $DATABASE_INTERNAL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# python manage.py flush --no-input
python manage.py migrate --database=$DATABASE_ALIAS
# python manage.py migrate --database=$DATABASE_SECONDARY_ALIAS

exec "$@"
