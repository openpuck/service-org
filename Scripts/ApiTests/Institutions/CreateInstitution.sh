#!/bin/bash

# Load in our common stuff.
source ../Common.sh

# Test Endpoint and Method
ENDPOINT="/institution"
METHOD="POST"

# Payload
read -d '' PAYLOAD << EndOfPayload
{
"cn": "${TEST_INSTITUTION_CN}",
"city": "ROCHESTER"
}
EndOfPayload

perform_call ${METHOD} ${URL} ${ENDPOINT} "${PAYLOAD}"