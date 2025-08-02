#!/bin/bash

if [ -f .flask.pid ]; then
  FLASK_PID=$(cat .flask.pid)
  kill "$FLASK_PID" && echo "🛑 Stopped Flask (PID $FLASK_PID)"
  rm .flask.pid
fi

if [ -f .socket.pid ]; then
  SOCKET_PID=$(cat .socket.pid)
  kill "$SOCKET_PID" && echo "🛑 Stopped WebSocket (PID $SOCKET_PID)"
  rm .socket.pid
fi