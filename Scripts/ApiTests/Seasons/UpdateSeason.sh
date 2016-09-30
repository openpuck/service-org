#!/bin/bash

# Load in our common stuff.
source ../Common.sh

# Test-specific vars
ENDPOINT="/season/$(get_season_id)"
METHOD="PUT"
SUB_ATTR="end_year"
SUB_VALUE=2020

# Cook up the new object
output=$(perform_call "GET" ${URL} ${ENDPOINT} "" true)
echo "EXISTING: $output"
PAYLOAD=$(sub_payload "${output}" "${SUB_ATTR}" "${SUB_VALUE}")
echo "NEW:      ${PAYLOAD}"

# Perform update
echo "Updating..."
perform_call ${METHOD} ${URL} ${ENDPOINT} "${PAYLOAD}"