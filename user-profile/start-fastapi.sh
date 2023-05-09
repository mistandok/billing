#!/bin/sh

wait_database()
{
  HOST=$1
  PORT=$2
  TYPE=$3

  echo "Waiting for $TYPE..."

  while ! nc -z $HOST $PORT; do
    sleep 0.1
  done

  echo "$TYPE started"
}

if [ ${USER_PROFILES_DB_TYPE} = "mongodb" ]
  then
    wait_database $MONGOS1_HOST $MONGOS1_PORT USER_PROFILES_DB_TYPE
fi

if [ ${USER_PROFILES_DB_TYPE} = "mongodb" ]
  then
    wait_database $MONGOS2_HOST $MONGOS2_PORT USER_PROFILES_DB_TYPE
fi

gunicorn main:app --workers 4\
 --worker-class uvicorn.workers.UvicornWorker\
  --bind 0.0.0.0:8102\
   --log-level "$LOGGING_LEVEL"

exec "$@"