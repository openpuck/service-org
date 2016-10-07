#!/bin/bash

# Load in our common stuff.
source ../Common.sh

# Test Endpoint and Method
ENDPOINT="/institution?cn=${TEST_INSTITUTION_CN}"
METHOD="GET"
PAYLOAD=''

perform_call ${METHOD} ${URL} ${ENDPOINT} "${PAYLOAD}"