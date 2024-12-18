#!/usr/bin/env bash

alembic upgrade head

gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000 --log-level debug --access-logfile - --error-logfile -
