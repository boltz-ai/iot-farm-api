#!/usr/bin/env bash

python manage.py dumpdata --natural-foreign --indent 2 users.User > authentication/fixtures/seeders.json