#!/bin/bash

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn --reload educative_django_blog.wsgi:application \
    --bind 0.0.0.0:8000
