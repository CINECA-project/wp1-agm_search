#!/bin/bash

echo "Importing pseudoCHILD Metadata"
./child_search_metadata.sh
echo "Importing Colaus Metadata"
./colaus_search_metadata.sh
echo "Importing H3Africa synthetic Metadata"
./h3africa_search_metadata.sh
echo "Importing VCFs"
./child_search_variants.py -n 2000 data/child.vcf
