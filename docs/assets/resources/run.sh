#!/bin/bash

export DB_USERNAME="ct_admin"
export DB_PASSWORD="wowimsosecure"
export DB_NAME="geoconnections"
export DB_HOST="localhost"
export DB_PORT="30010"
export DB_AUTO_INCREMENT_ST_POINT="20"

export KAFKA_BROKER="localhost:9092"
export KAFKA_LOCATION_SVC_TOPIC="locations"

export GRPC_PORT="5010"
export PERSON_SVC_GRPC_HOST="localhost"
export PERSON_SVC_GRPC_PORT="5010"

# PSQL_CONN="postgresql://ct_admin:wowimsosecure@localhost:5432/geoconnections?sslmode=require"
# command used to access the database using psql
# $ kubectl exec -it {{ postgres_pod_name }}  -- bash -c "psql \"sslmode=allow host=localhost dbname=geoconnections user=ct_admin\""

LOCATION_SVC_PATH="{{ path_project }}/udaconnect/modules/udaconnect-locations-service"
PERSONS_SVC_PATH="{{ path_project }}/udaconnect/modules/udaconnect-persons-service"
CONNS_SVC_PATH="{{ path_project }}/udaconnect/modules/udaconnect-connections-service"
MONOLITH_PATH="{{ path_project }}/udaconnect/modules/api"

source "${LOCATION_SVC_PATH}"/.venv/bin/activate

FLASK_APP="${LOCATION_SVC_PATH}"/wsgi.py flask run -p 5002

deactivate
