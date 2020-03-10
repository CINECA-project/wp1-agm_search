#!/bin/bash

echo "Importing Metadata"
./child_search_metadata.sh
echo "Importing VCFs"
./child_search_variants.py -n 2000 data/child.vcf
