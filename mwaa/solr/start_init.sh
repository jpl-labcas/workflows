#!/bin/bash
# Get the directory of the current script

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

solr start


# Wait for Solr to be ready
until curl -s http://localhost:8983/solr/admin/cores?wt=json | grep -q '"status":'; do
  echo "Waiting for Solr to start..."
  sleep 5
done

# Run your solr create commands
solr create -c collections -d ${SCRIPT_DIR}/confs/collections
solr create -c datasets -d ${SCRIPT_DIR}/confs/datasets
solr create -c files -d ${SCRIPT_DIR}/confs/files
solr create -c oodt-fm -d ${SCRIPT_DIR}/confs/oodt-fm
solr create -c userdata -d ${SCRIPT_DIR}/confs/userdata

# Keep the container running
tail -f /dev/null


