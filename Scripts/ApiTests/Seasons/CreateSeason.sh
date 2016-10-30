#!/bin/bash

# Load in our common stuff.
source ../Common.sh

# Test Endpoint and Method
ENDPOINT="/season"
METHOD="POST"

# Payload
read -d '' PAYLOAD << EndOfPayload
{
"is_women": "yes",
"league": "$(get_test_league_id)",
"start_year": ${TEST_SEASON_START_YEAR},
"end_year": $((${TEST_SEASON_START_YEAR}+1))
}
EndOfPayload

perform_call ${METHOD} ${URL} ${ENDPOINT} "${PAYLOAD}"