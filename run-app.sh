#!/usr/bin/env bash
gunicorn --bind 0.0.0.0:5000 --workers 2 --log-level error --error-logfile /var/log/error.log wsgi:app
