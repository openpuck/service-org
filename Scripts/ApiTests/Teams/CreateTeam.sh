#!/bin/bash

# Load in our common stuff.
source ../Common.sh

# Test Endpoint and Method
ENDPOINT="/team"
METHOD="POST"

# Payload
read -d '' PAYLOAD << EndOfPayload
{
"nickname": "Centurions",
"institution": "$(get_test_institution_id)",
"provider": "SidearmAdaptiveProvider",
"is_women": "yes",
"league": "$(get_test_league_id)",
"conference": "$(get_test_conference_id)",
"is_active": "yes",
"website": "http://foo"
}
EndOfPayload

perform_call ${METHOD} ${URL} ${ENDPOINT} "${PAYLOAD}"