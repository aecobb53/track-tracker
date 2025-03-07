#!/bin/bash

cd track_tracker/

echo "${LOGICAL_ENV}"

if [ "${LOGICAL_ENV}" == "DEV" ]; then
    echo "Running in DEV mode"
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
elif [ "${LOGICAL_ENV}" == "PROD" ]; then
    echo "Running in PROD mode"
    uvicorn main:app --workers 4 --host 0.0.0.0 --port 8000
else
    echo "UNKNOWN LOGICAL_ENV - EXITING"
    exit 1
fi
