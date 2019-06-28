#!/bin/bash

if [ ! -f uwsgi.pid ]; then
  echo "Server nebezi..."
  exit 1
fi	

pid=$(cat uwsgi.pid)

kill -SIGKILL $pid

rm uwsgi.pid

echo "Server zastaven..."
