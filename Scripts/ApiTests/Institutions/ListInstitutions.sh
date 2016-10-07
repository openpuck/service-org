#!/bin/bash

# Load in our common stuff.
source ../Common.sh

# Test Endpoint and Method
ENDPOINT="/institution"
METHOD="GET"
PAYLOAD=''

perform_call ${METHOD} ${URL} ${ENDPOINT} "${PAYLOAD}"