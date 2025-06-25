#!/bin/sh

# API URL to check
API_URL="http://webxploit-api:8000/docs"

echo "⏳ Waiting for the WebXPloit API at $API_URL ..."

# Loop until the API is reachable
until curl --silent --fail $API_URL > /dev/null; do
  echo "⌛ API not ready yet. Retrying in 2 seconds... 🔄"
  sleep 2
done

echo "✅ API is ready, starting WebXPloit! 🚀 Enjoy! 😄"

# Start the backend (modify this line according to your current startup command)
exec python run.py
