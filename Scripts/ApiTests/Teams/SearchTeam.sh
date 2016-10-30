#!/bin/bash

# Load in our common stuff.
source ../Common.sh

# Test Endpoint and Method
ENDPOINT="/team?institution=$(get_test_institution_id)&is_women=${TEST_TEAM_IS_WOMEN}"
METHOD="GET"
PAYLOAD=''

perform_call ${METHOD} ${URL} ${ENDPOINT} "${PAYLOAD}"