#!/bin/bash

echo "Importing WP3-mapped JSON"
mongoimport -d search \
            -c colaus_wp3 \
            --host=0.0.0.0:27012
            --drop \
            --jsonArray \
            --file="data/colaus_cineca.json"
