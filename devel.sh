#!/bin/bash
make build
export SECRET_KEY=$(uuid)
export DJANGO_DEBUG=True
./manage.py runserver
