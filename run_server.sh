#!/bin/sh
sleep 5
python cert_management/manage.py migrate
python cert_management/manage.py runserver 0.0.0.0:8000
