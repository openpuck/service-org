#!/bin/bash

# Load in our common stuff.
source ../Common.sh

# Test Endpoint and Method
ENDPOINT="/team/$(get_test_team_id)"
METHOD="DELETE"
PAYLOAD=''

perform_call ${METHOD} ${URL} ${ENDPOINT} "${PAYLOAD}"