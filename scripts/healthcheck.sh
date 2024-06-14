#!/bin/bash

URL="https://data.economie.gouv.fr/pages/healthcheck/"
OUTPUT_FILE="$HOME/data/healthcheck.log"

TIMEOUT=10

TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

HTTP_STATUS=$(curl -o /dev/null -s --max-time $TIMEOUT -w "%{http_code}\n" "$URL")
CURL_EXIT_CODE=$?

if [ "$CURL_EXIT_CODE" -ne 0 ]; then
    STATUS="DOWN"
    HTTP_STATUS="000"
else
    if [ "$HTTP_STATUS" -eq 200 ]; then
        STATUS="UP"
    else
        STATUS="DOWN"
    fi
fi

echo "$TIMESTAMP,$URL,$STATUS,$HTTP_STATUS" >> "$OUTPUT_FILE"
