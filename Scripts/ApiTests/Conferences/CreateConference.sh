#!/bin/bash

# Load in our common stuff.
source ../Common.sh

# Test Endpoint and Method
ENDPOINT="/conference"
METHOD="POST"

# Payload
read -d '' PAYLOAD << EndOfPayload
{
"abbr": "${TEST_CONFERENCE_ABBR}",
"cn": "Test Conference",
"website": "lolz",
"is_women": "yes",
"league": "$(get_test_league_id)"
}
EndOfPayload

perform_call ${METHOD} ${URL} ${ENDPOINT} "${PAYLOAD}"