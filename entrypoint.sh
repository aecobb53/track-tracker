#!/bin/bash

cd track_tracker/
# uvicorn main:app --workers 1 --host 0.0.0.0 --port 8000
uvicorn main:app --reload --workers 1 --host 0.0.0.0 --port 8000
