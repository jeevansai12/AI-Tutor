#!/usr/bin/env bash
set -o errexit
python -m gunicorn aitutor.wsgi:application
