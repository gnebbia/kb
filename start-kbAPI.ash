#!/bin/sh

# -*- encoding: utf-8 -*-
# kb v0.1.4
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

#
# kbAPI startup module  (for Docker containers)
#
# :Copyright: © 2020, alshapton.
# :License: GPLv3 (see /LICENSE).
#

# Move to correct application server directory
cd /app
echo "Starting Server"

# Start the server
python ./server.py
# gunicorn -w 4 server:kbapi_app --bind localhost:5000

# Ensure correct data directory is current
cd /data
