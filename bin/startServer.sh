#!/bin/bash

SCRIPT_PATH=$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
APP_PATH="$(dirname $SCRIPT_PATH)"
LOG_PATH="$APP_PATH/logs"

CONFIG_FILE="$SCRIPT_PATH/gunicorn.conf.py"
PID_FILE="$SCRIPT_PATH/gunicorn.pid"
LOG_FILE="$LOG_PATH/gunicorn.$(date '+%Y-%m-%d').log"
ACCESS_LOG_FILE="$LOG_PATH/access.$(date '+%Y-%m-%d').log"

SERVER_LOG_TAG="[SERVER LOG]"

mkdir -p $LOG_PATH

help_msg() {
  echo "usage: $0 [start|stop|restart]"
  echo "ex: $0 restart"
  exit 1
}

if [ $# -ne 1 ]; then
  help_msg
fi

if [ -f $PID_FILE ]; then
  PID=$(cat $PID_FILE)
fi

echo "--------------------------------------------------------------------------------"
echo "os environment variable (FASTAPI_TEMPLATE_ENV) : $FASTAPI_TEMPLATE_ENV"
echo "--------------------------------------------------------------------------------"

start_server() {
  if [ -f $PID_FILE ]; then
    echo "Already Started pid[$PID]"
    echo "$(date) : $SERVER_LOG_TAG already exist process pid[$PID]" >>$LOG_FILE
  else
    cd $APP_PATH/app
    # gunicorn --worker-class uvicorn.workers.UvicornWorker --workers 20 --bind 0.0.0.0:8080 --pid $PID_FILE --daemon --access-logfile $ACCESS_LOG_FILE --log-file $LOG_FILE main:app
    # gunicorn -c $CONFIG_FILE --pid $PID_FILE --daemon --access-logfile $ACCESS_LOG_FILE --log-file $LOG_FILE main:app
    pipenv run gunicorn -c $CONFIG_FILE --pid $PID_FILE --daemon --access-logfile $ACCESS_LOG_FILE --log-file $LOG_FILE main:app
    echo "Started"
    sleep 1
    echo "Started process pid[$(cat $PID_FILE)]"
    echo "$(date) : $SERVER_LOG_TAG started process pid[$(cat $PID_FILE)]" >>$LOG_FILE
  fi
}

stop_server() {
  if [ -f $PID_FILE ]; then
    pkill -f gunicorn
    rm -f $PID_FILE
    echo "Stopped"
    sleep 1
    echo "Stopped process pid[$PID]"
    echo "$(date) : $SERVER_LOG_TAG stopped process pid[$PID]" >>$LOG_FILE
  else
    echo "Not found PID File[$PID_FILE]"
    echo "$(date) : $SERVER_LOG_TAG not found pid file[$PID_FILE]" >>$LOG_FILE
  fi
}

case "$1" in
start)
  start_server
  ;;
stop)
  stop_server
  ;;
restart)
  stop_server
  sleep 1
  start_server
  ;;
*)
  help_msg
  ;;
esac

exit 0
