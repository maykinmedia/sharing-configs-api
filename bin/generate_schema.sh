#!/bin/bash
#
# Dump the current OAS into YAML file src/openapi.yml
#
# Run this script from the root of the repository


export SCHEMA_PATH=src/sharing/openapi.yaml

src/manage.py spectacular --file $SCHEMA_PATH --validate
