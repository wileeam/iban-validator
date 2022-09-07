#!/bin/sh

export FLASK_APP=./app.py
export FLASK_DEBUG=True

source $(pipenv --venv)/bin/activate
flask run -h 0.0.0.0 -p 5001
