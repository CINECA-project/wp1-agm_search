#!/bin/bash

echo "Importing WP3-mapped JSON"
mongoimport -d search \
            -c child_wp3 \
            --drop \
            --jsonArray \
            --file="data/patched_child.json"

echo "Importing unmapped questionnaire pseudodata"
mongoimport -d search \
            -c child_unmapped \
            --drop \
            --type=csv \
            --headerline \
            --file="data/CHILDPseudoData_03-10-20/Questionnaire pseudodata-Table 1.csv"

echo "Importing cohort attributes"
mongoimport -d search \
            -c child_attributes \
            --drop \
            --type=csv \
            --headerline \
            --file="data/CHILDPseudoData_03-10-20/Cohort attributes-Table 1.csv"

echo "Importing laboratory measures"
mongoimport -d search \
            -c child_measures \
            --drop \
            --type=csv \
            --headerline \
            --file="data/CHILDPseudoData_03-10-20/Laboratory measures-Table 1.csv"

echo "Importing biosamples table"
mongoimport -d search \
            -c child_biosamples \
            --drop \
            --type=csv \
            --headerline \
            --file="data/CHILDPseudoData_03-10-20/Biosamples-Table 1.csv"
