#!/bin/bash

# Load in our common stuff.
source ../Common.sh

# Test Endpoint and Method
ENDPOINT="/institution/$(get_test_institution_id)/teams"
METHOD="GET"
PAYLOAD=''

perform_call ${METHOD} ${URL} ${ENDPOINT} "${PAYLOAD}"