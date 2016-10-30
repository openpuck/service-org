#!/bin/bash

# Load in our common stuff.
source ../Common.sh

# Test Endpoint and Method
ENDPOINT="/league"
METHOD="POST"

# Payload
read -d '' PAYLOAD << EndOfPayload
{
"abbr": "${TEST_LEAGUE_ABBR}",
"cn": "Test League",
"website": "lolz",
}
EndOfPayload

perform_call ${METHOD} ${URL} ${ENDPOINT} "${PAYLOAD}"