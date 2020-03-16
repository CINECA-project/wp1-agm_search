#!/bin/bash

echo "Importing WP3-mapped JSON"
mongoimport --port 27011 \
            -d search \
            -c wp3 \
            --drop \
            --jsonArray \
            --file="data/patched_child.json"

echo "Importing unmapped questionnaire pseudodata"
mongoimport --port 27011 \
            -d search \
            -c unmapped \
            --drop \
            --type=csv \
            --headerline \
            --file="data/CHILDPseudoData_03-10-20/Questionnaire pseudodata-Table 1.csv"

echo "Importing cohort attributes"
mongoimport --port 27011 \
            -d search \
            -c attributes \
            --drop \
            --type=csv \
            --headerline \
            --file="data/CHILDPseudoData_03-10-20/Cohort attributes-Table 1.csv"

echo "Importing laboratory measures"
mongoimport --port 27011 \
            -d search \
            -c measures \
            --drop \
            --type=csv \
            --headerline \
            --file="data/CHILDPseudoData_03-10-20/Laboratory measures-Table 1.csv"

echo "Importing biosamples table"
mongoimport --port 27011 \
            -d search \
            -c biosamples \
            --drop \
            --type=csv \
            --headerline \
            --file="data/CHILDPseudoData_03-10-20/Biosamples-Table 1.csv"