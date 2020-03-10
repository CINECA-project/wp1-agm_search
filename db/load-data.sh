#!/usr/bin/env bash

echo "Loading initial data into the beacon database"

# Move to the script directory
pushd $(dirname ${BASH_SOURCE[0]})

# Schemas and Functions
docker_process_sql < scripts/schemas.sql

popd 
echo "Initial schemas loaded"
