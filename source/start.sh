#!/bin/bash -e

python -c 'import containeroso; containeroso.buildImage()'
gunicorn --workers 3 -t 180 --bind 0.0.0.0:5000 index:app
