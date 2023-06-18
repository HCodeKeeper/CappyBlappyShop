#!/bin/sh

echo "Waiting for mysql..."

while ! nc -z $MYSQL_HOST $MYSQL_PORT; do
    sleep 0.1
done

echo "MYSQL started"

# Run migrations
python manage.py migrate

exec "$@"