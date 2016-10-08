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
"institution": "05d7ab17-68e2-4cbe-ae3c-62bf908462bd",
"provider": "SidearmAdaptiveProvider",
"is_women": "yes",
"league": "ac99003b-845d-4cec-9c02-4dfe1acc1839",
"conference": "f550d8ed-bc80-407a-be09-ee1b85ba3bca",
"is_active": "yes",
"website": "http://foo"
}
EndOfPayload

perform_call ${METHOD} ${URL} ${ENDPOINT} "${PAYLOAD}"