#!/usr/bin/env bash
# Install GDAL system libraries
apt-get update && apt-get install -y gdal-bin libgdal-dev

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run Django migrations
python manage.py migrate
